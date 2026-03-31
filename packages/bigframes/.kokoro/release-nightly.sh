#!/bin/bash
# Copyright 2020 Google LLC
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

# Based loosely on
# https://github.com/googleapis/python-bigquery/blob/main/.kokoro/release.sh

set -eo pipefail
set -x

# Parse command line arguments
DRY_RUN=
while [ $# -gt 0 ] ; do
  case "$1" in
    -d | --dry-run )
      DRY_RUN=true
      ;;
    -h | --help )
      echo -e "USAGE: `basename $0` [ -d | --dry-run ]"
      exit
      ;;
  esac
  shift 1;
done

if [[ -z "${KOKORO_GOB_COMMIT}" ]]; then
    PROJECT_SCM="github/python-bigquery-dataframes"
else
    PROJECT_SCM="git/bigframes"
fi

if [ -z "${PROJECT_ROOT:-}" ]; then
    PROJECT_ROOT="${KOKORO_ARTIFACTS_DIR}/${PROJECT_SCM}"
fi

# Move into the package, build the distribution and upload to shared bucket.
# See internal bug 274624240 for details.

cd "${PROJECT_ROOT}"
rm -rf build dist

# Workaround the fact that the repository that has been fetched before the
# build script. See: go/kokoro-native-docker-migration#known-issues and
# internal issue b/261050975.
git config --global --add safe.directory "${PROJECT_ROOT}"

# Workaround for older pip not able to resolve dependencies. See internal
# issue 316909553.
python3.10 -m pip install pip==25.0.1

# Disable buffering, so that the logs stream through.
export PYTHONUNBUFFERED=1

# Install dependencies, as the following steps depend on it
python3.10 -m pip install -e .[all]

# Update version string to include git hash and date
CURRENT_DATE=$(date '+%Y%m%d')
GIT_HASH=$(git rev-parse --short HEAD)
BIGFRAMES_VERSION=$(python3.10 -c "import bigframes; print(bigframes.__version__)")
RELEASE_VERSION=${BIGFRAMES_VERSION}dev${CURRENT_DATE}+${GIT_HASH}
sed -i -e "s/$BIGFRAMES_VERSION/$RELEASE_VERSION/g" bigframes/version.py

# Generate the package wheel
python3.10 setup.py sdist bdist_wheel

# Make sure that the wheel file is generated
VERSION_WHEEL=`ls dist/bigframes-*.whl`
num_wheel_files=`echo $VERSION_WHEEL | wc -w`
if [ $num_wheel_files -ne 1 ] ; then
    echo "Exactly one wheel file should have been generated, found $num_wheel_files: $VERSION_WHEEL"
    exit -1
fi

# Create a copy of the wheel with a well known, version agnostic name
LATEST_WHEEL=dist/bigframes-latest-py2.py3-none-any.whl
cp $VERSION_WHEEL $LATEST_WHEEL
cp dist/bigframes-*.tar.gz dist/bigframes-latest.tar.gz

if ! [ ${DRY_RUN} ]; then
for gcs_path in gs://vertex_sdk_private_releases/bigframe/ \
                    gs://dl-platform-colab/bigframes/ \
                    gs://bigframes-wheels/;
    do
      gcloud storage cp --print-created-message dist/* ${gcs_path}
      gcloud storage cp --print-created-message LICENSE ${gcs_path}
      gcloud storage cp --recursive --print-created-message "notebooks/" ${gcs_path}notebooks/

    done

    # publish API coverage information to BigQuery
    # Note: only the kokoro service account has permission to write to this
    # table, if you want to test this step, point it to a table you have
    # write access to
    COVERAGE_TABLE=bigframes-metrics.coverage_report.bigframes_coverage_nightly
    python3.10 scripts/publish_api_coverage.py \
      bigquery \
      --bigframes_version=$BIGFRAMES_VERSION \
      --release_version=$RELEASE_VERSION \
      --bigquery_table=$COVERAGE_TABLE
fi

# Undo the file changes, in case this script is running on a
# non-temporary instance of the bigframes repo
# TODO: This doesn't work with (set -eo pipefail) if the failure happened after
# the changes were made but before this cleanup, because the script would
# terminate with the failure itself. See if we can ensure the cleanup.
sed -i -e "s/$RELEASE_VERSION/$BIGFRAMES_VERSION/g" bigframes/version.py

if ! [ ${DRY_RUN} ]; then
    # Copy docs and wheels to Google Drive
    python3.10 scripts/upload_to_google_drive.py
fi
