# proxmox2discord
Proxmox Discord Notifier Service


---

## Why Proxmox2Discord?

Discord messages are limited to **2000 characters**, which makes sending lengthy Proxmox backup or VM logs directly 
to a channel impractical. Proxmox2Discord captures full log output, stores it on your server, and sends a concise 
notification to Discord with a link to the complete, formatted log. This ensures:

* **Full context**: Never miss important details hidden in truncated messages.
* **Preserved formatting**: Tabs and newlines remain intact for easy readability.
* **Lightweight notifications**: Only summary is sent to Discord, avoiding message size limits.

---

## Features

* Accepts JSON payloads from Proxmox backup jobs or hook scripts
* Stores raw logs in a configurable `logs/` directory
* Sends rich Discord embeds with:

  * **Title** (e.g., `Backup 105 (test)`)
  * **Severity** (info, warning, error)
  * **Description**
  * **Link** to full log for deep dives

---

## Quickstart

**Clone & install**

```bash
git clone https://github.com/jordantshaw/proxmox2discord.git
cd proxmox2discord
pip install .
```

**Run the server**

```bash
proxmox2discord
```

**Verify**
Open `http://127.0.0.1:6068/docs` to see the Swagger UI and test `/notify`.

---

## License

This project is licensed under the [MIT License](LICENSE).

