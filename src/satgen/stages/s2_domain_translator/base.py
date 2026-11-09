from abc import ABC, abstractmethod

from satgen.types import FireState, TemperatureField


class DomainTranslator(ABC):
    """Translates generator output (probability/intensity) into temperature."""

    @abstractmethod
    def translate(self, fire: FireState) -> TemperatureField: ...
