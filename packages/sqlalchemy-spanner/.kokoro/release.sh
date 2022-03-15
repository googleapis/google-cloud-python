#!/bin/bash
# Copyright 2021 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

set -eo pipefail

# Start the releasetool reporter
python3 -m pip install gcp-releasetool
python3 -m releasetool publish-reporter-script > /tmp/publisher-script; source /tmp/publisher-script

# Ensure that we have the latest versions of Twine, Wheel, and Setuptools.
python3 -m pip install --upgrade twine wheel setuptools

# Disable buffering, so that the logs stream through.
export PYTHONUNBUFFERED=1

# Move into the package, build the distribution and upload.
TWINE_PASSWORD=$(cat "${KOKORO_KEYSTORE_DIR}/73713_google-cloud-pypi-token-keystore-1")
cd github/python-spanner-sqlalchemy
python3 setup.py sdist bdist_wheel
twine upload --username __token__ --password "${TWINE_PASSWORD}" dist/*
