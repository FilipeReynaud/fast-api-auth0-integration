from typing import Tuple

from auth0.authentication import Database, GetToken
from auth0.authentication.token_verifier import AsymmetricSignatureVerifier, TokenVerifier
from auth0.exceptions import Auth0Error, TokenValidationError
from fastapi.security.http import HTTPAuthorizationCredentials

from src.core.settings import settings
from src.schemas.auth0.response_models import Auth0LogInResponse, SignUpResponse, ValidateTokenResponse
from src.schemas.user.user_model import UserRequest


class AuthenticationService:

  domain = settings.AUTH0_DOMAIN
  client_id = settings.AUTH0_CLIENT_ID
  client_secret = settings.AUTH0_CLIENT_SECRET

  @staticmethod
  def login(user_request: UserRequest) -> Tuple[Auth0LogInResponse or None, Auth0Error]:
    try:
      token = GetToken(AuthenticationService.domain,
                       AuthenticationService.client_id,
                       client_secret=AuthenticationService.client_secret)
      res = token.login(
        username=user_request.email,
        password=user_request.password,
        realm="Username-Password-Authentication",
      )

      return Auth0LogInResponse(**res), None
    except Auth0Error as err:
      return None, err

  @staticmethod
  def sign_up_user(user_request: UserRequest) -> Tuple[SignUpResponse or None, Auth0Error]:
    try:
      database = Database(AuthenticationService.domain, AuthenticationService.client_id)
      res = database.signup(
        email=user_request.email,
        password=user_request.password,
        connection="Username-Password-Authentication",
      )
      return SignUpResponse(**res), None
    except Auth0Error as err:
      return None, err

  @staticmethod
  def validate_auth0_id_token(
      id_token: HTTPAuthorizationCredentials) -> Tuple[ValidateTokenResponse or None, TokenValidationError]:

    try:
      jwks_url = f"https://{AuthenticationService.domain}/.well-known/jwks.json"
      issuer = f"https://{AuthenticationService.domain}/"

      asymmetric_signature_verifier = AsymmetricSignatureVerifier(jwks_url)  # Reusable instance
      token_verifier = TokenVerifier(signature_verifier=asymmetric_signature_verifier,
                                     issuer=issuer,
                                     audience=AuthenticationService.client_id)
      res = token_verifier.verify(id_token.credentials)
      return ValidateTokenResponse(**res), None
    except TokenValidationError as err:
      return None, err
