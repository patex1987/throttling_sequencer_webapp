from typing import AsyncGenerator, Any

from strawberry.fastapi import GraphQLRouter

from throttling_sequencer.api.graphql.schema_entry.build import build_schema
from throttling_sequencer.api.graphql.schema_entry.context_getter import gql_operation_context_getter
from throttling_sequencer.api.graphql.schema_entry.resolver_context import GqlOperationContext


def create_graphql_router() -> GraphQLRouter[AsyncGenerator[GqlOperationContext, Any], None]:
    """

    TODO: add config support for enabling / disabling graphiql ide
    """
    gql_schema = build_schema()

    router = GraphQLRouter(
        schema=gql_schema,
        context_getter=gql_operation_context_getter,
        graphql_ide="graphiql",
        subscription_protocols=["graphql-ws", "graphql-transport-ws"],
    )
    return router
