#!/bin/bash

# Copyright 2016 Google LLC
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

set -ev

# If this is not a CircleCI tag, no-op.
if [[ -z "$CIRCLE_TAG" ]]; then
  echo "This is not a release tag. Doing nothing."
  exit 0
fi

# H/T: http://stackoverflow.com/a/246128/1068170
SCRIPT="$(dirname "${BASH_SOURCE[0]}")/get_tagged_package.py"
# Determine the package directory being deploying on this tag.
PKG_DIR="$(python ${SCRIPT})"

# Ensure that we have the latest versions of Twine, Wheel, and Setuptools.
python3 -m pip install --upgrade twine wheel setuptools

# Move into the package, build the distribution and upload.
cd ${PKG_DIR}
python3 setup.py sdist bdist_wheel
twine upload dist/*
