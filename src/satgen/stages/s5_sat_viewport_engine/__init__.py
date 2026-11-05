from satgen.stages.s5_sat_viewport_engine.base import SatViewportEngine
from satgen.stages.s5_sat_viewport_engine.dummy import DummySatViewportEngine

IMPLEMENTATIONS: dict[str, type[SatViewportEngine]] = {
    "dummy": DummySatViewportEngine,
}

__all__ = ["IMPLEMENTATIONS", "SatViewportEngine"]
