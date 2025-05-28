import svcs.fastapi

import fastapi

from throttling_sequencer.di.services import adjust_registry


@svcs.fastapi.lifespan
async def di_lifespan(app: fastapi.FastAPI, registry: svcs.Registry):
    # Startup

    adjust_registry(registry=registry)
    yield {"application": "throttling_calculator"}
    # Shutdown
