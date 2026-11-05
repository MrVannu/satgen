from dataclasses import dataclass
from typing import Self

import numpy as np
from numpy.typing import NDArray

from satgen.types.grid import Grid, TimeAxis
from satgen.types.stage_artifacts.base import SerializedArtifact, StageArtifact


@dataclass(frozen=True, eq=False)
class FireState(StageArtifact):
    """Output of the CatastropheGenerator."""

    grid: Grid
    time: TimeAxis
    probability: NDArray[np.float32]
    """Fire probability in [0, 1], shape [t, y, x]."""
    intensity: NDArray[np.float32]
    """Fire intensity, shape [t, y, x]. Unit depends on the generator (TBD)."""

    def serialize(self) -> SerializedArtifact:
        return SerializedArtifact(
            meta={"grid": self.grid.to_dict(), "time": self.time.to_dict()},
            arrays={"probability": self.probability, "intensity": self.intensity},
        )

    @classmethod
    def deserialize(cls, data: SerializedArtifact) -> Self:
        return cls(
            grid=Grid.from_dict(data.meta["grid"]),
            time=TimeAxis.from_dict(data.meta["time"]),
            probability=data.arrays["probability"],
            intensity=data.arrays["intensity"],
        )
