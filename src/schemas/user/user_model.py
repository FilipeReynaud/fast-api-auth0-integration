from typing import Optional

from pydantic import BaseModel


class UserRequest(BaseModel):
    email: str
    password: str


class User(UserRequest):
    id: int
    username: str
    hashed_password: str
    active: bool
    access_token: Optional[str]
