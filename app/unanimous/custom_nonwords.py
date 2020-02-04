"""
Support automatically locating a custom non-word list
assumed to be `spelling_wordlist.txt` or `doc(s)/spelling_wordlist.txt`
in any ancestor directory
"""

import io
import pathlib


def get_custom_wordlist(path):
    """
    If found load the custom word list
    """
    result = set()
    if not path:
        return result
    with io.open(path, "r", encoding="utf-8") as fobj:
        for line in fobj:
            result.add(line.lower().strip())
    return result


def locate_custom_wordlist():
    """
    From the current working directory locate the custom word list.
    """
    start = pathlib.Path(".").resolve()
    return locate_custom_wordlist_from(start)


def locate_custom_wordlist_from(path):
    """
    From the provided directory locate the custom word list.
    """
    check = [
        path / "spelling_wordlist.txt",
        path / "docs" / "spelling_wordlist.txt",
        path / "doc" / "spelling_wordlist.txt",
    ]
    for checkpath in check:
        if checkpath.is_file():
            return checkpath
    if path.parent == path:
        return None
    return locate_custom_wordlist_from(path.parent)
