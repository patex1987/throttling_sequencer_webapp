from tests.fake_implementations.di.registrars.repository import InMemoryRepositoryRegistrar
from throttling_sequencer.di.app_wide_registrar import ApplicationDIRegistrars
from throttling_sequencer.di.registrars.game_state import GameStateRegistrar
from throttling_sequencer.di.registrars.throttle_step_service import ThrottleStepsServiceRegistrar
from throttling_sequencer.infrastructure.infra_setup.base import LocalDevInfrastructureSetup


def get_development_registrars() -> ApplicationDIRegistrars:
    fastapi_lifespan_registrars = [ThrottleStepsServiceRegistrar(), GameStateRegistrar(), InMemoryRepositoryRegistrar()]
    app_registrars = ApplicationDIRegistrars(
        common_registrars=[],
        app_lifetime_registrars=[],
        fastapi_lifespan_registrars=fastapi_lifespan_registrars,
        infrastructure_bootstrapper=LocalDevInfrastructureSetup(),
    )
    return app_registrars
