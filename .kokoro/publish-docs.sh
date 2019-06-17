#!/bin/bash

set -eo pipefail

# Disable buffering, so that the logs stream through.
export PYTHONUNBUFFERED=1

cd github/google-cloud-python/${PACKAGE}

VERSION=$(python3 ../test_utils/scripts/get_package_version.py)

# build docs
nox -s docs

cd docs/_build/html

python3 -m pip install gcp-docuploader

# create metadata
python3 -m docuploader create-metadata \
--name ${NAME} \
--version ${VERSION} \
--language python

# upload docs
python3 -m docuploader upload . \
--credentials ${CREDENTIALS} \
--staging-bucket ${STAGING_BUCKET}
