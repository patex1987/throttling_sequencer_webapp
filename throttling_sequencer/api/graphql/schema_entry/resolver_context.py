from dataclasses import dataclass

from strawberry.fastapi import BaseContext
from svcs import Container


@dataclass
class ResolverContext(BaseContext):
    """
    info.context that is visible to all graphql resolvers
    """

    di_container: Container
