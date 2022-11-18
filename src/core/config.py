import os
from logging import config as logging_config

from pydantic import BaseSettings

from .logger import LOGGING

# from dotenv import load_dotenv


# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class AppSettings(BaseSettings):
    app_title: str = "LibraryApp"
    database_dsn: str = (
        'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres'
    )

    class Config:
        env_file = '.env'


app_settings = AppSettings()

# Название проекта. Используется в Swagger-документации
# PROJECT_NAME = os.getenv('PROJECT_NAME', 'library')
# PROJECT_HOST = os.getenv('PROJECT_HOST', '0.0.0.0')
# PROJECT_PORT = os.getenv('PROJECT_PORT', '8000')

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
