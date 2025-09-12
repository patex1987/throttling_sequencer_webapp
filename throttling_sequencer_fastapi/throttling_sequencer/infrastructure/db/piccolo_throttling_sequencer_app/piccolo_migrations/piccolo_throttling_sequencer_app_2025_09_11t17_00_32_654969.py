from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import UUID
from piccolo.columns.column_types import Varchar
from piccolo.columns.defaults.uuid import UUID4


ID = "2025-09-11T17:00:32:654969"
VERSION = "1.28.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID,
        app_name="piccolo_throttling_sequencer_app",
        description=DESCRIPTION,
    )

    manager.alter_column(
        table_class_name="GqlRequestInfoTable",
        tablename="gql_request_info_table",
        column_name="id",
        db_column_name="id",
        params={"default": UUID4()},
        old_params={"default": ""},
        column_class=UUID,
        old_column_class=Varchar,
        schema=None,
    )

    return manager
