from dataclasses import dataclass

from throttling_sequencer.domain.grid.coordinate import Coordinate


@dataclass
class Unit:
    coordinate: Coordinate
    speed: float
    mass: float
    friction: float
