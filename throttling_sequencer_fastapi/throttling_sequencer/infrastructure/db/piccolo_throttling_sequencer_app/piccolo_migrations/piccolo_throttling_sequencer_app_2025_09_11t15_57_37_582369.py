from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Integer
from piccolo.columns.column_types import Text
from piccolo.columns.column_types import Varchar
from piccolo.columns.indexes import IndexMethod


ID = "2025-09-11T15:57:37:582369"
VERSION = "1.28.0"
DESCRIPTION = "Creating"


async def forwards():
    manager = MigrationManager(
        migration_id=ID,
        app_name="piccolo_throttling_sequencer_app",
        description=DESCRIPTION,
    )

    manager.add_table(
        class_name="GqlRequestInfoTable",
        tablename="gql_request_info_table",
        schema=None,
        columns=None,
    )

    manager.add_column(
        table_class_name="GqlRequestInfoTable",
        tablename="gql_request_info_table",
        column_name="id",
        db_column_name="id",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 36,
            "default": "",
            "null": False,
            "primary_key": True,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.add_column(
        table_class_name="GqlRequestInfoTable",
        tablename="gql_request_info_table",
        column_name="request_id",
        db_column_name="request_id",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.add_column(
        table_class_name="GqlRequestInfoTable",
        tablename="gql_request_info_table",
        column_name="field_name",
        db_column_name="field_name",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.add_column(
        table_class_name="GqlRequestInfoTable",
        tablename="gql_request_info_table",
        column_name="user_id",
        db_column_name="user_id",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.add_column(
        table_class_name="GqlRequestInfoTable",
        tablename="gql_request_info_table",
        column_name="request_at_unix",
        db_column_name="request_at_unix",
        column_class_name="Integer",
        column_class=Integer,
        params={
            "default": 0,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    return manager
