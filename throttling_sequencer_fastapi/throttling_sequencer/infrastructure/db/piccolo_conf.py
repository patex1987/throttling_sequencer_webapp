import os

from piccolo.conf.apps import AppRegistry
from piccolo.engine import PostgresEngine

from throttling_sequencer.core.database_config import PiccoloDBConfig

PICCOLO_DB_CONFIG = PiccoloDBConfig()

POSTGRES_CONFIG = {
    "host": PICCOLO_DB_CONFIG.db_host,
    "port": PICCOLO_DB_CONFIG.db_port,
    "user": PICCOLO_DB_CONFIG.db_user,
    "password": PICCOLO_DB_CONFIG.db_password,
    "database": PICCOLO_DB_CONFIG.db_database,
}

DB = PostgresEngine(config=POSTGRES_CONFIG, extra_nodes=None)

APP_REGISTRY = AppRegistry(
    apps=["throttling_sequencer.infrastructure.db.piccolo_throttling_sequencer_app.piccolo_app"],
)

# from throttling_sequencer.infrastructure.db.piccolo_throttling_sequencer_app import piccolo_app
