#!/bin/bash
set -e -x
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

# Install dependencies using Pip

if [[ "$PANDAS" == "MASTER" ]]; then
  PRE_WHEELS="https://7933911d6844c6c53a7d-47bd50c35cd79bd838daf386af554a83.ssl.cf2.rackcdn.com";
  pip install --pre --upgrade --timeout=60 -f $PRE_WHEELS pandas;
else
  pip install pandas==$PANDAS
fi

# Install test requirements
pip install coverage pytest pytest-cov flake8 codecov

REQ="ci/requirements-${PYTHON}-${PANDAS}"
pip install -r "$REQ.pip"
pip install -e .

$DIR/run_tests.sh
