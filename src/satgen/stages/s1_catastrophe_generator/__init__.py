from satgen.stages.s1_catastrophe_generator.base import CatastropheGenerator
from satgen.stages.s1_catastrophe_generator.dummy import DummyCatastropheGenerator
from satgen.stages.s1_catastrophe_generator.from_artifact import (
    FromArtifactCatastropheGenerator,
)

IMPLEMENTATIONS: dict[str, type[CatastropheGenerator]] = {
    "dummy": DummyCatastropheGenerator,
    "from_artifact": FromArtifactCatastropheGenerator,
}

__all__ = ["IMPLEMENTATIONS", "CatastropheGenerator"]
