"""
Cache the details of non-words.
"""

import pathlib

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
    db = dataset.connect("sqlite://%s" % (path / "cache.db"))
    table = db["storage"]
    return table


def load_key(name, deflt=None, basepath=None):
    """
    Retrieve stored key value.
    """
    table = get_storage_table()
    row = table.find_one(key=key)
    if not row:
        return deflt
    return row["value"]


def save_key_value(key, value):
    """
    Save key, value to storage.
    """
    table = get_storage_table()
    table.upsert({"key": key, "value": value}, keys=["key"])


def get_cached_sha():
    """
    Lookup current sha value
    """
    return load_key("sha")


def check_upstream_zip_hash():
    """
    Quick check to see if the upstream master.zip has been updated.
    """
    cache_sha = get_cached_sha()
    if not cache_sha:
        return False
    url = (
        "https://github.com/resplendent-dev/unanimous"
        "/blob/master/master.sha256?raw=true"
    )
    current_sha = requests.text.strip().split(" ", 1)[0]
    return cache_sha == current_sha


def get_current_non_words():
    """
    Work out if our cache is up to date and update it if not and then return
    the list of current non-words
    """
    cached_words = get_cached_words()
    if cached_words:
        return cached_words
    return update_cached_nonwords()


def update_cached_nonwords():
    """
    """
    return None


def get_cached_words():
    """
    If the cache is current then return the list of words otherwise return
    None
    """
    timestamp = load_key("timestamp")
    if not timestamp:
        return None
    cache_time = datetime.datetime.strptime(timestamp, "%Y%m%d%H%M%S")
    if cache_time + datetime.timedelta(days=1) < datetime.datetime.now():
        return None
    return set(load_key("nonwords").splitlines())
