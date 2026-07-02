const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const password = '9router-sync-key-2026';
const algorithm = 'aes-256-ctr';
const key = crypto.scryptSync(password, 'salt', 32);

function decryptFile(inputPath, outputPath) {
    if (!fs.existsSync(inputPath)) {
        console.warn(`[Decrypt] File not found: ${inputPath}`);
        return;
    }
    const encrypted = fs.readFileSync(inputPath);
    const iv = encrypted.slice(0, 16);
    const data = encrypted.slice(16);
    const decipher = crypto.createDecipheriv(algorithm, key, iv);
    const decrypted = Buffer.concat([decipher.update(data), decipher.final()]);
    
    // Ensure parent directory of output path exists
    const parentDir = path.dirname(outputPath);
    if (!fs.existsSync(parentDir)) {
        fs.mkdirSync(parentDir, { recursive: true });
    }
    
    fs.writeFileSync(outputPath, decrypted);
    console.log(`[Decrypt] Success: ${inputPath} -> ${outputPath}`);
}

const targetDir = process.argv[2]; // Target AppData directory passed from powershell
if (!targetDir) {
    console.error('Usage: node decrypt.js <target_data_directory>');
    process.exit(1);
}

const backupDir = __dirname; // 9router-backup

decryptFile(path.join(backupDir, 'data', 'db', 'data.sqlite.enc'), path.join(targetDir, 'db', 'data.sqlite'));
decryptFile(path.join(backupDir, 'data', 'jwt-secret.enc'), path.join(targetDir, 'jwt-secret'));
decryptFile(path.join(backupDir, 'data', 'machine-id.enc'), path.join(targetDir, 'machine-id'));
