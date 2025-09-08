from throttling_sequencer.domain.game.game_state import GameState
from throttling_sequencer.domain.game.unit import Unit
from throttling_sequencer.domain.grid.goal import UnitGoal
from throttling_sequencer.services.navigation.path_finders.base import PathFinder


class LLMPathFinder(PathFinder):
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
