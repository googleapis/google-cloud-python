#!/bin/bash

set -ev

# If we're on Travis, we need to set up the environment.
if [[ "${TRAVIS}" == "true" ]]; then
  # If merging to master and not a pull request, run regression test.
  if [ "${TRAVIS_BRANCH}" == "master" ] && [ "${TRAVIS_PULL_REQUEST}" == "false" ]; then
    echo "Running in Travis during merge, decrypting stored key file."

    # Convert encrypted key file into decrypted file to be used.
    openssl aes-256-cbc -K $encrypted_a1b222e8c14d_key \
        -iv $encrypted_a1b222e8c14d_iv \
        -in regression/key.p12.enc \
        -out $GCLOUD_TESTS_KEY_FILE -d
  else
    echo "Running in Travis during non-merge to master, doing nothing."
    exit
  fi
fi

# Run the regression tests for each tested package.
python regression/run_regression.py --package datastore
