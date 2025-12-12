#!/bin/bash
# Copyright 2024 Google LLC
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

if [ -z "$(pyenv versions --bare | grep 3.8)" ]; then
    echo "Python 3.8 is not installed. Installing..."
    pyenv install 3.8
fi
pyenv shell 3.8

python -m pip install "setuptools<71"

# Start the releasetool reporter
python -m pip install --require-hashes -r ${REPO_ROOT}/.kokoro/requirements.txt
python -m releasetool publish-reporter-script > /tmp/publisher-script; source /tmp/publisher-script

ls ${REPO_ROOT}/wheels/
# Disable logging
set +x
TWINE_PASSWORD=$(cat "${KOKORO_KEYSTORE_DIR}/73713_google-cloud-pypi-token-keystore-3")
python -m twine upload --skip-existing --username __token__ --password "${TWINE_PASSWORD}" ${REPO_ROOT}/wheels/*
