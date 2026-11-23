#!/usr/bin/env node
/**
 * Cross-platform Stop hook for Claude Code.
 * Stages, commits, and pushes workspace changes on both macOS and Windows,
 * and mirrors to Google Drive on macOS when the Drive mount is present.
 */
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const workspaceDir = path.resolve(__dirname, '..');

function run(cmd, args) {
  return spawnSync(cmd, args, {
    cwd: workspaceDir,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  });
}

try {
  run('git', ['add', '-A']);
  const diff = run('git', ['diff', '--cached', '--name-only']);
  if (diff.status === 0 && diff.stdout) {
    const files = diff.stdout
      .split(/\r?\n/)
      .map((line) => line.trim())
      .filter(Boolean);

    if (files.length > 0) {
      const head = files.slice(0, 3).join(' ');
      const suffix = files.length > 3 ? ` (+${files.length - 3} more)` : '';
      const msg = `auto-sync: ${head}${suffix}`;
      const committed = run('git', ['commit', '-m', msg]);
      if (committed.status === 0) {
        run('git', ['push']);
      }
    }
  }

  if (process.platform === 'darwin') {
    const driveTarget =
      '/Users/ts-1148/Library/CloudStorage/GoogleDrive-lephuongkhanh1995@gmail.com/My Drive/Pulu-workspace/';
    if (fs.existsSync(driveTarget)) {
      run('rsync', ['-a', '--delete', '--exclude=.git/', `${workspaceDir}/`, driveTarget]);
    }
  }
} catch {
  // Never block Claude Code Stop hook on transient sync errors
}

process.exit(0);
