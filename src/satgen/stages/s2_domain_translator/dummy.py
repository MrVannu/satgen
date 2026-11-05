from dataclasses import dataclass

import numpy as np

from satgen.stages.s2_domain_translator.base import DomainTranslator
from satgen.types import FireState, TemperatureField


class DummyDomainTranslator(DomainTranslator):
    """Cells above a probability threshold get a fixed fire temperature."""

    @dataclass(frozen=True)
    class Params:
        threshold: float = 0.5
        background_k: float = 300.0
        fire_k: float = 800.0

    def __init__(self, params: Params) -> None:
        self.params = params

    def translate(self, fire: FireState) -> TemperatureField:
        temperature = np.where(
            fire.probability >= self.params.threshold,
            self.params.fire_k,
            self.params.background_k,
        ).astype(np.float32)
        return TemperatureField(grid=fire.grid, time=fire.time, temperature=temperature)
