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
echo "CHECKING ON LINUX"

VERSION=$(awk "/version \= ([0-9.]+)/" setup.cfg)
PACKAGE_VERSION=${VERSION:10}
WHEEL_FILE="wheels/google_crc32c-${PACKAGE_VERSION}-cp36-cp36m-manylinux1_x86_64.whl"
PYTHON=python3.6

# Using pyenv, set 3.6.1 as a local python version.
# pyenv versions
pyenv local 3.6.1

# Make sure we can create a virtual environment.
${PYTHON} -m pip install --upgrade setuptools pip wheel

# Create a virtual environment.
${PYTHON} -m venv venv

# Install the wheel.
venv/bin/pip install ${WHEEL_FILE}

# Verify that the module is installed and peek at contents.
venv/bin/python scripts/check_cffi_crc32c.py
unzip -l ${WHEEL_FILE}

# Clean up.
rm -fr venv/
