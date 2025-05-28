from dataclasses import dataclass

from throttling_sequencer.domain.game.unit import Unit


@dataclass
class GameState:
    player_units: list[Unit]
    enemy_units: list[Unit]
