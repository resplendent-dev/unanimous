"""
Test modules for unanimous.__main__
"""

import zipfile

import pytest
from click.testing import CliRunner

from unanimous.__main__ import get_project_path, main


def load_master_zip():
    """
    Load the word set from the master.zip
    """
    basedir = get_project_path()
    zippath = basedir / "master.zip"
    with zipfile.ZipFile(zippath) as zobj:
        filedata = zobj.read("nonwords.txt")
    words = set(word.strip() for word in filedata.splitlines())
    return words


@pytest.mark.parametrize("args,expected", [([], 0), (["invoke"], 0)])
def test_main(args, expected):
    """
    GIVEN the unanimous.__main__ module entry point WHEN calling main THEN the call
    executes successfully.
    """
    # Setup
    original_words = load_master_zip()
    runner = CliRunner()
    # Exercise
    result = runner.invoke(main, args)
    # Verify
    new_words = load_master_zip()
    assert result.exit_code == expected  # nosec # noqa=S101
    assert len(original_words - new_words) == 0  # nosec # noqa=S101
    # Allow for up to 5 new pypi packages to appear
    assert len(new_words - original_words) < 5  # nosec # noqa=S101
