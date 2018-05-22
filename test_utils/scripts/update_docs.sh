#!/bin/bash

# Copyright 2016 Google LLC
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

GH_OWNER='GoogleCloudPlatform'
GH_PROJECT_NAME='google-cloud-python'

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Function to build the docs.
function build_docs {
    rm -rf docs/_build/
    rm -rf docs/bigquery/generated
    sphinx-build -W -b html -d docs/_build/doctrees docs/ docs/_build/html/
    return $?
}

# Only update docs if we are on CircleCI.
if [[ "${CIRCLE_BRANCH}" == "master" ]] && [[ -z "${CIRCLE_PR_NUMBER}" ]]; then
    echo "Building new docs on a merged commit."
elif [[ -n "${CIRCLE_TAG}" ]]; then
    echo "Building new docs on a tag (but will not deploy)."
    build_docs
    exit $?
else
    echo "Not on master nor a release tag."
    echo "Building new docs for testing purposes, but not deploying."
    build_docs
    exit $?
fi

