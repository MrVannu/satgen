from satgen.stages.s3_radiance_processor.base import RadianceProcessor
from satgen.stages.s3_radiance_processor.dummy import DummyRadianceProcessor
from satgen.stages.s3_radiance_processor.from_artifact import (
    FromArtifactRadianceProcessor,
)

IMPLEMENTATIONS: dict[str, type[RadianceProcessor]] = {
    "dummy": DummyRadianceProcessor,
    "from_artifact": FromArtifactRadianceProcessor,
}

__all__ = ["IMPLEMENTATIONS", "RadianceProcessor"]
