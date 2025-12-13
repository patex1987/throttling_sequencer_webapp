from collections import OrderedDict

from throttling_sequencer.domain.request_meta.gql_request_info import GqlRequestInfo
from throttling_sequencer.domain.request_meta.gql_request_repo import AsyncGqlRequestRepository


class InMemoryGqlRequestRepository(AsyncGqlRequestRepository):
    def __init__(self):
        self._capacity = 100
        self._data_store: OrderedDict[str, GqlRequestInfo] = OrderedDict()

    async def save(self, gql_request_info: GqlRequestInfo):
        key = gql_request_info.request_id
        if key in self._data_store:
            self._data_store.pop(key)

        if len(self._data_store) >= self._capacity:
            self._data_store.popitem(last=False)
        self._data_store[key] = gql_request_info

    async def get(self, request_id: str) -> GqlRequestInfo | None:
        return self._data_store.get(request_id)

    async def get_all(self) -> list[GqlRequestInfo]:
        return list(self._data_store.values())
