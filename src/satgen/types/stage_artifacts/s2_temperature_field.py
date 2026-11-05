from dataclasses import dataclass
from pathlib import Path
from typing import Self

import numpy as np
from numpy.typing import NDArray

from satgen.types.grid import Grid, TimeAxis
from satgen.types.stage_artifacts.base import StageArtifact, read_npz, write_npz


@dataclass(frozen=True, eq=False)
class TemperatureField(StageArtifact):
    """Output of the DomainTranslator."""

    grid: Grid
    time: TimeAxis
    temperature: NDArray[np.float32]
    """Surface temperature in Kelvin, shape [t, y, x]."""

    def serialize(self, path: Path) -> None:
        write_npz(
            path,
            meta={"grid": self.grid.to_dict(), "time": self.time.to_dict()},
            arrays={"temperature": self.temperature},
        )

    @classmethod
    def deserialize(cls, path: Path) -> Self:
        meta, arrays = read_npz(path)
        return cls(
            grid=Grid.from_dict(meta["grid"]),
            time=TimeAxis.from_dict(meta["time"]),
            temperature=arrays["temperature"],
        )
