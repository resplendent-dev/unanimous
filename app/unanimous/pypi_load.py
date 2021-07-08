"""
Load the list of packages from `PyPi`.
"""

import backoff
from defusedxml.xmlrpc import monkey_patch, unmonkey_patch, xmlrpc_client


@backoff.on_exception(backoff.expo, xmlrpc_client.Fault)
def get_package_list():
    """
    Load the list of packages from `PyPi`.
    """
    monkey_patch()
    client = xmlrpc_client.ServerProxy("https://pypi.python.org/pypi")
    packages = client.list_packages()
    unmonkey_patch()
    return packages
