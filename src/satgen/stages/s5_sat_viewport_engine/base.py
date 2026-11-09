from abc import ABC, abstractmethod

from satgen.types import RadianceField, SatellitePositions, SatelliteViews


class SatViewportEngine(ABC):
    """Determines what each satellite sees of the radiance field over time."""

    @abstractmethod
    def observe(
        self, radiance: RadianceField, satellites: SatellitePositions
    ) -> SatelliteViews: ...
