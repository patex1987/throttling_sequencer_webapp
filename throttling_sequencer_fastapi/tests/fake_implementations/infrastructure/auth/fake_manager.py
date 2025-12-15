from throttling_sequencer.application.authentication.manager import AsyncAuthenticationManager
from throttling_sequencer.domain.authentication.user import AuthenticatedUser


class FakeAuthManager(AsyncAuthenticationManager):
    async def authenticate_jwt_token(self, token: str | None) -> AuthenticatedUser:
        return AuthenticatedUser(
            user_id="1",
            username="main_admin_user",
            email="main@company.xyz",
            roles=["admin"],
            scopes=["read", "write"],
        )
