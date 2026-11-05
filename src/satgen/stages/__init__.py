"""Pipeline stages. Each subpackage contains:

- `base.py`: the stage's ABC,
- one module per implementation (e.g. `dummy.py`),
- `__init__.py`: the `IMPLEMENTATIONS` registry, re-exporting the ABC.

Convention for implementations:
- import the ABC from `base.py`, not from the package (circular import),
- define a nested `Params` dataclass with every tunable parameter,
- take a single `params: Params` constructor argument,
- register it under a name in the stage's `IMPLEMENTATIONS`.
"""
