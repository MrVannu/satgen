# satgen
Modular, reproducible data generator that simulates how different satellites observe catastrophic events like wildfires.

## Setup

Requirements: [uv](https://docs.astral.sh/uv/getting-started/installation/). uv installs the correct Python version (3.13, see `.python-version`) automatically.

```bash
git clone git@github.com:Glitterrosie/satgen.git
cd satgen
uv sync
```

## Usage

```bash
uv run satgen configs/example.toml                 # writes to outputs/example/
uv run satgen configs/example.toml --out my_run/   # custom output directory
```

Without `--out`, results go to `outputs/<config name>/` in the repo root. Each run directory contains:

- `sN_<stage>.npz`: the output (artifact) of each stage listed in `store_artifacts`; load it with the artifact's `deserialize`, e.g. `FireState.deserialize(path)`
- `config.toml`: a copy of the config used
- `git_commit.txt`: the commit the run was made with (suffixed `-dirty` if there were uncommitted changes)

### Configuring a run

A config file defines one dataset version; see [configs/example.toml](configs/example.toml).

- `[run]` sets the bands (`I4`, `I5`, `M13`), the grid, the time steps and `store_artifacts`: the stages whose output is saved (default: only `sat_viewport_engine`).
- Each stage section picks an implementation with `implementation = "..."`. All other keys are that implementation's parameters.

To create a new version, copy the config and change values or implementations.

## Project structure

```text
configs/                 run configs
src/satgen/
├── __main__.py          entry point (`satgen` command)
├── pipeline.py          Pipeline, config loading
├── io.py                writing outputs
├── types/               shared types (Grid, TimeAxis, Band)
│   └── stage_artifacts/ output type of each stage, with serialize/deserialize
└── stages/sN_<stage>/
    ├── __init__.py      registry of implementations
    ├── base.py          abstract base class
    └── dummy.py         implementations, one module each
```

See [docs/adr/initial-mvp-architecture.md](docs/adr/initial-mvp-architecture.md) for the pipeline architecture.

**Adding an implementation:** create a module in the stage's folder with a class that subclasses the ABC from `base.py`, defines a nested `Params` dataclass and takes `params` in `__init__`. Then register it under a name in `IMPLEMENTATIONS` in the stage's `__init__.py`.

## Development

```bash
uv run ruff check . --fix   # lint (incl. import sorting)
uv run ruff format .        # format
uv run pytest               # run tests
```

Add dependencies with `uv add <package>` (or `uv add --dev <package>` for dev tools) and commit the updated `uv.lock`.

For test guidelines, see [tests/README.md](tests/README.md).
