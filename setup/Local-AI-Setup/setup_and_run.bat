@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

echo ===================================================
echo [1/4] Kiểm tra Git và Python trong hệ thống...
echo ===================================================

where git >nul 2>nul
if %errorlevel% neq 0 (
    echo [LỖI] Git chưa được cài đặt hoặc chưa được thêm vào PATH!
    echo Vui lòng tải và cài đặt Git từ: https://git-scm.com/
    pause
    exit /b 1
)

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [LỖI] Python chưa được cài đặt hoặc chưa được thêm vào PATH!
    echo Vui lòng tải và cài đặt Python 3.10 từ: https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Git và Python đã sẵn sàng.

echo.
echo ===================================================
echo [2/4] Kiểm tra và tải về WebUI Forge...
echo ===================================================
if not exist "stable-diffusion-webui-forge" (
    echo Thư mục WebUI Forge chưa tồn tại. Đang tiến hành clone...
    git clone https://github.com/lllyasviel/stable-diffusion-webui-forge.git
    if !errorlevel! neq 0 (
        echo [LỖI] Xảy ra lỗi khi clone repository!
        pause
        exit /b 1
    )
) else (
    echo [OK] Thư mục stable-diffusion-webui-forge đã có sẵn.
)

echo.
echo ===================================================
echo [3/4] Kiểm tra và tự động tải mô hình Flux.1-Dev NF4...
echo ===================================================
set MODEL_PATH=stable-diffusion-webui-forge\models\Stable-diffusion\flux1-dev-bnb-nf4-v2.safetensors
if not exist "%MODEL_PATH%" (
    echo Mô hình Flux.1 NF4 chưa tồn tại trong thư mục models.
    echo Bắt đầu tự động tải xuống (dung lượng ~6.3 GB, tùy tốc độ mạng)...
    python download_model.py "%MODEL_PATH%"
    if !errorlevel! neq 0 (
        echo [LỖI] Quá trình tải mô hình thất bại!
        pause
        exit /b 1
    )
) else (
    echo [OK] Mô hình Flux.1-Dev NF4 đã có sẵn đầy đủ.
)

echo.
echo ===================================================
echo [4/4] Khởi động ứng dụng WebUI Forge...
echo ===================================================
echo Đang kích hoạt máy chủ Local AI...
cd stable-diffusion-webui-forge
call webui-user.bat

pause
