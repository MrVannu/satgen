from abc import ABC, abstractmethod

from satgen.types import SatelliteViews


class Evaluator(ABC):
    """Computes metrics on generated satellite views.

    Not wired into the Pipeline yet: whether evaluation runs inside the
    pipeline or on saved outputs is still open.
    """

    @abstractmethod
    def evaluate(self, views: SatelliteViews) -> dict[str, float]: ...
