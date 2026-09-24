# Changelog

All notable changes to `py-etatouch-restful` will be documented in this file.

## Unreleased

## 0.2.1 - 2026-09-24

- Parse numeric raw values in scientific and decimal notation, including runtime
  counters, without falling back to formatted text. Non-finite values retain the
  display-text fallback.
- Apply the configured request timeout when using a caller-provided HTTP session.

## 0.2.0 - Unreleased

- Add menu-tree discovery helpers for Home Assistant entity discovery.

## 0.1.0 - 2026-06-18

- Initial async ETA Touch REST client.
- XML parsers for API version, menu, variables, variable sets, active errors and variable info.
- Typed dataclass models and package metadata.
- GitHub Actions CI and PyPI publish workflow.
