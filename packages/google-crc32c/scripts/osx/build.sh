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
echo "BUILDING FOR OSX"

# ``readlink -f`` is not our friend on OS X. This relies on **some**
# ``python`` being installed.
SCRIPT_FI=$(python -c "import os; print(os.path.realpath('${0}'))")
OSX_DIR=$(dirname ${SCRIPT_FI})
SCRIPTS_DIR=$(dirname ${OSX_DIR})
export REPO_ROOT=$(dirname ${SCRIPTS_DIR})

# NOTE: These are the Python.org versions of Python.
PYTHON36="/Library/Frameworks/Python.framework/Versions/3.6/bin"
PYTHON37="/Library/Frameworks/Python.framework/Versions/3.7/bin"
PYTHON38="/Library/Frameworks/Python.framework/Versions/3.8/bin"
PYTHON39="/Library/Frameworks/Python.framework/Versions/3.9/bin"

# Build and install `libcrc32c`
export PY_BIN="python3"
export CRC32C_INSTALL_PREFIX="${REPO_ROOT}/usr"

cd ${REPO_ROOT}
git submodule update --init --recursive

${OSX_DIR}/build_c_lib.sh

# Build wheel for Python 3.6.
export PY_BIN="python3.6"
export PY_TAG="cp36-cp36m"
${OSX_DIR}/build_python_wheel.sh

# Build wheel for Python 3.7.
export PY_BIN="python3.7"
export PY_TAG="cp37-cp37m"
${OSX_DIR}/build_python_wheel.sh

# Build wheel for Python 3.8.
# Note that the 'm' SOABI flag is no longer supported for Python >= 3.8
export PY_BIN="python3.8"
export PY_TAG="cp38-cp38"
${OSX_DIR}/build_python_wheel.sh

# TODO: As of 2020-12-11, 3.9 is not available on our CI
# Build wheel for Python 3.9.
#export PY_BIN="python3.9"
#export PY_TAG="cp39-cp39"
#${OSX_DIR}/build_python_wheel.sh


# Clean up.
rm -fr ${CRC32C_INSTALL_PREFIX}
