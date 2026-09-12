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
echo "BUILDING ON LINUX"
export BUILD_PYTHON=${BUILD_PYTHON}

MANYLINUX_DIR=$(echo $(cd $(dirname ${0}); pwd))
SCRIPTS_DIR=$(dirname ${MANYLINUX_DIR})
REPO_ROOT=$(dirname ${SCRIPTS_DIR})

cd $REPO_ROOT
git config --global --add safe.directory '*'

docker pull quay.io/pypa/manylinux2014_x86_64
docker run \
    --rm \
    --interactive \
    --volume ${REPO_ROOT}:/var/code/spanner-arrow/ \
    --env BUILD_PYTHON=${BUILD_PYTHON} \
    quay.io/pypa/manylinux2014_x86_64 \
    /var/code/spanner-arrow/scripts/manylinux/build_on_centos.sh

docker run --rm --privileged hypriot/qemu-register || true
docker pull quay.io/pypa/manylinux2014_aarch64 || true
docker run \
    --rm \
    --interactive \
    --volume ${REPO_ROOT}:/var/code/spanner-arrow/ \
    --env BUILD_PYTHON=${BUILD_PYTHON} \
    quay.io/pypa/manylinux2014_aarch64 \
    /var/code/spanner-arrow/scripts/manylinux/build_on_centos.sh || true

if [[ "${PUBLISH_WHEELS}" == "true" ]]; then
    . /${MANYLINUX_DIR}/publish_python_wheel.sh
fi
