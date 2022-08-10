#!/bin/bash
# Copyright 2022 Google LLC
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


set -eox pipefail

if [[ -z "${PROJECT_ROOT:-}"  ]]; then
    PROJECT_ROOT="github/python-logging"
fi

cd "${PROJECT_ROOT}/tests/performance"


# Disable buffering, so that the logs stream through.
export PYTHONUNBUFFERED=1

# Debug: show build environment
env | grep KOKORO


# Install nox
python3 -m pip install --upgrade --quiet nox

# run performance tests
set +e
python3 -m nox
TEST_STATUS_CODE=$?

# Workaround for Kokoro permissions issue: delete secrets
rm testing/{test-env.sh,client-secrets.json,service-account.json}

exit "$TEST_STATUS_CODE"
