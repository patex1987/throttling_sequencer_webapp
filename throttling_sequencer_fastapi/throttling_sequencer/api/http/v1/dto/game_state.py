from pydantic import BaseModel

from throttling_sequencer.api.http.v1.dto.unit import UnitDto


class GameStateDto(BaseModel):
    player_units: list[UnitDto]
    enemy_units: list[UnitDto]
