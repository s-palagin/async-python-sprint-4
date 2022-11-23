import os
import string
from logging import config as logging_config

from pydantic import BaseSettings

from .logger import LOGGING

# список запрещенных подсетей
BLACK_LIST: list[str] = [
    '127.0.0.2',
    '192.168.0.1',
]

ALPHABET = string.ascii_letters + string.digits
LINK_LENGTH = 6

logging_config.dictConfig(LOGGING)


class AppSettings(BaseSettings):
    app_title: str = "LibraryApp"
    database_dsn: str = (
        'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres'
    )
    project_host: str = '0.0.0.0'
    project_port: int = 8000
    test_database: str = (
        'postgresql+asyncpg://postgres:postgres@localhost:5432/test_db'
    )

    class Config:
        env_file = '.env'


app_settings = AppSettings()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
