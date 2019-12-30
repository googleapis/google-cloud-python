#!/bin/bash

set -eo pipefail

# Build for OSX
../scripts/osx/build.sh

./release.sh
