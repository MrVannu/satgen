from dataclasses import dataclass

from satgen.io import load_stage_artifact
from satgen.stages import check_matches
from satgen.stages.s2_domain_translator.base import DomainTranslator
from satgen.types import FireState, TemperatureField

STAGE = "domain_translator"


class FromArtifactDomainTranslator(DomainTranslator):
    """Loads the TemperatureField stored by a previous run."""

    @dataclass(frozen=True)
    class Params:
        run_dir: str
        """Output directory of a previous run; relative paths start at the repo root."""

    def __init__(self, params: Params) -> None:
        self.params = params

    def translate(self, fire: FireState) -> TemperatureField:
        temperature = load_stage_artifact(self.params.run_dir, STAGE, TemperatureField)
        check_matches(STAGE, "grid", temperature.grid, fire.grid)
        check_matches(STAGE, "time axis", temperature.time, fire.time)
        return temperature
