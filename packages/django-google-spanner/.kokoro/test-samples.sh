#!/bin/bash
# Copyright 2021 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd


# The default test runner for samples.
#
# For periodic builds, we rewinds the repo to the latest release, and
# run test-samples-impl.sh.

# `-e` enables the script to automatically fail when a command fails
# `-o pipefail` sets the exit code to the rightmost comment to exit with a non-zero
set -eo pipefail
# Enables `**` to include files nested inside sub-folders
shopt -s globstar

cd github/python-spanner-django

# Run periodic samples tests at latest release
if [[ $KOKORO_BUILD_ARTIFACTS_SUBDIR = *"periodic"* ]]; then
    # preserving the test runner implementation.
    cp .kokoro/test-samples-impl.sh "${TMPDIR}/test-samples-impl.sh"
    echo "--- IMPORTANT IMPORTANT IMPORTANT ---"
    echo "Now we rewind the repo back to the latest release..."
    LATEST_RELEASE=$(git describe --abbrev=0 --tags)
    git checkout $LATEST_RELEASE
    echo "The current head is: "
    echo $(git rev-parse --verify HEAD)
    echo "--- IMPORTANT IMPORTANT IMPORTANT ---"
    # move back the test runner implementation if there's no file.
    if [ ! -f .kokoro/test-samples-impl.sh ]; then
	cp "${TMPDIR}/test-samples-impl.sh" .kokoro/test-samples-impl.sh
    fi
fi

exec .kokoro/test-samples-impl.sh
