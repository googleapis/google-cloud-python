#!/bin/bash
set -e -x
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

if [ -f "$DIR/service_account.json" ]; then
    export GOOGLE_APPLICATION_CREDENTIALS="$DIR/service_account.json"
fi

# Install test requirements
pip install coverage pytest pytest-cov flake8 codecov
pytest -v -m "not local_auth" --cov=pandas_gbq --cov-report xml:/tmp/pytest-cov.xml tests
