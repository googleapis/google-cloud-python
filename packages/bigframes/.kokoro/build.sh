#!/bin/bash
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -eo pipefail

if [[ -z "${KOKORO_GOB_COMMIT}" ]]; then
    PROJECT_SCM="github/python-bigquery-dataframes"
else
    PROJECT_SCM="git/bigframes"
fi

if [[ -z "${PROJECT_ROOT:-}" ]]; then
    PROJECT_ROOT="${KOKORO_ARTIFACTS_DIR}/${PROJECT_SCM}"
fi

cd "${PROJECT_ROOT}"

# Disable buffering, so that the logs stream through.
export PYTHONUNBUFFERED=1

# Debug: show build environment
env | grep KOKORO

# Install pip
python3 -m pip install --upgrade --quiet pip
python3 -m pip --version

# Remove old nox
python3 -m pip uninstall --yes --quiet nox-automation

# Install nox
python3 -m pip install --upgrade --quiet nox
python3 -m nox --version

# If NOX_SESSION is set, it only runs the specified session,
# otherwise run all the sessions.
if [[ -n "${NOX_SESSION:-}" ]]; then
    python3 -m nox --stop-on-first-error -s ${NOX_SESSION:-}
else
    python3 -m nox --stop-on-first-error
fi
