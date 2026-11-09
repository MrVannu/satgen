from dataclasses import dataclass

from satgen.io import load_stage_artifact
from satgen.stages import check_matches
from satgen.stages.s3_radiance_processor.base import RadianceProcessor
from satgen.types import Band, RadianceField, TemperatureField

STAGE = "radiance_processor"


class FromArtifactRadianceProcessor(RadianceProcessor):
    """Loads the RadianceField stored by a previous run."""

    @dataclass(frozen=True)
    class Params:
        run_dir: str
        """Output directory of a previous run; relative paths start at the repo root."""

    def __init__(self, params: Params) -> None:
        self.params = params

    def process(
        self, temperature: TemperatureField, bands: tuple[Band, ...]
    ) -> RadianceField:
        radiance = load_stage_artifact(self.params.run_dir, STAGE, RadianceField)
        check_matches(STAGE, "grid", radiance.grid, temperature.grid)
        check_matches(STAGE, "time axis", radiance.time, temperature.time)
        check_matches(STAGE, "bands", radiance.bands, bands)
        return radiance
