from typing import Any

import strawberry
from strawberry import Info

from throttling_sequencer.api.graphql.field_extensions.auth_extension import HttpAuthExtension
from throttling_sequencer.api.graphql.field_extensions.request_info_collector import RequestInfoCollectorExtension
from throttling_sequencer.api.graphql.schema_entry.resolver_context import GqlOperationContext
from throttling_sequencer.api.graphql.types.game.game_state import GameStateInputType
from throttling_sequencer.api.graphql.types.navigation.unit_goal import UnitGoalType
from throttling_sequencer.api.graphql.mappers.game_state import GameStateGqlMapper
from throttling_sequencer.api.graphql.mappers.unit_goal import UnitGoalGqlMapper


@strawberry.type
class ThrottleStepQuery:

    # TODO: make the business logic of extensions injectable
    @strawberry.field(extensions=[HttpAuthExtension(), RequestInfoCollectorExtension()])
    async def calculate_throttle_steps(
        self,
        info: Info[GqlOperationContext, Any],
        game_state_input: GameStateInputType,
    ) -> list[UnitGoalType]:
        throttle_steps_service = info.context.step_service
        game_state = GameStateGqlMapper.from_gql_type(game_state_input)
        throttle_steps = throttle_steps_service.calculate_throttle_steps(game_state)
        throttle_steps_gql = [UnitGoalGqlMapper.to_gql_output(step) for step in throttle_steps]
        return throttle_steps_gql
