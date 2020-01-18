#!/bin/bash

set -eo pipefail

cd github/python-crc32c

# Build for ManyLinux
./scripts/manylinux/build.sh

REPO_ROOT=$(pwd)

mkdir ${REPO_ROOT}/../pypi

docker run \
    --rm \
    --interactive \
    --volume ${REPO_ROOT}:/var/code/python-crc32c/ \
    --volume ${KOKORO_KEYSTORE_DIR}:/keys \
    quay.io/pypa/manylinux2010_x86_64 \
    /var/code/python-crc32c/.kokoro/release.sh
