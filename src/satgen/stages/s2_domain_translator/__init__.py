from satgen.stages.s2_domain_translator.base import DomainTranslator
from satgen.stages.s2_domain_translator.dummy import DummyDomainTranslator
from satgen.stages.s2_domain_translator.from_artifact import (
    FromArtifactDomainTranslator,
)

IMPLEMENTATIONS: dict[str, type[DomainTranslator]] = {
    "dummy": DummyDomainTranslator,
    "from_artifact": FromArtifactDomainTranslator,
}

__all__ = ["IMPLEMENTATIONS", "DomainTranslator"]
