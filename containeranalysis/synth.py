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
# Generate Container Analysis GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    "containeranalysis",
    "v1",
    config_path="/google/devtools/containeranalysis/artman_containeranalysis_v1.yaml",
    include_protos=True,
)

excludes = [
    "nox.py",
    "setup.py",
    "google/cloud/containeranalysis_v1/proto",
    "google/cloud/devtools/__init__.py",  # other packages also use this namespace
    "README.rst",
    "docs/index.rst",
]

s.move(library, excludes=excludes)
# .proto files end up in the wrong place by default
s.move(
    library / "google/cloud/containeranalysis_v1/proto",
    "google/cloud/devtools/containeranalysis_v1/proto",
)

# Insert helper method to get grafeas client
s.replace(
    "google/**/container_analysis_client.py",
    r"""_GAPIC_LIBRARY_VERSION = pkg_resources\.get_distribution\(
    'google-cloud-containeranalysis',
\)\.version""",
    r"""from grafeas import grafeas_v1
from grafeas.grafeas_v1.gapic.transports import grafeas_grpc_transport

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    "google-cloud-containeranalysis"
).version
""",
)

s.replace(
    "google/**/container_analysis_client.py",
    r"""    \# Service calls
    def set_iam_policy\(""",
    r'''    def get_grafeas_client(self):
        """Returns an equivalent grafeas client.

        Returns:
            A :class:`~grafeas.grafeas_v1.GrafeasClient` instance.
        """
        grafeas_transport = grafeas_grpc_transport.GrafeasGrpcTransport(
            self.SERVICE_ADDRESS,
            self.transport._OAUTH_SCOPES)

        return grafeas_v1.GrafeasClient(grafeas_transport)

    # Service calls
    def set_iam_policy(''',
)
# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=45, cov_level=45)
s.move(templated_files)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
