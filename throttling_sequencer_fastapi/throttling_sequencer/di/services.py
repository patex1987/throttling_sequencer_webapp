# TODO: refactor this into smaller registrars
from svcs import Container

from throttling_sequencer.domain.navigation.path_finder import PathFinderStrategy
from throttling_sequencer.services.throttle_steps_service import ThrottleStepsService


def get_throttle_step_service(svcs_container: Container) -> ThrottleStepsService:
    path_finder = svcs_container.get(PathFinderStrategy)
    return ThrottleStepsService(path_finder=path_finder)
