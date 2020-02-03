"""
Tests for custom non-words.
"""

import os
import pathlib
import sys
import tempfile

from unanimous.custom_nonwords import get_custom_wordlist, locate_custom_wordlist


def get_basedir():
    """
    Locate the directory of the project root
    """
    this_py_path = pathlib.Path(sys.modules[__name__].__file__)
    tests_path = this_py_path.absolute().parent
    app_path = tests_path.parent
    workspace_path = app_path.parent
    return workspace_path


def test_get_custom_wordlist_emptydir():
    """
    Given an empty directory ensure the empty set of words is obtained for
    custom words.
    """
    # Setup
    tmpdir = tempfile.mkdtemp()
    os.chdir(tmpdir)
    # Exercise
    result = get_custom_wordlist(locate_custom_wordlist())
    # Verify
    assert len(result) == 0  # nosec # noqa=S101
    # Tear down
    os.chdir(str(get_basedir()))
