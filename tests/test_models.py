"""Regression tests for numeric raw values emitted by ETA controllers."""

import pytest

from etatouch_restful.models import EtaValue


@pytest.mark.parametrize(
    ("raw", "scale", "expected"),
    [
        ("1.32917e+08", 1, 132917000.0),
        ("2.6654e+07", 1, 26654000.0),
        ("6.72255e+07", 1, 67225500.0),
        ("1.11514e+06", 1, 1115140.0),
        ("4.25e+02", 10, 42.5),
        ("425", 10, 42.5),
        ("0", 1, 0.0),
        ("-125", 10, -12.5),
        ("2.5", 1, 2.5),
    ],
)
def test_scaled_numeric_values(raw, scale, expected):
    value = EtaValue("40/10021/0/0/12153", raw, "display", "s", 0, scale)
    assert value.native_value == expected


@pytest.mark.parametrize(
    ("raw", "scale"),
    [("text", 1), ("", 1), ("100", 0), ("nan", 1), ("inf", 1), ("-inf", 1), ("1e999", 1)],
)
def test_invalid_numeric_values_preserve_display(raw, scale):
    value = EtaValue("40/10021/0/0/12153", raw, "---", "s", 0, scale)
    assert value.native_value == "---"
