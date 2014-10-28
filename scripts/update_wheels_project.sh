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

#########################################
# Settings for specific wheels project. #
#########################################
WHEELS_PROJECT_NAME="gcloud-python-wheels"
# "gcloud-python-wheels" is already used by .travis.yml
FRESH_REPO_DIR="gcloud-python-wheels-fresh"

###################################
# Checkout the wheels repository. #
###################################
git config --global user.email "travis@travis-ci.org"
git config --global user.name "travis-ci"
git clone --quiet --branch=master \
    "https://${GH_OAUTH_TOKEN}@github.com//${GH_OWNER}/${WHEELS_PROJECT_NAME}" \
    ${FRESH_REPO_DIR}
# NOTE: Assumes ${GH_OAUTH_TOKEN} and ${GH_OWNER} are set in Travis build
#       settings for project. This also assumes the wheels project is owned by
#       ${GH_OWNER} and that the token can be used to make commits.

#################################################
# Add the current commit hash to a static file. #
#################################################
echo "${TRAVIS_COMMIT}" > ${FRESH_REPO_DIR}/LATEST_COMMIT

##############################################
# Display git status and push LATEST_COMMIT. #
##############################################
cd ${FRESH_REPO_DIR}
git add LATEST_COMMIT

git status
# H/T: http://stackoverflow.com/a/13730477/1068170
git commit -m "Latest wheels build by travis-ci. [ci skip]"
git status
git push origin master
