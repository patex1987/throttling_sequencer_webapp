import strawberry

from throttling_sequencer.api.graphql.types.navigation.coordinate import CoordinateType


@strawberry.type
class UnitGoalType:
    coordinate: CoordinateType
    throttle: float
