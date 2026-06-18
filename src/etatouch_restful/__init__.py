"""Async client for ETA Touch RESTful Webservices."""

from .exceptions import EtaTouchConnectionError, EtaTouchError, EtaTouchResponseError
from .models import EtaError, EtaMenuNode, EtaValidValue, EtaValue, EtaVariableInfo, EtaVariableSet

__version__ = "0.2.0"

__all__ = [
    "EtaError",
    "EtaDiscoveredVariable",
    "EtaMenuNode",
    "EtaTouchClient",
    "EtaTouchConnectionError",
    "EtaTouchError",
    "EtaTouchResponseError",
    "EtaValidValue",
    "EtaValue",
    "EtaVariableInfo",
    "EtaVariableSet",
    "__version__",
    "flatten_menu",
    "is_default_discovery_candidate",
]


def __getattr__(name: str) -> object:
    """Lazy-load the aiohttp based client only when requested."""

    if name == "EtaTouchClient":
        from .client import EtaTouchClient

        return EtaTouchClient
    if name in {"EtaDiscoveredVariable", "flatten_menu", "is_default_discovery_candidate"}:
        from .discovery import EtaDiscoveredVariable, flatten_menu, is_default_discovery_candidate

        exports = {
            "EtaDiscoveredVariable": EtaDiscoveredVariable,
            "flatten_menu": flatten_menu,
            "is_default_discovery_candidate": is_default_discovery_candidate,
        }
        return exports[name]
    raise AttributeError(name)
