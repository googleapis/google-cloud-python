#!/bin/bash
# Copyright (c) 2017 pandas-gbq Authors All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

set -e -x
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

eval "$(micromamba shell hook --shell=bash)"
micromamba activate

# Install dependencies using (micro)mamba
# https://github.com/mamba-org/micromamba-docker
REQ="ci/requirements-${PYTHON}-${PANDAS}"
micromamba install -q pandas=$PANDAS python=${PYTHON} -c conda-forge;
micromamba install -q --file "$REQ.conda" -c conda-forge;
micromamba list
micromamba info

python setup.py develop --no-deps

# Run the tests
$DIR/run_tests.sh
