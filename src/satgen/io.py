"""Writing pipeline outputs to disk."""

import shutil
import subprocess
from pathlib import Path

from satgen.pipeline import STAGE_NAMES, PipelineResult


def artifact_path(out_dir: Path, stage: str) -> Path:
    """Where a stage's artifact is stored, e.g. `<out_dir>/s1_catastrophe_generator.npz`."""
    return out_dir / f"s{STAGE_NAMES.index(stage) + 1}_{stage}.npz"


def save_run(
    result: PipelineResult,
    store_artifacts: tuple[str, ...],
    out_dir: Path,
    config_path: Path,
) -> list[Path]:
    """Serialize the selected stage artifacts plus the config and git commit used.

    Returns the paths of the written artifacts.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for stage, artifact in result.artifacts().items():
        if stage in store_artifacts:
            path = artifact_path(out_dir, stage)
            artifact.serialize(path)
            written.append(path)
    shutil.copy(config_path, out_dir / "config.toml")
    (out_dir / "git_commit.txt").write_text(_git_commit() + "\n")
    return written


def _git_commit() -> str:
    """Current commit hash, suffixed with '-dirty' if there are local changes."""
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
        ).stdout.strip()
        dirty = subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True, check=True
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"
    return f"{commit}-dirty" if dirty else commit
