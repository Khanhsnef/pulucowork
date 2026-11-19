#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
PORT="${1:-8765}"
echo "Starting My HCM GIS Web App on http://127.0.0.1:${PORT}"
cd "$DIR"
python3 -m http.server "$PORT" --bind 127.0.0.1
