from abc import ABC, abstractmethod

from satgen.types import FireState, Grid, TimeAxis


class CatastropheGenerator(ABC):
    """Simulates the event (e.g. a wildfire) on the grid over time."""

    @abstractmethod
    def generate(self, grid: Grid, time: TimeAxis) -> FireState: ...
