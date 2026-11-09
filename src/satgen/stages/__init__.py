"""Pipeline stages. Each subpackage contains:

- `base.py`: the stage's ABC,
- one module per implementation (e.g. `dummy.py`, `from_artifact.py`),
- `__init__.py`: the `IMPLEMENTATIONS` registry, re-exporting the ABC.

Convention for implementations:
- import the ABC from `base.py`, not from the package (circular import),
- define a nested `Params` dataclass with every tunable parameter,
- take a single `params: Params` constructor argument,
- register it under a name in the stage's `IMPLEMENTATIONS`.
"""

STAGE_NAMES: tuple[str, ...] = (
    "catastrophe_generator",
    "domain_translator",
    "radiance_processor",
    "satellite_position_generator",
    "sat_viewport_engine",
)
"""Stages with an artifact, in pipeline order. Names match the config sections."""


def check_matches(stage: str, what: str, loaded: object, expected: object) -> None:
    """Fail if a loaded artifact does not fit the current run."""
    if loaded != expected:
        raise ValueError(
            f"[{stage}] loaded artifact has a different {what} than this run:\n"
            f"  artifact: {loaded}\n  run:      {expected}"
        )
