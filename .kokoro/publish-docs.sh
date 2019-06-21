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

python3 -m pip install gcp-docuploader

# create metadata
python3 -m docuploader create-metadata \
  --name=$(cat .repo-metadata.json | json name) \
  --version=$(cat package.json | json version) \
  --language=$(cat .repo-metadata.json | json language) \
  --distribution-name=$(cat .repo-metadata.json | json distribution_name) \
  --product-page=$(cat .repo-metadata.json | json product_documentation) \
  --github-repository=$(cat .repo-metadata.json | json repo) \
  --issue-tracker=$(cat .repo-metadata.json | json issue_tracker)

# upload docs
python3 -m docuploader upload docs/_build/html --staging-bucket test-docs-staging