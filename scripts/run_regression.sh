#!/bin/bash

set -ev

# If merging to master and not a pull request, run regression test.
if [ "${TRAVIS_BRANCH}" == "master" ] && [ "${TRAVIS_PULL_REQUEST}" == "false" ]; then
  # Convert encrypted key file into decrypted file to be used.
  openssl aes-256-cbc -K $encrypted_a1b222e8c14d_key \
      -iv $encrypted_a1b222e8c14d_iv \
      -in regression/key.p12.enc \
      -out $GCLOUD_TESTS_KEY_FILE -d
  tox -e regression
fi
