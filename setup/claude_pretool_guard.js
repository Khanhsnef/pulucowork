#!/usr/bin/env node
/**
 * Cross-platform PreToolUse guard for Claude Code.
 * Blocks Edit/Write operations targeting protected `_scripts/` paths on both macOS and Windows.
 */
const fs = require('fs');

let raw = '';
try {
  raw = fs.readFileSync(0, 'utf8');
} catch {
  // No stdin provided
}

let data = {};
if (raw && raw.trim().startsWith('{')) {
  try {
    data = JSON.parse(raw);
  } catch {
    data = {};
  }
}

const filePath = (
  data.file_path ||
  (data.tool_input && data.tool_input.file_path) ||
  process.env.CLAUDE_TOOL_FILE_PATH ||
  ''
).replace(/\\/g, '/');

process.exit(filePath.includes('_scripts/') ? 1 : 0);
