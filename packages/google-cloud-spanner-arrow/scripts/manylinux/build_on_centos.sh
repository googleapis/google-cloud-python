#!/bin/bash
# Copyright 2026 Google LLC
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

set -e -x
MAIN_PYTHON_BIN="/opt/python/cp310-cp310/bin/"
echo "BUILD_PYTHON: ${BUILD_PYTHON}"
REPO_ROOT=/var/code/spanner-arrow/

${MAIN_PYTHON_BIN}/python -m pip install --upgrade pip
${MAIN_PYTHON_BIN}/python -m pip install \
    --requirement ${REPO_ROOT}/scripts/dev-requirements.txt

PYTHON_VERSIONS=""
if [[ -z ${BUILD_PYTHON} ]]; then
    for PYTHON_BIN in /opt/python/*/bin; do
        if [[ "${PYTHON_BIN}" == *"310"* ]]; then
            PYTHON_VERSIONS="${PYTHON_VERSIONS} ${PYTHON_BIN}"
        elif [[ "${PYTHON_BIN}" == *"311"* ]]; then
            PYTHON_VERSIONS="${PYTHON_VERSIONS} ${PYTHON_BIN}"
        elif [[ "${PYTHON_BIN}" == *"312"* ]]; then
            PYTHON_VERSIONS="${PYTHON_VERSIONS} ${PYTHON_BIN}"
        elif [[ "${PYTHON_BIN}" == *"313"* && "${PYTHON_BIN}" != *"313t"* ]]; then
            PYTHON_VERSIONS="${PYTHON_VERSIONS} ${PYTHON_BIN}"
        elif [[ "${PYTHON_BIN}" == *"314"* && "${PYTHON_BIN}" != *"314t"* ]]; then
            PYTHON_VERSIONS="${PYTHON_VERSIONS} ${PYTHON_BIN}"
        fi
    done
else
    STRIPPED_PYTHON=$(echo ${BUILD_PYTHON} | sed -e "s/\.//g" | sed -e "s/-dev$//")
    for PYTHON_BIN in /opt/python/*/bin; do
        if [[ "${PYTHON_BIN}" == *"${STRIPPED_PYTHON}"* ]]; then
            PYTHON_VERSIONS="${PYTHON_VERSIONS} ${PYTHON_BIN}"
        fi
    done
fi

# Build wheels
cd ${REPO_ROOT}
mkdir -p dist_wheels
for PYTHON_BIN in ${PYTHON_VERSIONS}; do
    ${PYTHON_BIN}/python -m pip install --upgrade pip
    ${PYTHON_BIN}/python -m pip install \
        --requirement ${REPO_ROOT}/scripts/dev-requirements.txt
    ${PYTHON_BIN}/python -m pip wheel . --wheel-dir dist_wheels/
done

# Audit wheels
mkdir -p wheels
for whl in dist_wheels/google_cloud_spanner_arrow*.whl; do
    "${MAIN_PYTHON_BIN}/auditwheel" repair "${whl}" --wheel-dir wheels/ || cp "${whl}" wheels/
done

# Install and test wheels
for PYTHON_BIN in ${PYTHON_VERSIONS}; do
    ABI_TAG=$(basename $(dirname ${PYTHON_BIN}))
    ARCH=$(uname -m)
    ${PYTHON_BIN}/python -m venv /tmp/venv
    WHEEL_FILE=$(ls ${REPO_ROOT}/wheels/google_cloud_spanner_arrow-*-${ABI_TAG}-*${ARCH}*.whl | head -n 1)
    /tmp/venv/bin/pip install "${WHEEL_FILE}"
    /tmp/venv/bin/python ${REPO_ROOT}/scripts/check_spanner_arrow_extension.py
    rm -rf /tmp/venv
done

rm -rf ${REPO_ROOT}/dist_wheels/
