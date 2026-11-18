const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const password = 'antigravity-sync-2026';
const algorithm = 'aes-256-ctr';
const key = crypto.scryptSync(password, 'salt', 32);

const workspaceDir = path.join(__dirname, '..');
const memoryDir = path.join(workspaceDir, '9router-backup', 'memory');
const tempTarPath = path.join(workspaceDir, 'temp-memory-restored.tar.gz');

const homedir = require('os').homedir();
const targetGeminiDir = path.join(homedir, '.gemini');

console.log('[*] Đang tìm các tệp tin chunks để khôi phục...');
try {
    const files = fs.readdirSync(memoryDir)
        .filter(f => f.startsWith('chunk.'))
        .sort((a, b) => {
            const idxA = parseInt(a.split('.')[1], 10);
            const idxB = parseInt(b.split('.')[1], 10);
            return idxA - idxB;
        });

    if (files.length === 0) {
        console.error('[ERROR] Không tìm thấy tệp tin chunk.* nào.');
        process.exit(1);
    }

    console.log(`[*] Tìm thấy ${files.length} chunks. Đang ghép các mảnh dữ liệu...`);
    const buffers = [];
    for (const file of files) {
        const filePath = path.join(memoryDir, file);
        buffers.push(fs.readFileSync(filePath));
    }
    const encryptedBuffer = Buffer.concat(buffers);

    console.log('[*] Đang giải mã bộ nhớ agent...');
    const iv = encryptedBuffer.slice(0, 16);
    const data = encryptedBuffer.slice(16);
    const decipher = crypto.createDecipheriv(algorithm, key, iv);
    const decryptedBuffer = Buffer.concat([decipher.update(data), decipher.final()]);

    fs.writeFileSync(tempTarPath, decryptedBuffer);
    console.log('[OK] Đã tạo file lưu trữ tạm thời.');

    // Ensure target .gemini directory exists
    if (!fs.existsSync(targetGeminiDir)) {
        fs.mkdirSync(targetGeminiDir, { recursive: true });
        console.log(`[OK] Đã tạo thư mục: ${targetGeminiDir}`);
    }

    console.log('[*] Đang giải nén bộ nhớ vào thư mục .gemini...');
    execSync(`tar -xzf "${tempTarPath}" -C "${targetGeminiDir}"`, { stdio: 'inherit' });
    console.log('[OK] Khôi phục bộ nhớ thành công!');

} catch (err) {
    console.error('[ERROR] Khôi phục bộ nhớ thất bại:', err);
} finally {
    if (fs.existsSync(tempTarPath)) {
        fs.unlinkSync(tempTarPath);
    }
}
