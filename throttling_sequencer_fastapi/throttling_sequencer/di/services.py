# TODO: refactor this into smaller registrars
from piccolo.engine import Engine, PostgresEngine
from svcs import Container, Registry

from throttling_sequencer.domain.genetic_path.configuration import GeneticConfiguration
from throttling_sequencer.domain.request_meta.gql_request_repo import AsyncGqlRequestRepository
from throttling_sequencer.infrastructure.db.piccolo_conf import DB
from throttling_sequencer.repositories.in_memory.request_meta.repo import InMemoryGqlRequestRepository
from throttling_sequencer.repositories.piccolo.request_meta.repo import PiccoloGqlRequestRepository
from throttling_sequencer.services.game_state_retriever.base import BaseGameStateRetriever
from throttling_sequencer.services.game_state_retriever.random import RandomGameStateRetriever
from throttling_sequencer.services.navigation.path_finders.base import PathFinder
from throttling_sequencer.services.navigation.path_finders.genetic import GeneticPathFinder
from throttling_sequencer.services.navigation.path_finders.random_dummy import RandomDummyPathFinder
from throttling_sequencer.services.navigation.throttle_steps_service import ThrottleStepsService


def get_path_finder(svcs_container: Container) -> PathFinder:
    # return RandomDummyPathFinder()
    genetic_configuration = svcs_container.get(GeneticConfiguration)
    return GeneticPathFinder(genetic_configration=genetic_configuration)


def get_path_finder_2() -> PathFinder:
    return RandomDummyPathFinder()


def get_throttle_step_service(svcs_container: Container) -> ThrottleStepsService:
    path_finder = svcs_container.get(PathFinder)
    return ThrottleStepsService(path_finder=path_finder)


def get_game_state_retriever() -> BaseGameStateRetriever:
    return RandomGameStateRetriever()


def get_piccolo_request_repository(svcs_container: Container) -> PiccoloGqlRequestRepository:
    postgres_engine = svcs_container.get(PostgresEngine)
    return PiccoloGqlRequestRepository(postgres_engine)


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
    registry.register_factory(PathFinder, factory=get_path_finder)
    DEFAULT_GENETIC_CONFIG = GeneticConfiguration()
    registry.register_value(GeneticConfiguration, DEFAULT_GENETIC_CONFIG)
    registry.register_factory(ThrottleStepsService, factory=get_throttle_step_service)
    registry.register_factory(BaseGameStateRetriever, factory=get_game_state_retriever)

    repository_registrar(registry)


_REGISTRY = None
_CONTAINER = None


def build_registry():
    registry = Registry()
    registry.register_factory(PathFinder, factory=get_path_finder)
    DEFAULT_GENETIC_CONFIG = GeneticConfiguration()
    registry.register_value(GeneticConfiguration, DEFAULT_GENETIC_CONFIG)
    registry.register_factory(ThrottleStepsService, factory=get_throttle_step_service)
    registry.register_factory(BaseGameStateRetriever, factory=get_game_state_retriever)

    return registry


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
