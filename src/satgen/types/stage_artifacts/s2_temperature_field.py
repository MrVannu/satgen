from dataclasses import dataclass
from typing import Self

import numpy as np
from numpy.typing import NDArray

from satgen.types.grid import Grid, TimeAxis
from satgen.types.stage_artifacts.base import SerializedArtifact, StageArtifact


@dataclass(frozen=True, eq=False)
class TemperatureField(StageArtifact):
    """Output of the DomainTranslator."""

    grid: Grid
    time: TimeAxis
    temperature: NDArray[np.float32]
    """Surface temperature in Kelvin, shape [t, y, x]."""

    def serialize(self) -> SerializedArtifact:
        return SerializedArtifact(
            meta={"grid": self.grid.to_dict(), "time": self.time.to_dict()},
            arrays={"temperature": self.temperature},
        )

    @classmethod
    def deserialize(cls, data: SerializedArtifact) -> Self:
        return cls(
            grid=Grid.from_dict(data.meta["grid"]),
            time=TimeAxis.from_dict(data.meta["time"]),
            temperature=data.arrays["temperature"],
        )
