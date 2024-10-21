#!/bin/bash
# Copyright 2022 Google LLC
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

# `-e` enables the script to automatically fail when a command fails
# `-o pipefail` sets the exit code to non-zero if any command fails,
# or zero if all commands in the pipeline exit successfully.
set -eo pipefail

pwd

# Move into the package, build the distribution and upload.
TWINE_PASSWORD=$(cat "${KOKORO_KEYSTORE_DIR}/73713_google-cloud-pypi-token-keystore-3")

python3 setup.py sdist bdist_wheel
twine upload --username __token__ --password "${TWINE_PASSWORD}" dist/*
