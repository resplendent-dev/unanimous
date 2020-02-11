#!/usr/bin/env python
"""
Module load handler for execution via:

python -m unanimous
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import hashlib
import io
import pathlib
import shutil
import sys
import tempfile
import zipfile

import click

from unanimous.pypi_load import get_package_list

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

__version__ = "0.1"


@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.version_option(version=__version__)
@click.pass_context
def main(ctxt):
    """
    Main click group handler
    """
    if ctxt.invoked_subcommand is None:
        run_invocation()


@main.command()
def invoke():
    """
    Primary command handler
    """
    run_invocation()


def get_project_path():
    """
    Locate the directory of the root folder for the project
    """
    this_file = pathlib.Path(sys.modules[__name__].__file__).resolve()
    test_dir = this_file.parent
    app_dir = test_dir.parent
    project_dir = app_dir.parent
    return project_dir


def run_invocation():
    """
    Execute the invocation
    """
    basedir = get_project_path()
    zippath = basedir / "master.zip"
    tmpdir = tempfile.mkdtemp()
    tmppath = pathlib.Path(tmpdir)
    tmpnonwordpath = build_nonwords_file(tmppath)
    with zipfile.ZipFile(str(zippath), "w") as zobj:
        zobj.write(tmpnonwordpath, "nonwords.txt")
        zobj.close()
    checksum = sha256(zippath)
    shapath = basedir / "master.sha256"
    with io.open(str(shapath), "w", encoding="utf-8") as fobj:
        print(checksum, file=fobj)


def build_nonwords_file(tmppath):
    """
    Prepare the zip output.
    """
    packages = get_package_list()
    nonwords = set()
    existing = set(package.strip().lower() for package in packages)
    basedir = get_project_path()
    nonwordpath = basedir / "nonwords.txt"
    tmpnonwordpath = tmppath / "nonwords.txt"
    shutil.copy(str(nonwordpath), str(tmpnonwordpath))
    with io.open(str(tmpnonwordpath), "w", encoding="utf-8") as fobjout:
        with io.open(str(nonwordpath), "r", encoding="utf-8") as fobjin:
            for line in fobjin:
                nonword = line.strip().lower()
                if nonword not in existing:
                    nonwords.add(nonword)
        for nonword in sorted(list(nonwords)):
            print(nonword, file=fobjout)
    shutil.copy(tmpnonwordpath, nonwordpath)
    return tmpnonwordpath


def sha256(filepath):
    """
    Get quick hash of file
    """
    sha = hashlib.sha256()
    with open(str(filepath), "rb") as fobj:
        while True:
            block = fobj.read(4096)
            if not block:
                break
            sha.update(block)
    return sha.hexdigest()


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
# vim: set ft=python:
