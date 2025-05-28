from dataclasses import dataclass

TIMEOUT_1000_MS = 1000


@dataclass
class GeneticConfiguration:
    """
    :param max_sequence_length: The length of each sequence in the population can vary
        from 1 to max_t.
    :param population_size:
    :param num_generations:
    :param mutation_rate:
    :param num_best_parents:
    :param num_worst_parents:
    :param speed_threshold:
    :param throttle_range:
    :param distance_weight:
    :param speed_weight:
    :param length_weight:
    :param nonzero_weight:
    :param timeout_ms:
    """

    max_sequence_length: int = 100
    population_size: int = 100
    num_generations: int = 100
    mutation_rate: float = 0.1
    num_best_parents: int = 20
    num_worst_parents: int = 10
    speed_threshold: int = 5
    throttle_range: tuple[int, int] = (0, 300)
    distance_weight: float = 1.0
    speed_weight: float = 0.5
    length_weight: float = 0.01
    nonzero_weight: float = 0.01
    timeout_ms: int = TIMEOUT_1000_MS

    def __post_init__(self):
        print(f"New genetic config instance {id(self)}")
