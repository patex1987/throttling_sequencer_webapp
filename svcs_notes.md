### Different ways of registering strawberry fields

#### Currently, we are using the decorator approach

See the following example
```python
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

```

#### But you can invoke it explicitly as well

```python
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


def independent_resolver(info: Info[GqlOperationContext, Any], game_state_input: GameStateInputType) -> list[UnitGoalType]:
    throttle_steps_service = info.context.step_service
    game_state = GameStateGqlMapper.from_gql_type(game_state_input)
    throttle_steps = throttle_steps_service.calculate_throttle_steps(game_state)
    throttle_steps_gql = [UnitGoalGqlMapper.to_gql_output(step) for step in throttle_steps]
    return throttle_steps_gql


@strawberry.type
class ThrottleStepQuery:
    calculate_throttle_steps_differently = strawberry.field(
        resolver=independent_resolver, extensions=[HttpAuthExtension(), RequestInfoCollectorExtension()]
    )
```

### How to create an independent di container (non fastapi di)

this is something I found on multiple places on github.
of course, if you are on a cli based app (for example `typer`), you can attach the registry, container on the
context object of typer

```python
from svcs import Registry, Container

from throttling_sequencer.di.navigation import get_path_finder
from throttling_sequencer.di.services import get_throttle_step_service
from throttling_sequencer.di.game_state import get_game_state_retriever
from throttling_sequencer.domain.game.retriever import GameStateRetriever
from throttling_sequencer.domain.genetic_path.configuration import GeneticConfiguration
from throttling_sequencer.domain.navigation.path_finder import PathFinderStrategy
from throttling_sequencer.services.throttle_steps_service import ThrottleStepsService


def build_registry():
    registry = Registry()
    registry.register_factory(PathFinderStrategy, factory=get_path_finder)
    DEFAULT_GENETIC_CONFIG = GeneticConfiguration()
    registry.register_value(GeneticConfiguration, DEFAULT_GENETIC_CONFIG)
    registry.register_factory(ThrottleStepsService, factory=get_throttle_step_service)
    registry.register_factory(GameStateRetriever, factory=get_game_state_retriever)

    return registry


_REGISTRY = None
_CONTAINER = None


def independent_di_container() -> Container:
    """
    An independent (non-fastapi) dependency container.

    This is a singleton that can be used anywhere in the logic,
    outside a fastapi based app
    :return: svcs.Container
    """
    global _REGISTRY
    global _CONTAINER
    if not _REGISTRY:
        _REGISTRY = build_registry()
    if not _CONTAINER:
        _CONTAINER = Container(registry=_REGISTRY)

    return _CONTAINER
```