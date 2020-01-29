"""
Test modules for unanimous.store
"""

import pathlib
import shutil
import tempfile

from unanimous.store import get_config_dir, get_current_non_words, load_key


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


def test_check_upstream_zip_hash():
    """
    GIVEN the upstream data contains a known value WHEN calling
    `get_current_non_words` THEN the known value is found.
    """
    # Exercise
    result = get_current_non_words()
    # Verify
    cached_result = get_current_non_words()
    assert result == cached_result
    assert "sexualized" in result  # nosec # noqa=S101


def test_load_key():
    """
    GIVEN a missing key WHEN calling `load_key` THEN the provided default
    should be returned.
    """
    # Setup
    # Exercise
    val = load_key("missing", 42)
    # Verify
    assert val == 42
