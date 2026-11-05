from dataclasses import dataclass

import numpy as np

from satgen.stages.s5_sat_viewport_engine.base import SatViewportEngine
from satgen.types import (
    RadianceField,
    SatellitePositions,
    SatelliteView,
    SatelliteViews,
)


class DummySatViewportEngine(SatViewportEngine):
    """Every satellite sees the whole scene at every time step."""

    @dataclass(frozen=True)
    class Params:
        pass

    def __init__(self, params: Params) -> None:
        self.params = params

    def observe(
        self, radiance: RadianceField, satellites: SatellitePositions
    ) -> SatelliteViews:
        visible = np.ones(radiance.time.n_steps, dtype=np.bool_)
        return SatelliteViews(
            grid=radiance.grid,
            time=radiance.time,
            views=tuple(
                SatelliteView(
                    satellite_id=sat_id,
                    radiance=dict(radiance.radiance),
                    visible=visible.copy(),
                )
                for sat_id in satellites.satellite_ids
            ),
        )
