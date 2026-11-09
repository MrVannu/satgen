from satgen.stages.s5_sat_viewport_engine.base import SatViewportEngine
from satgen.stages.s5_sat_viewport_engine.dummy import DummySatViewportEngine
from satgen.stages.s5_sat_viewport_engine.from_artifact import (
    FromArtifactSatViewportEngine,
)

IMPLEMENTATIONS: dict[str, type[SatViewportEngine]] = {
    "dummy": DummySatViewportEngine,
    "from_artifact": FromArtifactSatViewportEngine,
}

__all__ = ["IMPLEMENTATIONS", "SatViewportEngine"]
