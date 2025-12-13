import svcs.fastapi

import fastapi

from throttling_sequencer.di.registry import adjust_registry
from throttling_sequencer.infrastructure.db.piccolo_conf import DB
from throttling_sequencer.infrastructure.db.piccolo_throttling_sequencer_app.pool_config import get_db_pool_config


@svcs.fastapi.lifespan
async def di_lifespan(app: fastapi.FastAPI, registry: svcs.Registry):
    """
    Sets up the DI registry and the database connection pool

    :param app:
    :param registry:
    :return:
    """
    # Startup
    # TODO: make this optional and configurable through env vars
    db_pool_config = get_db_pool_config()
    await DB.start_connection_pool(**db_pool_config)
    adjust_registry(registry=registry)
    try:
        yield {"application": "throttling_calculator"}
    # Shutdown
    finally:
        await DB.close_connection_pool()  # graceful shutdown
