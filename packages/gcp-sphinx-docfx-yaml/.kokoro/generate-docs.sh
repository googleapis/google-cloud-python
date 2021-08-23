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

# If running locally, copy a service account file to
# /dev/shm/73713_docuploader_service_account before calling ci/trampoline_v2.sh.
export GOOGLE_APPLICATION_CREDENTIALS=$KOKORO_KEYSTORE_DIR/73713_docuploader_service_account

# Configure Google Cloud SDK to use service account details for gsutil commands.
gcloud auth activate-service-account --key-file ${GOOGLE_APPLICATION_CREDENTIALS}

# Install dependencies.
python3 -m pip install --user --quiet --upgrade nox
python3 -m pip install --user gcp-docuploader
python3 -m pip install -e .
python3 -m pip install recommonmark
# Required for some client libraries:
python3 -m pip install --user django==2.2 ipython

# Retrieve unique repositories to regenerate the YAML with.
for bucket_item in $(gsutil ls 'gs://docs-staging-v2/docfx-python*' | sort -u -t- -k5,5); do

  # Retrieve the GitHub Repository info.
  tarball=$(echo ${bucket_item} | cut -d "/" -f 4)

  # Make temporary directory to extract tarball content.
  mkdir ${tarball}
  cd ${tarball}

  gsutil cp ${bucket_item} .
  tar -zxvf ${tarball}
  repo=$(cat docs.metadata | grep "github_repository:" | cut -d "\"" -f 2 | cut -d "/" -f 2)

  # Clean up the tarball content.
  cd ..
  rm -rf ${tarball}

  # Clone the repository.
  git clone "https://github.com/googleapis/${repo}.git"

  # For each repo, process docs and docfx jobs to regenerate the YAML.
  cd ${repo}

  # Save the noxfile for usage throughout different releases. 
  cp "noxfile.py" ../

  if [[ ${FORCE_GENERATE_ALL_TAGS} == "true" ]]; then
    # Grabs all tags from the repository.
    GITHUB_TAGS=$(git tag --sort=-v:refname)

    # Turn off exit on failures, continue execution.
    set +eo pipefail
  else
    # Grab the latest released tag.
    GITHUB_TAGS=$(git describe --tags `git rev-list --tags --max-count=1`)
  fi

  for tag in ${GITHUB_TAGS}; do
    git checkout ${tag}

    # Use the latest noxfile for all tags.
    cp ../"noxfile.py" .

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

    # Test running with the plugin version locally.
    if [[ "${TEST_PLUGIN}" == "true" ]]; then
      # --no-use-pep517 is required for django-spanner install issue: see https://github.com/pypa/pip/issues/7953
      python3 -m pip install --user --no-use-pep517 -e .[all]
      sphinx-build -T -N -D extensions=sphinx.ext.autodoc,sphinx.ext.autosummary,docfx_yaml.extension,sphinx.ext.intersphinx,sphinx.ext.coverage,sphinx.ext.napoleon,sphinx.ext.todo,sphinx.ext.viewcode,recommonmark -b html -d docs/_build/doctrees/ docs/ docs/_build/html/
      continue
    fi

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
  rm "noxfile.py"
done
