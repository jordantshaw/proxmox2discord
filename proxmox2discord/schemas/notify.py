from pydantic import BaseModel, AnyUrl

class Notify(BaseModel):
    discord_webhook: AnyUrl
    message: str | None = None
    title: str | None = None
    severity: str | None = 'info'
    discord_description: str | None = None
    mention_user_id: str | None = None