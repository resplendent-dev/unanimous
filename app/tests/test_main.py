"""
Test modules for unanimous.__main__
"""
from unanimous.__main__ import main


def test_main():
    """
    GIVEN the unanimous.__main__
    module entry point WHEN calling main THEN the call executes successfully
    with a result of `None`
    """
    # Setup
    # Exercise
    result = main()  # pylint: disable=assignment-from-no-return
    # Verify
    assert result is None  # nosec
