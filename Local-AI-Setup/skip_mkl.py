"""
skip_mkl.py — Bỏ qua tải MKL 228MB bằng cách tạo stub package

Lý do an toàn:
- torch 2.3.1+cu121 đã bundle sẵn MKL DLLs trong thư mục torch/lib/
- Package 'mkl' trên PyPI chỉ là bản sao DLLs — không cần thiết khi dùng GPU
- Script này tạo một wheel rỗng tên mkl==2021.4.0 để pip nghĩ đã cài xong
"""
import os
import sys
import zipfile
import tempfile
import subprocess

# ── Tìm pip trong venv của WebUI Forge ────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_PIP = os.path.join(SCRIPT_DIR, "stable-diffusion-webui-forge", "venv", "Scripts", "pip.exe")

if not os.path.exists(VENV_PIP):
    print("[LOI] Khong tim thay venv pip tai:", VENV_PIP)
    print("      Hay dam bao da chay setup_and_run.bat it nhat 1 lan de tao venv.")
    input("Nhan Enter de thoat...")
    sys.exit(1)

print("Tim thay venv pip:", VENV_PIP)

# ── Tạo stub wheel mkl==2021.4.0 ─────────────────────────────────────────────
tmpdir = tempfile.mkdtemp()
wheel_name = "mkl-2021.4.0-py2.py3-none-any.whl"
wheel_path = os.path.join(tmpdir, wheel_name)
dist_info  = "mkl-2021.4.0.dist-info"

WHEEL_META = """\
Wheel-Version: 1.0
Generator: skip-mkl-stub
Root-Is-Purelib: true
Tag: py2-none-any
Tag: py3-none-any
"""

PKG_META = """\
Metadata-Version: 2.1
Name: mkl
Version: 2021.4.0
Summary: Intel MKL stub — DLLs bundled inside torch CUDA wheel
"""

RECORD = (
    f"{dist_info}/WHEEL,,\n"
    f"{dist_info}/METADATA,,\n"
    f"{dist_info}/RECORD,,\n"
)

print("Dang tao stub wheel: mkl-2021.4.0...")
with zipfile.ZipFile(wheel_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    zf.writestr(f"{dist_info}/WHEEL",    WHEEL_META)
    zf.writestr(f"{dist_info}/METADATA", PKG_META)
    zf.writestr(f"{dist_info}/RECORD",   RECORD)

print("Dang cai stub vao venv...")
result = subprocess.run(
    [VENV_PIP, "install", wheel_path, "--force-reinstall", "-q"],
    capture_output=True, text=True
)

if result.returncode == 0:
    print("")
    print("=" * 50)
    print(" OK  Stub mkl==2021.4.0 da duoc cai thanh cong!")
    print("     Pip se KHONG tai 228MB MKL nua.")
    print("=" * 50)
    print("")
    print("BUOC TIEP THEO:")
    print("  Gõ lenh nay trong CMD de khoi dong lai:")
    print("  setup_and_run.bat")
else:
    print("[LOI] Cai stub that bai:")
    print(result.stderr)
    print(result.stdout)
    sys.exit(1)

# Dọn dẹp
import shutil
shutil.rmtree(tmpdir, ignore_errors=True)
input("\nNhan Enter de dong...")
