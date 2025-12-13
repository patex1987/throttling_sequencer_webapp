from piccolo.columns import Text, Integer, UUID
from piccolo.table import Table


class GqlRequestInfoTable(Table):
    id = UUID(primary_key=True)
    request_id = Text()
    field_name = Text()
    user_id = Text()
    request_at_unix = Integer()
