import strawberry

from throttling_sequencer.api.graphql.operations.throttle_step_calculator.query import ThrottleStepQuery


@strawberry.type
class Query(ThrottleStepQuery):
    pass
