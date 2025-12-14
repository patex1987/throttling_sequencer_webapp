from throttling_sequencer.di.app_wide_registrar import ApplicationDIConfig
from throttling_sequencer.di.registrars.game_state import GameStateRegistrar
from throttling_sequencer.di.registrars.repository import RepositoryRegistrar
from throttling_sequencer.di.registrars.throttle_step_service import ThrottleStepsServiceRegistrar
from throttling_sequencer.infrastructure.infra_setup.production import ProductionInfrastructureSetup


def get_production_registrars() -> ApplicationDIConfig:
    fastapi_lifespan_registrars = [ThrottleStepsServiceRegistrar(), GameStateRegistrar(), RepositoryRegistrar()]
    app_wide_registrars = ApplicationDIConfig(
        app_lifetime_registrars=[],
        fastapi_lifespan_registrars=fastapi_lifespan_registrars,
        infrastructure_bootstrapper=ProductionInfrastructureSetup(),
    )

    return app_wide_registrars
