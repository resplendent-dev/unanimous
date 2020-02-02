"""
Cache the details of non-words.
"""

import datetime
import hashlib
import io
import logging
import pathlib
import zipfile

import dataset
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


def get_storage_table(basepath=None):
    """
    Connect to cache db
    """
    path = get_config_dir(basepath=basepath)
    con = dataset.connect("sqlite:///%s" % (path / "cache.db"))
    table = con["storage"]
    return table


def load_key(key, deflt=None, basepath=None):
    """
    Retrieve stored key value.
    """
    table = get_storage_table(basepath=basepath)
    row = table.find_one(key=key)
    if not row:
        return deflt
    return row["value"]


def save_key_value(key, value, basepath=None):
    """
    Save key, value to storage.
    """
    table = get_storage_table(basepath=basepath)
    table.upsert({"key": key, "value": value}, keys=["key"])


def get_cached_sha(basepath=None):
    """
    Lookup current hash value
    """
    return load_key("sha", basepath=basepath)


def check_upstream_zip_hash(basepath=None):
    """
    Quick check to see if the upstream master.zip has been updated.
    """
    cache_sha = get_cached_sha(basepath=basepath)
    if not cache_sha:
        return False
    url = (
        "https://github.com/resplendent-dev/unanimous"
        "/blob/master/master.sha256?raw=true"
    )
    try:
        response = requests.get(url, timeout=1)
    except OSError:
        logging.exception("Unable to check non-word cache at this time.")
        # Can not be reached - assume not updated
        return False
    else:
        current_sha = response.text.strip().split(" ", 1)[0]
        return cache_sha == current_sha


def get_current_non_words(basepath=None):
    """
    Work out if our cache is up to date and update it if not and then return
    the list of current non-words
    """
    cached_words = get_cached_words(basepath=basepath)
    if cached_words:
        return cached_words
    return update_cached_nonwords(basepath=basepath)


def update_cached_nonwords(basepath=None):
    """
    Load the latest non-words and update the db
    """
    url = (
        "https://github.com/resplendent-dev/unanimous"
        "/blob/master/master.zip?raw=true"
    )
    try:
        response = requests.get(url, timeout=1)
    except OSError:
        logging.exception("Unable to update non-word cache at this time.")
        return force_get_cached_words(basepath=basepath, deflt=set())
    else:
        content = response.content
        return update_cache_with_data(content, basepath=basepath)


def update_cache_with_data(bytedata, basepath=None):
    """
    Update the cache with the provided zip data
    """
    sha256 = hashlib.sha256(bytedata).hexdigest()
    with io.BytesIO(bytedata) as fobj:
        with zipfile.ZipFile(fobj) as zobj:
            data = zobj.read("nonwords.txt").decode("utf-8")
    save_key_value("nonwords", data, basepath=basepath)
    save_key_value("sha", sha256, basepath=basepath)
    save_key_value(
        "timestamp", datetime.datetime.now().strftime("%Y%m%d%H%M%S"), basepath=basepath
    )
    return set(data.splitlines())


def get_cached_words(basepath=None):
    """
    If the cache is current then return the list of words otherwise return
    None
    """
    timestamp = load_key("timestamp", basepath=basepath)
    if not timestamp:
        return None
    cache_time = datetime.datetime.strptime(timestamp, "%Y%m%d%H%M%S")
    if cache_time + datetime.timedelta(days=1) < datetime.datetime.now():
        # Is cache hash still okay anyway?
        if not check_upstream_zip_hash(basepath=basepath):
            return None
        # Refresh timestamp
        save_key_value(
            "timestamp",
            datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
            basepath=basepath,
        )
    return force_get_cached_words(basepath=basepath)


def force_get_cached_words(basepath=None, deflt=None):
    """
    Grab whatever is in the cache
    """
    nonwords = load_key("nonwords", basepath=basepath)
    if not nonwords:
        return deflt
    return set(nonwords.splitlines())
