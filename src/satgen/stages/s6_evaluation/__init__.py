from satgen.stages.s6_evaluation.base import Evaluator

IMPLEMENTATIONS: dict[str, type[Evaluator]] = {}

__all__ = ["IMPLEMENTATIONS", "Evaluator"]
