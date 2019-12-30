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

# ``readlink -f`` is not our friend on OS X. This relies on **some**
# ``python`` being installed.
SCRIPT_FI=$(python -c "import os; print(os.path.realpath('${0}'))")
OSX_DIR=$(dirname ${SCRIPT_FI})
SCRIPTS_DIR=$(dirname ${OSX_DIR})
export REPO_ROOT=$(dirname ${SCRIPTS_DIR})

ls ${REPO_ROOT}/wheels

# NOTE: These are the Python.org versions of Python.
PYTHON35="/Library/Frameworks/Python.framework/Versions/3.5/bin"
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

${PYTHON35}/python3 -m venv venv35
curl https://bootstrap.pypa.io/get-pip.py | venv35/bin/python3
WHL=${REPO_ROOT}/wheels/google_crc32c-0.0.1-cp35-cp35m-macosx_10_6_intel.whl
venv35/bin/pip install ${WHL}
venv35/bin/python ${REPO_ROOT}/scripts/check_cffi_crc32c.py
${LISTDEPS_CMD} ${WHL}
rm -fr venv35

${PYTHON36}/python3 -m venv venv36
curl https://bootstrap.pypa.io/get-pip.py | venv36/bin/python3
WHL=${REPO_ROOT}/wheels/google_crc32c-0.0.1-cp36-cp36m-macosx_10_9_x86_64.whl
venv36/bin/pip install ${WHL}
venv36/bin/python ${REPO_ROOT}/scripts/check_cffi_crc32c.py
${LISTDEPS_CMD} ${WHL}
rm -fr venv36

${PYTHON37}/python3 -m venv venv37
curl https://bootstrap.pypa.io/get-pip.py | venv37/bin/python3
WHL=${REPO_ROOT}/wheels/google_crc32c-0.0.1-cp37-cp37m-macosx_10_9_x86_64.whl
venv37/bin/pip install ${WHL}
venv37/bin/python ${REPO_ROOT}/scripts/check_cffi_crc32c.py
${LISTDEPS_CMD} ${WHL}
rm -fr venv37

# TODO: As of 2019-Dec-30, 3.8 is not available on our CI
# ${PYTHON38}/python3 -m venv venv38
# curl https://bootstrap.pypa.io/get-pip.py | venv38/bin/python3
# WHL=${REPO_ROOT}/wheels/google_crc32c-0.0.1-cp38-cp38m-macosx_10_9_x86_64.whl
# venv37/bin/pip install ${WHL}
# venv37/bin/python ${REPO_ROOT}/scripts/check_cffi_crc32c.py
# ${LISTDEPS_CMD} ${WHL}
# rm -fr venv38
