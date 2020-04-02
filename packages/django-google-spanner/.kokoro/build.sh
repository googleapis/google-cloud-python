#!/bin/bash
# Copyright 2020 Google LLC
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

cd github/python-spanner-django

# Disable buffering, so that the logs stream through.
export PYTHONUNBUFFERED=1

# Debug: show build environment
env | grep KOKORO

# Setup service account credentials.
export GOOGLE_APPLICATION_CREDENTIALS=${KOKORO_GFILE_DIR}/service-account.json

# Setup project id.
export PROJECT_ID=$(cat "${KOKORO_GFILE_DIR}/project-id.json")

# Install tox
python3.6 -m pip install --upgrade --quiet tox flake8 isort
python3.6 -m tox --version

python3.6 -m tox
python3.6 -m isort --recursive --check-only --diff
python3.6 -m flake8

# Run with the Django test apps.
export RUNNING_SPANNER_BACKEND_TESTS=1
export DJANGO_TEST_APPS="backends basic bulk_create choices custom_columns"
bash django_test_suite.sh
