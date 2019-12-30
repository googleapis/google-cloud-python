#!/bin/bash

set -eo pipefail

# Build for ManyLinux
../scripts/manylinux/build.sh

./release.sh
