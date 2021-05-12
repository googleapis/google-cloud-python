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
from synthtool.languages import python

logging.basicConfig(level=logging.DEBUG)

common = gcp.CommonTemplates()

default_version = "v1"

for library in s.get_staging_dirs(default_version):
    s.replace(
        library / "google/**/*client.py",
        r"""google-cloud-devtools-containeranalysis""",
        r"""google-cloud-containeranalysis""",
    )

    # Fix imported type from grafeas
    s.replace(
        library / "google/**/types/containeranalysis.py",
        "from grafeas\.v1 import vulnerability_pb2 as vulnerability",
        "from grafeas.grafeas_v1.types import vulnerability"
    )

    # Insert helper method to get grafeas client
    s.replace(
        library / "google/**/client.py",
        "class ContainerAnalysisClientMeta\(type\):",
        "from grafeas import grafeas_v1\n"
        "from grafeas.grafeas_v1.services.grafeas import transports\n\n"
        "class ContainerAnalysisClientMeta(type):",
    )

    s.replace(
        library / "google/**/async_client.py",
        "class ContainerAnalysisAsyncClient:",
        "from grafeas import grafeas_v1\n"
        "from grafeas.grafeas_v1.services.grafeas import transports\n\n"
        "class ContainerAnalysisAsyncClient:",
    )

    s.replace(
        library / "google/**/client.py",
        r"""(\s+)def set_iam_policy\(""",
        r'''\n\g<1>def get_grafeas_client(
            self
        ) -> grafeas_v1.GrafeasClient:
            transport = type(self).get_transport_class("grpc")()
            grafeas_transport = grafeas_v1.services.grafeas.transports.GrafeasGrpcTransport(
                host=transport._host,
                scopes=transport.AUTH_SCOPES
            )
            return grafeas_v1.GrafeasClient(transport=grafeas_transport)

    \g<1># Service calls
    \g<1>def set_iam_policy(''',
    )

    s.replace(
        library / "google/**/async_client.py",
        r"""(\s+)async def set_iam_policy\(""",
        r'''\n\g<1>def get_grafeas_client(
            self
        ) -> grafeas_v1.GrafeasClient:
            transport = type(self).get_transport_class("grpc_asyncio")()
            grafeas_transport = grafeas_v1.services.grafeas.transports.GrafeasGrpcTransport(
                host=transport._host,
                scopes=transport.AUTH_SCOPES
            )
            return grafeas_v1.GrafeasClient(transport=grafeas_transport)

    \g<1># Service calls
    \g<1>async def set_iam_policy(''',
    )

    s.move(library, excludes=["setup.py", "README.rst", "docs/index.rst"])

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=False,  # set to True only if there are samples
    microgenerator=True,
    cov_level=98,
)
s.move(templated_files, excludes=[".coveragerc"])  # microgenerator has a good coveragerc

python.py_samples(skip_readmes=True)


s.shell.run(["nox", "-s", "blacken"], hide_output=False)