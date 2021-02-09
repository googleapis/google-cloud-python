#!/bin/bash
# Copyright 2021 Google LLC
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

if [[ -z "${ENVIRONMENT:-}" ]]; then
  echo "ENVIRONMENT not set. Exiting"
  exit 1
fi

if [[ -z "${PROJECT_ROOT:-}"  ]]; then
    PROJECT_ROOT="github/python-logging"
fi

# make sure submodule is up to date
git submodule update --init --recursive

cd "${PROJECT_ROOT}/tests/environment"

# Disable buffering, so that the logs stream through.
export PYTHONUNBUFFERED=1

# Debug: show build environment
env | grep KOKORO

# Setup service account credentials.
export GOOGLE_APPLICATION_CREDENTIALS=${KOKORO_GFILE_DIR}/service-account.json
gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS

# Setup project id.
export PROJECT_ID=$(cat "${KOKORO_GFILE_DIR}/project-id.json")
gcloud config set project $PROJECT_ID

# authenticate docker
gcloud auth configure-docker -q

# Remove old nox
python3.6 -m pip uninstall --yes --quiet nox-automation

# Install nox
python3.6 -m pip install --upgrade --quiet nox
python3.6 -m nox --version

# create a unique id for this run
UUID=$(python  -c 'import uuid; print(uuid.uuid1())' | head -c 7)
export ENVCTL_ID=ci-$UUID
echo $ENVCTL_ID

# Run the specified environment test
set +e
python3.6 -m nox --session "tests(language='python', platform='$ENVIRONMENT')"
TEST_STATUS_CODE=$?

# destroy resources
echo "cleaning up..."
/workspace/python-logging/tests/environment/envctl/envctl python $ENVIRONMENT destroy

# exit with proper status code
exit $TEST_STATUS_CODE
