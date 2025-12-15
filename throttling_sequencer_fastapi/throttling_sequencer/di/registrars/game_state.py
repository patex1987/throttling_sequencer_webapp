import svcs

from tests.fake_implementations.infrastructure.game.retriever import RandomGameStateRetriever
from throttling_sequencer.di.registrars.base import Registrar
from throttling_sequencer.domain.game.retriever import GameStateRetriever


class GameStateRegistrar(Registrar):
    def register(self, registry: svcs.Registry) -> None:
        registry.register_value(GameStateRetriever, RandomGameStateRetriever())
