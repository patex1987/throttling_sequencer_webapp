import strawberry

from throttling_sequencer.api.graphql.operations.throttle_step_calculator.query import ThrottleStepQuery
from throttling_sequencer.api.graphql.schema_entry.root_query_schema import Query


def build_schema():
    """
    TODO: add custom extensions
    :return:
    """
    schema = strawberry.Schema(query=Query)
    return schema
