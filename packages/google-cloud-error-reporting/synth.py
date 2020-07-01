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

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate error_reporting GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    service="errorreporting",
    version="v1beta1",
    bazel_target="//google/devtools/clouderrorreporting/v1beta1:devtools-clouderrorreporting-v1beta1-py",
    include_protos=True,
)

s.move(library / "google/cloud/devtools/clouderrorreporting_v1beta1/proto",
       "google/cloud/errorreporting_v1beta1/proto")
s.move(library / "google/cloud/errorreporting_v1beta1/proto")
s.move(library / "google/cloud/errorreporting_v1beta1/gapic")
s.move(library / "tests/unit/gapic/v1beta1")
s.move(library / "tests/system/gapic/v1beta1")

s.replace(
    "google/cloud/**/*py",
    "google-cloud-devtools-clouderrorreporting",
    "google-cloud-error-reporting",
)

# Fix up imports
s.replace(
    "google/**/*.py",
    r"from google.cloud.devtools.clouderrorreporting_v1beta1.proto import ",
    r"from google.cloud.errorreporting_v1beta1.proto import ",
)

# Fix up docstrings in GAPIC clients
DISCARD_AUTH_BOILERPLATE = r"""
        This endpoint accepts either an OAuth token, or an API key for
        authentication. To use an API key, append it to the URL as the value of
        a ``key`` parameter. For example:

        \.\. raw:: html
        <pre>POST
            .*</pre>
"""

targets = [
    "google/cloud/errorreporting_v1beta1/gapic/*_client.py",
    "google/cloud/errorreporting_v1beta1/gapic/transports/*_transport.py",
]

s.replace(targets, DISCARD_AUTH_BOILERPLATE, r"")

# TODO(busunkim): Remove during microgenerator transition
s.replace(
    ["google/cloud/**/*.py", "tests/**/*.py"],
    "error_group_path",
    "group_path"
)

# TODO(busunkim) Remove during microgenerator transition
# Keeps the previous param order to avoid breaking existing
# code
n = s.replace(
    "google/cloud/**/error_stats_service_client.py",
"""def list_group_stats\(
\s+self,
\s+project_name,
\s+group_id=None,
\s+service_filter=None,
\s+time_range=None,
\s+timed_count_duration=None,
\s+alignment=None,
\s+alignment_time=None,
\s+order=None,
\s+page_size=None,
\s+retry=google\.api_core\.gapic_v1\.method\.DEFAULT,
\s+timeout=google\.api_core\.gapic_v1\.method\.DEFAULT,
\s+metadata=None\):""",
"""def list_group_stats(
        self,
        project_name,
        time_range=None, # DO NOT MOVE, see synth.py
        group_id=None,
        service_filter=None,
        timed_count_duration=None,
        alignment=None,
        alignment_time=None,
        order=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
"""
)

if n != 1:
    raise Exception("Required replacement not made.")
# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    unit_cov_level=97, cov_level=98, system_test_dependencies=["test_utils"]
)
s.move(templated_files)

# TODO(busunkim): Use latest sphinx after microgenerator transition
s.replace("noxfile.py", """['"]sphinx['"]""", '"sphinx<3.0.0"')


s.shell.run(["nox", "-s", "blacken"], hide_output=False)
