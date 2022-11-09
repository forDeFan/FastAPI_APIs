import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """
    Configuration class to set constants within app context.
    Some values taken from .env (see .env-example for reference).
    """

    DB_URL: str = os.getenv("DATABASE_URL")
    DB_SECRET: str = os.getenv("DB_SECRET")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_EXPIRE_MINUTES: int = 15
    JWT_ALGORITHM: str = "HS256"
    COOKIE_NAME: str = "access_token"
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD")


settings = Settings()
