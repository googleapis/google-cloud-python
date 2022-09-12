#!/bin/bash
# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

set -eo pipefail

if [[ -z "${PROJECT_ROOT:-}" ]]; then
    PROJECT_ROOT="github/python-spanner-django"
fi

cd "${PROJECT_ROOT}"

# Disable buffering, so that the logs stream through.
export PYTHONUNBUFFERED=1

# Setup service account credentials.
export GOOGLE_APPLICATION_CREDENTIALS=${KOKORO_GFILE_DIR}/service-account.json
export PROJECT_ID=$(cat "${KOKORO_GFILE_DIR}/project-id.json")
export GOOGLE_CLOUD_PROJECT=$(cat "${KOKORO_GFILE_DIR}/project-id.json")

export RUNNING_SPANNER_BACKEND_TESTS=1

if [[ $KOKORO_JOB_NAME == *"docs"* ]]
then
    echo "Running docs generation."
    # Remove old nox
    python3 -m pip uninstall --yes --quiet nox-automation

    # Install nox
    python3 -m pip install --upgrade --quiet nox
    # Generate docs.
    python3 -m nox -s docs docfx
else
    pip3 install .
    export DJANGO_TESTS_DIR="django_tests_dir"
    mkdir -p $DJANGO_TESTS_DIR && git clone --depth 1 --single-branch --branch "django/stable/2.2.x" https://github.com/googleapis/python-spanner-django.git $DJANGO_TESTS_DIR/django

    # Install dependencies for Django tests.
    sudo -E apt-get update
    apt-get install -y libffi-dev libjpeg-dev zlib1g-dev libmemcached-dev
    cd $DJANGO_TESTS_DIR/django && pip3 install -e . && pip3 install -r tests/requirements/py3.txt; cd ../../

    # Hardcode the max number of workers since Spanner has a very low
    # QPS for administrative RPCs of 5QPS (averaged every 100 seconds)
    if [[ $KOKORO_JOB_NAME == *"continuous"* ]]
    then
        # Disable continuous build as it creates too many Spanner instances
        # ("Quota exceeded for quota metric 'Instance create requests' and
        # limit 'Instance create requests per minute' of service
        # 'spanner.googleapis.com').
        export DJANGO_WORKER_COUNT=0
    else
        export DJANGO_WORKER_COUNT=5
    fi

    python3 ./run_testing_worker.py
fi
