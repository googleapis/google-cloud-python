#!/bin/bash

set -ev

# If merging to master and not a pull request, update docs.
if [ "${TRAVIS_BRANCH}" == "master" ] && [ "${TRAVIS_PULL_REQUEST}" == "false" ]; then
  # Generate new set of json files in docs/json/master.
  tox -e docs
  git submodule add -b gh-pages https://${GH_OAUTH_TOKEN}@github.com/${GH_OWNER}/${GH_PROJECT_NAME} ghpages
  cp -R docs/_build/html/* ghpages/
  cd ghpages
  git add .
  # Commit to gh-pages branch to apply changes.
  git config user.name "selfiebot"
  git commit -m "Update docs after merge to master."
  git push https://${GH_OAUTH_TOKEN}@github.com/${GH_OWNER}/${GH_PROJECT_NAME} HEAD:gh-pages
fi
