"""Async client for ETA Touch RESTful Webservices."""

from .exceptions import EtaTouchConnectionError, EtaTouchError, EtaTouchResponseError
from .models import EtaError, EtaMenuNode, EtaValidValue, EtaValue, EtaVariableInfo, EtaVariableSet

__version__ = "0.1.0"

__all__ = [
    "EtaError",
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
]


def __getattr__(name: str) -> object:
    """Lazy-load the aiohttp based client only when requested."""

    if name == "EtaTouchClient":
        from .client import EtaTouchClient

        return EtaTouchClient
    raise AttributeError(name)
