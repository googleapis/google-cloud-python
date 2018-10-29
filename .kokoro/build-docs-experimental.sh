#!/bin/bash

set -eo pipefail

# Kokoro currently uses 3.6.1
pyenv global 3.6.1

cd ${KOKORO_ARTIFACTS_DIR}/github/google-cloud-python

# Install Requirements
pip install --upgrade -r docs/requirements.txt

PACKAGE_ROOT=${KOKORO_ARTIFACTS_DIR}/github/google-cloud-python/${PACKAGE}
PACKAGE_VERSION=$(python ${KOKORO_ARTIFACTS_DIR}/github/google-cloud-python/test_utils/scripts/get_package_version.py ${PACKAGE_ROOT})
PACKAGE_DOCUMENTATION=${PACKAGE_ROOT}/docs/_build/html

cd ${PACKAGE_ROOT}

rm -rf docs/_build/

# -W -> warnings as errors
# -T -> show full traceback on exception
# -N -> no color
sphinx-build \
    -W -T -N \
    -b html \
    -d docs/_build/doctrees \
    docs/ \
    ${PACKAGE_DOCUMENTATION}

# docs-publisher will push the docs to git-on-borg repo
python ${KOKORO_ARTIFACTS_DIR}/github/google-cloud-python/test_utils/scripts/docs-publisher.py
