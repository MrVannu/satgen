"""Entry point: `uv run satgen <config.toml>` or `python -m satgen <config.toml>`."""

import argparse
import tomllib
from pathlib import Path

from satgen.io import save_run
from satgen.pipeline import from_config

# src/satgen/__main__.py -> repo root (valid for the editable install `uv sync` creates)
OUTPUTS_DIR = Path(__file__).resolve().parents[2] / "outputs"


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="satgen", description="Generate satellite views of a simulated event."
    )
    parser.add_argument("config", type=Path, help="path to a run config (.toml)")
    parser.add_argument(
        "--out",
        type=Path,
        help="output directory (default: <repo>/outputs/<config name>)",
    )
    args = parser.parse_args(argv)

    with args.config.open("rb") as f:
        cfg = tomllib.load(f)
    pipeline, settings = from_config(cfg)

    result = pipeline.run(settings.grid, settings.time, settings.bands)

    out_dir = args.out or OUTPUTS_DIR / args.config.stem
    written = save_run(result, settings.store_artifacts, out_dir, args.config)
    print(f"Wrote {len(written)} artifact(s) to {out_dir}:")
    for path in written:
        print(f"  {path.name}")


if __name__ == "__main__":
    main()
