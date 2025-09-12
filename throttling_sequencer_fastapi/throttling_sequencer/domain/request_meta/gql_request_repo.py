from typing import Protocol

from throttling_sequencer.domain.request_meta.gql_request_info import GqlRequestInfo


class AsyncGqlRequestRepository(Protocol):
    """Store meta information about the graphql request"""

    async def save(self, gql_request_info: GqlRequestInfo): ...

    async def get(self, request_id: str) -> GqlRequestInfo: ...

    async def get_all(self) -> list[GqlRequestInfo]: ...
