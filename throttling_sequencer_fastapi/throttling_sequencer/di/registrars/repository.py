import svcs
from piccolo.engine import engine_finder
from throttling_sequencer.di.registrars.base import Registrar
from throttling_sequencer.domain.request_meta.gql_request_repo import AsyncGqlRequestRepository
from throttling_sequencer.repositories.piccolo.request_meta.repo import PiccoloGqlRequestRepository


class RepositoryRegistrar(Registrar):
    def register(self, registry: svcs.Registry) -> None:
        registry.register_factory(AsyncGqlRequestRepository, factory=self.__class__.get_piccolo_request_repository)

    @classmethod
    def get_piccolo_request_repository(cls, svcs_container: svcs.Container) -> "PiccoloGqlRequestRepository":
        postgres_engine = engine_finder()
        return PiccoloGqlRequestRepository(postgres_engine)
