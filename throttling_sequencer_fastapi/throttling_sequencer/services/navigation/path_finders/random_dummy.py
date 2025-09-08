from uuid import uuid4

from throttling_sequencer.domain.game.game_state import GameState
from throttling_sequencer.domain.game.unit import Unit
from throttling_sequencer.domain.grid.coordinate import Coordinate
from throttling_sequencer.domain.grid.goal import UnitGoal
from throttling_sequencer.services.navigation.path_finders.base import PathFinder


class RandomDummyPathFinder(PathFinder):
    def __init__(self):
        self.id = uuid4()

    def find_path(self, game_state: GameState, main_unit: Unit, target_unit: Unit) -> list[UnitGoal]:
        random_path = [
            UnitGoal(Coordinate(1, 1), 1),
            UnitGoal(Coordinate(2, 2), 1),
            UnitGoal(Coordinate(3, 3), 1),
            UnitGoal(Coordinate(4, 4), 1),
            UnitGoal(Coordinate(5, 5), 1),
            UnitGoal(Coordinate(6, 6), 1),
            UnitGoal(Coordinate(7, 7), 1),
            UnitGoal(Coordinate(8, 8), 1),
            UnitGoal(Coordinate(9, 9), 1),
            UnitGoal(Coordinate(10, 10), 1),
        ]
        return random_path
