#!/bin/bash

set -euxo pipefail

THISDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASEDIR="$( dirname "$( dirname "${THISDIR}" )" )"

cp "${BASEDIR}/README.md" "${BASEDIR}/app/README.md"
cp "${BASEDIR}/LICENSE" "${BASEDIR}/app/LICENSE"

MAIN_MODULE="unanimous"
MODULES=( "${MAIN_MODULE}" "tests" )
