import os
import sys
import urllib.request

def download_file(url, filename):
    print(f"Bắt đầu tải xuống từ: {url}")
    print(f"Đường dẫn lưu tệp: {filename}")
    
    def report(block_num, block_size, total_size):
        read_so_far = block_num * block_size
        if total_size > 0:
            percent = read_so_far * 1e2 / total_size
            s = f"\rTiến độ: {percent:.2f}% ({read_so_far / (1024**3):.2f} GB / {total_size / (1024**3):.2f} GB)"
            sys.stdout.write(s)
            sys.stdout.flush()
        else:
            sys.stdout.write(f"\rĐã tải được: {read_so_far / (1024**2):.2f} MB")
            sys.stdout.flush()
            
    try:
        urllib.request.urlretrieve(url, filename, report)
        print("\nTải xuống hoàn tất thành công!")
    except Exception as e:
        print(f"\n[LỖI] Không thể tải xuống tệp: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    url = "https://huggingface.co/lllyasviel/flux1-dev-bnb-nf4/resolve/main/flux1-dev-bnb-nf4-v2.safetensors"
    dest = sys.argv[1] if len(sys.argv) > 1 else "flux1-dev-bnb-nf4-v2.safetensors"
    
    # Tạo thư mục cha nếu chưa tồn tại
    os.makedirs(os.path.dirname(os.path.abspath(dest)), exist_ok=True)
    download_file(url, dest)
