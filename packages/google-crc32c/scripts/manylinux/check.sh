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

# set up pyenv & shell environment for switching across python versions
eval "$(pyenv init -)"
eval "$(pyenv init --path)"
install_python_pyenv() {
    version=$1

    if [ -z "$(pyenv versions --bare | grep $version)" ]; then
        echo "Python $version is not installed. Installing..."
        pyenv install $version
        echo "Python $version installed."
    else
        echo "Python $version is already installed."
    fi
    pyenv shell $version
}

SUPPORTED_PYTHON_VERSIONS=("3.9" "3.10" "3.11" "3.12")

for PYTHON_VERSION in "${SUPPORTED_PYTHON_VERSIONS[@]}"; do
    PYTHON=python${PYTHON_VERSION}
    install_python_pyenv ${PYTHON_VERSION}
    ${PYTHON} -m pip install --upgrade setuptools pip wheel

    # Create a virtual environment.
    ${PYTHON} -m venv venv

    # Install the wheel.
    WHEEL_FILE="wheels/google_crc32c-${PACKAGE_VERSION}-cp${PYTHON_VERSION//.}-cp${PYTHON_VERSION//.}-manylinux_2_17_x86_64.manylinux2014_x86_64.whl"
    venv/bin/pip install ${WHEEL_FILE}

    # Verify that the module is installed and peek at contents.
    venv/bin/python scripts/check_crc32c_extension.py
    unzip -l ${WHEEL_FILE}

    # Clean up.
    rm -fr venv/
done
