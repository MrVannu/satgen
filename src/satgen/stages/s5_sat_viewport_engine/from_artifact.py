from dataclasses import dataclass

from satgen.io import load_stage_artifact
from satgen.stages import check_matches
from satgen.stages.s5_sat_viewport_engine.base import SatViewportEngine
from satgen.types import RadianceField, SatellitePositions, SatelliteViews

STAGE = "sat_viewport_engine"


class FromArtifactSatViewportEngine(SatViewportEngine):
    """Loads the SatelliteViews stored by a previous run."""

    @dataclass(frozen=True)
    class Params:
        run_dir: str
        """Output directory of a previous run; relative paths start at the repo root."""

    def __init__(self, params: Params) -> None:
        self.params = params

    def observe(
        self, radiance: RadianceField, satellites: SatellitePositions
    ) -> SatelliteViews:
        views = load_stage_artifact(self.params.run_dir, STAGE, SatelliteViews)
        check_matches(STAGE, "grid", views.grid, radiance.grid)
        check_matches(STAGE, "time axis", views.time, radiance.time)
        check_matches(
            STAGE,
            "satellites",
            tuple(v.satellite_id for v in views.views),
            satellites.satellite_ids,
        )
        return views
