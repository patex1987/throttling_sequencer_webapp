import svcs

from throttling_sequencer.di.registrars.base import Registrar
from throttling_sequencer.domain.game.retriever import GameStateRetriever
from throttling_sequencer.infrastructure.fake_implementations.game.retriever import RandomGameStateRetriever


class GameStateRegistrar(Registrar):
    def register(self, registry: svcs.Registry) -> None:
        registry.register_value(GameStateRetriever, RandomGameStateRetriever())
