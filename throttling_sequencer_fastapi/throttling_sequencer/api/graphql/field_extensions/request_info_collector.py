from datetime import datetime
from typing import Any

import structlog
from strawberry import Info
from strawberry.extensions import FieldExtension
from strawberry.extensions.field_extension import AsyncExtensionResolver

from throttling_sequencer.domain.request_meta.gql_request_info import GqlRequestInfo
from throttling_sequencer.domain.request_meta.gql_request_repo import AsyncGqlRequestRepository

logger = structlog.get_logger(__name__)


class RequestInfoCollectorExtension(FieldExtension):
    async def resolve_async(self, next_: AsyncExtensionResolver, source: Any, info: Info, **kwargs: Any) -> Any:
        request_obj = info.context.request

        request_info = GqlRequestInfo(
            request_id=request_obj.state.request_id,
            gql_operation_name="Base field",
            user_id=request_obj.state.user_id,
            request_at_unix=int(datetime.now().timestamp()),
        )

        request_info_repo: AsyncGqlRequestRepository = info.context.request_info_repository
        await request_info_repo.save(gql_request_info=request_info)
        current_data = await request_info_repo.get_all()

        logger.info(f"current_data in the db: {current_data}")

        return await next_(source, info, **kwargs)
