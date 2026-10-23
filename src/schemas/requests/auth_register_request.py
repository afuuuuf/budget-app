from pydantic import BaseModel, Field


class AuthRegisterRequest(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., min_length=8, description="Password (min 8 characters)")
