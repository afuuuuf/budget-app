from pydantic import BaseModel


class UserInfoResponse(BaseModel):
    id: str
    email: str
