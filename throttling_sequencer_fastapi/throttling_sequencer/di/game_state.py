from throttling_sequencer.domain.game.retriever import GameStateRetriever
from throttling_sequencer.infrastructure.fake_implementations.game.retriever import RandomGameStateRetriever


def get_game_state_retriever() -> GameStateRetriever:
    return RandomGameStateRetriever()
