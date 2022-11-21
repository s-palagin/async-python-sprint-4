import os
from logging import config as logging_config

from pydantic import BaseSettings

from .logger import LOGGING

from dotenv import load_dotenv

load_dotenv()
logging_config.dictConfig(LOGGING)


class AppSettings(BaseSettings):
    app_title: str = "LibraryApp"
    database_dsn: str = (
        'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres'
    )

    class Config:
        env_file = '.env'


app_settings = AppSettings()

PROJECT_HOST = os.getenv('PROJECT_HOST', '0.0.0.0')
PROJECT_PORT = int(os.getenv('PROJECT_PORT', '8000'))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
