from datetime import datetime
from typing import Any

import httpx
from fastapi import HTTPException
from pydantic import AnyUrl


SEVERITY_CONFIG = {
    "info":    {"color": 0x3498db, "emoji": "ℹ️"},
    "notice":  {"color": 0x2ecc71, "emoji": "🔔"},
    "warning": {"color": 0xf1c40f, "emoji": "⚠️"},
    "error":   {"color": 0xe74c3c, "emoji": "❌"},
    "unknown": {"color": 0x95a5a6, "emoji": "❔"},
}


def build_discord_payload(payload, log_url: str) -> dict:
    severity = (payload.severity or "unknown").lower()
    cfg = SEVERITY_CONFIG.get(severity, SEVERITY_CONFIG["unknown"])
    desc = payload.discord_description or ''

    embed = {
        "title":  f"{cfg['emoji']} {payload.title or 'Notification'}",
        "description": desc,
        "color": cfg["color"],
        "fields": [
            {"name": "Severity", "value": severity.capitalize(), "inline": True},
            {"name": "Logs", "value": f"[View full logs]({log_url})", "inline": True},
        ],
        "timestamp": datetime.now().isoformat(),
    }

    return {
        "content": f"<@{payload.mention_user_id}>\n" if payload.mention_user_id else "",
        "embeds": [embed]
    }


async def send_discord_notification(
    webhook_url: AnyUrl,
    payload: dict[str, Any],
    timeout: float = 10.0,
) -> int:
    """ Send a JSON payload to a Discord webhook URL. """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            str(webhook_url),
            json=payload,
            timeout=timeout,
        )

    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code,
            detail="Discord webhook call failed",
        )

    return response.status_code