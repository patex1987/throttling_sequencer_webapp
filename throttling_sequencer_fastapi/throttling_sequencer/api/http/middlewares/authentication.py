# TODO: move to a separate commit


import fastapi
import starlette.types

import structlog

from throttling_sequencer.application.authentication.manager import AsyncAuthenticationManager

logger = structlog.get_logger(__name__)


class AuthenticationMiddleware:
    def __init__(self, app: fastapi.FastAPI, authentication_manager: AsyncAuthenticationManager):
        self.app = app
        self.authentication_manager = authentication_manager
        self.excluded_paths = ("/health",)

    async def __call__(
        self, scope: starlette.types.Scope, receive: starlette.types.Receive, send: starlette.types.Send
    ):
        if scope["type"] not in ("http", "websocket"):
            return await self.app(scope, receive, send)

        raw_path = scope.get("path")
        if str(raw_path).startswith(self.excluded_paths):
            logger.debug("Auth validation skipped for health checks")
            return await self.app(scope, receive, send)

        user_identity = await self.authentication_manager.authenticate_jwt_token(None)

        # TODO: add exception handling here
        await self.app(scope, receive, send)
