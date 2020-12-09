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

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate Container Analysis GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    service="containeranalysis",
    version="v1",
    bazel_target="//google/devtools/containeranalysis/v1:devtools-containeranalysis-v1-py",
    proto_output_path="google/cloud/devtools/containeranalysis_v1/proto",
    include_protos=True,
)

excludes = [
    "setup.py",
    "README.rst",
    "docs/index.rst",
]

s.move(library, excludes=excludes)


s.replace(
    "google/**/*client.py",
    r"""google-cloud-devtools-containeranalysis""",
    r"""google-cloud-containeranalysis""",
)

# Fix imported type from grafeas

s.replace(
    "google/**/types/containeranalysis.py",
    "from grafeas\.v1 import vulnerability_pb2 as vulnerability",
    "from grafeas.grafeas_v1.types import vulnerability"
)

# Insert helper method to get grafeas client

s.replace(
    "google/**/client.py",
    "class ContainerAnalysisClientMeta\(type\):",
    """from grafeas import grafeas_v1
from grafeas.grafeas_v1.services.grafeas import transports

class ContainerAnalysisClientMeta(type):""",
)

s.replace(
    "google/**/async_client.py",
    "class ContainerAnalysisAsyncClient:",
    """from grafeas import grafeas_v1
from grafeas.grafeas_v1.services.grafeas import transports

class ContainerAnalysisAsyncClient:""",
)


s.replace(
    "google/**/client.py",
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
    "google/**/async_client.py",
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
