from datetime import datetime

from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    id: int | None = None
    exp: datetime | None = None


class UserResponse(BaseModel):
    username: str
    id: int
