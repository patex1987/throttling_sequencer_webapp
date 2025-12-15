"""
Authlib-based token validation client for OpenID Connect identity providers.
"""

from authlib.integrations.httpx_client import AsyncOAuth2Client
from authlib.jose import jwt
from authlib.oauth2.rfc8414 import get_well_known_url

from throttling_sequencer.application.authentication.token_validation_client import (
    TokenValidationClient,
)


class JWTValidationClient(TokenValidationClient):
    """
    Token validation client using authlib library.

    Communicates with OpenID Connect identity providers (Keycloak, Microsoft Entra, etc.)
    to validate JWT tokens by fetching JWKS keys and metadata.

    Note: theoretically you can add ttl, size limit to _metadata_cache to avoid explosion.
    """

    def __init__(self):
        # One client = shared connection pool + JWKS cache
        self._client = AsyncOAuth2Client(timeout=5.0)
        self._metadata_cache: dict[str, dict] = {}

    async def authenticate(
        self,
        token: str,
        audience: list[str],
        oidc_discovery_url: str,
    ) -> dict:
        """
        Validate a JWT token using OpenID Connect discovery and JWKS.

        :param token: The JWT token to validate
        :param audience: List of expected audience values
        :param oidc_discovery_url: The OpenID Connect discovery URL (issuer)
        :return: Validated token claims as a dictionary
        """
        metadata = await self._get_oidc_metadata(oidc_discovery_url)

        claims = jwt.decode(
            token,
            key=metadata["jwks_uri"],
            claims_options={
                "iss": {"essential": True, "value": metadata["issuer"]},
                "aud": {"essential": True, "values": audience},
                "exp": {"essential": True},
            },
        )

        claims.validate()
        return claims

    async def _get_oidc_metadata(self, issuer: str) -> dict:
        """Fetch and cache OpenID Connect metadata from the issuer."""
        if issuer not in self._metadata_cache:
            url = get_well_known_url(issuer, external=True)
            resp = await self._client.get(url)
            resp.raise_for_status()
            self._metadata_cache[issuer] = resp.json()
        return self._metadata_cache[issuer]
