import fastapi
from strawberry.fastapi import GraphQLRouter

from throttling_sequencer.api.graphql.schema_entry.build import build_schema
from throttling_sequencer.api.graphql.schema_entry.context_getter import gql_operation_context_getter
from throttling_sequencer.api.http.middlewares.authentication import CustomAuthenticationMiddleware
from throttling_sequencer.api.http.middlewares.log_context_enrichment import LogContextMiddleware
from throttling_sequencer.api.http.v1.routes.health import health_router
from throttling_sequencer.api.http.v1.routes.throttle_steps_calculator import throttle_router
from throttling_sequencer.core.log_config import configure_logging
from throttling_sequencer.core.telemetry import instrument_for_telemetry
from throttling_sequencer.di.fastapi_lifespan import di_lifespan
from throttling_sequencer.infrastructure.db.piccolo_throttling_sequencer_app.programmatic_migration import maybe_migrate


def create_app():
    configure_logging()
    app = fastapi.FastAPI(lifespan=di_lifespan)
    app.include_router(router=health_router, prefix="/api/v1/health", tags=["health"])
    app.include_router(router=throttle_router, prefix="/api/v1/throttle", tags=["throttle"])

    gql_schema = build_schema()
    graphql_router = GraphQLRouter(
        schema=gql_schema,
        context_getter=gql_operation_context_getter,
        graphql_ide="graphiql",
        subscription_protocols=["graphql-ws", "graphql-transport-ws"],
    )
    app.include_router(router=graphql_router, prefix="/graphql", tags=["graphql"])

    app.add_middleware(CustomAuthenticationMiddleware)
    app.add_middleware(LogContextMiddleware)
    instrument_for_telemetry(app)

    # app.add_exception_handler(Exception, exception_handler)
    # app.add_exception_handler(500, exception_handler)

    # maybe_migrate()

    return app
