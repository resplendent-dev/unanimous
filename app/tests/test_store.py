"""
Test modules for unanimous.store
"""

import pathlib
import shutil
import tempfile

from unanimous.store import get_config_dir


def test_get_config_dir():
    """
    GIVEN an empty temporary directory base WHEN calling `get_config_dir` THEN the call
    creates the missing directory.
    """
    # Setup
    tmpdir = tempfile.mkdtemp()
    tmppath = pathlib.Path(tmpdir)
    # Exercise
    get_config_dir(tmppath)
    # Verify
    assert ".unanimous" in set(  # nosec # noqa=S101
        subpath.name for subpath in tmppath.iterdir()
    )
    shutil.rmtree(tmpdir)


def test_get_config_dir_default():
    """
    GIVEN no parameters WHEN calling `get_config_dir` THEN the call
    creates the default directory.
    """
    # Setup
    # Exercise
    path = get_config_dir()
    # Verify
    assert path.is_dir()  # nosec # noqa=S101
