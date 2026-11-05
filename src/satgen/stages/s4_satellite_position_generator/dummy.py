from dataclasses import dataclass

import numpy as np

from satgen.stages.s4_satellite_position_generator.base import (
    SatellitePositionGenerator,
)
from satgen.types import SatellitePositions, TimeAxis


class DummySatellitePositionGenerator(SatellitePositionGenerator):
    """One satellite hovering at a fixed point above the scene."""

    @dataclass(frozen=True)
    class Params:
        satellite_id: str = "dummy-sat"
        altitude_m: float = 830_000.0

    def __init__(self, params: Params) -> None:
        self.params = params

    def positions(self, time: TimeAxis) -> SatellitePositions:
        positions = np.zeros((1, time.n_steps, 3))
        positions[..., 2] = self.params.altitude_m
        return SatellitePositions(
            satellite_ids=(self.params.satellite_id,),
            time=time,
            positions=positions,
            frame="scene-local",
        )
