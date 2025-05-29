import fastapi
import svcs.fastapi
from fastapi import APIRouter, HTTPException
from fastapi.security import HTTPBearer, HTTPBasic
from fastapi.security.http import HTTPBase

from throttling_sequencer.api.http.v1.dto.game_state import GameStateDto
from throttling_sequencer.api.http.v1.dto.unit_goal import UnitGoalDto
from throttling_sequencer.services.mappers.game_state import GameStateV1Mapper
from throttling_sequencer.services.mappers.unit_goal import UnitGoalMapperV1
from throttling_sequencer.services.navigation.throttle_steps_service import ThrottleStepsService

throttle_router = APIRouter()


@throttle_router.post(
    "/calculate_throttle_steps",
    response_model=list[UnitGoalDto],
    summary="Compute throttle steps for first player/enemy unit",
)
async def throttle_steps(
    state: GameStateDto,
    services: svcs.fastapi.DepContainer,
    request: fastapi.Request,
):
    # TODO: remove it - just some ideas - move it to a middleware
    x = HTTPBearer(auto_error=False)
    val = await x(request)
    x = HTTPBase(auto_error=False, scheme="")
    val = await x(request)
    x = HTTPBasic(auto_error=False)
    val = await x(request)

    try:
        # Map DTO → domain GameState (if needed) or pass DTO directly
        step_service = services.get(ThrottleStepsService)
        domain_state = GameStateV1Mapper.from_dto(state)
        goals = step_service.calculate_throttle_steps(domain_state)
        # Assuming each UnitGoal has .unit_id and .path attributes
        return [UnitGoalMapperV1.to_dto(goal) for goal in goals]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
