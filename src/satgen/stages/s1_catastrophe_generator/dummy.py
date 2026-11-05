from dataclasses import dataclass

import numpy as np

from satgen.stages.s1_catastrophe_generator.base import CatastropheGenerator
from satgen.types import FireState, Grid, TimeAxis


class DummyCatastropheGenerator(CatastropheGenerator):
    """A circular fire growing from the grid centre at constant speed."""

    @dataclass(frozen=True)
    class Params:
        start_radius_cells: float = 2.0
        growth_cells_per_step: float = 1.0
        intensity: float = 1.0

    def __init__(self, params: Params) -> None:
        self.params = params

    def generate(self, grid: Grid, time: TimeAxis) -> FireState:
        ny, nx = grid.shape
        y, x = np.mgrid[0:ny, 0:nx]
        dist = np.hypot(y - (ny - 1) / 2, x - (nx - 1) / 2)
        radii = (
            self.params.start_radius_cells
            + self.params.growth_cells_per_step * np.arange(time.n_steps)
        )
        probability = (dist[None] <= radii[:, None, None]).astype(np.float32)
        return FireState(
            grid=grid,
            time=time,
            probability=probability,
            intensity=probability * np.float32(self.params.intensity),
        )
