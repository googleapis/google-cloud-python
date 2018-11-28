# Copyright 2018 Google LLC
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

gapic = gcp.GAPICGenerator()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate error_reporting GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    "error_reporting",
    "v1beta1",
    config_path="/google/devtools/clouderrorreporting" "/artman_errorreporting.yaml",
    artman_output_name="error-reporting-v1beta1",
)

s.move(library / "google/cloud/errorreporting_v1beta1/proto")
s.move(library / "google/cloud/errorreporting_v1beta1/gapic")
s.move(library / "tests/unit/gapic/v1beta1")
s.move(library / "tests/system/gapic/v1beta1")

# Fix up imports
s.replace(
    "google/**/*.py",
    r"from google.devtools.clouderrorreporting_v1beta1.proto import ",
    r"from google.cloud.errorreporting_v1beta1.proto import ",
)

# Fix up docstrings in GAPIC clients
DISCARD_AUTH_BOILERPLATE = r"""
        This endpoint accepts either an OAuth token, or an API key for
        authentication. To use an API key, append it to the URL as the value of
        a ``key`` parameter. For example:

        \.\. raw:: html
        <pre>POST .*
"""

targets = [
    "google/cloud/errorreporting_v1beta1/gapic/*_client.py",
    "google/cloud/errorreporting_v1beta1/gapic/transports/*_transport.py",
]

s.replace(targets, DISCARD_AUTH_BOILERPLATE, r"")

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=97, cov_level=100)
s.move(templated_files)
