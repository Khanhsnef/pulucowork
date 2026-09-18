#!/bin/bash
# ==============================================================================
# DEEP MAC CLEANUP TOOL v2.0 (TỐI ƯU HÓA DUNG LƯỢNG CHUYÊN SÂU MACOS)
# ==============================================================================

echo "======================================================="
echo "🧹 BẮT ĐẦU DỌN DẸP DUNG LƯỢNG CHUYÊN SÂU (DEEP CLEAN)..."
echo "======================================================="

# Đo dung lượng trước khi dọn
BEFORE_FREE=$(df -h / | awk 'NR==2 {print $4}')
echo "📊 Dung lượng trống ban đầu: $BEFORE_FREE"
echo "-------------------------------------------------------"

# 1. Xóa mô hình AI On-Device cồng kềnh của Chrome (~4.1 GB)
echo "🤖 1. Dọn dẹp mô hình Chrome On-Device AI Models..."
rm -rf ~/Library/Application\ Support/Google/Chrome/OptGuideOnDeviceModel/* 2>/dev/null
rm -rf ~/Library/Application\ Support/Google/Chrome/OptGuideOnDeviceClassifierModel/* 2>/dev/null
rm -rf ~/Library/Application\ Support/Google/Chrome/component_crx_cache/* 2>/dev/null
rm -rf ~/Library/Application\ Support/Google/Chrome/SODALanguagePacks/* 2>/dev/null
echo "   -> Đã xóa ~4.1 GB tệp mô hình tạm của Chrome."

# 2. Dọn sạch Thùng rác
echo "🗑️ 2. Dọn sạch Thùng rác (Trash)..."
rm -rf ~/.Trash/* 2>/dev/null
echo "   -> Xong."

# 3. Dọn Caches của toàn bộ ứng dụng người dùng (~3.0 GB)
echo "⚡ 3. Dọn sạch ~/Library/Caches..."
rm -rf ~/Library/Caches/* 2>/dev/null
echo "   -> Đã dọn sạch User Caches."

# 4. Dọn Cache Lập trình (npm, pip, brew, yarn)
echo "📦 4. Dọn Cache Lập trình..."
if command -v npm &> /dev/null; then
    npm cache clean --force 2>/dev/null
    echo "   ✓ npm cache cleared."
fi

if command -v pip3 &> /dev/null; then
    pip3 cache purge 2>/dev/null
    echo "   ✓ pip cache cleared."
fi

if command -v brew &> /dev/null; then
    brew cleanup -s --prune=all 2>/dev/null
    echo "   ✓ Homebrew cache & old versions cleared."
fi

# 5. Dọn Playwright & Headless Browser Caches
echo "🌐 5. Dọn cache Playwright Browsers..."
rm -rf ~/Library/Caches/ms-playwright 2>/dev/null
echo "   -> Xong."

# 6. Dọn Logs, Crash Reports & Diagnostics
echo "📝 6. Dọn Logs & Crash Reports..."
rm -rf ~/Library/Logs/* 2>/dev/null
rm -rf ~/Library/Application\ Support/CrashReporter/* 2>/dev/null
echo "   -> Xong."

# 7. Dọn Xcode DerivedData & Simulators (nếu có)
if [ -d ~/Library/Developer/Xcode/DerivedData ]; then
    echo "🔨 7. Dọn Xcode DerivedData..."
    rm -rf ~/Library/Developer/Xcode/DerivedData/* 2>/dev/null
    echo "   -> Xong."
fi

echo "-------------------------------------------------------"
AFTER_FREE=$(df -h / | awk 'NR==2 {print $4}')
echo "🎉 HOÀN TẤT DỌN DẸP CHUYÊN SÂU!"
echo "📈 Dung lượng trống trước: $BEFORE_FREE"
echo "🚀 Dung lượng trống hiện tại: $AFTER_FREE"
echo "======================================================="
echo "🔴 BƯỚC CUỐI CÙNG (CỰC KỲ QUAN TRỌNG):"
echo "   Hiện máy của bạn đang bị nghẽn 18.05 GB Swap Memory do chạy 21 ngày."
echo "   Hãy BẤM RESTART MÁY NGAY ( -> Restart...) để lấy lại thêm ~18 GB!"
echo "======================================================="
