"""
Cache the details of non-words.
"""

import pathlib

import requests


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


def get_db():
    """
    Connect to cache db
    """


def check_upstream_zip_hash():
    """
    Quick check to see if the upstream master.zip has been updated.
    """
    url = (
        "https://github.com/resplendent-dev/unanimous"
        "/blob/master/master.zip?raw=true"
    )
    return repr(requests.head(url).headers.keys())
