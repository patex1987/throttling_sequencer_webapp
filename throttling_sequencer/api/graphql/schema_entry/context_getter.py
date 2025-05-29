import random

import svcs
from fastapi import Depends
from starlette.requests import Request
from starlette.websockets import WebSocket

from throttling_sequencer.api.graphql.schema_entry.resolver_context import ResolverContext


def di_context_getter(
    services: svcs.fastapi.DepContainer,
):
    return ResolverContext(di_container=services)

async def svcs_context(request: Request = None, websocket: WebSocket = None):
    scope = request or websocket
    registry = getattr(scope.state, svcs._core._KEY_REGISTRY)
    async with svcs.Container(registry) as container:
        # Include FastAPI's background_tasks if needed (not shown for brevity)
        yield ResolverContext(di_container=container)