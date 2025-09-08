from throttling_sequencer.domain.game.game_state import GameState
from throttling_sequencer.services.game_state_retriever.base import BaseGameStateRetriever


class FileBasedGameStateRetriever(BaseGameStateRetriever):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_current_state(self) -> GameState:
        with open(self.file_path, "r") as file:
            content = file.read()
        return GameState.from_json(content)
