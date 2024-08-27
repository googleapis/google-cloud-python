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

# Build a **single** Python wheel for a specified version. The version and
# associated paths should be set as environment variables; the expected
# environment variables will be verified below.

set -e -x

# Check that the REPO_ROOT, PY_BIN and PY_TAG environment variables are set.
if [[ -z "${REPO_ROOT}" ]]; then
    echo "REPO_ROOT environment variable should be set by the caller."
    exit 1
fi
if [[ -z "${PY_BIN}" ]]; then
    echo "PY_BIN environment variable should be set by the caller."
    exit 1
fi
if [[ -z "${PY_TAG}" ]]; then
    echo "PY_TAG environment variable should be set by the caller."
    exit 1
fi

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
install_python_pyenv ${PY_BIN}

# Create a virtualenv where we can install Python build dependencies.
VENV=${REPO_ROOT}/venv${PY_BIN}
"python${PY_BIN}" -m venv ${VENV}

curl https://bootstrap.pypa.io/get-pip.py | ${VENV}/bin/python
${VENV}/bin/python -m pip install \
    --requirement ${REPO_ROOT}/scripts/dev-requirements.txt

# Create the wheel.
DIST_WHEELS="${REPO_ROOT}/dist_wheels"
mkdir -p ${DIST_WHEELS}
cd ${REPO_ROOT}
${VENV}/bin/python setup.py build_ext \
    --include-dirs=${REPO_ROOT}/usr/include \
    --library-dirs=${REPO_ROOT}/usr/lib \
    --rpath=${REPO_ROOT}/usr/lib
${VENV}/bin/python -m pip wheel ${REPO_ROOT} --wheel-dir ${DIST_WHEELS}

# Delocate the wheel.
FIXED_WHEELS="${REPO_ROOT}/wheels"
mkdir -p ${FIXED_WHEELS}
${VENV}/bin/delocate-wheel \
    --wheel-dir ${FIXED_WHEELS} \
    --verbose \
    --check-archs \
    ${DIST_WHEELS}/google_crc32c*${PY_TAG}*.whl

if [[ "${PUBLISH_WHEELS}" == "true" ]]; then
    . /${OSX_DIR}/publish_python_wheel.sh
fi

# Clean up.
rm -fr ${DIST_WHEELS}
rm -fr ${VENV}
