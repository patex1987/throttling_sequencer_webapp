import strawberry

from throttling_sequencer.api.graphql.types.game.unit import UnitInputType


@strawberry.input
class GameStateInputType:
    player_units: list[UnitInputType]
    enemy_units: list[UnitInputType]
