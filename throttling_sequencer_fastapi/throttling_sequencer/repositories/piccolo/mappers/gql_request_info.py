from throttling_sequencer.domain.request_meta.gql_request_info import GqlRequestInfo
from throttling_sequencer.repositories.piccolo.request_meta.table import GqlRequestInfoTable


class GqlRequestInfoPiccoloMapper:
    """domain GqlRequestInfo <-> GqlRequestInfoTable ORM mapper"""

    @classmethod
    def from_domain_to_orm(cls, gql_request_info: GqlRequestInfo) -> GqlRequestInfoTable:
        return GqlRequestInfoTable(
            request_id=gql_request_info.request_id,
            field_name=gql_request_info.gql_operation_name,
            user_id=gql_request_info.user_id,
            request_at_unix=gql_request_info.request_at_unix,
        )

    @classmethod
    def from_orm_to_domain(cls, gql_request_info_table: GqlRequestInfoTable) -> GqlRequestInfo:
        return GqlRequestInfo(
            request_id=gql_request_info_table.request_id,
            gql_operation_name=gql_request_info_table.field_name,
            user_id=gql_request_info_table.user_id,
            request_at_unix=gql_request_info_table.request_at_unix,
        )
