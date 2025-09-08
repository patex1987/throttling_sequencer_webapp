import strawberry

from throttling_sequencer.api.graphql.schema_entry.root_query_schema import Query
from throttling_sequencer.api.graphql.schema_entry.root_subscription_schema import Subscription


def build_schema():
    """
    TODO: add custom extensions
    :return:
    """
    schema = strawberry.Schema(query=Query, subscription=Subscription)
    return schema
