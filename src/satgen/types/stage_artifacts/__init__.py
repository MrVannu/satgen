"""Stage outputs. Each artifact converts to and from a `SerializedArtifact`."""

from satgen.types.stage_artifacts.base import SerializedArtifact, StageArtifact
from satgen.types.stage_artifacts.s1_fire_state import FireState
from satgen.types.stage_artifacts.s2_temperature_field import TemperatureField
from satgen.types.stage_artifacts.s3_radiance_field import RadianceField
from satgen.types.stage_artifacts.s4_satellite_positions import SatellitePositions
from satgen.types.stage_artifacts.s5_satellite_views import (
    SatelliteView,
    SatelliteViews,
)

__all__ = [
    "FireState",
    "RadianceField",
    "SatellitePositions",
    "SatelliteView",
    "SatelliteViews",
    "SerializedArtifact",
    "StageArtifact",
    "TemperatureField",
]
