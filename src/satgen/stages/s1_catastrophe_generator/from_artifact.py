from dataclasses import dataclass

from satgen.io import load_stage_artifact
from satgen.stages import check_matches
from satgen.stages.s1_catastrophe_generator.base import CatastropheGenerator
from satgen.types import FireState, Grid, TimeAxis

STAGE = "catastrophe_generator"


class FromArtifactCatastropheGenerator(CatastropheGenerator):
    """Loads the FireState stored by a previous run."""

    @dataclass(frozen=True)
    class Params:
        run_dir: str
        """Output directory of a previous run; relative paths start at the repo root."""

    def __init__(self, params: Params) -> None:
        self.params = params

    def generate(self, grid: Grid, time: TimeAxis) -> FireState:
        fire = load_stage_artifact(self.params.run_dir, STAGE, FireState)
        check_matches(STAGE, "grid", fire.grid, grid)
        check_matches(STAGE, "time axis", fire.time, time)
        return fire
