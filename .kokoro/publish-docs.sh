#!/bin/bash

set -eo pipefail

# Disable buffering, so that the logs stream through.
export PYTHONUNBUFFERED=1

cd github/google-cloud-python/${PACKAGE}

VERSION=$(python3 setup.py --version)

# Remove old nox
python3.6 -m pip uninstall --yes --quiet nox-automation

# Install nox
python3.6 -m pip install --upgrade --quiet nox
python3.6 -m nox --version

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
python3 -m docuploader upload . --staging-bucket docs-staging