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

PY_BIN="python3.7"

# Check that the REPO_ROOT variable is set.
if [[ -z "${REPO_ROOT}" ]]; then
    echo "REPO_ROOT environment variable should be set by the caller."
    exit 1
fi

CRC32C_INSTALL_PREFIX=${REPO_ROOT}/usr

# NOTE: This assumes the local install has an up-to-date `pip`.
# Create a virtualenv where we can install `cmake`.
${PY_BIN} -m pip install --upgrade virtualenv
VENV=${REPO_ROOT}/venv
${PY_BIN} -m virtualenv ${VENV}
${VENV}/bin/python -m pip install "cmake >= 3.12.0"
# Build `libcrc32c`
cd ${REPO_ROOT}/crc32c
mkdir build
cd build/
${VENV}/bin/cmake \
    -DCRC32C_BUILD_TESTS=no \
    -DCRC32C_BUILD_BENCHMARKS=no \
    -DBUILD_SHARED_LIBS=yes \
    -DCMAKE_INSTALL_PREFIX:PATH=${CRC32C_INSTALL_PREFIX} \
    ..
# Install `libcrc32c` into CRC32C_INSTALL_PREFIX.
make all install

# Clean up.
rm -fr ${REPO_ROOT}/crc32c/build
rm -fr ${VENV}
