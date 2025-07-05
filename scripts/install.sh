#!/usr/bin/env bash

set -euo pipefail

REPO_URL="https://github.com/jordantshaw/proxmox2discord.git"
APP_DIR="${1:-$HOME/proxmox2discord}"

echo "📥 Cloning proxmox2discord into ${APP_DIR}…"
git clone "${REPO_URL}" "${APP_DIR}"

cd "${APP_DIR}"

echo "🐍 Installing Python dependencies…"
pip3 install -r requirements.txt

cat <<EOF

✅ Installation complete!

To start the server:
    proxmox2discord

Remember to configure your Proxmox notification‐script to point at:
    http://<YOUR_SERVER>:6068/notify

EOF