#!/bin/bash

# Copyright 2016 Google Inc.
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

GH_OWNER="GoogleCloudPlatform"
GH_PROJECT_NAME="google-cloud-python"

function buildDocs () {
  echo "Building JSON documentation..."
  python scripts/generate_json_docs.py --tag ${1}
  echo "Done building JSON documentation."
}


function pushDocs () {
  echo "Deploying JSON documentation..."
  if [[ ! -d "ghpages" ]]; then
      git submodule add -q -f -b gh-pages https://${GH_OAUTH_TOKEN}@github.com/${GH_OWNER}/${GH_PROJECT_NAME} ghpages
  fi
  mkdir -p ghpages/json/${1}
  cp -R docs/_build/json_build/* ghpages/
  cd ghpages
  git add .
  if [[ -n "$(git status --porcelain)" ]]; then
    git config user.name "travis-ci"
    git config user.email "travis@travis-ci.org"
    git commit -m "Updating docs for ${1}"
    git status
    git push -q https://${GH_OAUTH_TOKEN}@github.com/${GH_OWNER}/${GH_PROJECT_NAME} HEAD:gh-pages
  else
    echo "Nothing to commit."
  fi
  cd ..

  echo "Done deploying JSON documentation."
}

function cleanSubmodule () {
    echo "Cleaning up!"
    git submodule deinit -q -f ghpages
    git reset HEAD .gitmodules
    git reset HEAD ghpages
    rm -rf ghpages
    rm -f .gitmodules
    rm -rf .git/modules/ghpages
    echo "Done cleaning up!"
}

# Run this to verifiy that the docs build successfully.
DOC_VERSION='master'
if [[ ! -z ${TRAVIS_TAG} ]]; then
  DOC_VERSION=${TRAVIS_TAG}
else
  DOC_VERSION=${TRAVIS_BRANCH}
fi

buildDocs ${DOC_VERSION}

if [ "${TRAVIS_BRANCH}" == "master" ] && [ "${TRAVIS_PULL_REQUEST}" == "false" ]; then
  pushDocs ${DOC_VERSION}
  cleanSubmodule
  echo "Done pushing docsite. See: https://googlecloudplatform.github.io/google-cloud-python/"
fi

if [[ ! -z ${TRAVIS_TAG} ]]; then
  pushDocs ${DOC_VERSION}
  cleanSubmodule
  echo "Done pushing docsite. See: https://googlecloudplatform.github.io/google-cloud-python/"
fi
