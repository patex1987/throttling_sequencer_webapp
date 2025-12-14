from typing import Protocol

import structlog

logger = structlog.get_logger(__name__)


class InfrastructureSetup(Protocol):
    async def setup(self) -> None: ...

    async def shutdown(self) -> None: ...


class PiccoloInfrastructureSetup(InfrastructureSetup):
    async def setup(self) -> None:
        from throttling_sequencer.infrastructure.db.piccolo_conf import DB
        from throttling_sequencer.infrastructure.db.piccolo_throttling_sequencer_app.pool_config import (
            get_db_pool_config,
        )

        db_pool_config = get_db_pool_config()
        await DB.start_connection_pool(**db_pool_config)

    async def shutdown(self) -> None:
        from throttling_sequencer.infrastructure.db.piccolo_conf import DB

        logger.info("Shutting down db connection pool")

        await DB.close_connection_pool()


class LocalDevInfrastructureSetup(InfrastructureSetup):
    async def setup(self) -> None:
        pass

    async def shutdown(self) -> None:
        pass
