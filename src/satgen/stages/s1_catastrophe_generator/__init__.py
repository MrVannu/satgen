from satgen.stages.s1_catastrophe_generator.base import CatastropheGenerator
from satgen.stages.s1_catastrophe_generator.dummy import DummyCatastropheGenerator

IMPLEMENTATIONS: dict[str, type[CatastropheGenerator]] = {
    "dummy": DummyCatastropheGenerator,
}

__all__ = ["IMPLEMENTATIONS", "CatastropheGenerator"]
