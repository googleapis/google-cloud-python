#!/bin/bash

set -eo pipefail

cd ${KOKORO_ARTIFACTS_DIR}/github/google-cloud-python
pwd
ls
env

# Kokoro currently uses 3.6.1
pyenv global 3.6.1

# Kokoro exposes this as a file, but the scripts expect just a plain variable.
export GITHUB_TOKEN=$(cat ${KOKORO_GFILE_DIR}/${GITHUB_TOKEN_FILE})

# Add github to known hosts.
ssh-keyscan github.com >> ~/.ssh/known_hosts

# Activate the ssh key for dpebot. This is used to clone
# repositories using the ssh:// protocol.
eval `ssh-agent -s`
chmod 600 ${KOKORO_GFILE_DIR}/id_rsa
ssh-add ${KOKORO_GFILE_DIR}/id_rsa

# Install Requirements
pip install --upgrade -r docs/requirements.txt

# Build and Publish Documentation
bash test_utils/scripts/update_docs.sh kokoro
