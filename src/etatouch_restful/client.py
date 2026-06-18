"""HTTP client for ETA Touch RESTful Webservices."""

from __future__ import annotations

from typing import Any

import aiohttp

from .exceptions import EtaTouchConnectionError, EtaTouchResponseError
from .models import EtaError, EtaMenuNode, EtaValue, EtaVariableInfo, EtaVariableSet
from .parser import (
    ensure_success,
    parse_api_version,
    parse_errors,
    parse_menu,
    parse_value,
    parse_variable_info,
    parse_variable_set,
    parse_variable_sets,
)

DEFAULT_PORT = 8080
DEFAULT_TIMEOUT = 10


class EtaTouchClient:
    """Async client for an ETA Touch controller."""

    def __init__(
        self,
        host: str,
        *,
        port: int = DEFAULT_PORT,
        session: aiohttp.ClientSession | None = None,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        self.host = host
        self.port = port
        self._session = session
        self._owns_session = session is None
        self._timeout = aiohttp.ClientTimeout(total=timeout)

    async def __aenter__(self) -> EtaTouchClient:
        if self._session is None:
            self._session = aiohttp.ClientSession(timeout=self._timeout)
        return self

    async def __aexit__(self, *_exc: object) -> None:
        if self._owns_session and self._session is not None:
            await self._session.close()
            self._session = None

    @property
    def base_url(self) -> str:
        """Return the base URL for the ETA Touch webservice."""

        return f"http://{self.host}:{self.port}"

    async def get_api_version(self) -> str:
        """Read the API version."""

        return parse_api_version(await self._request("GET", "/user/api"))

    async def get_menu(self) -> list[EtaMenuNode]:
        """Read the ETA menu tree."""

        return parse_menu(await self._request("GET", "/user/menu"))

    async def get_variable(self, uri: str) -> EtaValue:
        """Read a single variable by CAN URI."""

        return parse_value(await self._request("GET", f"/user/var/{_clean_uri(uri)}"))

    async def set_variable(
        self,
        uri: str,
        value: int | float | str,
        *,
        begin: int | None = None,
        end: int | None = None,
    ) -> None:
        """Set a writable variable to a raw value."""

        data: dict[str, str] = {"value": str(value)}
        if begin is not None:
            data["begin"] = str(begin)
        if end is not None:
            data["end"] = str(end)
        ensure_success(await self._request("POST", f"/user/var/{_clean_uri(uri)}", data=data))

    async def list_variable_sets(self) -> list[str]:
        """List currently defined temporary variable sets."""

        return parse_variable_sets(await self._request("GET", "/user/vars"))

    async def create_variable_set(self, name: str) -> None:
        """Create a temporary variable set."""

        ensure_success(await self._request("PUT", f"/user/vars/{name}"))

    async def delete_variable_set(self, name: str) -> None:
        """Delete a temporary variable set."""

        ensure_success(await self._request("DELETE", f"/user/vars/{name}"))

    async def add_variable_to_set(self, name: str, uri: str) -> None:
        """Add a variable to a temporary variable set."""

        ensure_success(await self._request("PUT", f"/user/vars/{name}/{_clean_uri(uri)}"))

    async def remove_variable_from_set(self, name: str, uri: str) -> None:
        """Remove a variable from a temporary variable set."""

        ensure_success(await self._request("DELETE", f"/user/vars/{name}/{_clean_uri(uri)}"))

    async def get_variable_set(self, name: str) -> EtaVariableSet:
        """Read all values from a temporary variable set."""

        return parse_variable_set(await self._request("GET", f"/user/vars/{name}"))

    async def get_errors(self, node_id: int | None = None, fub_id: int | None = None) -> list[EtaError]:
        """Read active ETA errors."""

        path = "/user/errors"
        if node_id is not None:
            path += f"/{node_id}"
        if fub_id is not None:
            path += f"/{fub_id}"
        return parse_errors(await self._request("GET", path))

    async def get_variable_info(self, uri: str) -> EtaVariableInfo:
        """Read metadata for a variable."""

        return parse_variable_info(await self._request("GET", f"/user/varinfo/{_clean_uri(uri)}"))

    async def _request(self, method: str, path: str, **kwargs: Any) -> str:
        session = await self._get_session()
        url = f"{self.base_url}{path}"
        try:
            async with session.request(method, url, **kwargs) as response:
                text = await response.text(encoding="utf-8")
                if response.status >= 400:
                    raise EtaTouchResponseError(
                        f"ETA Touch returned HTTP {response.status} for {method} {path}",
                        status=response.status,
                        body=text,
                    )
                return text
        except TimeoutError as err:
            raise EtaTouchConnectionError(f"Timed out connecting to ETA Touch at {url}") from err
        except aiohttp.ClientError as err:
            raise EtaTouchConnectionError(f"Could not connect to ETA Touch at {url}") from err

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None:
            self._session = aiohttp.ClientSession(timeout=self._timeout)
        return self._session


def _clean_uri(uri: str) -> str:
    return uri.strip().strip("/")

