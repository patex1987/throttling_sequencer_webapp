import uuid
from typing import Any

import structlog
from fastapi.security import HTTPBasic, HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from strawberry import Info
from strawberry.extensions import FieldExtension
from strawberry.extensions.field_extension import AsyncExtensionResolver

logger = structlog.get_logger(__name__)


class HttpAuthExtension(FieldExtension):
    async def resolve_async(self, next_: AsyncExtensionResolver, source: Any, info: Info, **kwargs: Any) -> Any:
        request_obj = info.context.request

        logger.info(f"headers detected by HttpAuthExtension: {request_obj.headers}")
        authorization = request_obj.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)

        match scheme.lower():
            case "basic":
                logger.info(f"Graphql validation: Basic auth detected: {credentials}")
                basic_creds_extractor = HTTPBasic(auto_error=False)
                basic_creds = await basic_creds_extractor(request=request_obj)
                logger.info(f"Graphql validation: Basic auth creds: {basic_creds}")
            case "bearer":
                logger.info(f"Graphql validation: Bearer auth detected: {credentials}")
                bearer_creds_extractor = HTTPBearer(auto_error=False)
                bearer_creds = await bearer_creds_extractor(request=request_obj)
                logger.info(f"Graphql validation: Bearer auth creds: {bearer_creds}")
            case "internal":
                logger.info(f"Graphql validation: Internal auth detected: {credentials}")
            case _:
                logger.info(f"Graphql validation: Unknown auth scheme detected: {scheme}")

        uniq_val = uuid.uuid4().hex
        structlog.contextvars.bind_contextvars(custom_gql_data=f"GABOR_{uniq_val}")
        return await next_(source, info, **kwargs)
