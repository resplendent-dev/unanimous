"""
Tests for `unanimous.pypi_load`
"""

from unanimous.pypi_load import get_package_list


def test_get_package_list():
    """
    GIVEN the `pypi` package list WHEN calling `get_package_list` THEN the
    package `unanimous` should be found.
    """
    # Exercise
    result = get_package_list()
    # Verify
    assert "unanimous" in result  # nosec # noqa=S101
