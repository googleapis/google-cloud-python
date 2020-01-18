#!/bin/bash

set -eo pipefail


if [ "$(uname)" == "Darwin" ]; then
    # Mac OS
    PYTHON_BIN=/Library/Frameworks/Python.framework/Versions/3.7/bin
    PYTHON=${PYTHON_BIN}/python3

    RELEASETOOL=~/Library/Python/3.7/bin/releasetool
    TWINE=~/Library/Python/3.7/bin/twine
    ${PYTHON} -m pip install gcp-releasetool twine --user

else
    # Kokoro Linux

    # add python3 to path, used by tooling
    PATH=/opt/python/cp38-cp38/bin:$PATH
    mv /keys/73713_google_cloud_pypi_password /73713_google_cloud_pypi_password 

    PYTHON_BIN=/opt/python/cp38-cp38/bin
    RELEASETOOL=${PYTHON_BIN}/releasetool
    PYTHON=${PYTHON_BIN}/python
    TWINE=${PYTHON_BIN}/twine
    ${PYTHON} -m pip install gcp-releasetool twine

    ls ${PYTHON_BIN}


    echo "Change to code directory"
    cd /var/code/python-crc32c/
fi


# Start the releasetool reporter
${RELEASETOOL} publish-reporter-script > /tmp/publisher-script; source /tmp/publisher-script

# Ensure that we have the latest versions of Twine, Wheel, and Setuptools.
${PYTHON} -m pip install --upgrade twine wheel setuptools --user

# Disable buffering, so that the logs stream through.
export PYTHONUNBUFFERED=1

# Move into the package, build the distribution and upload.
TWINE_PASSWORD=$(cat "${KOKORO_KEYSTORE_DIR}/73713_google_cloud_pypi_password")
${PYTHON} setup.py sdist
${TWINE} upload --skip-existing --username gcloudpypi --password "${TWINE_PASSWORD}" dist/* wheels/*
