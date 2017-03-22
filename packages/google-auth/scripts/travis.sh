#!/bin/bash

# Copyright 2015 Google Inc. All rights reserved.
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

set -eo pipefail

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT=$( dirname "$DIR" )

# Work from the project root.
cd $ROOT

# Decrypt secrets and run system tests if not on an external PR.
if [[ -n $SYSTEM_TEST ]]; then
    if [[ $TRAVIS_SECURE_ENV_VARS == "true" ]]; then
        echo 'Extracting secrets.'
        scripts/decrypt-secrets.sh "$SECRETS_PASSWORD"
        # Prevent build failures from leaking our password.
        # looking at you, Tox.
        export SECRETS_PASSWORD=""
    else
        # This is an external PR, so just mark system tests as green.
        echo 'In system test but secrets are not available, skipping.'
        exit 0
    fi
fi

# Run tox.
echo "Running tox..."
tox

# Run tox for sub-packages.
if [[ $TOXENV != "docs"  && -z $SYSTEM_TEST ]]; then
    echo "Running tox for google_auth_httplib2..."
    cd additional_packages/google_auth_httplib2
    # --workdir is specified to avoid path names being too long, which
    # causes subprocess calls to hit the execve character limit.
    # See https://github.com/pypa/virtualenv/issues/596
    tox --workdir ~/.tox-httplib2
    cd $ROOT
    echo "Running tox for google_auth_oauthlib..."
    cd additional_packages/google_auth_oauthlib
    tox --workdir  ~/.tox-oauthlib
fi
