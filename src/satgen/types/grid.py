"""Spatial and temporal axes shared by all gridded data."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Self


@dataclass(frozen=True)
class Grid:
    """Regular raster the scene is simulated on."""

    origin: tuple[float, float]
    """(x, y) of the upper-left corner, in CRS units."""
    cell_size: float
    """Edge length of one cell, in CRS units (metres for projected CRS)."""
    shape: tuple[int, int]
    """(ny, nx)"""
    crs: str
    """e.g. "EPSG:32632" """

    def to_dict(self) -> dict[str, Any]:
        return {
            "origin": list(self.origin),
            "cell_size": self.cell_size,
            "shape": list(self.shape),
            "crs": self.crs,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Self:
        return cls(
            origin=tuple(d["origin"]),
            cell_size=d["cell_size"],
            shape=tuple(d["shape"]),
            crs=d["crs"],
        )


@dataclass(frozen=True)
class TimeAxis:
    """Equidistant simulation time steps."""

    start: datetime
    step: timedelta
    n_steps: int

    @property
    def times(self) -> list[datetime]:
        return [self.start + i * self.step for i in range(self.n_steps)]

    def to_dict(self) -> dict[str, Any]:
        return {
            "start": self.start.isoformat(),
            "step_seconds": self.step.total_seconds(),
            "n_steps": self.n_steps,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Self:
        start = d["start"]
        if isinstance(start, str):
            start = datetime.fromisoformat(start)
        return cls(
            start=start,
            step=timedelta(seconds=d["step_seconds"]),
            n_steps=d["n_steps"],
        )
