import os
from pydantic import BaseSettings
from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    DB_URL: str = os.getenv('DATABASE_URL')
    DB_SECRET: str = os.getenv('DB_SECRET')
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY')
    JWT_EXPIRE_MINUTES: int = 15
    JWT_ALGORITHM: str = "HS256"
    COOKIE_NAME: str = "access_token"
    ADMIN_PASSWORD: str = os.getenv('ADMIN_PASSWORD')


settings = Settings()