import fastapi
from strawberry.fastapi import GraphQLRouter

from throttling_sequencer.api.graphql.schema_entry.build import build_schema
from throttling_sequencer.api.graphql.schema_entry.context_getter import di_context_getter
from throttling_sequencer.api.http.middlewares.authentication import CustomAuthenticationMiddleware
from throttling_sequencer.api.http.v1.routes.throttle_steps_calculator import throttle_router
from throttling_sequencer.core.telemetry import instrument_for_telemetry
from throttling_sequencer.di.fastapi_lifespan import di_lifespan


def create_app():
    app = fastapi.FastAPI(lifespan=di_lifespan)
    app.include_router(router=throttle_router, prefix="/api/v1/throttle", tags=["throttle"])

    graphql_router = GraphQLRouter(
        schema=build_schema(),
        # context_getter=di_context_getter,
        context_getter=di_context_getter,
        graphql_ide="graphiql",
    )
    app.include_router(router=graphql_router, prefix="/graphql", tags=["graphql"])

    app.add_middleware(CustomAuthenticationMiddleware)
    instrument_for_telemetry(app)

    # app.add_exception_handler(Exception, exception_handler)
    # app.add_exception_handler(500, exception_handler)

    return app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(create_app(), host="0.0.0.0", port=8080, log_level="info")
