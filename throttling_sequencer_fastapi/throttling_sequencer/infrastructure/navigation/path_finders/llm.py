from throttling_sequencer.domain.game.game_state import GameState
from throttling_sequencer.domain.game.unit import Unit
from throttling_sequencer.domain.grid.goal import UnitGoal
from throttling_sequencer.domain.navigation.path_finder import PathFinderStrategy


class LLMPathFinderStrategy(PathFinderStrategy):
    """
    PathFinder that uses an LLM to determine the path to the destination.
    """

    def find_path(self, game_state: GameState, main_unit: Unit, target_unit: Unit) -> list[UnitGoal]:
        """
        TODO: add the actual LLM call
        :param game_state:
        :param main_unit:
        :param target_unit:
        :return:
        """
        path = [UnitGoal(main_unit.coordinate, 0), UnitGoal(main_unit.coordinate, 1)]
        return path
