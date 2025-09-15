from throttling_sequencer.api.graphql.types.navigation.unit_goal import UnitGoalType
from throttling_sequencer.domain.grid.goal import UnitGoal


class UnitGoalGqlMapper:
    @classmethod
    def to_gql_output(cls, unit_goal: UnitGoal) -> UnitGoalType:
        return UnitGoalType(coordinate=unit_goal.coordinate, throttle=unit_goal.throttle)
