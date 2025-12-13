import svcs
from starlette.requests import Request
from starlette.websockets import WebSocket

from throttling_sequencer.api.graphql.schema_entry.resolver_context import ResolverContext, GqlOperationContext
from throttling_sequencer.domain.request_meta.gql_request_repo import AsyncGqlRequestRepository
from throttling_sequencer.services.throttle_steps_service import ThrottleStepsService


def di_context_getter(
    services: svcs.fastapi.DepContainer,
):
    """
    Doesn't work with subscription / websocket based graphql operations

    :param services:
    :return:
    """
    return ResolverContext(di_container=services)


async def svcs_context_getter(request: Request = None, websocket: WebSocket = None):
    """
    Works even with graphql subscription operations (websocket)

    :param request:
    :param websocket:
    :return:
    """
    scope = request or websocket
    registry = getattr(scope.state, svcs._core._KEY_REGISTRY)
    async with svcs.Container(registry) as container:
        yield ResolverContext(di_container=container)


async def gql_operation_context_getter(request: Request = None, websocket: WebSocket = None):
    """
    A more explicit context for graphql operations, this way the operations
    won't have access to the whole container, but only to the limited scope
    of dependencies

    :param request:
    :param websocket:
    :return:
    """
    scope = request or websocket
    registry = getattr(scope.state, svcs._core._KEY_REGISTRY)
    async with svcs.Container(registry) as container:
        # Include FastAPI's background_tasks if needed (not shown for brevity)
        step_service = container.get(ThrottleStepsService)
        request_info_repo = container.get(AsyncGqlRequestRepository)

        yield GqlOperationContext(step_service=step_service, request_info_repository=request_info_repo)
