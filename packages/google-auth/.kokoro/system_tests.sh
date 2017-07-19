#!/bin/bash

# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -eo pipefail

export PATH=${PATH}:${HOME}/gcloud/google-cloud-sdk/bin

cd github/google-auth-library-python

# Unencrypt and extract secrets
SECRETS_PASSWORD=$(cat "${KOKORO_GFILE_DIR}/secrets-password.txt")
./scripts/decrypt-secrets.sh "${SECRETS_PASSWORD}"

# Setup gcloud, this is needed for the App Engine system test.
gcloud auth activate-service-account --key-file system_tests/data/service_account.json
gcloud config set project "${TEST_PROJECT}"

# Run tests
tox -e py27-system
tox -e py36-system
