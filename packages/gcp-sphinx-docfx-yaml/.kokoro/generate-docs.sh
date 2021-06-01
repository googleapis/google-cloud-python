#!/bin/bash
# Copyright 2021 Google LLC
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

set -eo pipefail

# Disable buffering, so that the logs stream through.
export PYTHONUNBUFFERED=1

export PATH="${HOME}/.local/bin:${PATH}"

# Install dependencies.
python3 -m pip install --user --quiet --upgrade nox
python3 -m pip install --user gcp-docuploader

# Retrieve unique repositories to regenerate the YAML with.
for bucket_item in $(gsutil ls 'gs://docs-staging-v2/docfx-python*' | sort -u -t- -k5,5); do

  # Retrieve the GitHub Repository info.
  gsutil cp ${bucket_item} .
  tarball=$(echo ${bucket_item} | cut -d "/" -f 4)
  tar -xf ${tarball} docs.metadata
  repo=$(cat docs.metadata | grep "github_repository:" | cut -d "\"" -f 2 | cut -d "/" -f 2)

  echo "cloning ${repo}..."
  git clone https://github.com/googleapis/${repo}.git

  # Clean up resources we don't need anymore.
  rm ${tarball}
  rm docs.metadata

  # For each repo, process docs and docfx jobs to regenerate the YAML.
  cd ${repo}

  if [ ${FORCE_GENERATE_ALL_TAGS} = "true" ]; then
    # Grabs all tags from the repository
    GITHUB_TAGS=$(git tag --sort=-v:refname)
  else
    # Grab the latest released tag
    GITHUB_TAGS=$(git describe --tags `git rev-list --tags --max-count=1`)
  fi

  # TODO: allow skipping failing docs builds and continue with the rest of the generation.
  for tag in ${GITHUB_TAGS}; do
    git checkout ${tag}

    # TODO: support building all googleapis.dev docs through an environmental variable option passed.
    ## Build HTML docs for googleapis.dev.
    # nox -s docs

    # python3 -m docuploader create-metadata \
    #  --name=$(jq --raw-output '.name // empty' .repo-metadata.json) \
    #  --version=$(python3 setup.py --version) \
    #  --language=$(jq --raw-output '.language // empty' .repo-metadata.json) \
    #  --distribution-name=$(python3 setup.py --name) \
    #  --product-page=$(jq --raw-output '.product_documentation // empty' .repo-metadata.json) \
    #  --github-repository=$(jq --raw-output '.repo // empty' .repo-metadata.json) \
    #  --issue-tracker=$(jq --raw-output '.issue_tracker // empty' .repo-metadata.json)

    # cat docs.metadata

    ## upload docs
    # python3 -m docuploader upload docs/_build/html --metadata-file docs.metadata --staging-bucket "${STAGING_BUCKET}"


    # Build YAML tarballs for Cloud-RAD.
    nox -s docfx

    python3 -m docuploader create-metadata \
      --name=$(jq --raw-output '.name // empty' .repo-metadata.json) \
      --version=$(python3 setup.py --version) \
      --language=$(jq --raw-output '.language // empty' .repo-metadata.json) \
      --distribution-name=$(python3 setup.py --name) \
      --product-page=$(jq --raw-output '.product_documentation // empty' .repo-metadata.json) \
      --github-repository=$(jq --raw-output '.repo // empty' .repo-metadata.json) \
      --issue-tracker=$(jq --raw-output '.issue_tracker // empty' .repo-metadata.json)

    cat docs.metadata

    # upload docs
    python3 -m docuploader upload docs/_build/html/docfx_yaml --metadata-file docs.metadata --destination-prefix docfx --staging-bucket "${V2_STAGING_BUCKET}"
  done
  
  # Clean up the repository to make room.
  cd ../
  rm -rf ${repo} 
done
