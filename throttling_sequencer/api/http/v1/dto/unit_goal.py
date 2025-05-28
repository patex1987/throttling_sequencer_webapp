from pydantic import BaseModel

from throttling_sequencer.domain.grid.coordinate import Coordinate


class UnitGoalDto(BaseModel):
    coordinate: Coordinate
    throttle: float


if __name__ == "__main__":
    # print(UnitGoalDto(coordinate=Coordinate(x=0, y=0), throttle=0.5).model_dump_json())
    unit = UnitGoalDto.model_validate_json('{"coordinate": {"x": 0, "y": 0}, "throttle": 0.5}')
    print(unit)
    x = unit.model_construct()
    print(unit.model_construct())
