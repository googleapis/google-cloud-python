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
versions = ["v1beta1", "v1beta2", "v1"]

for version in versions:
    library = gapic.py_library(
        service="bigquery_storage",
        version=version,
        bazel_target=f"//google/cloud/bigquery/storage/{version}:bigquery-storage-{version}-py",
        include_protos=True,
    )

    s.move(
        library,
        excludes=[
            "docs/conf.py",
            "docs/index.rst",
            f"google/cloud/bigquery_storage_{version}/__init__.py",
            "README.rst",
            "nox*.py",
            "setup.py",
            "setup.cfg",
        ],
    )

    # We need to parameterize aspects of the client as it varies in different versions.
    #
    # In the future once the read and write client are colocated in the same version,
    # we'll need to loop through through multiple clients.  Perhaps by the time that
    # happens we'll be on a generator that needs less post-generation modifications.
    
    clientinfo = {
        "file": "big_query_storage_client.py",
        "type": "storage",
        "name": "BigQueryStorageClient",
        "badpkg": "google-cloud-bigquerystorage",
        "goodpkg": "google-cloud-bigquery-storage",
    }
    if version in ["v1beta2","v1"]:
        clientinfo = {
            "file": "big_query_read_client.py",
            "type": "read",
            "name": "BigQueryReadClient",
            "badpkg": "google-cloud-bigquerystorage",
            "goodpkg": "google-cloud-bigquery-storage",
        }
    if version in ["v1alpha2"]:
        clientinfo = {
            "file": "big_query_write_client.py",
            "type": "write",
            "name": "BigQueryWriteClient",
            "badpkg": "google-cloud-bigquerystorage",
            "goodpkg": "google-cloud-bigquery-storage",
        }

    s.replace(
        [
            f"google/cloud/bigquery_storage_{version}/proto/storage_pb2.py",
            f"google/cloud/bigquery_storage_{version}/proto/storage_pb2_grpc.py",
            f"google/cloud/bigquery_storage_{version}/proto/stream_pb2.py",
            f"google/cloud/bigquery_storage_{version}/proto/stream_pb2_grpc.py",
        ],
        f"from google.cloud.bigquery.storage_{version}.proto",
        f"from google.cloud.bigquery_storage_{version}.proto",
    )

    # This is used to populate _GAPIC_LIBRARY_VERSION in the client.
    s.replace(
        f"google/cloud/bigquery_storage_{version}/gapic/{clientinfo['file']}",
        clientinfo['badpkg'],
        clientinfo['goodpkg']
    )

    s.replace(
        f"google/cloud/bigquery_storage_{version}/gapic/{clientinfo['file']}",
        "import google.api_core.gapic_v1.method\n",
        "\g<0>import google.api_core.path_template\n",
    )

    s.replace(
        [f"tests/unit/gapic/{version}/test_big_query_{clientinfo['type']}_client_{version}.py"],
        f"from google.cloud import bigquery_storage_{version}",
        f"from google.cloud.bigquery_storage_{version}.gapic import big_query_{clientinfo['type']}_client  # noqa",
    )

    s.replace(
        [f"tests/unit/gapic/{version}/test_big_query_{clientinfo['type']}_client_{version}.py"],
        f"bigquery_storage_{version}.{clientinfo['name']}",
        f"big_query_{clientinfo['type']}_client.{clientinfo['name']}",
    )

    # START: Ignore lint and coverage
    s.replace(
        [f"google/cloud/bigquery_storage_{version}/gapic/big_query_{clientinfo['type']}_client.py"],
        "if transport:",
        "if transport:  # pragma: no cover",
    )

    s.replace(
        [f"google/cloud/bigquery_storage_{version}/gapic/big_query_{clientinfo['type']}_client.py"],
        r"metadata.append\(routing_metadata\)",
        "metadata.append(routing_metadata)  # pragma: no cover",
    )

    s.replace(
        [
            f"google/cloud/bigquery_storage_{version}/gapic/transports/big_query_{clientinfo['type']}_grpc_transport.py"
        ],
        "if channel is not None and credentials is not None:",
        "if channel is not None and credentials is not None:  # pragma: no cover",
    )

    s.replace(
        [
            f"google/cloud/bigquery_storage_{version}/gapic/transports/big_query_{clientinfo['type']}_grpc_transport.py"
        ],
        "if channel is None:",
        "if channel is None:  # pragma: no cover",
    )

    s.replace(
        [
            f"google/cloud/bigquery_storage_{version}/gapic/transports/big_query_{clientinfo['type']}_grpc_transport.py"
        ],
        r"google.api_core.grpc_helpers.create_channel\(",
        "google.api_core.grpc_helpers.create_channel(  # pragma: no cover",
    )

    # Fix up proto docs that are missing summary line.
    s.replace(
        f"google/cloud/bigquery_storage_{version}/proto/storage_pb2.py",
        '"""Attributes:',
        '"""Protocol buffer.\n\n  Attributes:',
    )
    # END: Ignore lint and coverage


# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
optional_deps = [".[fastavro,pandas,pyarrow]"]
system_test_deps = optional_deps
templated_files = common.py_library(
    unit_cov_level=79,
    cov_level=79,
    samples_test=True,
    system_test_dependencies=system_test_deps,
    unit_test_dependencies=optional_deps,
    samples=True,
)
s.move(templated_files)


# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

python.py_samples(skip_readmes=True)


# install bigquery as a (non-editable) package
s.replace(
    "noxfile.py",
    r'session\.install\("--pre", "grpcio"\)',
    '\g<0>\n\n    session.install("google-cloud-bigquery")',
)

# TODO(busunkim): Use latest sphinx after microgenerator transition
s.replace("noxfile.py", """['"]sphinx['"]""", '"sphinx<3.0.0"')


s.shell.run(["nox", "-s", "blacken"], hide_output=False)
