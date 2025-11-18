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

# ``readlink -f`` is not our friend on OS X. This relies on **some**
# ``python`` being installed.
SCRIPT_FI=$(python3 -c "import os; print(os.path.realpath('${0}'))")
OSX_DIR=$(dirname ${SCRIPT_FI})
SCRIPTS_DIR=$(dirname ${OSX_DIR})
export REPO_ROOT=$(dirname ${SCRIPTS_DIR})

# Create a virtualenv where we can install Python build dependencies.
VENV=${REPO_ROOT}/venv_build
"python3" -m venv ${VENV}

curl https://bootstrap.pypa.io/get-pip.py | ${VENV}/bin/python
${VENV}/bin/python -m pip install \
    --requirement ${REPO_ROOT}/scripts/dev-requirements.txt

# Create the wheel.
DIST_WHEELS="${REPO_ROOT}/dist_wheels"
mkdir -p ${DIST_WHEELS}
cd ${REPO_ROOT}
${VENV}/bin/python setup.py build_ext \
    --include-dirs=${REPO_ROOT}/usr/include \
    --library-dirs=${REPO_ROOT}/usr/lib \
    --rpath=${REPO_ROOT}/usr/lib
${VENV}/bin/python -m pip wheel ${REPO_ROOT} --wheel-dir ${DIST_WHEELS}

# Delocate the wheel.
FIXED_WHEELS="${REPO_ROOT}/wheels"
mkdir -p ${FIXED_WHEELS}
${VENV}/bin/delocate-wheel \
    --wheel-dir ${FIXED_WHEELS} \
    --verbose \
    --check-archs \
    ${DIST_WHEELS}/google_crc32c*.whl

# Clean up.
rm -fr ${DIST_WHEELS}
rm -fr ${VENV}
