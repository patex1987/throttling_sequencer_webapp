from throttling_sequencer.api.graphql.types.game.game_state import GameStateInputType
from throttling_sequencer.domain.game.game_state import GameState
from throttling_sequencer.domain.game.unit import Unit
from throttling_sequencer.domain.grid.coordinate import Coordinate


class GameStateGqlMapper:
    """Gql GameStateInputType <-> Domain GameState"""

    @classmethod
    def from_gql_type(cls, game_state_type: GameStateInputType) -> GameState:
        player_units = [
            Unit(
                coordinate=Coordinate(unit.coordinate.x, unit.coordinate.y),
                speed=unit.speed,
                mass=unit.mass,
                friction=unit.friction,
            )
            for unit in game_state_type.player_units
        ]

        enemy_units = [
            Unit(
                coordinate=Coordinate(unit.coordinate.x, unit.coordinate.y),
                speed=unit.speed,
                mass=unit.mass,
                friction=unit.friction,
            )
            for unit in game_state_type.enemy_units
        ]

        return GameState(player_units=player_units, enemy_units=enemy_units)
