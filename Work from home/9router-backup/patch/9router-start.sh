#!/bin/bash
cd ~/tools/9router

CURRENT_VERSION=$(node -e "console.log(require('./package.json').version)")
BUILD_VERSION=$(cat .next/BUILD_VERSION 2>/dev/null || echo "none")

if [ "$CURRENT_VERSION" != "$BUILD_VERSION" ]; then
  echo "[9router] New version detected ($BUILD_VERSION → $CURRENT_VERSION), building..."
  npm run build
  cp -r .next/static .next/standalone/.next/static
  cp -r public .next/standalone/public 2>/dev/null || true
  echo "$CURRENT_VERSION" > .next/BUILD_VERSION
  echo "[9router] Build done."
fi

export PORT=20128
exec node .next/standalone/server.js
