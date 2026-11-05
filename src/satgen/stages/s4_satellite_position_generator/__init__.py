from satgen.stages.s4_satellite_position_generator.base import (
    SatellitePositionGenerator,
)
from satgen.stages.s4_satellite_position_generator.dummy import (
    DummySatellitePositionGenerator,
)

IMPLEMENTATIONS: dict[str, type[SatellitePositionGenerator]] = {
    "dummy": DummySatellitePositionGenerator,
}

__all__ = ["IMPLEMENTATIONS", "SatellitePositionGenerator"]
