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

PUBLISH_VENV="/tmp/publish_venv"
rm -rf "${PUBLISH_VENV}"
python3.12 -m venv "${PUBLISH_VENV}"

"${PUBLISH_VENV}/bin/python" -m pip install --upgrade pip "setuptools<71"
"${PUBLISH_VENV}/bin/python" -m pip install --require-hashes -r "${REPO_ROOT}/scripts/release-requirements.txt"

echo "Built wheels in ${REPO_ROOT}/wheels/:"
ls -la "${REPO_ROOT}/wheels/"

for VER in $(awk -F': ' '/^versions:/ {print $2}' "${REPO_ROOT}/scripts/python_versions.yaml"); do
    SHORT="${VER:0:4}"
    ABI="cp${SHORT//.}-cp${SHORT//.}"
    for ARCH in x86_64 aarch64; do
        ls "${REPO_ROOT}/wheels/"*${ABI}*${ARCH}*.whl >/dev/null || {
            echo "ERROR: Missing Linux wheel for ${ABI} (${ARCH})!"
            exit 1
        }
    done
done

"${PUBLISH_VENV}/bin/python" -m twine check "${REPO_ROOT}/wheels/"*

if [[ "${PUBLISH_WHEELS}" == "true" ]]; then
    # Start the releasetool reporter
    "${PUBLISH_VENV}/bin/python" -m releasetool publish-reporter-script > /tmp/publisher-script; source /tmp/publisher-script

    # Disable logging
    set +x
    TWINE_PASSWORD=$(cat "${KOKORO_KEYSTORE_DIR}/73713_google-cloud-pypi-token-keystore-3")
    "${PUBLISH_VENV}/bin/python" -m twine upload --skip-existing --username __token__ --password "${TWINE_PASSWORD}" "${REPO_ROOT}/wheels/"*
else
    echo "PUBLISH_WHEELS is not 'true'; skipping PyPI upload after twine check."
fi

rm -rf "${PUBLISH_VENV}"
