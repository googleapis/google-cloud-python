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

set -e -x
echo "CHECKING OSX WHEELS"
VERSION=$(awk "/version \= ([0-9.]+)/" setup.cfg)
PACKAGE_VERSION=${VERSION:10}

# ``readlink -f`` is not our friend on OS X. This relies on **some**
# ``python`` being installed.
SCRIPT_FI=$(python -c "import os; print(os.path.realpath('${0}'))")
OSX_DIR=$(dirname ${SCRIPT_FI})
SCRIPTS_DIR=$(dirname ${OSX_DIR})
export REPO_ROOT=$(dirname ${SCRIPTS_DIR})

ls ${REPO_ROOT}/wheels

# NOTE: These are the Python.org versions of Python.
PYTHON36="/Library/Frameworks/Python.framework/Versions/3.6/bin"
PYTHON37="/Library/Frameworks/Python.framework/Versions/3.7/bin"
PYTHON38="/Library/Frameworks/Python.framework/Versions/3.8/bin"

# PYTHON37="/users/crwilcox/.pyenv/versions/3.7.2/bin"
# PYTHON36="/users/crwilcox/.pyenv/versions/3.6.6/bin"
# PYTHON35="/users/crwilcox/.pyenv/versions/3.5.6/bin"

# Make sure we have an updated `pip`.
curl https://bootstrap.pypa.io/get-pip.py | ${PYTHON37}/python3

# Make sure virtualenv and delocate.
${PYTHON37}/python3 -m pip install --upgrade delocate
LISTDEPS_CMD="${PYTHON37}/delocate-listdeps --all --depending"
VIRTUALENV_CMD="${PYTHON37}/python3 -m venv"


${PYTHON36}/python3 -m venv venv36
curl https://bootstrap.pypa.io/get-pip.py | venv36/bin/python3
WHL=${REPO_ROOT}/wheels/google_crc32c-${PACKAGE_VERSION}-cp36-cp36m-macosx_10_9_x86_64.whl
venv36/bin/pip install ${WHL}
venv36/bin/python ${REPO_ROOT}/scripts/check_cffi_crc32c.py
${LISTDEPS_CMD} ${WHL}
rm -fr venv36

${PYTHON37}/python3 -m venv venv37
curl https://bootstrap.pypa.io/get-pip.py | venv37/bin/python3
WHL=${REPO_ROOT}/wheels/google_crc32c-${PACKAGE_VERSION}-cp37-cp37m-macosx_10_9_x86_64.whl
venv37/bin/pip install ${WHL}
venv37/bin/python ${REPO_ROOT}/scripts/check_cffi_crc32c.py
${LISTDEPS_CMD} ${WHL}
rm -fr venv37

${PYTHON38}/python3 -m venv venv38
curl https://bootstrap.pypa.io/get-pip.py | venv38/bin/python3
WHL=${REPO_ROOT}/wheels/google_crc32c-${PACKAGE_VERSION}-cp38-cp38-macosx_10_9_x86_64.whl
venv38/bin/pip install ${WHL}
venv38/bin/python ${REPO_ROOT}/scripts/check_cffi_crc32c.py
${LISTDEPS_CMD} ${WHL}
rm -fr venv38

# TODO: As of 2020-12-11, 3.9 is not available on our CI
# ${PYTHON39}/python3 -m venv venv39
# curl https://bootstrap.pypa.io/get-pip.py | venv39/bin/python3
# WHL=${REPO_ROOT}/wheels/google_crc32c-${PACKAGE_VERSION}-cp39-cp39-macosx_10_9_x86_64.whl
# venv37/bin/pip install ${WHL}
# venv37/bin/python ${REPO_ROOT}/scripts/check_cffi_crc32c.py
# ${LISTDEPS_CMD} ${WHL}
# rm -fr venv39
