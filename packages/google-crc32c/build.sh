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

PYTHON_BIN="/opt/python/cp37-cp37m/bin"
PKG_NAME="py_crc32c"

# Upgrade `pip` before using it.
${PYTHON_BIN}/python -m pip install --upgrade pip
# Install `cmake` and `cffi`
# See: https://github.com/pypa/auditwheel/issues/102
${PYTHON_BIN}/python -m pip install --upgrade \
  auditwheel cmake cffi "wheel != 0.32.*"

# Build and install `crc32c`
cd /var/code/py-crc32c/crc32c/
mkdir build
cd build/
${PYTHON_BIN}/cmake \
  -DCRC32C_BUILD_TESTS=0 \
  -DCRC32C_BUILD_BENCHMARKS=0 \
  -DBUILD_SHARED_LIBS=yes \
  ..
make all install

# Build the package.
cd /var/code/py-crc32c/
${PYTHON_BIN}/python -m pip wheel . -w dist_wheels/

# Bundle external shared libraries into the wheels
for whl in dist_wheels/${PKG_NAME}*.whl; do
    ${PYTHON_BIN}/auditwheel repair "${whl}" -w .
done

# Clean up.
rm -fr /var/code/py-crc32c/crc32c/build/
rm -fr /var/code/py-crc32c/dist_wheels/
