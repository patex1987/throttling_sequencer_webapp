from dataclasses import dataclass
from typing import Sequence

from throttling_sequencer.di.registrars.base import Registrar
from throttling_sequencer.infrastructure.infra_setup.base import InfrastructureSetup


@dataclass
class ApplicationDIRegistrars:
    """
    Container for app specific registrars and infrastructure setup.

    - common_registrars
    - app_lifetime_registrars
    - fastapi_lifespan_registrars
    - infrastructure_bootstrapper
    """

    common_registrars: Sequence[Registrar]
    app_lifetime_registrars: Sequence[Registrar]
    fastapi_lifespan_registrars: Sequence[Registrar]
    infrastructure_bootstrapper: InfrastructureSetup
