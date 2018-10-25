#!/bin/bash
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

# ``readlink -f`` is not our friend on OS X. This relies on **some**
# ``python`` being installed.
SCRIPT_FI=$(python -c "import os; print(os.path.realpath('${0}'))")
OSX_DIR=$(dirname ${SCRIPT_FI})
SCRIPTS_DIR=$(dirname ${OSX_DIR})
export REPO_ROOT=$(dirname ${SCRIPTS_DIR})

# NOTE: These are the Python.org versions of Python.
PYTHON27="/Library/Frameworks/Python.framework/Versions/2.7/bin"
PYTHON35="/Library/Frameworks/Python.framework/Versions/3.5/bin"
PYTHON36="/Library/Frameworks/Python.framework/Versions/3.6/bin"
PYTHON37="/Library/Frameworks/Python.framework/Versions/3.7/bin"

# Make sure we have an updated `pip`.
${PYTHON37}/python3 -m pip install --upgrade pip
# Make sure virtualenv and delocate.
${PYTHON37}/python3 -m pip install --upgrade delocate virtualenv
LISTDEPS_CMD="${PYTHON37}/delocate-listdeps --all --depending"
VIRTUALENV_CMD="${PYTHON37}/python3 -m virtualenv"

# Create Python 2.7 virtual environment and check.
WHL=${REPO_ROOT}/py_crc32c-0.0.1-cp27-cp27m-macosx_10_6_intel.whl
${VIRTUALENV_CMD} --python=${PYTHON27}/python2 venv27
venv27/bin/pip install ${WHL}
venv27/bin/python ${REPO_ROOT}/check_cffi_crc32c.py
${LISTDEPS_CMD} ${WHL}
rm -fr venv27

${VIRTUALENV_CMD} --python=${PYTHON35}/python3 venv35
WHL=${REPO_ROOT}/py_crc32c-0.0.1-cp35-cp35m-macosx_10_6_intel.whl
venv35/bin/pip install ${WHL}
venv35/bin/python ${REPO_ROOT}/check_cffi_crc32c.py
${LISTDEPS_CMD} ${WHL}
rm -fr venv35

${VIRTUALENV_CMD} --python=${PYTHON36}/python3 venv36
WHL=${REPO_ROOT}/py_crc32c-0.0.1-cp36-cp36m-macosx_10_6_intel.whl
venv36/bin/pip install ${WHL}
venv36/bin/python ${REPO_ROOT}/check_cffi_crc32c.py
${LISTDEPS_CMD} ${WHL}
rm -fr venv36

${VIRTUALENV_CMD} --python=${PYTHON37}/python3 venv37
WHL=${REPO_ROOT}/py_crc32c-0.0.1-cp37-cp37m-macosx_10_6_intel.whl
venv37/bin/pip install ${WHL}
venv37/bin/python ${REPO_ROOT}/check_cffi_crc32c.py
${LISTDEPS_CMD} ${WHL}
rm -fr venv37
