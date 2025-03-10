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

python3 -m nox --version

# If this is a continuous build, send the test log to the FlakyBot.
# See https://github.com/googleapis/repo-automation-bots/tree/main/packages/flakybot.
if [[ $KOKORO_BUILD_ARTIFACTS_SUBDIR = *"continuous"* ]]; then
  cleanup() {
    chmod +x $KOKORO_GFILE_DIR/linux_amd64/flakybot
    $KOKORO_GFILE_DIR/linux_amd64/flakybot
  }
  trap cleanup EXIT HUP
fi

# If NOX_SESSION is set, it only runs the specified session,
# otherwise run all the sessions.
if [[ -n "${NOX_SESSION:-}" ]]; then
    python3 -m nox -s ${NOX_SESSION:-}
else
    python3 -m nox -s unit
    python3 -m nox -s system
fi
