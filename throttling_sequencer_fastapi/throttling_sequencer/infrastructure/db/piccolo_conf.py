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

    # These are asyncpg connection options. They’ll apply to EACH new connection.
    # Failover- & PgBouncer-friendly: no server-side prepared statements
    "statement_cache_size": 0,
    # Default command timeout on the client side (seconds)
    "command_timeout": 3.0,
    # Server parameters set on connect:
    "server_settings": {
        "application_name": "fastapi-strawberry-piccolo",
        # "statement_timeout": "3000",  # ms; DB kills long queries fast

    },
    # Optional: how long to wait for TCP connect (seconds) - NOT WORKING
    # "connect_timeout": "2.0",
}

def start_engine():
    engine = PostgresEngine(config=POSTGRES_CONFIG, extra_nodes=None)
    return engine

DB = start_engine()

APP_REGISTRY = AppRegistry(
    apps=["throttling_sequencer.infrastructure.db.piccolo_throttling_sequencer_app.piccolo_app"],
)

# from throttling_sequencer.infrastructure.db.piccolo_throttling_sequencer_app import piccolo_app
