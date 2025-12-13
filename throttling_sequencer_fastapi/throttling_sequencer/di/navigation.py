from svcs import Container

from throttling_sequencer.domain.genetic_path.configuration import GeneticConfiguration
from throttling_sequencer.domain.navigation.path_finder import PathFinderStrategy
from throttling_sequencer.infrastructure.fake_implementations.navigation.path_finders.random_dummy import (
    RandomDummyPathFinderStrategy,
)
from throttling_sequencer.infrastructure.navigation.path_finders.genetic import GeneticPathFinderStrategy


def get_path_finder(svcs_container: Container) -> PathFinderStrategy:
    # return RandomDummyPathFinder()
    genetic_configuration = svcs_container.get(GeneticConfiguration)
    return GeneticPathFinderStrategy(genetic_configration=genetic_configuration)


def get_path_finder_2() -> PathFinderStrategy:
    return RandomDummyPathFinderStrategy()
