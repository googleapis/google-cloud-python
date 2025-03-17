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

# set deployment target
export MACOSX_DEPLOYMENT_TARGET=12

# ``readlink -f`` is not our friend on OS X. This relies on **some**
# ``python`` being installed.
SCRIPT_FI=$(python -c "import os; print(os.path.realpath('${0}'))")
OSX_DIR=$(dirname ${SCRIPT_FI})
SCRIPTS_DIR=$(dirname ${OSX_DIR})
export REPO_ROOT=$(dirname ${SCRIPTS_DIR})

# install required packages for pyenv
# https://github.com/pyenv/pyenv/wiki#suggested-build-environment
brew install openssl readline sqlite3 xz zlib tcl-tk

# Replace the old version of pyenv with the latest version.
rm -rf /Users/kbuilder/.pyenv
git clone https://github.com/pyenv/pyenv.git /Users/kbuilder/.pyenv

# Build and install `libcrc32c`
export PY_BIN="${PY_BIN:-python3}"
export CRC32C_INSTALL_PREFIX="${REPO_ROOT}/usr"

cd ${REPO_ROOT}
# Add directory as safe to avoid "detected dubious ownership" fatal issue
git config --global --add safe.directory $REPO_ROOT
git config --global --add safe.directory $REPO_ROOT/google_crc32c
git submodule update --init --recursive

${OSX_DIR}/build_c_lib.sh

SUPPORTED_PYTHON_VERSIONS=("3.9" "3.10" "3.11" "3.12" "3.13")

for PYTHON_VERSION in ${SUPPORTED_PYTHON_VERSIONS[@]}; do
    echo "Build wheel for Python ${PYTHON_VERSION}"
    export PY_BIN=$PYTHON_VERSION
    export PY_TAG="cp${PYTHON_VERSION//.}-cp${PYTHON_VERSION//.}"
    . /${OSX_DIR}/build_python_wheel.sh
done

# Clean up.
rm -fr ${CRC32C_INSTALL_PREFIX}
