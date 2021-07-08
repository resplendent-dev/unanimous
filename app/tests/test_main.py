"""
Test modules for unanimous.__main__
"""

import io
import pathlib
import shutil
import tempfile
import zipfile

import mock
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
    tmppath = pathlib.Path(tempfile.mkdtemp())
    nonwordstmppath = tmppath / "nonwords.txt"
    shutil.copy(get_project_path() / "nonwords.txt", nonwordstmppath)
    with io.open(nonwordstmppath, "a", encoding="utf-8") as fobj:
        print("unanimous", file=fobj)
    with mock.patch("unanimous.__main__.get_project_path", return_value=tmppath):
        # Exercise
        result = runner.invoke(main, args, catch_exceptions=False)
        # Verify
        new_words = load_master_zip()
    assert not result.exception  # nosec # noqa=S101
    assert result.exit_code == expected  # nosec # noqa=S101
    assert len(original_words - new_words) == 0  # nosec # noqa=S101
    # Allow for up to 5 new packages to appear
    assert len(new_words - original_words) < 5  # nosec # noqa=S101
