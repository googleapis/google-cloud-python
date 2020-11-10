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

import re

import synthtool as s
from synthtool import gcp
from synthtool.languages import python

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()
versions = ["v1"]

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
    if version in {"v1"}:
        clientinfo = {
            "file": "big_query_read_client.py",
            "type": "read",
            "name": "BigQueryReadClient",
            "badpkg": "google-cloud-bigquerystorage",
            "goodpkg": "google-cloud-bigquery-storage",
        }

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
optional_deps = [".[fastavro,pandas,pyarrow]"]

templated_files = common.py_library(
    microgenerator=True,
    samples=True,
    unit_test_local_dependencies=optional_deps,
    system_test_local_dependencies=optional_deps,
    cov_level=95,
)
s.move(
    templated_files, excludes=[".coveragerc"]
)  # microgenerator has a good .coveragerc file


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

# Remove client-side validation of message length.
# https://github.com/googleapis/python-bigquery-storage/issues/78
s.replace(
    [
        "google/cloud/bigquery_storage_v1/services/big_query_read/transports/grpc.py",
        "google/cloud/bigquery_storage_v1/services/big_query_read/transports/grpc_asyncio.py",
    ],
    (
        r"type\(self\).create_channel\(\s*"
        r"host,\s*"
        r"credentials=credentials,\s*"
        r"credentials_file=credentials_file,\s*"
        r"ssl_credentials=ssl_[a-z_]*credentials,\s*"
        r"scopes=scopes or self.AUTH_SCOPES,\s*"
        r"quota_project_id=quota_project_id"
    ),
    """\g<0>,
    options=(
        ('grpc.max_send_message_length', -1),
        ('grpc.max_receive_message_length', -1)
    )""",
)
s.replace(
    "tests/unit/gapic/bigquery_storage_v1/test_big_query_read.py",
    (
        r"grpc_create_channel\.assert_called_once_with\([^()]+"
        r"scopes=\([^()]+\),\s*"
        r"ssl_credentials=[a-z_]+,\s*"
        r"quota_project_id=None"
    ),
    """\g<0>,
    options=(
        ('grpc.max_send_message_length', -1),
        ('grpc.max_receive_message_length', -1)
    )""",
)


# We don't want the generated client to be accessible through
# "google.cloud.bigquery_storage", replace it with the hand written client that
# wraps it.
s.replace(
    "google/cloud/bigquery_storage/__init__.py",
    r"from google\.cloud\.bigquery_storage_v1\.services.big_query_read.client import",
    "from google.cloud.bigquery_storage_v1 import",
)

# We also don't want to expose the async client just yet, at least not until
# it is wrapped in its own manual client class.
s.replace(
    "google/cloud/bigquery_storage/__init__.py",
    (
        r"from google\.cloud\.bigquery_storage_v1\.services.big_query_read.async_client "
        r"import BigQueryReadAsyncClient\n"
    ),
    "",
)
s.replace(
    "google/cloud/bigquery_storage/__init__.py",
    r"""["']BigQueryReadAsyncClient["'],\n""",
    "",
)

# We want types and __version__ to be accessible through the "main" library
# entry point.
s.replace(
    "google/cloud/bigquery_storage/__init__.py",
    r"from google\.cloud\.bigquery_storage_v1\.types\.arrow import ArrowRecordBatch",
    (
        "from google.cloud.bigquery_storage_v1 import types\n"
        "from google.cloud.bigquery_storage_v1 import __version__\n"
        "\g<0>"
    ),
)
s.replace(
    "google/cloud/bigquery_storage/__init__.py",
    r"""["']ArrowRecordBatch["']""",
    ('"__version__",\n' '    "types",\n' "    \g<0>"),
)

# We want to expose all types through "google.cloud.bigquery_storage.types",
# not just the types generated for the BQ Storage library. For example, we also
# want to include common proto types such as Timestamp.
s.replace(
    "google/cloud/bigquery_storage/__init__.py",
    r"import types",
    "import gapic_types as types",
)

# The DataFormat enum is not exposed in bigquery_storage_v1/types, add it there.
s.replace(
    "google/cloud/bigquery_storage_v1/types/__init__.py",
    r"from \.stream import \(",
    "\g<0>\n    DataFormat,",
)
s.replace(
    "google/cloud/bigquery_storage_v1/types/__init__.py",
    r"""["']ReadSession["']""",
    '"DataFormat",\n    \g<0>',
)

# Fix library installations in nox sessions (unit and system tests) - it's
# redundant to install the library twice.
s.replace(
    "noxfile.py",
    r'\)\s*session\.install\("-e", "\."\)\n',
    ")\n",
)

# Fix test coverage plugin paths.
s.replace(
    "noxfile.py",
    r'"--cov=google\.cloud\.bigquerystorage"',
    (
        '"--cov=google.cloud.bigquery_storage",\n'
        '        "--cov=google.cloud.bigquery_storage_v1"'
    ),
)
s.replace(
    "noxfile.py", r"--cov=tests\.unit", "--cov=tests/unit",
)

# TODO(busunkim): Use latest sphinx after microgenerator transition
s.replace("noxfile.py", """['"]sphinx['"]""", '"sphinx<3.0.0"')

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
