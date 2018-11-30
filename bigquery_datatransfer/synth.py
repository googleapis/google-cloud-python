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
version = "v1"

# ----------------------------------------------------------------------------
# Generate bigquery_datatransfer GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    "bigquery-datatransfer",
    version,
    config_path="/google/cloud/bigquery/datatransfer/"
    "artman_bigquerydatatransfer.yaml",
    artman_output_name="bigquerydatatransfer-v1",
)

s.move(
    library,
    excludes=["docs/conf.py", "docs/index.rst", "README.rst", "nox.py", "setup.py"],
)

s.replace(
    [
        "google/cloud/bigquery_datatransfer_v1/proto/datatransfer_pb2.py",
        "google/cloud/bigquery_datatransfer_v1/proto/datatransfer_pb2_grpc.py",
    ],
    "from google.cloud.bigquery.datatransfer_v1.proto",
    "from google.cloud.bigquery_datatransfer_v1.proto",
)

s.replace(
    "google/cloud/bigquery_datatransfer_v1/gapic/" "data_transfer_service_client.py",
    "google-cloud-bigquerydatatransfer",
    "google-cloud-bigquery-datatransfer",
)

s.replace(
    "google/cloud/bigquery_datatransfer_v1/gapic/" "data_transfer_service_client.py",
    "import google.api_core.gapic_v1.method\n",
    "\g<0>import google.api_core.path_template\n",
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=80, cov_level=80)
s.move(templated_files)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
