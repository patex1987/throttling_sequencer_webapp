from tests.fake_implementations.di.registrars.repository import InMemoryRepositoryRegistrar
from throttling_sequencer.di.app_wide_registrar import ApplicationDIConfig
from throttling_sequencer.di.registrars.game_state import GameStateRegistrar
from throttling_sequencer.di.registrars.throttle_step_service import ThrottleStepsServiceRegistrar
from throttling_sequencer.infrastructure.infra_setup.local_dev import LocalDevInfrastructureSetup


def get_development_registrars() -> ApplicationDIConfig:
    fastapi_lifespan_registrars = [ThrottleStepsServiceRegistrar(), GameStateRegistrar(), InMemoryRepositoryRegistrar()]
    app_registrars = ApplicationDIConfig(
        app_lifetime_registrars=[],
        fastapi_lifespan_registrars=fastapi_lifespan_registrars,
        infrastructure_bootstrapper=LocalDevInfrastructureSetup(),
    )
    return app_registrars
