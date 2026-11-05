"""All disk access: writing and reading stage artifacts and run metadata.

An artifact is stored as one .npz file containing its arrays, its metadata as
JSON (`__meta__`) and its type name (`__type__`, checked on load).
"""

import json
import shutil
import subprocess
from pathlib import Path

import numpy as np

from satgen.stages import STAGE_NAMES
from satgen.types import SerializedArtifact, StageArtifact

# src/satgen/io.py -> repo root (valid for the editable install `uv sync` creates)
REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUTS_DIR = REPO_ROOT / "outputs"

_META_KEY = "__meta__"
_TYPE_KEY = "__type__"


def artifact_path(run_dir: Path, stage: str) -> Path:
    """Where a stage's artifact is stored, e.g. `<run_dir>/s1_catastrophe_generator.npz`."""
    return run_dir / f"s{STAGE_NAMES.index(stage) + 1}_{stage}.npz"


def resolve(path: str | Path) -> Path:
    """Resolve relative paths against the repo root, like the default output dir."""
    path = Path(path)
    return path if path.is_absolute() else REPO_ROOT / path


def write_artifact(path: Path, artifact: StageArtifact) -> None:
    data = artifact.serialize()
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        path,
        **{
            _META_KEY: np.array(json.dumps(data.meta)),
            _TYPE_KEY: np.array(type(artifact).__name__),
        },
        **data.arrays,
    )


def read_artifact[A: StageArtifact](path: Path, cls: type[A]) -> A:
    with np.load(path, allow_pickle=False) as npz:
        stored_type = str(npz[_TYPE_KEY])
        if stored_type != cls.__name__:
            raise ValueError(
                f"{path} contains a {stored_type}, expected {cls.__name__}"
            )
        data = SerializedArtifact(
            meta=json.loads(str(npz[_META_KEY])),
            arrays={k: npz[k] for k in npz.files if k not in (_META_KEY, _TYPE_KEY)},
        )
    return cls.deserialize(data)


def load_stage_artifact[A: StageArtifact](
    run_dir: str | Path, stage: str, cls: type[A]
) -> A:
    """Load the artifact a previous run stored for `stage`."""
    path = artifact_path(resolve(run_dir), stage)
    if not path.exists():
        raise FileNotFoundError(
            f"[{stage}] no artifact at {path}; was {stage!r} in store_artifacts?"
        )
    return read_artifact(path, cls)


def save_run(
    artifacts: dict[str, StageArtifact],
    store_artifacts: tuple[str, ...],
    out_dir: Path,
    config_path: Path,
) -> list[Path]:
    """Write the selected stage artifacts plus the config and git commit used.

    Returns the paths of the written artifacts.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for stage, artifact in artifacts.items():
        if stage in store_artifacts:
            path = artifact_path(out_dir, stage)
            write_artifact(path, artifact)
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
