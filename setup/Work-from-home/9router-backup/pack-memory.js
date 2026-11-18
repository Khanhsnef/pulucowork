const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const password = 'antigravity-sync-2026';
const algorithm = 'aes-256-ctr';
const key = crypto.scryptSync(password, 'salt', 32);

const workspaceDir = path.join(__dirname, '..');
const outputDir = path.join(workspaceDir, '9router-backup', 'memory');
const tempTarPath = path.join(workspaceDir, 'temp-memory.tar.gz');

// Ensure output directory exists
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}

console.log('[*] Đang nén các tệp tin bộ nhớ bằng tar...');
const homedir = require('os').homedir();

try {
    // Run tar command
    execSync(
        `tar -czf "${tempTarPath}" -C "${homedir}/.gemini" antigravity/brain antigravity/conversations antigravity-ide/brain antigravity-ide/conversations config google_accounts.json oauth_creds.json projects.json installation_id`,
        { stdio: 'inherit' }
    );
    console.log('[OK] Đã tạo file nén tạm thời.');

    // Encrypt the compressed file
    console.log('[*] Đang mã hóa dữ liệu...');
    const inputBuffer = fs.readFileSync(tempTarPath);
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv(algorithm, key, iv);
    const encryptedBuffer = Buffer.concat([iv, cipher.update(inputBuffer), cipher.final()]);

    // Split encrypted buffer into chunks of 85MB (89,128,960 bytes)
    const chunkSize = 85 * 1024 * 1024;
    const totalChunks = Math.ceil(encryptedBuffer.length / chunkSize);
    console.log(`[*] Tổng kích thước đã mã hóa: ${(encryptedBuffer.length / (1024 * 1024)).toFixed(2)} MB. Đang chia thành ${totalChunks} chunks...`);

    // Clear old chunks
    const files = fs.readdirSync(outputDir);
    for (const file of files) {
        if (file.startsWith('chunk.')) {
            fs.unlinkSync(path.join(outputDir, file));
        }
    }

    // Write chunks
    for (let i = 0; i < totalChunks; i++) {
        const start = i * chunkSize;
        const end = Math.min(start + chunkSize, encryptedBuffer.length);
        const chunk = encryptedBuffer.slice(start, end);
        const chunkPath = path.join(outputDir, `chunk.${i}`);
        fs.writeFileSync(chunkPath, chunk);
        console.log(`[OK] Đã lưu: ${chunkPath} (${(chunk.length / (1024 * 1024)).toFixed(2)} MB)`);
    }

} catch (err) {
    console.error('[ERROR] Đóng gói thất bại:', err);
} finally {
    if (fs.existsSync(tempTarPath)) {
        fs.unlinkSync(tempTarPath);
    }
}
