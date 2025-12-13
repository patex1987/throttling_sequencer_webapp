import structlog
from piccolo.engine import Engine

import asyncpg
import backoff

from throttling_sequencer.domain.request_meta.gql_request_info import GqlRequestInfo
from throttling_sequencer.domain.request_meta.gql_request_repo import AsyncGqlRequestRepository
from throttling_sequencer.repositories.piccolo.request_meta.table import GqlRequestInfoTable
from throttling_sequencer.repositories.piccolo.mappers.gql_request_info import GqlRequestInfoPiccoloMapper

from piccolo.table import Table

logger = structlog.get_logger(__name__)


async def get_db_metadata():
    row = await Table.raw("select inet_server_addr() as addr, pg_is_in_recovery() as ro").run()
    if not row:
        return None
    match = row[0]
    return match.get("addr"), match.get("ro")


TRANSIENT = (
    asyncpg.exceptions.ReadOnlySQLTransactionError,  # 25006
    asyncpg.exceptions.ConnectionDoesNotExistError,
    ConnectionError,
)


class PiccoloGqlRequestRepository(AsyncGqlRequestRepository):
    def __init__(self, piccolo_engine: Engine):
        self.piccolo_engine = piccolo_engine
        self.request_mapper = GqlRequestInfoPiccoloMapper

    @backoff.on_exception(backoff.expo, TRANSIENT, max_time=4, jitter=backoff.full_jitter)
    async def save(self, gql_request_info: GqlRequestInfo):
        db_addr, db_read_only = await get_db_metadata()
        logger.info(f"DB failover metadata: {db_addr=}, {db_read_only=}")

        # fail early !!! (let's not use in prod)
        if db_read_only:
            raise asyncpg.exceptions.ReadOnlySQLTransactionError("on reader")

        piccolo_request_info = self.request_mapper.from_domain_to_orm(gql_request_info)
        async with self.piccolo_engine.transaction():
            await piccolo_request_info.save()

    async def get(self, request_id: str) -> GqlRequestInfo:
        selected_request_piccolo = await (
            GqlRequestInfoTable.objects().where(GqlRequestInfoTable.request_id == request_id).first()
        )
        return self.request_mapper.from_orm_to_domain(selected_request_piccolo)

    async def get_all(self) -> list[GqlRequestInfo]:
        # all_requests_piccolo = await GqlRequestInfoTable.select()
        all_requests_piccolo = await GqlRequestInfoTable.objects()
        return [self.request_mapper.from_orm_to_domain(request_piccolo) for request_piccolo in all_requests_piccolo]
