import json
from functools import wraps

from opentelemetry import trace
import uuid
from typing import Any, Callable, Awaitable

import structlog


logger = structlog.get_logger(__name__)


def get_wrapped_receive(receive, scope, receive_custom_attributes):
    @wraps(receive)
    async def wrapped_receive():
        message = await receive()
        logger.warning(f"----- Message: {message}")
        if message["type"] != "websocket.receive":
            return message

        text_data = message.get("text")
        if not text_data:
            return message

        data = json.loads(text_data)

        if data.get("type") not in "connection_init":
            return message

        scope["state"]["checkpoint"] = "connection_init_happened"
        payload = message.get("payload")
        if not payload:
            return message

        _authorization_header = payload.get("authorization")
        ws_entity = "custom_ws_entity"
        scope["state"]["ws_entity"] = ws_entity
        return message

    return wrapped_receive


class LogContextMiddleware:
    """
    Enriches structlog's contextvars with a business context
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
        if scope["type"] not in ("http", "websocket"):
            return await self.app(scope, receive, send)

        scope.setdefault("state", {})

        unique_request_id = str(uuid.uuid4())
        logger.info("new request id has been created")
        span = trace.get_current_span()
        ctx = span.get_span_context()
        if ctx.trace_id:
            trace_id = f"{ctx.trace_id:032x}"
            structlog.contextvars.bind_contextvars(trace_id=trace_id)
        # this is just for the sake of exercise,
        # imagine some actual business context retrieval
        structlog.contextvars.bind_contextvars(
            user_id="main_user_xyz",
            request_id=unique_request_id,
        )
        scope["state"]["user_id"] = "main_user_xyz"
        scope["state"]["request_id"] = unique_request_id

        wrapped_receive = receive
        if scope["type"] == "websocket":
            receive_custom_attributes = {}
            wrapped_receive = get_wrapped_receive(receive, scope, receive_custom_attributes)

        try:
            await self.app(scope, wrapped_receive, send)
        finally:
            # logger.warning(f'scope on exit {scope}')
            structlog.contextvars.clear_contextvars()
