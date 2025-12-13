from typing import Protocol

from throttling_sequencer.domain.game.game_state import GameState


class GameStateRetriever(Protocol):
    def get_current_state(self) -> GameState: ...
