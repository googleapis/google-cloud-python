#!/bin/bash

set -eo pipefail

REPO_ROOT=$(pwd)/github/python-crc32c
cd github/python-crc32c

export PUBLISH_WHEELS="true"

# Build and publish OSX wheels
./scripts/osx/build.sh
