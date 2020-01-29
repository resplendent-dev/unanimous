"""
Test modules for unanimous.store
"""

import io
import pathlib
import shutil
import tempfile

from unanimous.store import (
    check_upstream_zip_hash,
    get_cached_words,
    get_config_dir,
    get_current_non_words,
    load_key,
)


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


def setup_fake_requests(requests_mock):
    """
    Used to setup dummy responses
    """
    url = (
        "https://github.com/resplendent-dev/unanimous"
        "/blob/master/master.zip?raw=true"
    )
    with open(zippath, "rb") as fobj:
        requests_mock.get(url, content=fobj.read())
    url = (
        "https://github.com/resplendent-dev/unanimous"
        "/blob/master/master.sha256?raw=true"
    )
    with io.open(shapath, "r", encoding="utf-8") as fobj:
        requests_mock.get(url, text=fobj.read())


def test_get_current_non_words(requests_mock):
    """
    GIVEN the upstream data contains a known value WHEN calling
    `get_current_non_words` THEN the known value is found.
    """
    # Setup
    setup_fake_requests(requests_mock)
    # Exercise
    result = get_current_non_words()
    # Verify
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
    assert val == 42  # nosec # noqa=S101


def test_check_upstream_zip_hash():
    """
    GIVEN an updated cache WHEN calling `check_upstream_zip_hash` THEN the
    upstream cache check returns True
    """
    # Setup
    get_current_non_words()
    # Exercise
    cache_updated = check_upstream_zip_hash()
    # Verify
    assert cache_updated  # nosec # noqa=S101


def test_get_cached_words():
    """
    GIVEN an updated cache WHEN calling `get_cached_words` THEN the
    current words are the same
    """
    # Setup
    current_result = get_current_non_words()
    # Exercise
    cached_result = get_cached_words()
    # Verify
    assert current_result == cached_result  # nosec # noqa=S101
