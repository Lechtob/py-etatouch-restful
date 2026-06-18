"""Helpers for discovering ETA variables from the menu tree."""

from __future__ import annotations

from dataclasses import dataclass

from .models import EtaMenuNode

EXCLUDED_PATH_PARTS = frozenset(
    {
        "Heizzeiten",
        "Ladezeiten",
        "Zeitfenster",
        "Montag",
        "Dienstag",
        "Mittwoch",
        "Donnerstag",
        "Freitag",
        "Samstag",
        "Sonntag",
        "Estrich",
        "Heizkurve",
    }
)

EXCLUDED_NAME_PARTS = frozenset(
    {
        "Absenkung",
        "Ausschalt",
        "Einschalt",
        "Fixwert",
        "Kalibrier",
        "Max",
        "Maximal",
        "Min",
        "Mindest",
        "Name",
        "Nenn",
        "Soll",
        "Typ",
        "Verzögerung",
        "Zeitüberwachung",
    }
)

PREFERRED_NAME_PARTS = frozenset(
    {
        "Anforderung",
        "Außentemperatur",
        "Austragleistung",
        "Drehzahl",
        "Eingang",
        "Ist",
        "Leistung",
        "Luftfeuchte",
        "Rücklauf",
        "Strom",
        "Status",
        "Temperatur",
        "Ventilzustand",
        "Vorlauf",
        "Warmwasserspeicher",
        "Zähler",
        "Zustand",
    }
)


@dataclass(frozen=True, slots=True)
class EtaDiscoveredVariable:
    """A menu leaf that can be considered for entity creation."""

    uri: str
    name: str
    path: tuple[str, ...]

    @property
    def full_name(self) -> str:
        """Return a stable human-readable path name."""

        return " > ".join(part for part in self.path if part)


def flatten_menu(
    menu: list[EtaMenuNode] | tuple[EtaMenuNode, ...],
) -> tuple[EtaDiscoveredVariable, ...]:
    """Return all leaf variables from an ETA menu tree."""

    discovered: list[EtaDiscoveredVariable] = []
    for node in menu:
        _flatten_node(node, (), discovered)
    return tuple(discovered)


def is_default_discovery_candidate(variable: EtaDiscoveredVariable) -> bool:
    """Return whether a menu leaf is a conservative default discovery candidate."""

    if not variable.uri:
        return False
    path_parts = set(variable.path)
    if path_parts & EXCLUDED_PATH_PARTS:
        return False
    full_name = variable.full_name
    if any(part in full_name for part in EXCLUDED_NAME_PARTS):
        return False
    return any(part in full_name for part in PREFERRED_NAME_PARTS)


def _flatten_node(
    node: EtaMenuNode,
    parent_path: tuple[str, ...],
    discovered: list[EtaDiscoveredVariable],
) -> None:
    path = (*parent_path, node.name)
    if node.children:
        for child in node.children:
            _flatten_node(child, path, discovered)
        return
    discovered.append(EtaDiscoveredVariable(uri=node.uri.strip("/"), name=node.name, path=path))
