from throttling_sequencer.api.http.v1.dto.game_state import GameStateDto
from throttling_sequencer.domain.game.game_state import GameState
from throttling_sequencer.domain.game.unit import Unit
from throttling_sequencer.domain.grid.coordinate import Coordinate


class GameStateV1Mapper:
    """Rest GameStateDto <-> Domain GameState"""

    @classmethod
    def from_dto(cls, game_state_dto: GameStateDto) -> GameState:
        player_units = [
            Unit(
                coordinate=Coordinate(unit.coordinate.x, unit.coordinate.y),
                speed=unit.speed,
                mass=unit.mass,
                friction=unit.friction,
            )
            for unit in game_state_dto.player_units
        ]
        enemy_units = [
            Unit(
                coordinate=Coordinate(unit.coordinate.x, unit.coordinate.y),
                speed=unit.speed,
                mass=unit.mass,
                friction=unit.friction,
            )
            for unit in game_state_dto.enemy_units
        ]
        return GameState(player_units=player_units, enemy_units=enemy_units)
