from piccolo.engine import PostgresEngine
from svcs import Registry, Container

from throttling_sequencer.di.navigation import get_path_finder
from throttling_sequencer.di.services import get_throttle_step_service
from throttling_sequencer.di.repositories import get_piccolo_request_repository
from throttling_sequencer.di.game_state import get_game_state_retriever
from throttling_sequencer.domain.game.retriever import GameStateRetriever
from throttling_sequencer.domain.genetic_path.configuration import GeneticConfiguration
from throttling_sequencer.domain.navigation.path_finder import PathFinderStrategy
from throttling_sequencer.domain.request_meta.gql_request_repo import AsyncGqlRequestRepository
from throttling_sequencer.infrastructure.db.piccolo_conf import DB
from throttling_sequencer.services.throttle_steps_service import ThrottleStepsService


def repository_registrar(registry: Registry):
    """
    Inject the repository implementations into the registry.

    :param registry:
    :return:
    """
    # registry.register_value(AsyncGqlRequestRepository, InMemoryGqlRequestRepository())
    postgres_engine = DB
    registry.register_value(PostgresEngine, postgres_engine)
    registry.register_factory(AsyncGqlRequestRepository, factory=get_piccolo_request_repository)


def adjust_registry(registry: Registry):
    registry.register_factory(PathFinderStrategy, factory=get_path_finder)
    DEFAULT_GENETIC_CONFIG = GeneticConfiguration()
    registry.register_value(GeneticConfiguration, DEFAULT_GENETIC_CONFIG)
    registry.register_factory(ThrottleStepsService, factory=get_throttle_step_service)
    registry.register_factory(GameStateRetriever, factory=get_game_state_retriever)

    repository_registrar(registry)


def build_registry():
    registry = Registry()
    registry.register_factory(PathFinderStrategy, factory=get_path_finder)
    DEFAULT_GENETIC_CONFIG = GeneticConfiguration()
    registry.register_value(GeneticConfiguration, DEFAULT_GENETIC_CONFIG)
    registry.register_factory(ThrottleStepsService, factory=get_throttle_step_service)
    registry.register_factory(GameStateRetriever, factory=get_game_state_retriever)

    return registry


_REGISTRY = None
_CONTAINER = None


def independent_di_container() -> Container:
    """
    An independent (non-fastapi) dependency container.

    This is a singleton that can be used anywhere in the logic,
    outside a fastapi based app
    :return: svcs.Container
    """
    global _REGISTRY
    global _CONTAINER
    if not _REGISTRY:
        _REGISTRY = build_registry()
    if not _CONTAINER:
        _CONTAINER = Container(registry=_REGISTRY)

    return _CONTAINER
