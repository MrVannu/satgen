from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import rasterio
from numpy.typing import NDArray
from propagator.cli.main import fuels_from_yaml
from propagator.core import FUEL_SYSTEM_LEGACY, Propagator, PropagatorOutOfBoundsError
from propagator.io.configuration import PropagatorConfigurationLegacy
from propagator.io.geo import GeographicInfo
from rasterio.crs import CRS
from rasterio.enums import Resampling
from rasterio.transform import from_origin
from rasterio.warp import reproject, transform_bounds

from satgen.io import resolve
from satgen.stages.s1_catastrophe_generator.base import CatastropheGenerator
from satgen.types import FireState, Grid, TimeAxis

STAGE = "catastrophe_generator"


class PropagatorCatastropheGenerator(CatastropheGenerator):
    """Runs the PROPAGATOR wildfire simulator on the run grid.

    The DEM and fuel map are resampled onto the grid. `intensity` is
    PROPAGATOR's mean fireline intensity over the realizations that burned
    the cell.
    """

    @dataclass(frozen=True)
    class Params:
        dem: str
        """Elevation GeoTIFF; relative paths start at the repo root."""
        fuel: str
        """Fuel type GeoTIFF; relative paths start at the repo root."""
        ignitions: list[str]
        """PROPAGATOR geometries in lat/lon, e.g. "POINT: [52.51751;-6.82354]"."""
        boundary_conditions: list[dict[str, Any]]
        """Weather and actions over time, with the keys of PROPAGATOR's JSON config.

        Must contain an entry with `time = 0`.
        """
        fuel_config: str | None = None
        """Fuel system YAML; PROPAGATOR's built-in fuels when not set."""
        realizations: int = 30
        do_spotting: bool = False
        ros_model: str = "wang"
        moisture_model: str = "trucchia"
        ignore_out_of_bounds: bool = False
        """Keep simulating when the fire reaches the grid edge instead of failing."""

    def __init__(self, params: Params) -> None:
        self.params = params

    def generate(self, grid: Grid, time: TimeAxis) -> FireState:
        p = self.params
        geo_info = _geo_info(grid)
        dem = _resample(resolve(p.dem), geo_info, Resampling.bilinear)
        fuel = _resample(resolve(p.fuel), geo_info, Resampling.nearest)
        fuels = (
            fuels_from_yaml(resolve(p.fuel_config))
            if p.fuel_config
            else FUEL_SYSTEM_LEGACY
        )
        cfg = PropagatorConfigurationLegacy(
            init_date=time.start,
            ignitions=list(p.ignitions),
            boundary_conditions=[dict(bc) for bc in p.boundary_conditions],
            ros_model=p.ros_model,
            prob_moist_model=p.moisture_model,
        )

        simulator = Propagator(
            dem=dem.astype(np.int16),
            veg=fuel.astype(np.int8),
            fuels=fuels,
            cellsize=grid.cell_size,
            do_spotting=p.do_spotting,
            realizations=p.realizations,
            out_of_bounds_mode="ignore" if p.ignore_out_of_bounds else "raise",
            p_time_fn=cfg.p_time_fn,
            p_moist_fn=cfg.p_moist_fn,
        )
        for bc in cfg.get_boundary_conditions(geo_info, fuels.get_non_vegetated()):
            simulator.set_boundary_conditions(bc)

        step_seconds = int(time.step.total_seconds())
        probability = np.empty((time.n_steps, *grid.shape), dtype=np.float32)
        intensity = np.empty_like(probability)
        for i in range(time.n_steps):
            try:
                simulator.step(seconds=0 if i == 0 else step_seconds)
            except PropagatorOutOfBoundsError:
                raise ValueError(
                    f"[{STAGE}] the fire reached the grid edge at {time.times[i]}; "
                    "enlarge [run.grid] or set ignore_out_of_bounds = true"
                ) from None
            probability[i] = simulator.compute_fire_probability()
            intensity[i] = np.nan_to_num(simulator.compute_fireline_int_mean())

        return FireState(
            grid=grid, time=time, probability=probability, intensity=intensity
        )


def _geo_info(grid: Grid) -> GeographicInfo:
    ny, nx = grid.shape
    x0, y0 = grid.origin
    size = grid.cell_size
    return GeographicInfo(
        crs=CRS.from_user_input(grid.crs),
        trans=from_origin(x0, y0, size, size),
        bounds=(x0, y0 - ny * size, x0 + nx * size, y0),
        shape=(ny, nx),
    )


def _resample(
    path: Path, geo_info: GeographicInfo, resampling: Resampling
) -> NDArray[np.float32]:
    with rasterio.open(path) as src:
        west, south, east, north = transform_bounds(
            geo_info.crs, src.crs, *geo_info.bounds
        )
        b = src.bounds
        if west < b.left or east > b.right or south < b.bottom or north > b.top:
            raise ValueError(f"[{STAGE}] the run grid is not fully covered by {path}")
        out = np.full(geo_info.shape, np.nan, dtype=np.float32)
        reproject(
            source=rasterio.band(src, 1),
            destination=out,
            dst_transform=geo_info.trans,
            dst_crs=geo_info.crs,
            dst_nodata=np.nan,
            resampling=resampling,
        )
    if np.isnan(out).any():
        raise ValueError(f"[{STAGE}] {path} has no data inside the run grid")
    return out
