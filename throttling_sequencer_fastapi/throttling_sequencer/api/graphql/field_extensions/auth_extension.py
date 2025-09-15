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
        """TODO: add real credential validation"""
        request_obj = info.context.request

        authorization = request_obj.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)

        match scheme.lower():
            case "basic":
                logger.debug(f"Graphql validation: Basic auth detected: {credentials}")
                basic_creds_extractor = HTTPBasic(auto_error=False)
                _basic_creds = await basic_creds_extractor(request=request_obj)
            case "bearer":
                logger.debug(f"Graphql validation: Bearer auth detected: {credentials}")
                bearer_creds_extractor = HTTPBearer(auto_error=False)
                _bearer_creds = await bearer_creds_extractor(request=request_obj)
            case "internal":
                logger.debug(f"Graphql validation: Internal auth detected: {credentials}")
            case _:
                logger.debug(f"Graphql validation: Unknown auth scheme detected: {scheme}")

        uniq_val = uuid.uuid4().hex
        structlog.contextvars.bind_contextvars(custom_gql_data=f"GABOR_{uniq_val}")
        return await next_(source, info, **kwargs)
