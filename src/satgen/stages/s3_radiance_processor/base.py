from abc import ABC, abstractmethod

from satgen.types import Band, RadianceField, TemperatureField


class RadianceProcessor(ABC):
    """Turns temperatures into per-band radiance, including sensor noise."""

    @abstractmethod
    def process(
        self, temperature: TemperatureField, bands: tuple[Band, ...]
    ) -> RadianceField: ...
