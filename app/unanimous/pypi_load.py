"""
Load the list of packages from PyPi
"""

import pathlib


def get_config_dir():
    """
    Return the directory to store the cache of PyPi packages
    """
    path = pathlib.Path.home() / ".unanimous"
    if not path.exists():
        path.mkdir()
    return path


def test():
    """
    Called to run current test.
    """
    print(get_config_dir())
