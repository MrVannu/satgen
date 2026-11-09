from satgen.stages.s4_satellite_position_generator.base import (
    SatellitePositionGenerator,
)
from satgen.stages.s4_satellite_position_generator.dummy import (
    DummySatellitePositionGenerator,
)
from satgen.stages.s4_satellite_position_generator.from_artifact import (
    FromArtifactSatellitePositionGenerator,
)

IMPLEMENTATIONS: dict[str, type[SatellitePositionGenerator]] = {
    "dummy": DummySatellitePositionGenerator,
    "from_artifact": FromArtifactSatellitePositionGenerator,
}

__all__ = ["IMPLEMENTATIONS", "SatellitePositionGenerator"]
