from throttling_sequencer.api.graphql.types.navigation.unit_goal import UnitGoalType
from throttling_sequencer.api.http.v1.dto.unit_goal import UnitGoalDto
from throttling_sequencer.domain.grid.goal import UnitGoal


class UnitGoalMapperV1:
    @classmethod
    def to_dto(cls, unit_goal: UnitGoal):
        return UnitGoalDto(coordinate=unit_goal.coordinate, throttle=unit_goal.throttle)


class UnitGoalGqlMapper:
    @classmethod
    def to_gql_output(cls, unit_goal: UnitGoal) -> UnitGoalType:
        return UnitGoalType(coordinate=unit_goal.coordinate, throttle=unit_goal.throttle)
