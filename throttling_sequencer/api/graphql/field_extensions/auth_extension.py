from typing import Any

from fastapi.security import HTTPBasic, HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from strawberry import Info
from strawberry.extensions import FieldExtension
from strawberry.extensions.field_extension import AsyncExtensionResolver


class HttpAuthExtension(FieldExtension):
    async def resolve_async(self, next_: AsyncExtensionResolver, source: Any, info: Info, **kwargs: Any) -> Any:
        request_obj = info.context.request

        print(f"headers detected by HttpAuthExtension: {request_obj.headers}")
        authorization = request_obj.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)

        match scheme.lower():
            case "basic":
                print(f"Graphql validation: Basic auth detected: {credentials}")
                basic_creds_extractor = HTTPBasic(auto_error=False)
                basic_creds = await basic_creds_extractor(request=request_obj)
                print(f"Graphql validation: Basic auth creds: {basic_creds}")
            case "bearer":
                print(f"Graphql validation: Bearer auth detected: {credentials}")
                bearer_creds_extractor = HTTPBearer(auto_error=False)
                bearer_creds = await bearer_creds_extractor(request=request_obj)
                print(f"Graphql validation: Bearer auth creds: {bearer_creds}")
            case "internal":
                print(f"Graphql validation: Internal auth detected: {credentials}")
            case _:
                print(f"Graphql validation: Unknown auth scheme detected: {scheme}")

        return await next_(source, info, **kwargs)
