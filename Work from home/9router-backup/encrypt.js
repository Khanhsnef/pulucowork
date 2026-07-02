const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const password = '9router-sync-key-2026';
const algorithm = 'aes-256-ctr';
const key = crypto.scryptSync(password, 'salt', 32);

function encryptFile(inputPath, outputPath) {
    if (!fs.existsSync(inputPath)) {
        console.warn(`[Encrypt] File not found: ${inputPath}`);
        return;
    }
    const input = fs.readFileSync(inputPath);
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv(algorithm, key, iv);
    const encrypted = Buffer.concat([iv, cipher.update(input), cipher.final()]);
    
    // Ensure parent directory of output path exists
    const parentDir = path.dirname(outputPath);
    if (!fs.existsSync(parentDir)) {
        fs.mkdirSync(parentDir, { recursive: true });
    }
    
    fs.writeFileSync(outputPath, encrypted);
    console.log(`[Encrypt] Success: ${inputPath} -> ${outputPath}`);
}

const homedir = require('os').homedir();
const sourceDir = path.join(homedir, '.9router');
const outputDir = __dirname; // Work from home/9router-backup
const workspaceDir = path.join(__dirname, '..', '..'); // Pulu-workspace

encryptFile(path.join(sourceDir, 'db', 'data.sqlite'), path.join(outputDir, 'data', 'db', 'data.sqlite.enc'));
encryptFile(path.join(sourceDir, 'jwt-secret'), path.join(outputDir, 'data', 'jwt-secret.enc'));
encryptFile(path.join(sourceDir, 'machine-id'), path.join(outputDir, 'data', 'machine-id.enc'));
encryptFile(path.join(workspaceDir, '.env'), path.join(outputDir, 'data', 'workspace-env.enc'));
