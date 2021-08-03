#!/bin/bash
# Copyright 2021 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd


# A customized test runner for samples.
#
# For periodic builds, you can specify this file for testing against head.

# `-e` enables the script to automatically fail when a command fails
# `-o pipefail` sets the exit code to the rightmost comment to exit with a non-zero
set -eo pipefail
# Enables `**` to include files nested inside sub-folders
shopt -s globstar

cd github/python-spanner-django

exec .kokoro/test-samples-impl.sh
