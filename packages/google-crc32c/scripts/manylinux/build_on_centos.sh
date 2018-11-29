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

MAIN_PYTHON_BIN="/opt/python/cp37-cp37m/bin"
PKG_NAME="python-crc32c"

# Upgrade `pip` before using it.
${MAIN_PYTHON_BIN}/python -m pip install --upgrade pip
# Install `cmake` (i.e. non-Python build dependency).
${MAIN_PYTHON_BIN}/python -m pip install "cmake >= 3.12.0"
# Install Python build dependencies.
${MAIN_PYTHON_BIN}/python -m pip install \
    --requirement /var/code/py-crc32c/scripts/dev-requirements.txt

# Build and install `crc32c`
cd /var/code/py-crc32c/crc32c/
mkdir build
cd build/
${MAIN_PYTHON_BIN}/cmake \
    -DCRC32C_BUILD_TESTS=no \
    -DCRC32C_BUILD_BENCHMARKS=no \
    -DBUILD_SHARED_LIBS=yes \
    ..
make all install

# Collect all target Python versions.
VERSION_WHITELIST=""
for PYTHON_BIN in /opt/python/*/bin; do
    # H/T: https://stackoverflow.com/a/229606/1068170
    if [[ "${PYTHON_BIN}" == *"27"* ]]; then
        VERSION_WHITELIST="${VERSION_WHITELIST} ${PYTHON_BIN}"
        continue
    elif [[ "${PYTHON_BIN}" == *"35"* ]]; then
        VERSION_WHITELIST="${VERSION_WHITELIST} ${PYTHON_BIN}"
        continue
    elif [[ "${PYTHON_BIN}" == *"36"* ]]; then
        VERSION_WHITELIST="${VERSION_WHITELIST} ${PYTHON_BIN}"
        continue
    elif [[ "${PYTHON_BIN}" == *"37"* ]]; then
        VERSION_WHITELIST="${VERSION_WHITELIST} ${PYTHON_BIN}"
        continue
    else
        echo "Ignoring unsupported version: ${PYTHON_BIN}"
        echo "====================================="
    fi
done

# Build the wheels.
cd /var/code/py-crc32c/
for PYTHON_BIN in ${VERSION_WHITELIST}; do
    ${PYTHON_BIN}/python -m pip install --upgrade pip
    ${PYTHON_BIN}/python -m pip install \
        --requirement /var/code/py-crc32c/scripts/dev-requirements.txt
    ${PYTHON_BIN}/python -m pip wheel . --wheel-dir dist_wheels/
done

# Bundle external shared libraries into the wheels
for whl in dist_wheels/${PKG_NAME}*.whl; do
    ${MAIN_PYTHON_BIN}/auditwheel repair "${whl}" --wheel-dir wheels/
done

# Clean up.
rm -fr /var/code/py-crc32c/crc32c/build/
rm -fr /var/code/py-crc32c/dist_wheels/
