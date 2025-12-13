from throttling_sequencer.di.services import independent_di_container
from throttling_sequencer.services.game_state_retriever.base import BaseGameStateRetriever
from throttling_sequencer.services.throttle_steps_service import ThrottleStepsService


def execute():
    container = independent_di_container()
    # path_finder = container.get(PathFinder)
    throttle_steps_service = container.get(ThrottleStepsService)
    game_state_retriever = container.get(BaseGameStateRetriever)

    game_state = game_state_retriever.get_current_state()
    throttle_paths = throttle_steps_service.calculate_throttle_steps(game_state)
    return throttle_paths


if __name__ == "__main__":
    throttle_paths = execute()
    for throttle_path in throttle_paths:
        print(throttle_path)
