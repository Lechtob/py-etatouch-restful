from __future__ import annotations

import aiohttp
import pytest

from etatouch_restful import EtaTouchClient, EtaTouchConnectionError


class FakeResponse:
    def __init__(self, status: int, text: str) -> None:
        self.status = status
        self._text = text

    async def __aenter__(self) -> FakeResponse:
        return self

    async def __aexit__(self, *_exc: object) -> None:
        return None

    async def text(self, *, encoding: str = "utf-8") -> str:
        return self._text


class FakeSession:
    def __init__(self, response: FakeResponse) -> None:
        self.response = response
        self.calls: list[tuple[str, str, dict[str, object]]] = []

    def request(self, method: str, url: str, **kwargs: object) -> FakeResponse:
        self.calls.append((method, url, kwargs))
        return self.response


@pytest.mark.asyncio
async def test_get_api_version_requests_expected_path() -> None:
    session = FakeSession(
        FakeResponse(
            200,
            """
            <eta version="1.0" xmlns="http://www.eta.co.at/rest/v1">
              <api version="1.2" />
            </eta>
            """,
        )
    )
    client = EtaTouchClient("192.168.1.50", session=session)

    assert await client.get_api_version() == "1.2"
    assert session.calls == [
        ("GET", "http://192.168.1.50:8080/user/api", {"timeout": aiohttp.ClientTimeout(total=10)})
    ]


@pytest.mark.asyncio
async def test_set_variable_posts_raw_value_and_time_slot() -> None:
    session = FakeSession(
        FakeResponse(
            200,
            """
            <eta version="1.0" xmlns="http://www.eta.co.at/rest/v1">
              <success uri="/user/var/112/10111/12130/0/1082"/>
            </eta>
            """,
        )
    )
    client = EtaTouchClient("eta.local", session=session)

    await client.set_variable("112/10111/12130/0/1082", 400, begin=0, end=48)

    assert session.calls == [
        (
            "POST",
            "http://eta.local:8080/user/var/112/10111/12130/0/1082",
            {
                "data": {"value": "400", "begin": "0", "end": "48"},
                "timeout": aiohttp.ClientTimeout(total=10),
            },
        )
    ]


@pytest.mark.asyncio
async def test_custom_timeout_with_borrowed_session() -> None:
    session = FakeSession(
        FakeResponse(200, '<eta xmlns="http://www.eta.co.at/rest/v1"><api version="1.2" /></eta>')
    )
    async with EtaTouchClient("eta.test", session=session, timeout=3) as client:
        assert await client.get_api_version() == "1.2"
    assert session.calls[0][2]["timeout"].total == 3
    # A borrowed session has no close method and must remain owned by its caller.


@pytest.mark.asyncio
async def test_timeout_becomes_connection_error() -> None:
    class TimeoutSession:
        def request(self, *args, **kwargs):
            raise TimeoutError

    client = EtaTouchClient("eta.test", session=TimeoutSession(), timeout=3)
    with pytest.raises(EtaTouchConnectionError, match="Timed out"):
        await client.get_api_version()
