from dataclasses import dataclass


@dataclass
class GqlRequestInfo:
    request_id: str
    gql_operation_name: str
    user_id: str
    request_at_unix: int
