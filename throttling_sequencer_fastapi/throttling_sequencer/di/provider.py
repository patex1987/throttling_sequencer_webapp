from typing import Protocol

from throttling_sequencer.di.app_wide_registrar import FastapiDIRegistrars


class RegistrarProvider(Protocol):
    def __call__(self) -> FastapiDIRegistrars: ...
