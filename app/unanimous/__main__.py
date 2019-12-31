#!/usr/bin/env python
"""
Module load handler for execution via:

python -m unanimous
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import click

import unanimous.pypi_load

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


def run_invocation():
    """
    Execute the invocation
    """
    unanimous.pypi_load.test()


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
# vim: set ft=python:
