from throttling_sequencer.api.http.v1.dto.unit_goal import UnitGoalDto
from throttling_sequencer.domain.grid.goal import UnitGoal


class UnitGoalMapperV1:
    @classmethod
    def to_dto(cls, unit_goal: UnitGoal):
        return UnitGoalDto(coordinate=unit_goal.coordinate, throttle=unit_goal.throttle)
