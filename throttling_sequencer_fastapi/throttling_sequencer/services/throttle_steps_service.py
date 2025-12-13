import logging

from throttling_sequencer.domain.game.game_state import GameState
from throttling_sequencer.domain.grid.goal import UnitGoal
from throttling_sequencer.services.navigation.path_finders.base import PathFinder

import structlog

external_logger = logging.getLogger("external")
logger = structlog.get_logger(__name__)


class ThrottleStepsService:
    def __init__(self, path_finder: PathFinder):
        logger.info(f"new throttle step service created {id(self)}")
        self.path_finder = path_finder

    def calculate_throttle_steps(self, game_state: GameState) -> list[UnitGoal]:
        external_logger.info("step service - coming from the outside world - python logger")
        return self.path_finder.find_path(game_state, game_state.player_units[0], game_state.enemy_units[0])
