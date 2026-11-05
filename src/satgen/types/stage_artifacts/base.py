"""Base class for stage outputs that can be converted to and from plain data.

Artifacts never touch the disk themselves: `serialize` produces a
`SerializedArtifact` that `satgen.io` writes as is, and `deserialize` rebuilds
the artifact from what `satgen.io` read back.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Self

from numpy.typing import NDArray


@dataclass(frozen=True, eq=False)
class SerializedArtifact:
    """Storage-agnostic representation of an artifact."""

    meta: dict[str, Any]
    """JSON-serializable metadata (grid, time, ids, ...)."""
    arrays: dict[str, NDArray[Any]]
    """Named numpy arrays."""


class StageArtifact(ABC):
    """The output of one pipeline stage."""

    @abstractmethod
    def serialize(self) -> SerializedArtifact:
        """Convert the artifact into metadata and arrays."""

    @classmethod
    @abstractmethod
    def deserialize(cls, data: SerializedArtifact) -> Self:
        """Recreate the artifact from the output of `serialize`."""
