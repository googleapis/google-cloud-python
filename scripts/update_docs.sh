#!/bin/bash

# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -ev

# Adding GitHub pages branch. `git submodule add` checks it
# out at HEAD.
GH_PAGES_DIR="ghpages"
git submodule add -b gh-pages \
    "https://${GH_OAUTH_TOKEN}@github.com/${GH_OWNER}/${GH_PROJECT_NAME}" \
    ${GH_PAGES_DIR}

# Determine if we are building a new tag or are building docs
# for master. Then build new docset in docs/_build from master.
if [[ -z "${TRAVIS_TAG}" ]]; then
    SPHINX_RELEASE=$(git log -1 --pretty=%h) tox -e docs
else
    # Sphinx will use the package version by default.
    tox -e docs
fi

# Get the current version. Assumes the PWD is the root of the git repo.
# We run this after `tox -e docs` to make sure the `docs` env is
# set up.
CURRENT_VERSION=$(.tox/docs/bin/python scripts/get_version.py)

# Update gh-pages with the created docs.
cd ${GH_PAGES_DIR}
if [[ -z "${TRAVIS_TAG}" ]]; then
    git rm -fr master/
    cp -R ../docs/_build/html/ master/
else
    if [[ -d ${CURRENT_VERSION} ]]; then
        echo "The directory ${CURRENT_VERSION} already exists."
        exit 1
    fi
    git rm -fr latest/
    # Put the new release in latest and with the actual version.
    cp -R ../docs/_build/html/ latest/
    cp -R ../docs/_build/html/ "${CURRENT_VERSION}/"

    # Also update the versions file.
    ../.tox/docs/bin/python ../scripts/update_versions.py
    # Update the files which were updated in the release.
    git add versions.html versions.json
fi

# Update the files push to gh-pages.
git add .
git status

# H/T: https://github.com/dhermes
if [[ -z "$(git status --porcelain)" ]]; then
    echo "Nothing to commit. Exiting without pushing changes."
    exit
fi

# Commit to gh-pages branch to apply changes.
git config --global user.email "travis@travis-ci.org"
git config --global user.name "travis-ci"
git commit -m "Update docs after merge to master."
# NOTE: This may fail if two docs updates (on merges to master)
#       happen in close proximity.
git push \
    "https://${GH_OAUTH_TOKEN}@github.com/${GH_OWNER}/${GH_PROJECT_NAME}" \
    HEAD:gh-pages
