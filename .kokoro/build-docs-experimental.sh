#!/bin/bash

set -eo pipefail

# TODO: Get package from environment variable.
PACKAGE="websecurityscanner"

# Kokoro currently uses 3.6.1
pyenv global 3.6.1

cd ${KOKORO_ARTIFACTS_DIR}/github/google-cloud-python

# Install Requirements
pip install --upgrade -r docs/requirements.txt

cd ${KOKORO_ARTIFACTS_DIR}/github/google-cloud-python/${PACKAGE}

VERSION=$(python ${KOKORO_ARTIFACTS_DIR}/github/google-cloud-python/test_utils/scripts/get_package_version.py .)

# Build documentation
function build_docs {
    rm -rf docs/_build/
    # -W -> warnings as errors
    # -T -> show full traceback on exception
    # -N -> no color
    sphinx-build \
        -W -T -N \
        -b html \
        -d docs/_build/doctrees \
        docs/ \
        docs/_build/html/
    return $?
}

build_docs

# Run the GOB cookie daemon
git clone https://gerrit.googlesource.com/gcompute-tools ${KOKORO_ARTIFACTS_DIR}/gcompute-tools
${KOKORO_ARTIFACTS_DIR}/gcompute-tools/git-cookie-authdaemon

# Clone Git-on-Borg docs repository
git clone https://devrel.googlesource.com/cloud-docs/library-reference-docs

cd library-reference-docs

# Set up remote to use cookie and bypass gerrit
git remote add direct https://devrel.googlesource.com/_direct/cloud-docs/library-reference-docs

# Copy docmentation
mkdir -p python/${PACKAGE}/${VERSION}
cp -R ../docs/_build/html/* python/${PACKAGE}/${VERSION}

# Update the files
git add .
git status
git commit -m "Publish documentation for ${PACKAGE} v${VERSION}"
git push direct master
