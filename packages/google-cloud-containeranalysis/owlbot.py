# Copyright 2022 Google LLC
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

import json
from pathlib import Path
import shutil

import synthtool as s
import synthtool.gcp as gcp
from synthtool.languages import python

# ----------------------------------------------------------------------------
# Copy the generated client from the owl-bot staging directory
# ----------------------------------------------------------------------------

clean_up_generated_samples = True

# Load the default version defined in .repo-metadata.json.
default_version = json.load(open(".repo-metadata.json", "rt")).get("default_version")

for library in s.get_staging_dirs(default_version):
    if clean_up_generated_samples:
        shutil.rmtree("samples/generated_samples", ignore_errors=True)
        clean_up_generated_samples = False

    # Fix imported type from grafeas
    s.replace(
        library / "google/**/types/containeranalysis.py",
        "from grafeas\.v1 import severity_pb2",
        "import grafeas.grafeas_v1",
    )

    # Fix imported type from grafeas
    s.replace(
        library / "google/**/types/containeranalysis.py", "severity_pb2", "grafeas.grafeas_v1"
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
        r"""\n\g<1>def get_grafeas_client(
            self
        ) -> grafeas_v1.GrafeasClient:
            grafeas_transport = grafeas_v1.services.grafeas.transports.GrafeasGrpcTransport(
                credentials=self.transport._credentials,
                # Set ``credentials_file`` to ``None`` here as
                # transport._credentials contains the credentials
                # which are saved
                credentials_file=None,
                host = self.transport._host,
                scopes=self.transport.AUTH_SCOPES
            )
            return grafeas_v1.GrafeasClient(transport=grafeas_transport)

    \g<1># Service calls
    \g<1>def set_iam_policy(""",
    )

    s.replace(
        library / "google/**/async_client.py",
        r"""(\s+)async def set_iam_policy\(""",
        r"""\n\g<1>def get_grafeas_client(
            self
        ) -> grafeas_v1.GrafeasClient:
            grafeas_transport = grafeas_v1.services.grafeas.transports.GrafeasGrpcTransport(
                credentials=self.transport._credentials,
                # Set ``credentials_file`` to ``None`` here as
                # transport._credentials contains the credentials
                # which are saved
                credentials_file=None,
                host = self.transport._host,
                scopes=self.transport.AUTH_SCOPES
            )
            return grafeas_v1.GrafeasClient(transport=grafeas_transport)

    \g<1># Service calls
    \g<1>async def set_iam_policy(""",
    )

    # Add test to ensure that credentials propagate to client.get_grafeas_client()
    num_replacements = s.replace(
        library / "tests/**/test_container_analysis.py",
        """create_channel.assert_called_with\(
            "containeranalysis.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=\(
                'https://www.googleapis.com/auth/cloud-platform',
\),
            scopes=None,
            default_host="containeranalysis.googleapis.com",
            ssl_credentials=None,
            options=\[
                \("grpc.max_send_message_length", -1\),
                \("grpc.max_receive_message_length", -1\),
            \],
        \)""",
        """create_channel.assert_called_with(
            "containeranalysis.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=(
                'https://www.googleapis.com/auth/cloud-platform',
),
            scopes=None,
            default_host="containeranalysis.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

        # Also check client.get_grafeas_client() to make sure that the file credentials are used
        assert file_creds == client.get_grafeas_client().transport._credentials
        """,
    )

    assert num_replacements == 1

    s.move([library], excludes=["**/gapic_version.py", "setup.py", "testing/constraints-3.7.txt"])
s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------

templated_files = gcp.CommonTemplates().py_library(
    cov_level=100,
    microgenerator=True,
    versions=gcp.common.detect_versions(path="./google", default_first=True),
)
s.move(
    templated_files,
    excludes=[
        ".coveragerc",
        ".github/release-please.yml",
        ".github/workflows",
    ],
)  # exclude templated gh actions as tests require credentials
python.py_samples(skip_readmes=True)

# run format session for all directories which have a noxfile
for noxfile in Path(".").glob("**/noxfile.py"):
    s.shell.run(["nox", "-s", "format"], cwd=noxfile.parent, hide_output=False)
