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
    unit_test_python_versions=["3.7", "3.8", "3.9", "3.10"],
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
        ".kokoro/samples/python3.6", # remove python 3.6 support
        ".github/workflows", # exclude gh actions as credentials are needed for tests
        ".github/release-please.yml", # special support for a python2 branch in this repo
    ],
)

python.py_samples(skip_readmes=True)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
