from pydantic import BaseModel


class AuthRefreshRequest(BaseModel):
    refresh_token: str
