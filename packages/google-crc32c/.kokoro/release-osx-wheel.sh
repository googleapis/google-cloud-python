#!/bin/bash

set -eo pipefail

cd github/python-crc32c

# Build for OSX
./scripts/osx/build.sh

./.kokoro/release.sh
