#!/bin/bash
# Starts the local website editor GUI.
# Usage: ./start_gui.sh   (from repo root)

set -e
cd "$(dirname "$0")/gui"

# Install dependencies if needed
if ! python3 -c "import flask, frontmatter" 2>/dev/null; then
  echo "Installing dependencies..."
  pip3 install -q --break-system-packages -r requirements.txt 2>/dev/null || \
  pip3 install -q -r requirements.txt
fi

python3 app.py
