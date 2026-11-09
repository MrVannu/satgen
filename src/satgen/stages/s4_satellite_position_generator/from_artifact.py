from dataclasses import dataclass

from satgen.io import load_stage_artifact
from satgen.stages import check_matches
from satgen.stages.s4_satellite_position_generator.base import (
    SatellitePositionGenerator,
)
from satgen.types import SatellitePositions, TimeAxis

STAGE = "satellite_position_generator"


class FromArtifactSatellitePositionGenerator(SatellitePositionGenerator):
    """Loads the SatellitePositions stored by a previous run."""

    @dataclass(frozen=True)
    class Params:
        run_dir: str
        """Output directory of a previous run; relative paths start at the repo root."""

    def __init__(self, params: Params) -> None:
        self.params = params

    def positions(self, time: TimeAxis) -> SatellitePositions:
        positions = load_stage_artifact(self.params.run_dir, STAGE, SatellitePositions)
        check_matches(STAGE, "time axis", positions.time, time)
        return positions
