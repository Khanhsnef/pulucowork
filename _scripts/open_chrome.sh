#!/bin/bash
PROFILE_DIR="$(pwd)/.chrome_debug_profile"
mkdir -p "$PROFILE_DIR"
open -na "Google Chrome" --args --remote-debugging-port=9222 --user-data-dir="$PROFILE_DIR" --no-first-run --no-default-browser-check https://chatgpt.com
echo "✅ Google Chrome đã được mở ở cổng Debug 9222!"
