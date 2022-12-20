import uuid

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class AccessTokenData(BaseModel):
    id: str
    exp: int
