"""Data types shared between pipeline stages.

- `grid.py`, `band.py`: shared inputs used by several stages,
- `stage_artifacts/`: the output of each stage, serializable to disk.

Rule of thumb: a type lives here if it appears in a stage's ABC signature.
Parameters and helper types used by a single implementation stay in that stage.
"""

from satgen.types.band import VIIRS_BANDS, Band
from satgen.types.grid import Grid, TimeAxis
from satgen.types.stage_artifacts import (
    FireState,
    RadianceField,
    SatellitePositions,
    SatelliteView,
    SatelliteViews,
    StageArtifact,
    TemperatureField,
)

__all__ = [
    "VIIRS_BANDS",
    "Band",
    "FireState",
    "Grid",
    "RadianceField",
    "SatellitePositions",
    "SatelliteView",
    "SatelliteViews",
    "StageArtifact",
    "TemperatureField",
    "TimeAxis",
]
