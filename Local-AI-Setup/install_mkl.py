"""
install_mkl.py — Tải MKL từ Tsinghua CDN (nhanh hơn) và cài vào venv
"""
import os, sys, io, threading, time, zipfile, subprocess, urllib.request

MKL_URL  = "https://pypi.tuna.tsinghua.edu.cn/packages/fe/1c/5f6dbf18e8b73e0a5472466f0ea8d48ce9efae39bd2ff38cebf8dce61259/mkl-2021.4.0-py2.py3-none-win_amd64.whl"
DEST     = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mkl-2021.4.0-win_amd64.whl")
VENV_PIP = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "stable-diffusion-webui-forge", "venv", "Scripts", "pip.exe")
NUM_THREADS = 16

def get_size(url):
    req = urllib.request.Request(url, method='HEAD')
    with urllib.request.urlopen(req, timeout=30) as r:
        return int(r.headers.get('Content-Length', 0))

def download_chunk(url, start, end, part, progress, lock, idx):
    req = urllib.request.Request(url, headers={'Range': f'bytes={start}-{end}'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r, open(part, 'wb') as f:
            while True:
                buf = r.read(256*1024)
                if not buf: break
                f.write(buf)
                with lock: progress[idx] += len(buf)
    except Exception as e:
        print(f"\n[LOI] Thread {idx}: {e}")
        sys.exit(1)

def fast_download(url, dest):
    print(f"Lay thong tin file tu Tsinghua CDN...")
    total = get_size(url)
    print(f"Kich thuoc: {total/(1024**2):.1f} MB — bat dau tai voi {NUM_THREADS} ket noi...")
    chunk = total // NUM_THREADS
    threads, progress, lock = [], [0]*NUM_THREADS, threading.Lock()
    for i in range(NUM_THREADS):
        s = i * chunk
        e = (s + chunk - 1) if i < NUM_THREADS-1 else (total-1)
        t = threading.Thread(target=download_chunk, args=(url, s, e, f"{dest}.part{i}", progress, lock, i), daemon=True)
        threads.append(t); t.start()
    t0 = time.time()
    while any(t.is_alive() for t in threads):
        dl = sum(progress); el = time.time()-t0
        sp = dl/el if el else 0; rem = (total-dl)/sp if sp else 0
        sys.stdout.write(f"\r{dl/total*100:.1f}% | {dl/(1024**2):.1f}/{total/(1024**2):.1f} MB | {sp/(1024**2):.2f} MB/s | Con lai: {int(rem//60)}p{int(rem%60)}s   ")
        sys.stdout.flush(); time.sleep(0.5)
    for t in threads: t.join()
    print("\nDang ghep file...")
    with open(dest, 'wb') as out:
        for i in range(NUM_THREADS):
            p = f"{dest}.part{i}"
            with open(p,'rb') as pf:
                while True:
                    b = pf.read(1024*1024)
                    if not b: break
                    out.write(b)
            os.remove(p)
    print(f"OK - Tai xong: {dest}")

def install(whl, pip_exe):
    print(f"\nDang cai {os.path.basename(whl)} vao venv...")
    r = subprocess.run([pip_exe, "install", whl, "--force-reinstall", "-q"], capture_output=True, text=True)
    if r.returncode == 0:
        print("=" * 50)
        print(" OK  mkl-2021.4.0 da cai thanh cong!")
        print(" Bay gio chay: setup_and_run.bat")
        print("=" * 50)
    else:
        print(f"[LOI]: {r.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    if not os.path.exists(VENV_PIP):
        print(f"[LOI] Khong tim thay: {VENV_PIP}"); sys.exit(1)
    if os.path.exists(DEST):
        print(f"File da ton tai: {DEST}")
    else:
        fast_download(MKL_URL, DEST)
    install(DEST, VENV_PIP)
    input("\nNhan Enter de dong...")
