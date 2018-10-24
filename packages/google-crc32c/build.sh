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
${PYTHON_BIN}/cmake -DCRC32C_BUILD_TESTS=0 -DCRC32C_BUILD_BENCHMARKS=0 ..
make all install

# Build the CFFI Python extension
cd /var/code/py-crc32c/
${PYTHON_BIN}/python crc32c_build.py
