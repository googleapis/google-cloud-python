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

set -e

PYTHON_BIN="/opt/python/cp37-cp37m/bin"

# Upgrade `pip` before using it.
${PYTHON_BIN}/python -m pip install --upgrade pip
# Install `cmake` and `cffi`
${PYTHON_BIN}/python -m pip install --upgrade cmake cffi

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

# Build the CFFI Python extension
cd /var/code/py-crc32c/
${PYTHON_BIN}/python crc32c_build.py

# Make sure it was built.
${PYTHON_BIN}/python check_cffi_crc32c.py

# Clean up.
rm -f /var/code/py-crc32c/_crc32c_cffi.c
rm -f /var/code/py-crc32c/_crc32c_cffi.o
rm -f /var/code/py-crc32c/_crc32c_cffi.cpython-37m-x86_64-linux-gnu.so
rm -fr /var/code/py-crc32c/crc32c/build/
