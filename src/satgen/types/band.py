"""Sensor frequency bands."""

from dataclasses import asdict, dataclass
from typing import Any, Self


@dataclass(frozen=True)
class Band:
    """A sensor frequency band. Spectral response functions to be added."""

    name: str
    center_wavelength_um: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Self:
        return cls(**d)


VIIRS_BANDS: dict[str, Band] = {
    "I4": Band("I4", 3.74),
    "I5": Band("I5", 11.45),
    "M13": Band("M13", 4.05),
}
