#!/bin/bash

function docker_compose_run() {
    USEROPT="$(id -u):$(id -g)"
    SHORTPYVER="$(echo "${PYVER}" | sed "s/[.]//")"
    docker-compose -p "py${SHORTPYVER}" build --build-arg PYVER="${PYVER}"
    docker-compose -p "py${SHORTPYVER}" up -d
    docker-compose -p "py${SHORTPYVER}" run --rm -u "${USEROPT}" "$@"
    docker-compose -p "py${SHORTPYVER}" down
}
