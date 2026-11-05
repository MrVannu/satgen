from dataclasses import dataclass

import numpy as np

from satgen.stages.s3_radiance_processor.base import RadianceProcessor
from satgen.types import Band, RadianceField, TemperatureField

_H = 6.62607015e-34  # Planck constant [J s]
_C = 2.99792458e8  # speed of light [m/s]
_K = 1.380649e-23  # Boltzmann constant [J/K]


class DummyRadianceProcessor(RadianceProcessor):
    """Blackbody radiance at each band's centre wavelength plus Gaussian noise.

    Ignores spectral response functions and emissivity.
    """

    @dataclass(frozen=True)
    class Params:
        noise_level: float = 0.0
        """Relative std. deviation of multiplicative Gaussian noise."""
        seed: int = 0

    def __init__(self, params: Params) -> None:
        self.params = params

    def process(
        self, temperature: TemperatureField, bands: tuple[Band, ...]
    ) -> RadianceField:
        rng = np.random.default_rng(self.params.seed)
        t = temperature.temperature.astype(np.float64)
        radiance = {}
        for band in bands:
            lam = band.center_wavelength_um * 1e-6
            planck = 2 * _H * _C**2 / lam**5 / np.expm1(_H * _C / (lam * _K * t))
            planck *= 1e-6  # per metre -> per micrometre
            noise = rng.normal(1.0, self.params.noise_level, size=t.shape)
            radiance[band.name] = (planck * noise).astype(np.float32)
        return RadianceField(
            grid=temperature.grid,
            time=temperature.time,
            bands=bands,
            radiance=radiance,
        )
