from dataclasses import dataclass
from pathlib import Path
from typing import Self

import numpy as np
from numpy.typing import NDArray

from satgen.types.band import Band
from satgen.types.grid import Grid, TimeAxis
from satgen.types.stage_artifacts.base import StageArtifact, read_npz, write_npz


@dataclass(frozen=True, eq=False)
class RadianceField(StageArtifact):
    """Output of the RadianceProcessor."""

    grid: Grid
    time: TimeAxis
    bands: tuple[Band, ...]
    radiance: dict[str, NDArray[np.float32]]
    """Band name -> spectral radiance [W m^-2 sr^-1 um^-1], shape [t, y, x]."""

    def serialize(self, path: Path) -> None:
        write_npz(
            path,
            meta={
                "grid": self.grid.to_dict(),
                "time": self.time.to_dict(),
                "bands": [band.to_dict() for band in self.bands],
            },
            arrays={f"radiance_{name}": arr for name, arr in self.radiance.items()},
        )

    @classmethod
    def deserialize(cls, path: Path) -> Self:
        meta, arrays = read_npz(path)
        bands = tuple(Band.from_dict(b) for b in meta["bands"])
        return cls(
            grid=Grid.from_dict(meta["grid"]),
            time=TimeAxis.from_dict(meta["time"]),
            bands=bands,
            radiance={b.name: arrays[f"radiance_{b.name}"] for b in bands},
        )
