#!/bin/bash
# Copyright 2021 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

set -eo pipefail

if [[ -z "${PROJECT_ROOT:-}" ]]; then
    PROJECT_ROOT="github/python-spanner-sqlalchemy"
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
fi
