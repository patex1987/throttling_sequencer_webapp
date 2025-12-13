from dataclasses import dataclass

from strawberry.fastapi import BaseContext

from throttling_sequencer.domain.request_meta.gql_request_repo import AsyncGqlRequestRepository
from throttling_sequencer.services.throttle_steps_service import ThrottleStepsService


@dataclass
class GqlOperationContext(BaseContext):
    """
    info.context that is visible to all graphql resolvers
    """

    step_service: ThrottleStepsService
    request_info_repository: AsyncGqlRequestRepository
