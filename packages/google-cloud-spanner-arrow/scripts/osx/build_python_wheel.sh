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

if [[ -z "${REPO_ROOT}" ]]; then
    echo "REPO_ROOT environment variable should be set by the caller."
    exit 1
fi
if [[ -z "${PY_BIN}" ]]; then
    echo "PY_BIN environment variable should be set by the caller."
    exit 1
fi

VENV=${REPO_ROOT}/venv${PY_BIN}
"python${PY_BIN}" -m venv ${VENV}
${VENV}/bin/python -m pip install --upgrade pip setuptools wheel
${VENV}/bin/python -m pip install --requirement ${REPO_ROOT}/scripts/dev-requirements.txt

DIST_WHEELS="${REPO_ROOT}/dist_wheels"
mkdir -p ${DIST_WHEELS}
cd ${REPO_ROOT}
${VENV}/bin/python -m pip wheel ${REPO_ROOT} --wheel-dir ${DIST_WHEELS}

FIXED_WHEELS="${REPO_ROOT}/wheels"
mkdir -p ${FIXED_WHEELS}
cp ${DIST_WHEELS}/google_cloud_spanner_arrow*${PY_TAG}*.whl ${FIXED_WHEELS}/ 2>/dev/null || cp ${DIST_WHEELS}/*.whl ${FIXED_WHEELS}/

# Test wheel
${VENV}/bin/pip install --no-index --find-links=${FIXED_WHEELS} google-cloud-spanner-arrow --force-reinstall
${VENV}/bin/pip install pytest
${VENV}/bin/pytest ${REPO_ROOT}/tests
${VENV}/bin/python ${REPO_ROOT}/scripts/check_spanner_arrow_extension.py

rm -rf ${DIST_WHEELS}
rm -rf ${VENV}
