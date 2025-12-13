from piccolo.engine import PostgresEngine
from svcs import Container

from throttling_sequencer.repositories.piccolo.request_meta.repo import PiccoloGqlRequestRepository


def get_piccolo_request_repository(svcs_container: Container) -> PiccoloGqlRequestRepository:
    postgres_engine = svcs_container.get(PostgresEngine)
    return PiccoloGqlRequestRepository(postgres_engine)
