import os
from pydantic import BaseSettings
from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    DB_URL: str = os.getenv('DATABASE_URL')
    DB_SECRET: str = os.getenv('DB_SECRET')


settings = Settings()