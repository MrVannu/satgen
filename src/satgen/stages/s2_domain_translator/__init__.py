from satgen.stages.s2_domain_translator.base import DomainTranslator
from satgen.stages.s2_domain_translator.dummy import DummyDomainTranslator

IMPLEMENTATIONS: dict[str, type[DomainTranslator]] = {
    "dummy": DummyDomainTranslator,
}

__all__ = ["IMPLEMENTATIONS", "DomainTranslator"]
