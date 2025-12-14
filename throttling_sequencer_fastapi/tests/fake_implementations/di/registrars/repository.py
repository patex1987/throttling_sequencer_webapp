import svcs

from throttling_sequencer.di.registrars.base import Registrar
from throttling_sequencer.domain.request_meta.gql_request_repo import AsyncGqlRequestRepository
from throttling_sequencer.repositories.in_memory.request_meta.repo import InMemoryGqlRequestRepository


class InMemoryRepositoryRegistrar(Registrar):
    def register(self, registry: svcs.Registry) -> None:
        registry.register_factory(AsyncGqlRequestRepository, factory=InMemoryGqlRequestRepository)
