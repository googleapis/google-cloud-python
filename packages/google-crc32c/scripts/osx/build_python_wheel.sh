#!/bin/bash
# Copyright 2018 Google LLC
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

# Build a **single** Python wheel for a specified version. The version and
# associated paths should be set as environment variables; the expected
# environment variables will be verified below.

set -e -x

# Check that the REPO_ROOT, PY_BIN and PY_TAG environment variables are set.
if [[ -z "${REPO_ROOT}" ]]; then
    echo "REPO_ROOT environment variable should be set by the caller."
    exit 1
fi
if [[ -z "${PY_BIN}" ]]; then
    echo "PY_BIN environment variable should be set by the caller."
    exit 1
fi
if [[ -z "${PY_TAG}" ]]; then
    echo "PY_TAG environment variable should be set by the caller."
    exit 1
fi

# Make sure we have an updated `pip`.
${PY_BIN} -m pip install --upgrade pip
# Create a virtualenv where we can install Python build dependencies.
${PY_BIN} -m pip install --upgrade virtualenv
VENV=${REPO_ROOT}/venv
${PY_BIN} -m virtualenv ${VENV}
${VENV}/bin/python -m pip install \
    --requirement ${REPO_ROOT}/scripts/dev-requirements.txt

# Create the wheel.
DIST_WHEELS="${REPO_ROOT}/dist_wheels"
mkdir ${DIST_WHEELS}
${VENV}/bin/python -m pip wheel ${REPO_ROOT} --wheel-dir ${DIST_WHEELS}

# Delocate the wheel.
FIXED_WHEELS="${REPO_ROOT}/wheels"
mkdir -p ${FIXED_WHEELS}
${VENV}/bin/delocate-wheel \
    --check-archs \
    --wheel-dir ${FIXED_WHEELS} \
    --verbose \
    ${DIST_WHEELS}/python_crc32c*${PY_TAG}*.whl

# Clean up.
rm -fr ${DIST_WHEELS}
rm -fr ${VENV}
