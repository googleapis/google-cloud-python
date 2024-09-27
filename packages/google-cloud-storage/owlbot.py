# Copyright 2020 Google LLC
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

"""This script is used to synthesize generated parts of this library."""

import synthtool as s
from synthtool import gcp
from synthtool.languages import python

common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    cov_level=100,
    split_system_tests=True,
    system_test_external_dependencies=[
        "google-cloud-iam",
        "google-cloud-pubsub < 2.0.0",
        # See: https://github.com/googleapis/python-storage/issues/226
        "google-cloud-kms < 2.0dev",
    ],
    intersphinx_dependencies={
        # python-requests url temporary change related to
        # https://github.com/psf/requests/issues/6140#issuecomment-1135071992
        "requests": "https://requests.readthedocs.io/en/stable/"
    },
)

s.move(
    templated_files,
    excludes=[
        "docs/multiprocessing.rst",
        "noxfile.py",
        "CONTRIBUTING.rst",
        "README.rst",
        ".kokoro/continuous/continuous.cfg",
        ".kokoro/presubmit/system-3.8.cfg",
        ".kokoro/samples/python3.6", # remove python 3.6 support
        ".github/blunderbuss.yml", # blunderbuss assignment to python squad
        ".github/workflows", # exclude gh actions as credentials are needed for tests
        ".github/release-please.yml", # special support for a python2 branch in this repo
    ],
)

s.replace(
    ".kokoro/build.sh",
    "export PYTHONUNBUFFERED=1",
    """export PYTHONUNBUFFERED=1

# Export variable to override api endpoint
export API_ENDPOINT_OVERRIDE

# Export variable to override api endpoint version
export API_VERSION_OVERRIDE

# Export dual region locations
export DUAL_REGION_LOC_1
export DUAL_REGION_LOC_2

# Setup universe domain testing needed environment variables.
export TEST_UNIVERSE_DOMAIN_CREDENTIAL=$(realpath ${KOKORO_GFILE_DIR}/secret_manager/client-library-test-universe-domain-credential)
export TEST_UNIVERSE_DOMAIN=$(gcloud secrets versions access latest --project cloud-devrel-kokoro-resources --secret=client-library-test-universe-domain)
export TEST_UNIVERSE_PROJECT_ID=$(gcloud secrets versions access latest --project cloud-devrel-kokoro-resources --secret=client-library-test-universe-project-id)
export TEST_UNIVERSE_LOCATION=$(gcloud secrets versions access latest --project cloud-devrel-kokoro-resources --secret=client-library-test-universe-storage-location)

""")

s.replace(
    ".coveragerc",
    "omit =",
    """omit =
  .nox/*""")

s.replace(
    ".kokoro/release/common.cfg",
    'value: "releasetool-publish-reporter-app,releasetool-publish-reporter-googleapis-installation,releasetool-publish-reporter-pem"',
    'value: "releasetool-publish-reporter-app,releasetool-publish-reporter-googleapis-installation,releasetool-publish-reporter-pem, client-library-test-universe-domain-credential"'
)

python.py_samples(skip_readmes=True)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
