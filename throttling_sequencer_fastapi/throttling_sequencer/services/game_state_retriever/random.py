from throttling_sequencer.domain.game.game_state import GameState
from throttling_sequencer.domain.game.unit import Unit
from throttling_sequencer.domain.grid.coordinate import Coordinate
from throttling_sequencer.services.game_state_retriever.base import BaseGameStateRetriever


class RandomGameStateRetriever(BaseGameStateRetriever):
    def get_current_state(self) -> GameState:
        state = GameState(
            player_units=[Unit(coordinate=Coordinate(x=0, y=0), speed=0, mass=10, friction=0.01)],
            enemy_units=[Unit(coordinate=Coordinate(x=0, y=5000), speed=0, mass=50, friction=0.8)],
        )
        return state
