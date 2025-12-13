import svcs
from starlette.requests import Request
from starlette.websockets import WebSocket

from throttling_sequencer.api.graphql.schema_entry.resolver_context import GqlOperationContext
from throttling_sequencer.domain.request_meta.gql_request_repo import AsyncGqlRequestRepository
from throttling_sequencer.services.throttle_steps_service import ThrottleStepsService


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
