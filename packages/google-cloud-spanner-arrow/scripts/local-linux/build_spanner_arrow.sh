#!/bin/bash
# Copyright 2026 Google LLC
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

PY_BIN=${PY_BIN:-python3.12}
REPO_ROOT=${REPO_ROOT:-$(pwd)}

VENV=${REPO_ROOT}/venv
${PY_BIN} -m venv ${VENV}
${VENV}/bin/python -m pip install --upgrade setuptools pip wheel
${VENV}/bin/python -m pip install --requirement ${REPO_ROOT}/scripts/dev-requirements.txt

cd ${REPO_ROOT}
${VENV}/bin/python -m pip wheel . --wheel-dir=wheels

rm -fr ${VENV}
