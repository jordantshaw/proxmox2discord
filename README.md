# proxmox2discord
Reliable Proxmox Backup and VM Log Notifications in Discord

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)


## Overview
Discord enforces a 2000‑character limit per message, which can truncate lengthy Proxmox backup logs or VM events and obscure critical details. **Proxmox2Discord** solves this by:

- Capturing full Proxmox output in raw log files.
- Sending concise Discord notifications with a link to the complete log.

Whether you run nightly backups or ad‑hoc snapshots, Proxmox2Discord ensures you never miss important context.

## Features

- Raw Log Storage: Saves complete Proxmox logs in a configurable directory.
- Discord Embeds: Sends rich notifications with title, severity, and log link.
- Configurable Retention: Auto-cleanup of old logs after _N_ days. _Coming Soon!_
- Lightweight: Single Python package; minimal dependencies.
- Docker‑Ready: Official Dockerfile for fast deployment.

## Prerequisites
- Python 3.12+ or Docker

## Installation

### Docker (Recommended)
Build and run with Docker:

```bash
docker build -t proxmox2discord:latest .
docker run -d \
  -p 6068:6068 \
  -e TZ="UTC" \
  -v "./logs:/var/logs/p2d" \
  proxmox2discord:latest
```

Optionally you can use docker-compose as well.
```yaml
services:
  proxmox2discord:
    container_name: proxmox2discord
    build: .
    restart: unless-stopped
    volumes:
      - ./logs:/var/logs/p2d
    environment:
      - TZ=UTC
    ports:
      - '6068:6068'
```
```bash
docker compose up -d
```

### One‑Line Install
**Unix/macOS:**
```bash
curl -fsSL https://raw.githubusercontent.com/jordantshaw/proxmox2discord/main/scripts/install.sh | bash
```

**Windows (PowerShell):**
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -Command "iex (iwr https://raw.githubusercontent.com/jordantshaw/proxmox2discord/main/scripts/install.ps1 -UseBasicParsing)"
```


## Quickstart
1. **Start the server**
   ```bash
   proxmox2discord
   ```

2. **Verify**
   Open [http://<YOUR_HOST>:6068/docs](http://<YOUR_HOST>:6068/docs) for the interactive API docs.

3. **Configure Proxmox** (see below)


## Proxmox Integration
Use Proxmox’s `--notification-script` to POST JSON to `/notify`:

```bash
vzdump 105 \
  --storage backup --mode snapshot --compress zstd \
  --notification-script '
    curl -fsSL -X POST http://<YOUR_HOST>:6068/notify \
      -H "Content-Type: application/json" \
      -d "{\
        \"discord_webhook\":\"https://discord.com/api/webhooks/XXX/YYY\",\
        \"title\":\"Backup %VMID% (%GUESTNAME%)\",\
        \"severity\":\"%STATUS%\",\
        \"message\":\"Time: %TIME%\\nSize: %SIZE%\\nFilename: %FILENAME%\"\
      }"
'
```

Or globally in `/etc/vzdump.conf`:
```ini
[global]
notification-mode: notification-script
template: \
  curl -fsSL -X POST http://<YOUR_HOST>:6068/notify \
    -H 'Content-Type: application/json' \
    -d '{{ json.encode({ \
      "discord_webhook": "https://discord.com/api/webhooks/XXX/YYY", \
      "title": "Backup %VMID% (%GUESTNAME%)", \
      "severity": "%STATUS%", \
      "message": "Time: %TIME%\nSize: %SIZE%\nFilename: %FILENAME%" \
    }) }}'
```


## Configuration
Environment variables and their defaults:

| Env Variable    | Default                     | Description                   |
|-----------------|-----------------------------| ----------------------------- |
| `LOG_DIRECTORY` | `/opt/proxmox2discord/logs` | Path to store raw logs  |

You can override these at runtime or via a `.env` file (if using `python-dotenv`).



## License
Released under the [MIT License](LICENSE).