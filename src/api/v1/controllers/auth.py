from fastapi import APIRouter, Depends, Response, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

from src.domain.services.auth0.authentication_service import AuthenticationService
from src.schemas.auth0.response_models import LogInResponse
from src.schemas.user.user_model import UserRequest

# Scheme for the Authorization header
token_auth_scheme = HTTPBearer()

router = APIRouter()


class AuthController:

  @staticmethod
  @router.post("/login")
  def login(response: Response, user_request: UserRequest) -> LogInResponse or None:
    res, error = AuthenticationService.login(user_request)

    if not error and res:
      return LogInResponse(bearer_token=res.id_token)

    response.status_code = error.status_code
    return error

  @staticmethod
  @router.post("/signup")
  def sign_up(response: Response, user_request: UserRequest):
    _, error = AuthenticationService.sign_up_user(user_request)
    
    if not error:
      return "OK"

    response.status_code = error.status_code
    return error

  @staticmethod
  @router.get("/get_user_info")
  def private(
      response: Response,
      token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
  ):
    """A valid access token is required to access this route"""

    result, error = AuthenticationService.validate_auth0_id_token(token)

    if error:
      response.status_code = status.HTTP_403_FORBIDDEN
      return error

    return result
