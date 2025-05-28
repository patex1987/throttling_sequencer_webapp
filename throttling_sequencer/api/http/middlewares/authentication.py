# TODO: move to a separate commit

from typing import Callable, Awaitable, Any

from fastapi.security import HTTPBearer, HTTPBasic
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request


class CustomAuthenticationMiddleware:
    """
    The ASGI application middleware.

    currently just a no-op that checks the auth type from the headers
    and extracts the values
    """
    def __init__(
        self,
        app,
    ):
        self.app = app

    async def __call__(
        self,
        scope: dict[str, Any],
        receive: Callable[[], Awaitable[dict[str, Any]]],
        send: Callable[[dict[str, Any]], Awaitable[None]],
    ) -> None:
        """
        TODO: remove the print statements
        TODO: get rid of the code duplication

        :param scope:
        :param receive:
        :param send:
        :return:
        """
        if scope["type"] not in ("http", "websocket"):
            return await self.app(scope, receive, send)

        request = Request(scope, receive)

        authorization = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        print(f'headers detected by fastapi ExampleMiddleware: {request.headers}')

        match scheme.lower():
            case 'basic':
                print(f'Fastapi validation: Basic auth detected: {credentials}')
                basic_creds_extractor = HTTPBasic(auto_error=False)
                basic_creds = await basic_creds_extractor(request=request)
                print(f'Fastapi validation: Basic auth creds: {basic_creds}')
            case 'bearer':
                print(f'Fastapi validation: Bearer auth detected: {credentials}')
                bearer_creds_extractor = HTTPBearer(auto_error=False)
                bearer_creds = await bearer_creds_extractor(request=request)
                print(f'Fastapi validation: Bearer auth creds: {bearer_creds}')
            case 'internal':
                print(f'Fastapi validation: Internal auth detected: {credentials}')
            case _:
                print(f'Fastapi validation: Unknown auth scheme detected: {scheme}')

        return await self.app(scope, receive, send)