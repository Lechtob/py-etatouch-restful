# Release Process

This project publishes `py-etatouch-restful` to PyPI from GitHub Releases.

## One-Time PyPI Setup

1. Configure PyPI Trusted Publishing for:
   - Owner: `Lechtob`
   - Repository: `py-etatouch-restful`
   - Workflow: `publish.yml`
   - Environment: `pypi`
2. The first GitHub Release creates the package on PyPI when Trusted Publishing is set.

## Release Checklist

1. Work from `develop` and make sure CI is green.
2. Update `CHANGELOG.md`.
3. Open and merge a release PR from `develop` into `main`.
4. Create a GitHub Release with a tag matching the package version, for example `v0.1.0`.
5. The `Publish` workflow builds the package and publishes it to PyPI.
6. After publishing, merge `main` back into `develop`.

## Local Verification

```powershell
python -m pip install -e ".[test,build]"
ruff check .
pytest
python -m build
twine check dist/*
```
