#!/bin/bash
# Copyright (c) 2017 pandas-gbq Authors All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

set -e -x
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

if [ -f "$DIR/service_account.json" ]; then
    export GOOGLE_APPLICATION_CREDENTIALS="$DIR/service_account.json"
fi

# Install test requirements
pip install coverage pytest pytest-cov flake8 codecov google-cloud-testutils
pytest -v -m "not local_auth" --cov=pandas_gbq --cov-report xml:/tmp/pytest-cov.xml tests
