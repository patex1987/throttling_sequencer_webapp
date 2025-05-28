from throttling_sequencer.domain.game.game_state import GameState
from throttling_sequencer.domain.grid.goal import UnitGoal
from throttling_sequencer.services.navigation.path_finders.base import PathFinder


class ThrottleStepsService:
    def __init__(self, path_finder: PathFinder):
        print(f"new throttle step service created {id(self)}")
        self.path_finder = path_finder

    def calculate_throttle_steps(self, game_state: GameState) -> list[UnitGoal]:
        return self.path_finder.find_path(game_state, game_state.player_units[0], game_state.enemy_units[0])
