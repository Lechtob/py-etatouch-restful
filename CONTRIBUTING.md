# Contributing

## Branching

This project follows GitFlow:

- `main`: stable releases only.
- `develop`: integration branch for upcoming work.
- `feature/<name>`: focused feature branches.
- `release/<version>`: release preparation.
- `hotfix/<version>`: urgent fixes from `main`.

## Local Checks

```powershell
python -m pip install -e ".[test,build]"
ruff check .
pytest
python -m build
twine check dist/*
```

## Scope

Keep this package independent from Home Assistant. It should only contain the ETA Touch
HTTP/XML client, models, parser logic and tests.
