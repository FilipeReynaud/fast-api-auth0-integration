from unittest.mock import MagicMock, patch

import pytest
from auth0.exceptions import Auth0Error
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)

authentication_service_path = 'src.domain.services.auth0.authentication_service.AuthenticationService.{}'


@pytest.fixture
def mocked_authentication_service_validate_auth0_id_token(mocker):

  def validate_auth0_id_token(token):
    if token.credentials == 'valid-token':
      return {
        'sub': 'user_id',
        'email': 'test@example.com',
      }, None
    else:
      return None, 'Invalid token'

  mocked_method = MagicMock(side_effect=validate_auth0_id_token)

  with patch(authentication_service_path.format('validate_auth0_id_token'), mocked_method):
    yield mocked_method


@pytest.fixture
def mocked_authentication_service_login(mocker):

  def login(user_request):

    class ValidLoginResponse:
      id_token = 'valid_token'

    class InvalidLoginResponse(Auth0Error):
      status_code = 403
      meessage = 'Wrong email or password.'

    if user_request.email == 'test@example.com' and user_request.password == 'test_password':
      return ValidLoginResponse, None
    else:
      return None, InvalidLoginResponse

  mocked_method = MagicMock(side_effect=login)

  with patch(authentication_service_path.format('login'), mocked_method):
    yield mocked_method


def test_protected_route_with_valid_token_should_return_200(mocked_authentication_service_validate_auth0_id_token):
  # Arrange
  requestHeadersWithValidToken = {'Authorization': 'Bearer valid-token'}
  expectedStatusCode = 200
  expectedTokenPassed = HTTPAuthorizationCredentials(scheme='Bearer', credentials='valid-token')

  # Act
  response = client.get('/api/v1/auth/get_user_info', headers=requestHeadersWithValidToken)

  # Assert
  assert response.status_code == expectedStatusCode
  mocked_authentication_service_validate_auth0_id_token.assert_called_once_with(expectedTokenPassed)


def test_protected_route_without_token_should_return_403(mocked_authentication_service_validate_auth0_id_token):
  # Arrange
  requestHeadersWithoutToken = {'Authorization': 'Bearer '}
  expectedStatusCode = 403

  # Act
  response = client.get('/api/v1/auth/get_user_info', headers=requestHeadersWithoutToken)

  # Assert
  assert response.status_code == expectedStatusCode
  mocked_authentication_service_validate_auth0_id_token.assert_not_called()


def test_protected_route_with_invalid_token_should_return_403(mocked_authentication_service_validate_auth0_id_token):
  # Arrange
  requestHeadersWithInvalidToken = {'Authorization': 'Bearer invalid-token'}
  expectedStatusCode = 403
  expectedTokenPassed = HTTPAuthorizationCredentials(scheme='Bearer', credentials='invalid-token')

  # Act
  response = client.get('/api/v1/auth/get_user_info', headers=requestHeadersWithInvalidToken)

  # Assert
  assert response.status_code == expectedStatusCode
  mocked_authentication_service_validate_auth0_id_token.assert_called_once_with(expectedTokenPassed)


def test_login_with_valid_credentials_should_return_200(mocked_authentication_service_login):
  # Arrange
  requestHeadersWithValidFields = {'email': 'test@example.com', 'password': 'test_password'}
  expectedStatusCode = 200

  # Act
  response = client.post('/api/v1/auth/login', json=requestHeadersWithValidFields)

  # Assert
  assert response.status_code == expectedStatusCode
  mocked_authentication_service_login.assert_called_once_with(requestHeadersWithValidFields)


def test_login_with_invalid_credentials_email_should_return_403(mocked_authentication_service_login):
  # Arrange
  requestHeadersWithInvalidEmail = {'email': 'TEST@example.com', 'password': 'test_password'}
  expectedStatusCode = 403

  # Act
  response = client.post('/api/v1/auth/login', json=requestHeadersWithInvalidEmail)

  # Assert
  assert response.status_code == expectedStatusCode
  mocked_authentication_service_login.assert_called_once_with(requestHeadersWithInvalidEmail)


def test_login_with_invalid_credentials_password_should_return_403(mocked_authentication_service_login):
  # Arrange
  requestHeadersWithInvalidEmail = {'email': 'test@example.com', 'password': 'test_PASSWORD'}
  expectedStatusCode = 403

  # Act
  response = client.post('/api/v1/auth/login', json=requestHeadersWithInvalidEmail)

  # Assert
  assert response.status_code == expectedStatusCode
  mocked_authentication_service_login.assert_called_once_with(requestHeadersWithInvalidEmail)
