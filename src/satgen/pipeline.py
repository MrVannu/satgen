"""Wires the stages together and builds a pipeline from a config.

`Pipeline` only depends on the stage ABCs. Each stage's `IMPLEMENTATIONS`
(in its `__init__.py`) maps the `implementation = "..."` names used in config
files to concrete classes.
"""

from dataclasses import dataclass, fields
from typing import Any

from satgen.stages.s1_catastrophe_generator import (
    IMPLEMENTATIONS as CATASTROPHE_GENERATORS,
)
from satgen.stages.s1_catastrophe_generator import CatastropheGenerator
from satgen.stages.s2_domain_translator import IMPLEMENTATIONS as DOMAIN_TRANSLATORS
from satgen.stages.s2_domain_translator import DomainTranslator
from satgen.stages.s3_radiance_processor import IMPLEMENTATIONS as RADIANCE_PROCESSORS
from satgen.stages.s3_radiance_processor import RadianceProcessor
from satgen.stages.s4_satellite_position_generator import (
    IMPLEMENTATIONS as SATELLITE_POSITION_GENERATORS,
)
from satgen.stages.s4_satellite_position_generator import SatellitePositionGenerator
from satgen.stages.s5_sat_viewport_engine import IMPLEMENTATIONS as SAT_VIEWPORT_ENGINES
from satgen.stages.s5_sat_viewport_engine import SatViewportEngine
from satgen.types import (
    VIIRS_BANDS,
    Band,
    FireState,
    Grid,
    RadianceField,
    SatellitePositions,
    SatelliteViews,
    StageArtifact,
    TemperatureField,
    TimeAxis,
)


@dataclass(frozen=True)
class PipelineResult:
    """The artifacts of all stages of one run, in pipeline order.

    Field names match the stage sections in config files.
    """

    catastrophe_generator: FireState
    domain_translator: TemperatureField
    radiance_processor: RadianceField
    satellite_position_generator: SatellitePositions
    sat_viewport_engine: SatelliteViews

    def artifacts(self) -> dict[str, StageArtifact]:
        return {f.name: getattr(self, f.name) for f in fields(self)}


STAGE_NAMES: tuple[str, ...] = tuple(f.name for f in fields(PipelineResult))


@dataclass
class Pipeline:
    catastrophe_generator: CatastropheGenerator
    domain_translator: DomainTranslator
    radiance_processor: RadianceProcessor
    satellite_position_generator: SatellitePositionGenerator
    sat_viewport_engine: SatViewportEngine

    def run(
        self, grid: Grid, time: TimeAxis, bands: tuple[Band, ...]
    ) -> PipelineResult:
        fire = self.catastrophe_generator.generate(grid, time)
        temperature = self.domain_translator.translate(fire)
        radiance = self.radiance_processor.process(temperature, bands)
        satellites = self.satellite_position_generator.positions(time)
        views = self.sat_viewport_engine.observe(radiance, satellites)
        return PipelineResult(
            catastrophe_generator=fire,
            domain_translator=temperature,
            radiance_processor=radiance,
            satellite_position_generator=satellites,
            sat_viewport_engine=views,
        )


@dataclass(frozen=True)
class RunSettings:
    """Inputs of a single run that are not tied to one stage."""

    grid: Grid
    time: TimeAxis
    bands: tuple[Band, ...]
    store_artifacts: tuple[str, ...]
    """Stage names whose artifacts are written to the output directory."""


def from_config(cfg: dict[str, Any]) -> tuple[Pipeline, RunSettings]:
    """Build a pipeline and its run settings from a parsed TOML config."""
    pipeline = Pipeline(
        catastrophe_generator=_build(
            CATASTROPHE_GENERATORS, cfg, "catastrophe_generator"
        ),
        domain_translator=_build(DOMAIN_TRANSLATORS, cfg, "domain_translator"),
        radiance_processor=_build(RADIANCE_PROCESSORS, cfg, "radiance_processor"),
        satellite_position_generator=_build(
            SATELLITE_POSITION_GENERATORS, cfg, "satellite_position_generator"
        ),
        sat_viewport_engine=_build(SAT_VIEWPORT_ENGINES, cfg, "sat_viewport_engine"),
    )
    return pipeline, _run_settings(cfg["run"])


def _build[T](registry: dict[str, type[T]], cfg: dict[str, Any], stage: str) -> T:
    section = dict(cfg[stage])
    implementation = section.pop("implementation")
    try:
        cls: Any = registry[implementation]
    except KeyError:
        raise ValueError(
            f"[{stage}] unknown implementation {implementation!r}, "
            f"available: {sorted(registry)}"
        ) from None
    try:
        params = cls.Params(**section)
    except TypeError as e:
        raise ValueError(
            f"[{stage}] invalid parameters for {implementation!r}: {e}"
        ) from None
    return cls(params)


def _run_settings(run: dict[str, Any]) -> RunSettings:
    _check_known("bands", run["bands"], VIIRS_BANDS)
    store_artifacts = run.get("store_artifacts", ["sat_viewport_engine"])
    _check_known("store_artifacts", store_artifacts, STAGE_NAMES)
    return RunSettings(
        grid=Grid.from_dict(run["grid"]),
        time=TimeAxis.from_dict(run["time"]),
        bands=tuple(VIIRS_BANDS[name] for name in run["bands"]),
        store_artifacts=tuple(store_artifacts),
    )


def _check_known(key: str, values: list[str], known: Any) -> None:
    unknown = set(values) - set(known)
    if unknown:
        raise ValueError(
            f"[run] unknown {key} {sorted(unknown)}, available: {list(known)}"
        )
