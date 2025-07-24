import uuid

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import PlainTextResponse
from typing import Any

from .discord import build_discord_payload, send_discord_notification
from .config import settings
from .schemas.notify import Notify
from .schemas.responses import NotifyResponse


router = APIRouter(prefix="/api")


@router.post(
    "/notify",
    status_code=200,
    response_model=NotifyResponse,
    responses={200: {"description": "Success"}},
)
async def notify(
    payload: Notify,
    request: Request,
) -> dict[str, Any]:
    """
    Forward a Proxmox alert to Discord and archive the full Proxmox message.
    """

    log_id = uuid.uuid4().hex
    log_url = str(request.url_for("get_log", log_id=log_id))
    log_path = settings.log_directory / f"{log_id}.log"

    try:
        log_path.write_text(payload.message, encoding="utf-8")
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Could not write log file")


    discord_payload = build_discord_payload(payload, log_url)
    status_code = await send_discord_notification(
        webhook_url=payload.discord_webhook,
        payload=discord_payload,
    )

    return {"logs": log_url, "discord_status": status_code}



@router.get(
    "/logs/{log_id}",
    response_class=PlainTextResponse,
    name="get_log",
)
async def get_log(log_id: str) -> str:
    """
    Fetch the full text of a stored Proxmox alert message.

    """
    log_path = settings.log_directory / f"{log_id}.log"
    if not log_path.exists():
        raise HTTPException(status_code=404, detail="Log not found")
    return log_path.read_text(encoding="utf-8")
