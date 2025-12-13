from throttling_sequencer.di.app_wide_registrar import FastapiDIRegistrars
from throttling_sequencer.di.registrars.game_state import GameStateRegistrar
from throttling_sequencer.di.registrars.repository import RepositoryRegistrar
from throttling_sequencer.di.registrars.throttle_step_service import ThrottleStepsServiceRegistrar


def get_production_registrars() -> FastapiDIRegistrars:
    fastapi_lifespan_registrars = [ThrottleStepsServiceRegistrar(), GameStateRegistrar(), RepositoryRegistrar()]
    app_wide_registrars = FastapiDIRegistrars(
        common_registrars=[],
        app_lifetime_registrars=[],
        fastapi_lifespan_registrars=fastapi_lifespan_registrars,
    )

    return app_wide_registrars
