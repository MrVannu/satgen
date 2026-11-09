# satgen
Modular, reproducible data generator that simulates how different satellites observe catastrophic events like wildfires.

## Setup

Requirements: [uv](https://docs.astral.sh/uv/getting-started/installation/). uv installs the correct Python version (3.13, see `.python-version`) automatically.

```bash
git clone git@github.com:Glitterrosie/satgen.git
cd satgen
uv sync
```

## Development

```bash
uv run ruff check . --fix   # lint (incl. import sorting)
uv run ruff format .        # format
uv run pytest               # run tests
```

Add dependencies with `uv add <package>` (or `uv add --dev <package>` for dev tools) and commit the updated `uv.lock`.

For test guidelines, see [tests/README.md](tests/README.md).
