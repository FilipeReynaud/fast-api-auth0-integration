from pydantic import BaseModel


class SignUpResponse(BaseModel):
    _id: str
    email_verified: bool
    email: str


class Auth0LogInResponse(BaseModel):
    access_token: str
    id_token: str
    scope: str
    expires_in: int
    token_type: str


class LogInResponse(BaseModel):
    bearer_token: str


class ValidateTokenResponse(BaseModel):
    nickname: str
    name: str
    picture: str
    updated_at: str
    email: str
    email_verified: bool
    iss: str
    aud: str
    iat: int
    exp: int
    sub: str
