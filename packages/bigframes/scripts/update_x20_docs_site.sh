#!/bin/bash
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

################################################################################
# This script uses corp credentials to sync the files to x20.
# Make sure you:
# 1. Have write permission to /x20/teams/bigframes-swe
# 2. Have run `gcert` before running the script
################################################################################

set -e -o pipefail
set -x

GIT_DOCS_DIR=docs/_build/html/
X20_BIGFRAMES_DIR=/x20/teams/bigframes-swe/bigframes/docs
MAX_BACKFILL=10
REQ_PYTHON_VERSION=3.9

# Create a temporary directory
tempdir=`mktemp --directory --tmpdir bigframes.XXXXXXXXXX`

# Clone the repository
git clone sso://team/bigquery-query-swe/bigframes ${tempdir}

# Enter the temporary bigframes directory
pushd ${tempdir}

# Python version 3.9 is required to build bigframes docs, install if not present
if ! python3 --version | grep ${REQ_PYTHON_VERSION}; then
    # Install pyenv to install the required python version
    ## https://github.com/pyenv/pyenv#basic-github-checkout
    git clone https://github.com/pyenv/pyenv.git .pyenv
    pushd .pyenv && src/configure && make -C src && popd

    ## https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv
    export PYENV_ROOT=${PWD}/.pyenv
    PATH=${PYENV_ROOT}/bin:${PATH}
    eval "$(pyenv init -)"

    ## Install the required python version
    pyenv install ${REQ_PYTHON_VERSION}

    ## Make the required python version available
    pyenv global ${REQ_PYTHON_VERSION}
fi

# Create a virtual environment with nox installed
python3 -m venv venv
source venv/bin/activate
pip install nox

# i = 0 means docs for the latest version, and i = 1 onwards means backfill
for i in `seq 0 ${MAX_BACKFILL}`; do
    # If it is backfill turn, back off the version by 1
    if [ ${i} -ne 0 ]; then
        git reset --hard HEAD~1

        # Clean up any old docs
        rm -rf ${GIT_DOCS_DIR}
    fi

    # Construct a docs path in x20
    commit_hash=`git rev-parse --short HEAD`
    x20_docs_dir_commit=${X20_BIGFRAMES_DIR}/${commit_hash}

    # If the x20 docs path already exists, let's assume that it was created
    # properly in the previous attempt
    if fileutil test -d ${x20_docs_dir_commit}; then
        echo ${x20_docs_dir_commit} exists, skipping rebuilding it..
        continue
    fi

    # Build the docs
    echo Building docs for commit ${commit_hash}..
    nox -s docs

    # TODO(shobs): Check if a symlink can be created instead of another copy of
    # the latest commit's docs, using fileutil CLI or otherwise
    x20_docs_dirs=${x20_docs_dir_commit}
    if [ ${i} -eq 0 ]; then
        x20_docs_dirs="${x20_docs_dirs} ${X20_BIGFRAMES_DIR}/latest"
    fi

    for x20_docs_dir in ${x20_docs_dirs}; do
        fileutil mirror -parallelism=4 -force ${GIT_DOCS_DIR} ${x20_docs_dir}
        x20_own request_change --recursive --path=${x20_docs_dir} --new_mode=a+r
    done
done

# Exit the temporary bigframes directory
popd

# Clean up the temporary bigframes directory
rm -rf ${tempdir}
