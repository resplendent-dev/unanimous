"""
Test modules for unanimous.store
"""

import io
import logging
import pathlib
import shutil
import sys
import tempfile

import requests

from unanimous.store import (
    check_upstream_zip_hash,
    get_cached_words,
    get_config_dir,
    get_current_non_words,
    load_key,
    save_key_value,
    update_cached_nonwords,
)


def get_basedir():
    """
    Locate the directory of the project root
    """
    this_py_path = pathlib.Path(sys.modules[__name__].__file__)
    tests_path = this_py_path.absolute().parent
    app_path = tests_path.parent
    workspace_path = app_path.parent
    return workspace_path


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
    basepath = get_basedir()
    zippath = basepath / "master.zip"
    with open(zippath, "rb") as fobj:
        content = fobj.read()
        logging.warning("Read content as %r", content)
        requests_mock.get(url, content=content)
    url = (
        "https://github.com/resplendent-dev/unanimous"
        "/blob/master/master.sha256?raw=true"
    )
    shapath = basepath / "master.sha256"
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


def test_check_upstream_zip_hash(requests_mock):
    """
    GIVEN an updated cache WHEN calling `check_upstream_zip_hash` THEN the
    upstream cache check returns True
    """
    # Setup
    setup_fake_requests(requests_mock)
    get_current_non_words()
    # Exercise
    cache_updated = check_upstream_zip_hash()
    # Verify
    assert cache_updated  # nosec # noqa=S101


def test_get_cached_words(requests_mock):
    """
    GIVEN an updated cache WHEN calling `get_cached_words` THEN the
    current words are the same
    """
    # Setup
    setup_fake_requests(requests_mock)
    current_result = get_current_non_words()
    # Exercise
    cached_result = get_cached_words()
    # Verify
    assert current_result == cached_result  # nosec # noqa=S101


def test_get_cached_words_expired(requests_mock):
    """
    GIVEN an updated but old cache WHEN calling `get_cached_words` THEN the
    current words are the same
    """
    # Setup
    setup_fake_requests(requests_mock)
    current_result = get_current_non_words()
    save_key_value("timestamp", "20010101120000")
    # Exercise
    cached_result = get_cached_words()
    # Verify
    assert current_result == cached_result  # nosec # noqa=S101


def test_get_cached_words_expunged(requests_mock):
    """
    GIVEN an old empty cache WHEN calling `get_cached_words` THEN
    None is returned.
    """
    # Setup
    setup_fake_requests(requests_mock)
    get_current_non_words()
    save_key_value("timestamp", "20010101120000")
    save_key_value("nonwords", "")
    # Exercise
    cached_result = get_cached_words()
    # Verify
    assert cached_result is None  # nosec # noqa=S101


def test_get_cached_words_bad_hash(requests_mock):
    """
    GIVEN an old cache with a bad hash WHEN calling `get_cached_words` THEN
    None is returned.
    """
    # Setup
    setup_fake_requests(requests_mock)
    get_current_non_words()
    save_key_value("timestamp", "20010101120000")
    save_key_value("sha", "")
    # Exercise
    cached_result = get_cached_words()
    # Verify
    assert cached_result is None  # nosec # noqa=S101


def test_get_cached_words_bad_timestamp(requests_mock):
    """
    GIVEN a bad timestamp saved WHEN calling `get_cached_words` THEN
    None is returned.
    """
    # Setup
    setup_fake_requests(requests_mock)
    save_key_value("timestamp", "")
    # Exercise
    cached_result = get_cached_words()
    # Verify
    assert cached_result is None  # nosec # noqa=S101


def test_update_cached_nonwords(requests_mock):
    """
    GIVEN an unavailable upstream zip WHEN calling `update_cached_nonwords`
    THEN it will fallback to the cache.
    """
    # Setup
    url = (
        "https://github.com/resplendent-dev/unanimous"
        "/blob/master/master.zip?raw=true"
    )
    requests_mock.get(url, exc=requests.exceptions.ConnectTimeout)
    save_key_value("nonwords", "fakewordish")
    # Exercise
    cached_result = update_cached_nonwords()
    # Verify
    assert "fakewordish" in cached_result  # nosec # noqa=S101
