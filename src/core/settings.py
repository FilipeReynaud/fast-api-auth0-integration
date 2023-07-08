from environs import Env
from pydantic import BaseSettings

env = Env()
env.read_env()


class Settings(BaseSettings):
  API_V1_STR: str = "/api/v1"

  # Auth0
  AUTH0_DOMAIN: str
  AUTH0_CLIENT_ID: str
  AUTH0_CLIENT_SECRET: str


settings = Settings()
