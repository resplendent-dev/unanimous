"""
Load the list of packages from PyPi
"""

import pathlib


def get_config_dir(basepath=None):
    """
    Return the directory to store the cache of PyPi packages
    """
    if basepath is None:
        basepath = pathlib.Path.home()
    path = basepath / ".unanimous"
    if not path.exists():
        path.mkdir()
    return path


def test():
    """
    Called to run current test.
    """
    print(get_config_dir())
