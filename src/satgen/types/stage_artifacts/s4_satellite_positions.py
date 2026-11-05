from dataclasses import dataclass
from typing import Self

import numpy as np
from numpy.typing import NDArray

from satgen.types.grid import TimeAxis
from satgen.types.stage_artifacts.base import SerializedArtifact, StageArtifact


@dataclass(frozen=True, eq=False)
class SatellitePositions(StageArtifact):
    """Output of the SatellitePositionGenerator."""

    satellite_ids: tuple[str, ...]
    time: TimeAxis
    positions: NDArray[np.float64]
    """Shape [n_satellites, t, 3], in `frame` coordinates."""
    frame: str
    """Coordinate frame of `positions` (TBD by team, e.g. "ECEF")."""

    def serialize(self) -> SerializedArtifact:
        return SerializedArtifact(
            meta={
                "satellite_ids": list(self.satellite_ids),
                "time": self.time.to_dict(),
                "frame": self.frame,
            },
            arrays={"positions": self.positions},
        )

    @classmethod
    def deserialize(cls, data: SerializedArtifact) -> Self:
        return cls(
            satellite_ids=tuple(data.meta["satellite_ids"]),
            time=TimeAxis.from_dict(data.meta["time"]),
            positions=data.arrays["positions"],
            frame=data.meta["frame"],
        )
