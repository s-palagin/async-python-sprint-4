# import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src.api.v1 import links
from src.core.config import app_settings
#  from src.core import config
from src.middleware.middleware import BlackListMiddleware
from src.utils.settings import BLACK_LIST

# from src.core.logger import LOGGING

app = FastAPI(
    title=app_settings.app_title,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    # Можно сразу сделать небольшую оптимизацию сервиса
    # и заменить стандартный JSON-сериализатор на более шуструю версию,
    # написанную на Rust
    default_response_class=ORJSONResponse,
    redoc_url=None
)

app.include_router(links.router, prefix='/api/v1', tags=['links'])
blm = BlackListMiddleware(black_list=BLACK_LIST)
app.add_middleware(BaseHTTPMiddleware, dispatch=blm)


if __name__ == '__main__':
    # Приложение может запускаться командой
    # `uvicorn main:app --host 0.0.0.0 --port 8080`
    # но чтобы не терять возможность использовать дебагер,
    # запустим uvicorn сервер через python
    uvicorn.run(
        'main:app',
        #        host=config.PROJECT_HOST,
        #        port=config.PROJECT_PORT,
    )
