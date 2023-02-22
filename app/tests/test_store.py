"""
Test modules for unanimous.store
"""

import io
import pathlib
import shutil
import sys
import tempfile

import mock
import requests

from unanimous.store import (
    check_upstream_zip_hash,
    force_get_cached_words,
    get_cached_words,
    get_config_dir,
    get_current_non_words,
    load_key,
    save_key_value,
    update_cache_with_data,
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
        requests_mock.get(url, content=content)
    url = (
        "https://github.com/resplendent-dev/unanimous"
        "/blob/master/master.sha256?raw=true"
    )
    shapath = basepath / "master.sha256"
    with io.open(shapath, "r", encoding="utf-8") as fobj:
        requests_mock.get(url, text=fobj.read())
    return content


def setup_cache(requests_mock):
    """
    Push values into the cache
    """
    bytedata = setup_fake_requests(requests_mock)
    update_cache_with_data(bytedata)


def test_get_current_non_words(requests_mock):
    """
    GIVEN the upstream data contains a known value WHEN calling
    `get_current_non_words` THEN the known value is found.
    """
    # Setup
    setup_cache(requests_mock)
    # Exercise
    result = get_current_non_words()
    # Verify
    assert "sexualized" in result  # nosec # noqa=S101
    # Tear down
    setup_cache(requests_mock)


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
    setup_cache(requests_mock)
    # Exercise
    cache_updated = check_upstream_zip_hash()
    # Verify
    assert cache_updated  # nosec # noqa=S101
    # Tear down
    setup_cache(requests_mock)


def test_get_cached_words(requests_mock):
    """
    GIVEN an updated cache WHEN calling `get_cached_words` THEN the
    current words are the same
    """
    # Setup
    setup_cache(requests_mock)
    current_result = get_current_non_words()
    # Exercise
    cached_result = get_cached_words()
    # Verify
    assert current_result == cached_result  # nosec # noqa=S101
    # Tear down
    setup_cache(requests_mock)


def test_get_cached_words_expired(requests_mock):
    """
    GIVEN an updated but old cache WHEN calling `get_cached_words` THEN the
    current words are the same
    """
    # Setup
    setup_cache(requests_mock)
    current_result = get_current_non_words()
    setup_cache(requests_mock)
    save_key_value("timestamp", "20010101120000")
    # Exercise
    cached_result = get_cached_words()
    # Verify
    assert current_result == cached_result  # nosec # noqa=S101
    # Tear down
    setup_cache(requests_mock)


def test_get_cached_words_expunged(requests_mock):
    """
    GIVEN an old empty cache WHEN calling `get_cached_words` THEN
    no error is raised
    """
    # Setup
    setup_cache(requests_mock)
    save_key_value("timestamp", "20010101120000")
    save_key_value("nonwords", "")
    # Exercise
    get_cached_words()
    # Tear down
    setup_cache(requests_mock)


def test_get_cached_words_bad_hash(requests_mock):
    """
    GIVEN an old cache with a bad hash WHEN calling `get_cached_words` THEN
    no error is raised.
    """
    # Setup
    setup_cache(requests_mock)
    save_key_value("timestamp", "20010101120000")
    save_key_value("sha", "")
    # Exercise
    get_cached_words()
    # Tear down
    setup_cache(requests_mock)


def test_get_cached_words_bad_timestamp(requests_mock):
    """
    GIVEN a bad timestamp saved WHEN calling `get_cached_words` THEN
    no error is raised.
    """
    # Setup
    setup_cache(requests_mock)
    save_key_value("timestamp", "")
    # Exercise
    get_cached_words()
    # Tear down
    setup_cache(requests_mock)


def test_get_current_non_words_bad_timestamp(requests_mock):
    """
    GIVEN a bad timestamp saved WHEN calling `get_current_non_words` THEN
    the words are still returned.
    """
    # Setup
    setup_cache(requests_mock)
    save_key_value("timestamp", "")
    # Exercise
    result = get_current_non_words()
    # Verify
    assert "sexualized" in result  # nosec # noqa=S101
    # Tear down
    setup_cache(requests_mock)


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
    setup_cache(requests_mock)
    requests_mock.get(url, exc=requests.exceptions.ConnectTimeout)
    # Exercise
    cached_result = update_cached_nonwords()
    # Verify
    assert "sexualized" in cached_result  # nosec # noqa=S101
    # Tear down
    setup_cache(requests_mock)


def test_check_upstream_zip_hash_offline(requests_mock):
    """
    GIVEN an unavailable upstream hash WHEN calling `check_upstream_zip_hash`
    THEN it will return False
    """
    # Setup
    url = (
        "https://github.com/resplendent-dev/unanimous"
        "/blob/master/master.sha256?raw=true"
    )
    requests_mock.get(url, exc=requests.exceptions.ConnectTimeout)
    with mock.patch("unanimous.store.get_cached_sha", return_value="fake"):
        # Exercise
        result = check_upstream_zip_hash()
    # Verify
    assert not result  # nosec # noqa=S101


def test_force_get_cached_words(requests_mock):
    """
    GIVEN an empty cache and a default empty dict WHEN calling
    `force_get_cached_words` THEN the result should be a dictionary.
    """
    setup_cache(requests_mock)
    save_key_value("nonwords", "")
    # Exercise
    result = force_get_cached_words(deflt={})
    assert isinstance(result, dict)  # nosec # noqa=S101
    # Tear down
    setup_cache(requests_mock)


@mock.patch("pathlib.Path.home")
def test_get_config_dir_no_home(mockhome):
    """
    GIVEN an older python without home method WHEN calling `get_config_dir` THEN
    the result should be provided.
    """
    # Setup
    mockhome.side_effect = AttributeError("no home")
    # Exercise
    result = get_config_dir()
    # Verify
    assert result is not None  # noqa # nosec


@mock.patch("unanimous.store.get_cached_sha")
def test_not_cached(mockget):
    """
    GIVEN an empty cache WHEN calling `check_upstream_zip_hash` THEN the result
    should be False indicating not cached.
    """
    # Setup
    mockget.return_value = None
    # Exercise
    result = check_upstream_zip_hash()
    # Verify
    assert result is False  # noqa # nosec


@mock.patch("unanimous.store.get_cached_words")
@mock.patch("unanimous.store.update_cached_nonwords")
def test_get_current_updates(mockup, mockget):
    """
    GIVEN an empty cache WHEN calling `get_cached_words` THEN the
    `update_cached_nonwords` is called.
    """
    # Setup
    mockget.return_value = False
    # Exercise
    get_current_non_words()
    # Verify
    mockup.assert_called_once()
