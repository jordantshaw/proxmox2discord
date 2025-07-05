from pydantic import BaseModel, AnyUrl

class NotifyResponse(BaseModel):
    """
    Response model for the /notify endpoint.
    """
    logs: AnyUrl
    discord_status: int