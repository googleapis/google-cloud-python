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
import logging

logging.basicConfig(level=logging.DEBUG)

gapic = gcp.GAPICGenerator()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate dlp GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    "grafeas", "v1", config_path="/grafeas/artman_grafeas_v1.yaml", include_protos=True
)

excludes = ["README.rst", "nox.py", "setup.py", "docs/index.rst", "grafeas/__init__.py"]

# This library is an atypical generation, so move over directories one by one.

s.move(library / "grafeas", excludes=excludes)
s.move(library / "docs", excludes=excludes)
s.move(
    library / "google/cloud/grafeas_v1/proto", "grafeas/grafeas_v1", excludes=excludes
)
s.move(library / "tests")

# Fix proto imports
s.replace(
    ["grafeas/**/*.py", "tests/**/*.py"],
    "from grafeas\.v1 (import \w*_pb2)",
    "from grafeas.v1.proto \g<1>",
)
s.replace(
    ["grafeas/**/*_pb2.py", "grafeas/**/*_grpc.py"],
    "from grafeas_v1\.proto",
    "from grafeas.v1.proto",
)


# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=78, cov_level=78)
s.move(templated_files, excludes=["noxfile.py"])

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
