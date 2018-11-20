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

# NOTE: This assumes the host is running Linux.

set -e -x

WHEEL_FILE="wheels/py_crc32c-0.0.1-cp37-cp37m-manylinux1_x86_64.whl"
PYTHON="python3.7"

# Make sure we can create a virtual environment.
${PYTHON} -m pip install --upgrade pip
${PYTHON} -m pip install --upgrade virtualenv wheel

# Create a virtual environment.
${PYTHON} -m virtualenv venv

# Install the wheel.
venv/bin/pip install ${WHEEL_FILE}

# Verify that the module is installed and peek at contents.
venv/bin/python scripts/check_cffi_crc32c.py
unzip -l ${WHEEL_FILE}

# Clean up.
rm -fr venv/
