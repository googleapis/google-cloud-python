#!/bin/bash

set -e

function pushDocs () {

  PYTHONPATH=_testing python scripts/generate_json_docs.py --tag ${1}

  if [[ ! -d "ghpages" ]]; then
      git submodule add -f -b gh-pages https://${GH_OAUTH_TOKEN}@github.com/${GH_OWNER}/${GH_PROJECT_NAME} ghpages
  fi
  mkdir -p ghpages/json/${1}
  cp -R docs/_build/json/${1}/* ghpages/json/${1}
  cp docs/json/toc.json ghpages/json/${1}
  cp docs/json/index.json ghpages/json/${1}
  cp docs/json/overview.html ghpages/json/${1}
  cp docs/json/home.html ghpages/json/
  cp -R docs/json/src ghpages
  cp docs/json/manifest.json ghpages
  cp docs/json/index.html ghpages
  cd ghpages
  git add .
  if [[ -n "$(git status --porcelain)" ]]; then
    git config user.name "travis-ci"
    git config user.email "travis@travis-ci.org"
    git commit -m "Updating docs for ${1}"
    git status
    git push https://${GH_OAUTH_TOKEN}@github.com/${GH_OWNER}/${GH_PROJECT_NAME} HEAD:gh-pages
  else
    echo "Nothing to commit."
  fi
  cd ..
}

function cleanSubmodule () {
    echo "Cleaning up..."
    git submodule deinit -f ghpages
    git reset HEAD .gitmodules
    git reset HEAD ghpages
    rm -rf ghpages
    rm -f .gitmodules
    rm -rf .git/modules/ghpages
}

if [ "${TRAVIS_BRANCH}" == "master" ] && [ "${TRAVIS_PULL_REQUEST}" == "false" ]; then
  pushDocs $TRAVIS_BRANCH
  cleanSubmodule
  echo "Done pushing docsite. See: https://googlecloudplatform.github.io/gcloud-python/"
fi

if [[ ! -z $TRAVIS_TAG ]]; then
  pushDocs $TRAVIS_TAG
  cleanSubmodule
  echo "Done pushing docsite. See: https://googlecloudplatform.github.io/gcloud-python/"
fi
