import svcs

from throttling_sequencer.application.authentication.manager import AsyncAuthenticationManager
from throttling_sequencer.di.registrars.base import Registrar
from throttling_sequencer.infrastructure.authentication.jwt_manager import JwtAuthenticationManager
from throttling_sequencer.infrastructure.authentication.jwt_validator import JWTValidationClient
from throttling_sequencer.infrastructure.service_discovery.static.static_oidc import StaticOpenIdConfigurationProvider


class ProdAuthRegistrar(Registrar):

    def register(self, registry: svcs.Registry) -> None:

        # TODO: make service discovery better and not hardcoded (use files and env vars for the static one at least)
        openid_conf_provider = StaticOpenIdConfigurationProvider(
            realm_name="throttling_test",
            discovery_url="http://localhost:8082/realms/throttling-test/.well-known/openid-configuration",
        )

        token_validation_client = JWTValidationClient()

        auth_manager = JwtAuthenticationManager(
            token_validation_client=token_validation_client,
            openid_configuration_provider=openid_conf_provider,
        )
        registry.register_value(AsyncAuthenticationManager, auth_manager)