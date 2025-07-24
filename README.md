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
- Optional User Mentions: Include a Discord user ID to automatically @mention a specific user in the alert.
- Configurable Retention: Auto-cleanup of old logs after _N_ days. _Coming Soon!_
- Lightweight: Single Python package; minimal dependencies.
- Docker‑Ready: Official Dockerfile for fast deployment.

## Prerequisites
- Python 3.12+ or Docker

## Installation

### Docker (Recommended)
Clone repository and build Docker image.
```bash
git clone https://github.com/jordantshaw/proxmox2discord.git
cd proxmox2discord
docker build -t proxmox2discord:latest .
```

### One‑Line Manual Install
This will install the application into your users HOME directory.

**Linux/macOS:**
```bash
curl -fsSL https://raw.githubusercontent.com/jordantshaw/proxmox2discord/main/scripts/install.sh | bash
```

**Windows (PowerShell):**
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -Command "iex (iwr https://raw.githubusercontent.com/jordantshaw/proxmox2discord/main/scripts/install.ps1 -UseBasicParsing)"
```

### Manual Install
```bash
git clone https://github.com/jordantshaw/proxmox2discord.git
cd proxmox2discord
pip install -r requirements.txt
```


## Quickstart

### Using Docker
Run with Docker.
```bash
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

### Run Manually
```bash
proxmox2discord
```

### Verify
Open [http://<YOUR_HOST>:6068/docs](http://<YOUR_HOST>:6068/docs) for the interactive API docs.


## Proxmox Integration
Point your Proxmox cluster at the `/notify` endpoint so every alert is mirrored to Discord and archived.

| UI Field            | Value / Example                                                                                                                                                                                                                                                                     |
|---------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Endpoint Name**   | `proxmox2discord `                                                                                                                                                                                                                                                                  |
| **Method**          | `POST`                                                                                                                                                                                                                                                                              |
| **URL**             | `http://<API_SERVER_IP>:6068/api/notify`                                                                                                                                                                                                                                            |
| **Headers**         | `Content-Type: application/json`                                                                                                                                                                                                                                                    |
| **Body**            | <pre lang=json>{<br/>  "discord_webhook": "https://discord.com/api/webhooks/{{ secrets.id }}/{{ secrets.token }}",<br/>  "title" : "{{ title }}",<br/>  "message": "{{ escape message }}",<br/>  "severity": "{{ severity }}"<br/>  "mention_user_id":"{{ secrets.user_id }}"<br/>} |
| **Secrets**         | `id` → your Discord webhook **ID**<br>`token` → your Discord webhook **token** <br>`user_id` → your Discord user ID **token**                                                                                                                                                       |
| **Enable**          | ✓                                                                                                                                                                                                                                                                                   |

> Optional Mentions:  Add discord_user_id (the numeric user ID) to the payload to @mention a specific user in Discord.


## License
Released under the [MIT License](LICENSE).