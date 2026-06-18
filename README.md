# py-etatouch-restful

Async Python client for ETA Touch RESTful Webservices.

The ETA documentation exposes the webservices at `http://<eta-ip>:8080`:

- `GET /user/api`: read the API version.
- `GET /user/menu`: read the menu tree.
- `GET /user/var/<uri>`: read a single variable.
- `POST /user/var/<uri>`: set a writable variable.
- `GET/PUT/DELETE /user/vars`: manage temporary variable sets.
- `GET /user/errors`: read active errors.
- `GET /user/varinfo/<uri>`: read variable metadata and valid values.

## Installation

```powershell
python -m pip install py-etatouch-restful
```

## Example

```python
import asyncio

from etatouch_restful import EtaTouchClient


async def main() -> None:
    async with EtaTouchClient("192.168.1.50") as client:
        api_version = await client.get_api_version()
        value = await client.get_variable("112/10021/0/0/12112")
        print(api_version, value.str_value, value.native_value)


asyncio.run(main())
```

## Development

```powershell
python -m pip install -e ".[test,build]"
ruff check .
pytest
python -m build
twine check dist/*
```

## Notes

ETA variable URIs are device-specific. For an ETA PU15, discover them through
`/user/menu` and inspect writable values through `/user/varinfo/<uri>`.

## Discovery Helpers

The package includes helpers to flatten the ETA menu tree and select conservative
default discovery candidates:

```python
from etatouch_restful import flatten_menu, is_default_discovery_candidate

variables = [
    variable
    for variable in flatten_menu(await client.get_menu())
    if is_default_discovery_candidate(variable)
]
```

## Repository Setup

Empfohlene GitHub-Repo-Einstellungen:

- Repository-Name: `py-etatouch-restful`
- Default Branch: `main`
- Develop Branch: `develop`
- PyPI-Paketname: `py-etatouch-restful`

Initialer Push in ein leeres Repo:

```powershell
git init
git add .
git commit -m "Initial py-etatouch-restful scaffold"
git branch -M main
git remote add origin https://github.com/<user>/py-etatouch-restful.git
git push -u origin main
git switch -c develop
git push -u origin develop
```

## Release Notes

Releases are published from GitHub Releases through PyPI Trusted Publishing. See
`RELEASE.md`.
