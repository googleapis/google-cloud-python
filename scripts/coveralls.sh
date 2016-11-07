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

#############################################################
# Only run coveralls during a CircleCI / Travis push build. #
#############################################################
if [[ "${TRAVIS_BRANCH}" == "master" ]] && \
       [[ "${TRAVIS_PULL_REQUEST}" == "false" ]]; then
  echo "Sending coverage report on a Travis merge to master."
elif [[ "${CIRCLECI}" == "true" ]] && \
       [[ "${CIRCLE_BRANCH}" == "master" ]] && \
       [[ "${CI_PULL_REQUEST}" == "" ]]; then
  echo "Sending coverage report on a CircleCI merge to master."
else
  echo "Not on a push build for master, skipping coveralls."
  exit
fi

tox -e coveralls
