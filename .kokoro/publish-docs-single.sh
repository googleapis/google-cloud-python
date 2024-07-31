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

# `-e` enables the script to automatically fail when a command fails
# `-o pipefail` sets the exit code to non-zero if any command fails,
# or zero if all commands in the pipeline exit successfully.
set -eo pipefail

pwd

# build docs
nox -s docs

# create metadata
python3.10 -m docuploader create-metadata \
  --name=$(jq --raw-output '.name // empty' .repo-metadata.json) \
  --version=$(python3.10 setup.py --version) \
  --language=$(jq --raw-output '.language // empty' .repo-metadata.json) \
  --distribution-name=$(python3.10 setup.py --name) \
  --product-page=$(jq --raw-output '.product_documentation // empty' .repo-metadata.json) \
  --github-repository=$(jq --raw-output '.repo // empty' .repo-metadata.json) \
  --issue-tracker=$(jq --raw-output '.issue_tracker // empty' .repo-metadata.json)

cat docs.metadata

# upload docs
python3.10 -m docuploader upload docs/_build/html --metadata-file docs.metadata --staging-bucket "${STAGING_BUCKET}"


# docfx yaml files
nox -s docfx

# create metadata.
python3.10 -m docuploader create-metadata \
  --name=$(jq --raw-output '.name // empty' .repo-metadata.json) \
  --version=$(python3.10 setup.py --version) \
  --language=$(jq --raw-output '.language // empty' .repo-metadata.json) \
  --distribution-name=$(python3.10 setup.py --name) \
  --product-page=$(jq --raw-output '.product_documentation // empty' .repo-metadata.json) \
  --github-repository=$(jq --raw-output '.repo // empty' .repo-metadata.json) \
  --issue-tracker=$(jq --raw-output '.issue_tracker // empty' .repo-metadata.json)

cat docs.metadata

if [[ -d "google/cloud" ]]; then
  # Push google cloud library docs to the Cloud RAD bucket `docs-staging-v2`
  staging_v2_bucket="docs-staging-v2"
else
  # Push non-cloud library docs to `docs-staging-v2-staging` instead of the
  # Cloud RAD bucket `docs-staging-v2`
  staging_v2_bucket="docs-staging-v2-staging"
fi

# upload docs
python3.10 -m docuploader upload docs/_build/html/docfx_yaml --metadata-file docs.metadata --destination-prefix docfx --staging-bucket "${staging_v2_bucket}"
