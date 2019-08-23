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
version = "v1beta1"

library = gapic.py_library(
    "bigquery_storage",
    version,
    config_path="/google/cloud/bigquery/storage/" "artman_bigquerystorage_v1beta1.yaml",
    artman_output_name="bigquerystorage-v1beta1",
    include_protos=True,
)

s.move(
    library,
    excludes=[
        "docs/conf.py",
        "docs/index.rst",
        "google/cloud/bigquery_storage_v1beta1/__init__.py",
        "README.rst",
        "nox*.py",
        "setup.py",
        "setup.cfg",
    ],
)

s.replace(
    [
        "google/cloud/bigquery_storage_v1beta1/proto/storage_pb2.py",
        "google/cloud/bigquery_storage_v1beta1/proto/storage_pb2_grpc.py",
    ],
    "from google.cloud.bigquery.storage_v1beta1.proto",
    "from google.cloud.bigquery_storage_v1beta1.proto",
)

s.replace(
    "google/cloud/bigquery_storage_v1beta1/gapic/" "big_query_storage_client.py",
    "google-cloud-bigquerystorage",
    "google-cloud-bigquery-storage",
)

s.replace(
    "google/cloud/bigquery_storage_v1beta1/gapic/" "big_query_storage_client.py",
    "import google.api_core.gapic_v1.method\n",
    "\g<0>import google.api_core.path_template\n",
)

s.replace(
    ["tests/unit/gapic/v1beta1/test_big_query_storage_client_v1beta1.py"],
    "from google.cloud import bigquery_storage_v1beta1",
    "from google.cloud.bigquery_storage_v1beta1.gapic import big_query_storage_client  # noqa",
)

s.replace(
    ["tests/unit/gapic/v1beta1/test_big_query_storage_client_v1beta1.py"],
    "bigquery_storage_v1beta1.BigQueryStorageClient",
    "big_query_storage_client.BigQueryStorageClient",
)

# START: Ignore lint and coverage
s.replace(
    ["google/cloud/bigquery_storage_v1beta1/gapic/big_query_storage_client.py"],
    "if transport:",
    "if transport:  # pragma: no cover",
)

s.replace(
    ["google/cloud/bigquery_storage_v1beta1/gapic/big_query_storage_client.py"],
    r"to_grpc_metadata\(\n",
    "to_grpc_metadata(  # pragma: no cover\n",
)

s.replace(
    ["google/cloud/bigquery_storage_v1beta1/gapic/big_query_storage_client.py"],
    r"metadata.append\(routing_metadata\)",
    "metadata.append(routing_metadata)  # pragma: no cover",
)

s.replace(
    [
        "google/cloud/bigquery_storage_v1beta1/gapic/transports/big_query_storage_grpc_transport.py"
    ],
    "if channel is not None and credentials is not None:",
    "if channel is not None and credentials is not None:  # pragma: no cover",
)

s.replace(
    [
        "google/cloud/bigquery_storage_v1beta1/gapic/transports/big_query_storage_grpc_transport.py"
    ],
    "if channel is None:",
    "if channel is None:  # pragma: no cover",
)

s.replace(
    [
        "google/cloud/bigquery_storage_v1beta1/gapic/transports/big_query_storage_grpc_transport.py"
    ],
    r"google.api_core.grpc_helpers.create_channel\(",
    "google.api_core.grpc_helpers.create_channel(  # pragma: no cover",
)
# END: Ignore lint and coverage

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
optional_deps = [".[fastavro,pandas,pyarrow]"]
system_test_deps = optional_deps + ["../bigquery/"]
templated_files = common.py_library(
    unit_cov_level=79,
    cov_level=79,
    samples_test=True,
    system_test_dependencies=system_test_deps,
    unit_test_dependencies=optional_deps,
)
s.move(templated_files)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
