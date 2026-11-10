from satgen.stages.s1_catastrophe_generator.base import CatastropheGenerator
from satgen.stages.s1_catastrophe_generator.dummy import DummyCatastropheGenerator
from satgen.stages.s1_catastrophe_generator.from_artifact import (
    FromArtifactCatastropheGenerator,
)
from satgen.stages.s1_catastrophe_generator.propagator import (
    PropagatorCatastropheGenerator,
)

IMPLEMENTATIONS: dict[str, type[CatastropheGenerator]] = {
    "dummy": DummyCatastropheGenerator,
    "from_artifact": FromArtifactCatastropheGenerator,
    "propagator": PropagatorCatastropheGenerator,
}

__all__ = ["IMPLEMENTATIONS", "CatastropheGenerator"]
