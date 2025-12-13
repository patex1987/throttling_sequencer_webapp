from dataclasses import dataclass
from typing import Sequence

from throttling_sequencer.di.registrars.base import Registrar


@dataclass
class FastapiDIRegistrars:
    """
    This class is used to register the dependencies for the FastAPI application.
    """

    common_registrars: Sequence[Registrar]
    app_lifetime_registrars: Sequence[Registrar]
    fastapi_lifespan_registrars: Sequence[Registrar]
