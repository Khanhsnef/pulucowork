"""setup_env.py —— chuẩn bị môi trường chạy chỉ bằng một chạm (Python + frida + adb + kết nối giả lập)

Làm 4 việc:
  1. Kiểm tra phiên bản Python
  2. Cài frida 16.5.9 (bắt buộc để inject script; 17.x đã bỏ Java bridge, không dùng được)
  3. Tìm adb: biến môi trường → PATH → MuMu đi kèm → không có thì tự tải platform-tools
  4. Kết nối giả lập rồi chạy tự kiểm tra bằng ultra0.py --check

Cách dùng: bấm đúp Cai_dat_moi_truong.bat, hoặc python setup_env.py
"""
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

BASE = Path(__file__).resolve().parent
ADB_CANDIDATES = [
    os.environ.get("ADB_PATH", ""),
    r"C:\Program Files\Netease\MuMuPlayer-12.0\shell\adb.exe",
    r"C:\Program Files\Netease\MuMuPlayerGlobal-12.0\shell\adb.exe",
    r"C:\Program Files (x86)\Netease\MuMuPlayer-12.0\shell\adb.exe",
    r"D:\Program Files\Netease\MuMu\nx_main\adb.exe",
    r"D:\Program Files\Netease\MuMu\nx_device\12.0\shell\adb.exe",
    r"C:\Program Files\Netease\MuMu\nx_main\adb.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe"),
    os.path.expandvars(r"%USERPROFILE%\AppData\Local\Android\Sdk\platform-tools\adb.exe"),
]
PLATFORM_TOOLS_URL = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"


def step(msg):
    print(f"\n▶ {msg}", flush=True)


def ok(msg):
    print(f"   ✅ {msg}", flush=True)


def warn(msg):
    print(f"   ⚠️  {msg}", flush=True)


def die(msg):
    print(f"\n❌ {msg}", flush=True)
    sys.exit(1)


def check_python():
    step("Kiểm tra Python")
    v = sys.version_info
    print(f"   {platform.python_version()}  ({platform.architecture()[0]})")
    if v < (3, 9):
        die("Phiên bản Python quá thấp, hãy cài 3.10 trở lên: https://www.python.org/downloads/")
    ok("Python dùng được")


def install_frida():
    step("Cài frida 16.5.9 (bắt buộc để inject)")
    try:
        import frida
        if frida.__version__.startswith("16."):
            ok(f"Đã cài frida {frida.__version__}")
            return
        warn(f"Hiện đang là frida {frida.__version__}, 17.x không dùng được, đang hạ cấp…")
    except Exception:
        pass

    cmds = [
        [sys.executable, "-m", "pip", "install", "--no-cache-dir", "frida==16.5.9"],
        [sys.executable, "-m", "pip", "install", "--no-cache-dir",
         "-i", "https://pypi.tuna.tsinghua.edu.cn/simple", "frida==16.5.9"],
    ]
    for c in cmds:
        print("   " + " ".join(c[2:]))
        r = subprocess.run(c, capture_output=True, text=True, errors="ignore")
        if r.returncode == 0:
            break
        print("   " + (r.stderr or r.stdout).strip().splitlines()[-1][:160])
    try:
        import importlib
        import frida
        importlib.reload(frida)
        ok(f"Đã cài xong frida {frida.__version__}")
    except Exception as e:
        die(f"Cài frida thất bại: {e}\n   Chạy tay: pip install frida==16.5.9")


def download_platform_tools():
    dest = BASE / "platform-tools"
    print(f"   Tải platform-tools về {dest}")
    tmp = Path(tempfile.gettempdir()) / "platform-tools.zip"
    with urllib.request.urlopen(PLATFORM_TOOLS_URL, timeout=180) as r, open(tmp, "wb") as f:
        f.write(r.read())
    with zipfile.ZipFile(tmp) as z:
        z.extractall(BASE)
    tmp.unlink(missing_ok=True)
    adb = dest / "adb.exe"
    if adb.exists():
        ok(f"platform-tools đã sẵn sàng: {adb}")
        return str(adb)
    die("Giải nén platform-tools xong mà không thấy adb.exe")


def find_adb():
    step("Tìm adb")
    for c in ADB_CANDIDATES:
        if not c:
            continue
        if c in ("adb", "adb.exe"):
            continue
        if Path(c).exists():
            ok(f"Dùng {c}")
            return c
    w = shutil.which("adb")
    if w:
        ok(f"Dùng {w} trong PATH")
        return w
    warn("Không tìm thấy adb, bắt đầu tải tự động")
    return download_platform_tools()


def connect_emulator(adb):
    step("Kết nối giả lập")
    ports = ["16384", "7555", "16416", "21503", "62001"]
    for p in ports:
        subprocess.run([adb, "connect", f"127.0.0.1:{p}"], capture_output=True, text=True, errors="ignore")
    out = subprocess.run([adb, "devices"], capture_output=True, text=True, errors="ignore").stdout
    devices = [l.split("\t")[0] for l in out.splitlines()[1:] if "\tdevice" in l]
    if not devices:
        warn("Chưa kết nối được thiết bị nào. Hãy chắc chắn MuMu đã khởi động và đã bật gỡ lỗi ADB trong Cài đặt")
        print("   " + out.strip().replace("\n", "\n   "))
        return None
    ok(f"Đã kết nối: {', '.join(devices)}")
    return devices[0]


def run_check(adb, serial):
    step("Chạy tự kiểm tra môi trường (ultra0.py --check)")
    env = dict(os.environ)
    env["ADB_PATH"] = adb
    env["PYTHONIOENCODING"] = "utf-8"
    r = subprocess.run([sys.executable, "ultra0.py", "--check"], cwd=str(BASE),
                       env=env, capture_output=True, encoding="utf-8", errors="ignore")
    print(r.stdout.strip() or r.stderr.strip())
    return r.returncode == 0


def main():
    print("=" * 60)
    print("  Google Ultra / Pro mở bằng một chạm · Cài đặt môi trường")
    print("=" * 60)
    check_python()
    install_frida()
    adb = find_adb()
    serial = connect_emulator(adb)

    if serial:
        good = run_check(adb, serial)
        print("\n" + "=" * 60)
        if good:
            print("  ✅ Môi trường đã sẵn sàng, có thể bấm đúp «2_Pro_12_thang_Buoc_1.bat» để bắt đầu mở gói")
        else:
            print("  ⚠️  Tự kiểm tra chưa đạt hết, xem gợi ý ở trên để xử lý (thường là do Cửa hàng Play chưa mở lên)")
        print("=" * 60)
    else:
        print("\nCài xong MuMu và bật gỡ lỗi ADB rồi chạy lại script này một lần nữa.")


if __name__ == "__main__":
    main()
