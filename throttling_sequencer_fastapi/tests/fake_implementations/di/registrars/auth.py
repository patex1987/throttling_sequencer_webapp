import svcs

from tests.fake_implementations.infrastructure.auth.fake_manager import FakeAuthManager
from throttling_sequencer.application.authentication.manager import AsyncAuthenticationManager
from throttling_sequencer.application.execution_context import ExecutionContextEnricher
from throttling_sequencer.di.registrars.base import Registrar
from throttling_sequencer.infrastructure.execution_context.fake import FakeExecutionContextEnricher


class DevelopmentAuthRegistrar(Registrar):
    def register(self, registry: svcs.Registry) -> None:
        registry.register_factory(ExecutionContextEnricher, FakeExecutionContextEnricher)
        registry.register_value(AsyncAuthenticationManager, FakeAuthManager())
