# Unanimous - A pyspelling plugin for common non-words

[![Azure Status](https://dev.azure.com/timgates/timgates/_apis/build/status/resplendent-dev.unanimous?branchName=master)](https://dev.azure.com/timgates/timgates/_build/latest?definitionId=16&branchName=master)
[![Travis Status](https://travis-ci.org/resplendent-dev/unanimous.svg?branch=master)](https://travis-ci.org/resplendent-dev/unanimous)
[![Appveyor Status](https://ci.appveyor.com/api/projects/status/y5vhp2fmcirqatyg/branch/master?svg=true)](https://ci.appveyor.com/project/timgates42/unanimous)
[![PyPI version](https://img.shields.io/pypi/v/unanimous.svg)](https://pypi.org/project/unanimous)
[![Python Versions](https://img.shields.io/pypi/pyversions/unanimous.svg)](https://pypi.org/project/unanimous)
[![PyPI downloads per month](https://img.shields.io/pypi/dm/unanimous.svg)](https://pypi.org/project/unanimous)
[![Documentation Status](https://readthedocs.org/projects/unanimous/badge/?version=latest)](https://unanimous.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/resplendent-dev/unanimous/badge.svg)](https://coveralls.io/github/resplendent-dev/unanimous/)
[![Black](https://camo.githubusercontent.com/28a51fe3a2c05048d8ca8ecd039d6b1619037326/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f636f64652532307374796c652d626c61636b2d3030303030302e737667)](https://github.com/psf/black)

Extension to make running pyspelling in CI easier. Maintains a common word exception list of technical terms so that every project does not need to exclude words like PyPi and GitHub etc..

More details can be found in the
[Online Documentation.](https://unanimous.readthedocs.io/en/latest/)

# Installation

You can install unanimous for
[Python](https://www.python.org/) via
[pip](https://pypi.org/project/pip/)
from [PyPI](https://pypi.org/).

```
$ pip install unanimous
```

Note: if using Python 3.4 the latest version of lxml only supports python 3.5 and above so install lxml 4.3.4


## Prerequisites:
- pyspelling
- dataset
- requests
- click
- defusedxml


## Download from PyPI.org

https://pypi.org/project/unanimous/



# Contributing

Contributions are very welcome, consider using the
[file an issue](https://github.com/resplendent-dev/unanimous/issues)
to discuss the work before beginning, but if you already have a Pull Request
ready then this is no problem, please submit it and it will be very gratefully
considered. The [Contribution Guidelines](CONTRIBUTING.md)
outlines the unanimous commitment to ensuring all
contributions receive appropriate recognition.

# License


Distributed under the terms of the [GPLv3](https://opensource.org/licenses/GPL-3.0)
license, "unanimous" is free and open source software


# Issues

If you encounter any problems, please
[file an issue](https://github.com/resplendent-dev/unanimous/issues)
along with a detailed description.

# Additional Documentation:

* [Online Documentation](https://unanimous.readthedocs.io/en/latest/)
* [News](NEWS.rst).
* [Template Updates](COOKIECUTTER_UPDATES.md).
* [Code of Conduct](CODE_OF_CONDUCT.md).
* [Contribution Guidelines](CONTRIBUTING.md).
