"""
Test modules for unanimous.__main__
"""
from click.testing import CliRunner

from unanimous.__main__ import main


def test_main():
    """
    GIVEN the unanimous.__main__ module entry point WHEN calling main THEN the call
    executes successfully.
    """
    # Setup
    runner = CliRunner()
    # Exercise
    result = runner.invoke(main, [])
    # Verify
    assert result.exit_code == 0  # nosec # noqa=S101
