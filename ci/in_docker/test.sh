#!/bin/bash

set -euxo pipefail

THISDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASEDIR="$( dirname "$( dirname "${THISDIR}" )" )"

source ${BASEDIR}/ci/in_docker/prepare.sh

# Version independant checks
PYVER=3.7
# Run pyspelling in root to check docs
cd "${BASEDIR}"
"python${PYVER}" -m pyspelling
cd "${BASEDIR}/app"
# Version dependant checks
for PYVER in ${PYTHONVERS} ; do
  "python${PYVER}" -m flake8 "${MODULES[@]}"
  "python${PYVER}" -m isort -rc -c --diff "${MODULES[@]}"
  "python${PYVER}" -m bandit -r "${MODULES[@]}"
  find "${MODULES[@]}" -iname \*.py -print0 | xargs -0 -n 1 "${BASEDIR}/ci/in_docker/pylint.sh" "python${PYVER}"
  "python${PYVER}" -m pytest -n auto --cov-config=.coveragerc --cov-fail-under=100 "--cov=${MAIN_MODULE}" --cov-report=xml:test-cov.xml --cov-report=html
done
echo 'Testing Complete'
