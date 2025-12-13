from throttling_sequencer.di.app_wide_registrar import FastapiDIRegistrars


def get_development_registrars() -> FastapiDIRegistrars:
    app_registrars = FastapiDIRegistrars(
        common_registrars=[],
        app_lifetime_registrars=[],
        fastapi_lifespan_registrars=[],
    )
    return app_registrars
