from dataclasses import dataclass
from typing import Self

import numpy as np
from numpy.typing import NDArray

from satgen.types.grid import Grid, TimeAxis
from satgen.types.stage_artifacts.base import SerializedArtifact, StageArtifact


@dataclass(frozen=True, eq=False)
class SatelliteView:
    """What one satellite sees of the scene over time."""

    satellite_id: str
    radiance: dict[str, NDArray[np.float32]]
    """Band name -> observed radiance, shape [t, y, x]; zeros where not visible."""
    visible: NDArray[np.bool_]
    """Shape [t]: whether the scene is in view at each time step."""


@dataclass(frozen=True, eq=False)
class SatelliteViews(StageArtifact):
    """Output of the SatViewportEngine: the views of all satellites."""

    grid: Grid
    time: TimeAxis
    views: tuple[SatelliteView, ...]

    def serialize(self) -> SerializedArtifact:
        # Arrays are keyed by view index, satellite ids live in the metadata.
        arrays: dict[str, NDArray[np.generic]] = {}
        for i, view in enumerate(self.views):
            arrays[f"{i}_visible"] = view.visible
            for band, arr in view.radiance.items():
                arrays[f"{i}_radiance_{band}"] = arr
        return SerializedArtifact(
            meta={
                "grid": self.grid.to_dict(),
                "time": self.time.to_dict(),
                "views": [
                    {"satellite_id": v.satellite_id, "bands": list(v.radiance)}
                    for v in self.views
                ],
            },
            arrays=arrays,
        )

    @classmethod
    def deserialize(cls, data: SerializedArtifact) -> Self:
        views = tuple(
            SatelliteView(
                satellite_id=v["satellite_id"],
                radiance={b: data.arrays[f"{i}_radiance_{b}"] for b in v["bands"]},
                visible=data.arrays[f"{i}_visible"],
            )
            for i, v in enumerate(data.meta["views"])
        )
        return cls(
            grid=Grid.from_dict(data.meta["grid"]),
            time=TimeAxis.from_dict(data.meta["time"]),
            views=views,
        )
