from dataclasses import dataclass
from pathlib import Path
from typing import Self

import numpy as np
from numpy.typing import NDArray

from satgen.types.grid import Grid, TimeAxis
from satgen.types.stage_artifacts.base import StageArtifact, read_npz, write_npz


@dataclass(frozen=True, eq=False)
class FireState(StageArtifact):
    """Output of the CatastropheGenerator."""

    grid: Grid
    time: TimeAxis
    probability: NDArray[np.float32]
    """Fire probability in [0, 1], shape [t, y, x]."""
    intensity: NDArray[np.float32]
    """Fire intensity, shape [t, y, x]. Unit depends on the generator (TBD)."""

    def serialize(self, path: Path) -> None:
        write_npz(
            path,
            meta={"grid": self.grid.to_dict(), "time": self.time.to_dict()},
            arrays={"probability": self.probability, "intensity": self.intensity},
        )

    @classmethod
    def deserialize(cls, path: Path) -> Self:
        meta, arrays = read_npz(path)
        return cls(
            grid=Grid.from_dict(meta["grid"]),
            time=TimeAxis.from_dict(meta["time"]),
            probability=arrays["probability"],
            intensity=arrays["intensity"],
        )
