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
from synthtool.languages import python


gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()
versions = ["v1"]

# ----------------------------------------------------------------------------
# Generate bigquery_datatransfer GAPIC layer
# ----------------------------------------------------------------------------
for version in versions:
    library = gapic.py_library(
        service="bigquery_datatransfer",
        version=version,
        bazel_target=(
            f"//google/cloud/bigquery/datatransfer/{version}:"
            "bigquery-datatransfer-v1-py"
        ),
        include_protos=True,
    )
    s.move(library, excludes=["*.tar.gz", "setup.py", "docs/index.rst"])


# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(microgenerator=True, samples=True, cov_level=99)
s.move(templated_files, excludes=[".coveragerc"])

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

python.py_samples(skip_readmes=True)

# Fix missing async client in datatransfer_v1
s.replace(
    "google/cloud/bigquery_datatransfer_v1/__init__.py",
    r"from \.services\.data_transfer_service import DataTransferServiceClient",
    "\\g<0>\nfrom .services.data_transfer_service import DataTransferServiceAsyncClient",
)
s.replace(
    "google/cloud/bigquery_datatransfer_v1/__init__.py",
    r"'DataTransferServiceClient',",
    '\\g<0>\n    "DataTransferServiceAsyncClient"',
)


# TODO(busunkim): Use latest sphinx after microgenerator transition
s.replace("noxfile.py", "'sphinx'", '"sphinx<3.0.0"')

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
