from dataclasses import dataclass

from throttling_sequencer.domain.grid.coordinate import Coordinate


@dataclass
class UnitGoal:
    coordinate: Coordinate
    throttle: float
