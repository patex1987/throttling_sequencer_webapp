from piccolo.conf.apps import AppRegistry
from piccolo.engine import PostgresEngine

POSTGRES_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "postgres",
    "database": "postgres",
}

DB = PostgresEngine(config=POSTGRES_CONFIG, extra_nodes=None)

APP_REGISTRY = AppRegistry(
    apps=["throttling_sequencer.infrastructure.db.piccolo_throttling_sequencer_app.piccolo_app"],
)

# from throttling_sequencer.infrastructure.db.piccolo_throttling_sequencer_app import piccolo_app
