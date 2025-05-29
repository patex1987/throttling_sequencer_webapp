import asyncio
from typing import Any, AsyncGenerator

import strawberry
from strawberry import Info

from throttling_sequencer.api.graphql.field_extensions.auth_extension import HttpAuthExtension
from throttling_sequencer.api.graphql.field_extensions.ws_auth_extension import WsHttpAuthExtension
from throttling_sequencer.api.graphql.schema_entry.resolver_context import ResolverContext
from throttling_sequencer.api.graphql.types.game.game_state import GameStateInputType
from throttling_sequencer.api.graphql.types.navigation.unit_goal import UnitGoalType
from throttling_sequencer.domain.grid.coordinate import Coordinate
from throttling_sequencer.domain.grid.goal import UnitGoal
from throttling_sequencer.services.mappers.unit_goal import UnitGoalGqlMapper


@strawberry.type
class ThrottleStepSubscription:
    @strawberry.subscription(extensions=[WsHttpAuthExtension()])
    async def generate_steps(
        self,
        info: Info[ResolverContext, Any],
        game_state_input: GameStateInputType
    ) -> AsyncGenerator[UnitGoalType, None]:
        """
        Emits StepInfo objects from range_input.start up to range_input.end,
        pausing `delay_ms` milliseconds between each.
        """

        delay_ms = 500

        # for idx in range(range_input.start, range_input.end + 1):
        for idx in range(0, 9 + 1):
            # Here you’d compute or fetch real data;
            # we’ll just synthesize some values
            domain_goal = UnitGoal(coordinate=Coordinate(0, 1), throttle=0.5)
            goal_gql = UnitGoalGqlMapper.to_gql_output(domain_goal)
            yield goal_gql
            await asyncio.sleep(delay_ms / 1000)
