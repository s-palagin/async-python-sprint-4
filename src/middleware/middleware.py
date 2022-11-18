from typing import Any, Callable

from fastapi import Request, Response, status


class BlackListMiddleware:
    def __init__(self, black_list: list[str]):
        self._black_list = black_list

    async def __call__(self, request: Request, call_next: Callable) -> Any:
        if request.client and request.client.host not in self._black_list:
            response = await call_next(request)
            return response
        return Response('Acsess denied', status_code=status.HTTP_403_FORBIDDEN)
