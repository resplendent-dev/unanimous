#!/usr/bin/env python
"""
Module load handler for execution via:

python -m unanimous
"""
from __future__ import absolute_import, division, print_function, unicode_literals

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
    nonwordpath = basedir / "nonwords.txt"
    tmpdir = tempfile.mkdtemp()
    tmppath = pathlib.Path(tmpdir)
    tmpnonwordpath = tmppath / "nonwords.txt"
    shutil.copy(nonwordpath, tmpnonwordpath)
    packages = get_package_list()
    with io.open(tmpnonwordpath, "w", encoding="utf-8") as fobjout:
        with io.open(nonwordpath, "r", encoding="utf-8") as fobjin:
            for line in fobjin:
                print(line.strip().lower(), file=fobjout)
        for package in packages:
            print(package.strip().lower(), file=fobjout)
    with zipfile.ZipFile(str(zippath), "w") as zobj:
        zobj.write(tmpnonwordpath, "nonwords.txt")
        zobj.close()


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
# vim: set ft=python:
