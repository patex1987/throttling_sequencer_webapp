from typing import Any

import strawberry
from strawberry import Info

from throttling_sequencer.api.graphql.field_extensions.auth_extension import HttpAuthExtension
from throttling_sequencer.api.graphql.field_extensions.request_info_collector import RequestInfoCollectorExtension
from throttling_sequencer.api.graphql.schema_entry.resolver_context import ResolverContext, GqlOperationContext
from throttling_sequencer.api.graphql.types.game.game_state import GameStateInputType
from throttling_sequencer.api.graphql.types.navigation.unit_goal import UnitGoalType
from throttling_sequencer.services.mappers.game_state import GameStateGqlMapper
from throttling_sequencer.services.mappers.unit_goal import UnitGoalGqlMapper
from throttling_sequencer.services.navigation.throttle_steps_service import ThrottleStepsService


def independent_resolver(info: Info[ResolverContext, Any], game_state_input: GameStateInputType) -> list[UnitGoalType]:
    throttle_steps_service = info.context.di_container.get(ThrottleStepsService)
    game_state = GameStateGqlMapper.from_gql_type(game_state_input)
    throttle_steps = throttle_steps_service.calculate_throttle_steps(game_state)
    throttle_steps_gql = [UnitGoalGqlMapper.to_gql_output(step) for step in throttle_steps]
    return throttle_steps_gql


@strawberry.type
class ThrottleStepQuery:
    calculate_throttle_steps_differently = strawberry.field(
        resolver=independent_resolver, extensions=[HttpAuthExtension()]
    )

    # TODO: make the business logic of extensions injectable
    @strawberry.field(extensions=[HttpAuthExtension(), RequestInfoCollectorExtension()])
    async def calculate_throttle_steps(
        self,
        info: Info[GqlOperationContext, Any],
        game_state_input: GameStateInputType,
        # self, info: Info[ResolverContext, Any], game_state_input: GameStateInputType
    ) -> list[UnitGoalType]:
        # throttle_steps_service = info.context.di_container.get(ThrottleStepsService)
        throttle_steps_service = info.context.step_service
        game_state = GameStateGqlMapper.from_gql_type(game_state_input)
        throttle_steps = throttle_steps_service.calculate_throttle_steps(game_state)
        throttle_steps_gql = [UnitGoalGqlMapper.to_gql_output(step) for step in throttle_steps]
        return throttle_steps_gql
