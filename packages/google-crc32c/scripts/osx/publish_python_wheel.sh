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

if ! pyenv versions --bare | grep -qE "^3\.10(\.|$)"; then
    echo "Python 3.10 is not installed. Installing..."
    pyenv install -s 3.10
fi
installed_310=$(pyenv versions --bare | grep -E "^3\.10(\.|$)" | head -n 1)
pyenv shell "${installed_310}"

python -m pip install --upgrade "setuptools<71" twine wheel pkginfo

echo "Built wheels in ${REPO_ROOT}/wheels/:"
ls -la "${REPO_ROOT}/wheels/"

for VER in $(awk -F': ' '/^versions:/ {print $2}' "${REPO_ROOT}/scripts/python_versions.yaml"); do
    SHORT=$(echo "$VER" | cut -d. -f1,2)
    ABI="cp${SHORT//.}-cp${SHORT//.}"
    ls "${REPO_ROOT}/wheels/"*${ABI}*.whl >/dev/null || {
        echo "ERROR: Missing macOS wheel for ${ABI}!"
        exit 1
    }
done

python -m twine check "${REPO_ROOT}/wheels/"*

if [[ "${PUBLISH_WHEELS}" == "true" ]]; then
    # Start the releasetool reporter
    python -m pip install --upgrade gcp-releasetool
    python -m releasetool publish-reporter-script > /tmp/publisher-script
    source /tmp/publisher-script

    # Disable logging
    set +x
    TWINE_PASSWORD=$(cat "${KOKORO_KEYSTORE_DIR}/73713_google-cloud-pypi-token-keystore-3")
    python -m twine upload --skip-existing --username __token__ --password "${TWINE_PASSWORD}" "${REPO_ROOT}/wheels/"*
else
    echo "PUBLISH_WHEELS is not set to 'true'. Skipping releasetool and twine upload (dry-run validation passed)."
fi
