from abc import ABC, abstractmethod

from satgen.types import SatellitePositions, TimeAxis


class SatellitePositionGenerator(ABC):
    """Computes where each satellite is at each time step."""

    @abstractmethod
    def positions(self, time: TimeAxis) -> SatellitePositions: ...
