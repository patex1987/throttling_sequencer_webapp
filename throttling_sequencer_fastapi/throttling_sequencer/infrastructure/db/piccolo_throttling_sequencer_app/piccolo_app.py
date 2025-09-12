"""
Import all of the Tables subclasses in your app here, and register them with
the APP_CONFIG.
"""

import os

from piccolo.conf.apps import AppConfig, table_finder, get_package

from throttling_sequencer.repositories.piccolo.request_meta.table import GqlRequestInfoTable

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


APP_CONFIG = AppConfig(
    app_name="piccolo_throttling_sequencer_app",
    migrations_folder_path=os.path.join(CURRENT_DIRECTORY, "piccolo_migrations"),
    # table_classes=table_finder(
    #     modules=[".tables"],
    #     package=get_package(__name__),
    #     exclude_imported=True,
    # ),
    table_classes=[GqlRequestInfoTable],
    migration_dependencies=[],
    commands=[],
)
