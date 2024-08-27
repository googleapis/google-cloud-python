#!/bin/bash

set -eo pipefail

cd github/python-crc32c

export PUBLISH_WHEELS="true"

# Build and publish ManyLinux wheels
./scripts/manylinux/build.sh
