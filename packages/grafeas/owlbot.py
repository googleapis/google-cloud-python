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
import re
import shutil

import synthtool as s
import synthtool.gcp as gcp
from synthtool.languages import python

# ----------------------------------------------------------------------------
# Copy the generated client from the owl-bot staging directory
# ----------------------------------------------------------------------------

clean_up_generated_samples = True

# Load the default version defined in .repo-metadata.json.
default_version = json.load(open(".repo-metadata.json", "rt")).get(
    "default_version"
)

for library in s.get_staging_dirs(default_version):
    if clean_up_generated_samples:
        shutil.rmtree("samples/generated_samples", ignore_errors=True)
        clean_up_generated_samples = False

    # ----------------------------------------------------------------------------
    # Remove google-specific portions of library
    # ----------------------------------------------------------------------------

    # Please see this PR for more context
    # https://github.com/googleapis/google-cloud-python/pull/8186/

    # Remove default service address, default scopes, default credentials
    # Users must pass a transport to the client constructor

    # Remove default endpoint
    s.replace(
        library / "grafeas/**/*client.py",
        r"""\s+DEFAULT_ENDPOINT\s+=\s+"containeranalysis\.googleapis\.com"
\s+DEFAULT_MTLS_ENDPOINT\s+=\s+_get_default_mtls_endpoint\.__func__\(  # type: ignore
\s+DEFAULT_ENDPOINT
\s+\)""",
    "",
    )

    s.replace(
        library / "grafeas/**/*client.py",
        """DEFAULT_ENDPOINT = GrafeasClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = GrafeasClient.DEFAULT_MTLS_ENDPOINT""",
        """""",
    )

    s.replace(
    library / "grafeas/**/transports/*.py", r"""'containeranalysis\.googleapis\.com'""", """''""",
    )

    # Remove 'from_service_account_file' method
    s.replace(
    library / "grafeas/**/*client.py",
    """@classmethod
    def from_service_account_file.*
    from_service_account_json = from_service_account_file""",
    "",
    flags=re.MULTILINE | re.DOTALL,
    )

    # Remove `get_mtls_endpoint_and_cert_source` method
    s.replace(
        library / "grafeas/**/client.py",
        """@classmethod
    def get_mtls_endpoint_and_cert_source.*?return api_endpoint, client_cert_source""",
        "",
        flags=re.MULTILINE | re.DOTALL,
    )

    # Remove `get_mtls_endpoint_and_cert_source` method
    s.replace(
        library / "grafeas/**/async_client.py",
        """@classmethod
    def get_mtls_endpoint_and_cert_source.*?return GrafeasClient.get_mtls_endpoint_and_cert_source\(client_options\)  # type: ignore""",
        "",
        flags=re.MULTILINE | re.DOTALL,
    )

    # Remove credentials and client options from the service celint
    # A transport must be used to initialize the client
    s.replace(
    library / "grafeas/**/client.py",
    """(\s+)def __init__\(self.*?def """,
    '''\g<1>def __init__(self, *,
            transport: Union[str, GrafeasTransport] = None,
            credentials: Optional[ga_credentials.Credentials] = None,
            ) -> None:
        """Instantiate the grafeas client.

        Args:
            transport (Union[str, ~.GrafeasTransport]): The
                transport to use.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        
        if isinstance(transport, GrafeasTransport):
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(credentials=credentials)
\g<1>def ''',
    flags=re.MULTILINE | re.DOTALL,
    )

    # do the same for async
    s.replace(
    library / "grafeas/**/async_client.py",
    """(\s+)def __init__\(self.*?async def """,
    '''\g<1>def __init__(self, *,
            transport: Union[str, GrafeasTransport] = 'grpc_asyncio',
            credentials: Optional[ga_credentials.Credentials] = None,
            ) -> None:
        """Instantiate the grafeas client.

        Args:
            transport (Union[str, ~.GrafeasTransport]): The
                transport to use.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """

        self._client = GrafeasClient(
            transport=transport,
            credentials=credentials,
        )
\g<1>async def ''',
    flags=re.MULTILINE | re.DOTALL,
    )


    # Changes tests

    # Remove hardcoded default endpoint
    s.replace(library / "tests/**/test_grafeas.py", "containeranalysis.googleapis.com", "")

    # Delete irrelevant tests

    # client options tests
    s.replace(
    library / "tests/**/test_grafeas.py",
    """def client_cert_source_callback.*?def test_get_occurrence""",
    """def client_cert_source_callback():
    return b"cert bytes", b"key bytes"\n
@pytest.mark.parametrize("request_type", [
  grafeas.GetOccurrenceRequest,
  dict,
])
def test_get_occurrence""",
    flags=re.MULTILINE | re.DOTALL,
    )

    # Remove test_client_withDEFAULT_CLIENT_INFO test
    s.replace(
    library / "tests/**/test_grafeas.py",
    """def test_client_with_default_client_info.*
        prep\.assert_called_once_with\(client_info\)$""",
    "",
    flags=re.MULTILINE | re.DOTALL,
    )

    # default endpoint test
    s.replace(
    library / "tests/**/test_grafeas.py",
    """@pytest.mark.parametrize\("transport_name", \[
    "grpc",
    "grpc_asyncio",
    "rest",
\]\)
def test_grafeas_host_no_port.*?def test_grafeas_grpc_transport_channel""",
    """def test_grafeas_grpc_transport_channel""",
    flags=re.MULTILINE | re.DOTALL,
    )

    # duplicate credentials tests
    s.replace(
    library / "tests/**/test_grafeas.py",
    """def test_credentials_transport_error.*?def test_transport_instance""",
    """def test_transport_instance""",
    flags=re.MULTILINE | re.DOTALL,
    )

    s.replace(
    library / "tests/**/test_grafeas.py",
    """def test_grafeas_base_transport_error.*?def test_grafeas_base_transport""",
    """def test_grafeas_base_transport""",
    flags=re.MULTILINE | re.DOTALL,
    )

    # remove test api key credentials
    s.replace(
        library / "tests/**/test_grafeas.py",
        """@pytest.mark.parametrize\("client_class,transport_class", \[
    \(GrafeasClient, transports.GrafeasGrpcTransport\),
    \(GrafeasAsyncClient, transports.GrafeasGrpcAsyncIOTransport\),
\]\)
def test_api_key_credentials.*?client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            \)""",
    """""",

    flags=re.MULTILINE | re.DOTALL,
    )

    s.move([library], excludes=["**/gapic_version.py", "README.rst", "setup.py", "docs/index.rst"])
s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------

templated_files = gcp.CommonTemplates().py_library(
    cov_level=99,
    microgenerator=True,
    versions=gcp.common.detect_versions(path="./google", default_first=True),
)
s.move(templated_files, excludes=[".coveragerc", ".github/release-please.yml", ".github/workflows", "README.rst", ".github/snippet-bot.yml", "docs/index.rst"])

python.py_samples(skip_readmes=True)

# Library code is in "grafeas" instead of "google"
s.replace("noxfile.py", """['"]google['"]""", '''"grafeas"''')
s.replace(
    "noxfile.py",
    "--cov=google",
    "--cov=grafeas",
)

# run format session for all directories which have a noxfile
for noxfile in Path(".").glob("**/noxfile.py"):
    s.shell.run(["nox", "-s", "blacken"], cwd=noxfile.parent, hide_output=False)

