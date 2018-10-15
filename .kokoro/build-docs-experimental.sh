#!/bin/bash

set -eo pipefail

cd ${KOKORO_ARTIFACTS_DIR}/github/google-cloud-python
pwd
ls
env

# Kokoro currently uses 3.6.1
pyenv global 3.6.1

# Install Requirements
pip install --upgrade -r docs/requirements.txt

# Function to build the docs.
function build_docs {
    rm -rf docs/_build/
    rm -rf docs/bigquery/generated
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
git clone https://gerrit.googlesource.com/gcompute-tools $KOKORO_ARTIFACTS_DIR/gcompute-tools
$KOKORO_ARTIFACTS_DIR/gcompute-tools/git-cookie-authdaemon

# Clone Git-on-Borg docs repository
git clone https://devrel.googlesource.com/cloud-docs/library-reference-docs

cd library-reference-docs

# Set up remote to use cookie and bypass gerrit
git remote add direct https://devrel.googlesource.com/_direct/cloud-docs/library-reference-docs

cp -R ../docs/_build/html/* latest/

# Update the files
git add .
git status

# If there are no changes, just exit cleanly.
if [[ -z "$(git status --porcelain)" ]]; then
    echo "Nothing to commit. Exiting without pushing changes."
    exit
fi

git commit -m "Update docs"

git push direct master
