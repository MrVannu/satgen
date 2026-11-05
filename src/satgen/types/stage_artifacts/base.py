"""Base class for stage outputs that can be written to and read from disk."""

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Self

import numpy as np
from numpy.typing import NDArray

_META_KEY = "__meta__"


class StageArtifact(ABC):
    """The output of one pipeline stage."""

    @abstractmethod
    def serialize(self, path: Path) -> None:
        """Write the artifact to `path` (a .npz file)."""

    @classmethod
    @abstractmethod
    def deserialize(cls, path: Path) -> Self:
        """Recreate the artifact from a file written by `serialize`."""


def write_npz(
    path: Path, meta: dict[str, Any], arrays: dict[str, NDArray[Any]]
) -> None:
    """Store JSON-serializable `meta` and named arrays in one .npz file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(path, **{_META_KEY: np.array(json.dumps(meta))}, **arrays)


def read_npz(path: Path) -> tuple[dict[str, Any], dict[str, NDArray[Any]]]:
    """Inverse of `write_npz`: returns (meta, arrays)."""
    with np.load(path, allow_pickle=False) as data:
        meta = json.loads(str(data[_META_KEY]))
        arrays = {key: data[key] for key in data.files if key != _META_KEY}
    return meta, arrays
