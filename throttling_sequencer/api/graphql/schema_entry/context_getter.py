import random

import svcs
from fastapi import Depends

from throttling_sequencer.api.graphql.schema_entry.resolver_context import ResolverContext

def di_context_getter(
    services: svcs.fastapi.DepContainer,
):
    return ResolverContext(di_container=services)
