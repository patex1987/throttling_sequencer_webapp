from piccolo.engine import engine_finder, Engine

from throttling_sequencer.domain.request_meta.gql_request_info import GqlRequestInfo
from throttling_sequencer.domain.request_meta.gql_request_repo import AsyncGqlRequestRepository
from throttling_sequencer.repositories.piccolo.request_meta.table import GqlRequestInfoTable
from throttling_sequencer.services.mappers.gql_request_info import GqlRequestInfoPiccoloMapper


class PiccoloGqlRequestRepository(AsyncGqlRequestRepository):
    def __init__(self, piccolo_engine: Engine):
        self.piccolo_engine = piccolo_engine
        self.request_mapper = GqlRequestInfoPiccoloMapper

    async def save(self, gql_request_info: GqlRequestInfo):
        piccolo_request_info = self.request_mapper.from_domain_to_orm(gql_request_info)
        async with self.piccolo_engine.transaction():
            await piccolo_request_info.save()

    async def get(self, request_id: str) -> GqlRequestInfo:
        selected_request_piccolo = await (
            GqlRequestInfoTable.objects()
                .where(GqlRequestInfoTable.request_id == request_id)
                .first()
        )
        return self.request_mapper.from_orm_to_domain(selected_request_piccolo)


    async def get_all(self) -> list[GqlRequestInfo]:
        # all_requests_piccolo = await GqlRequestInfoTable.select()
        all_requests_piccolo = await GqlRequestInfoTable.objects()
        return [self.request_mapper.from_orm_to_domain(request_piccolo) for request_piccolo in all_requests_piccolo]

