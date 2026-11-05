from dataclasses import dataclass
from pathlib import Path
from typing import Self

import numpy as np
from numpy.typing import NDArray

from satgen.types.grid import TimeAxis
from satgen.types.stage_artifacts.base import StageArtifact, read_npz, write_npz


@dataclass(frozen=True, eq=False)
class SatellitePositions(StageArtifact):
    """Output of the SatellitePositionGenerator."""

    satellite_ids: tuple[str, ...]
    time: TimeAxis
    positions: NDArray[np.float64]
    """Shape [n_satellites, t, 3], in `frame` coordinates."""
    frame: str
    """Coordinate frame of `positions` (TBD by team, e.g. "ECEF")."""

    def serialize(self, path: Path) -> None:
        write_npz(
            path,
            meta={
                "satellite_ids": list(self.satellite_ids),
                "time": self.time.to_dict(),
                "frame": self.frame,
            },
            arrays={"positions": self.positions},
        )

    @classmethod
    def deserialize(cls, path: Path) -> Self:
        meta, arrays = read_npz(path)
        return cls(
            satellite_ids=tuple(meta["satellite_ids"]),
            time=TimeAxis.from_dict(meta["time"]),
            positions=arrays["positions"],
            frame=meta["frame"],
        )
