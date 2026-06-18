"""Typed models returned by the ETA Touch client."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class EtaValue:
    """A single ETA variable value."""

    uri: str
    raw: str
    str_value: str
    unit: str
    decimal_places: int
    scale_factor: float
    advanced_text_offset: int | None = None

    @property
    def native_value(self) -> float | str:
        """Return a scaled numeric value when possible, otherwise the formatted string."""

        try:
            return int(self.raw) / self.scale_factor
        except (TypeError, ValueError, ZeroDivisionError):
            return self.str_value


@dataclass(frozen=True, slots=True)
class EtaMenuNode:
    """A node in the ETA menu tree."""

    uri: str
    name: str
    kind: str
    children: tuple[EtaMenuNode, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class EtaVariableSet:
    """A temporary ETA variable set."""

    uri: str
    variables: tuple[EtaValue, ...]


@dataclass(frozen=True, slots=True)
class EtaError:
    """An active ETA error."""

    fub_uri: str
    fub_name: str
    message: str
    priority: str
    time: str
    description: str


@dataclass(frozen=True, slots=True)
class EtaValidValue:
    """A valid raw value for a writable ETA variable."""

    raw: str
    str_value: str


@dataclass(frozen=True, slots=True)
class EtaVariableInfo:
    """Metadata for an ETA variable."""

    uri: str
    name: str
    full_name: str
    unit: str
    decimal_places: int
    scale_factor: float
    advanced_text_offset: int | None
    is_writable: bool
    value_type: str
    valid_values: tuple[EtaValidValue, ...]

