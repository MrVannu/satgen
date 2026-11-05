from satgen.stages.s3_radiance_processor.base import RadianceProcessor
from satgen.stages.s3_radiance_processor.dummy import DummyRadianceProcessor

IMPLEMENTATIONS: dict[str, type[RadianceProcessor]] = {
    "dummy": DummyRadianceProcessor,
}

__all__ = ["IMPLEMENTATIONS", "RadianceProcessor"]
