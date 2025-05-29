import strawberry

from throttling_sequencer.api.graphql.operations.throttle_step_calculator.subscription import ThrottleStepSubscription


@strawberry.type
class Subscription(ThrottleStepSubscription):
    pass
