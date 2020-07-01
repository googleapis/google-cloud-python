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
import synthtool.gcp as gcp

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate trace GAPIC layer
# ----------------------------------------------------------------------------
for version in ["v1", "v2"]:
    library = gapic.py_library(
        service="trace",
        version=version,
        bazel_target=f"//google/devtools/cloudtrace/{version}:devtools-cloudtrace-{version}-py",
        proto_output_path=f"google/cloud/trace_{version}/proto",
        include_protos=True,
    )

    s.move(library / f"google/cloud/trace_{version}")
    s.move(library / f"tests/unit/gapic/{version}")
    s.move(library/ f"google/cloud/devtools/cloudtrace_{version}/proto",
           f"google/cloud/trace_{version}/proto")

    # Fix up imports
    s.replace(
        "google/**/*.py",
        f"from google.cloud.devtools.cloudtrace_{version}.proto import ",
        f"from google.cloud.trace_{version}.proto import ",
    )

    s.replace(
        f"google/cloud/trace_{version}/gapic/trace_service_client.py",
        "google-cloud-devtools-cloudtrace",
        "google-cloud-trace",
    )

# Copy docs configuration
s.move(library / f"docs/conf.py")

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(cov_level=98)
s.move(templated_files)

# TODO(busunkim): Use latest sphinx after microgenerator transition
s.replace("noxfile.py", '''['"]sphinx["']''', '"sphinx<3.0.0"')

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
