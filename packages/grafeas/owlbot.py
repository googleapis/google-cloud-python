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
import synthtool.gcp as gcp
import logging
from synthtool.languages import python

logging.basicConfig(level=logging.DEBUG)

common = gcp.CommonTemplates()

default_version = "v1"

for library in s.get_staging_dirs(default_version):
    # Make package name 'grafeas'
    s.replace(library / "grafeas/**/*.py", "grafeas-grafeas", "grafeas")

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
            ) -> None:
        """Instantiate the grafeas client.

        Args:
            transport (Union[str, ~.GrafeasTransport]): The
                transport to use.
            

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        
        if isinstance(transport, GrafeasTransport):
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport()
\g<1>def ''',
    flags=re.MULTILINE | re.DOTALL,
    )

    # do the same for async
    s.replace(
    library / "grafeas/**/async_client.py",
    """(\s+)def __init__\(self.*?async def """,
    '''\g<1>def __init__(self, *,
            transport: Union[str, GrafeasTransport] = 'grpc_asyncio',
            ) -> None:
        """Instantiate the grafeas client.

        Args:
            transport (Union[str, ~.GrafeasTransport]): The
                transport to use.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """

        self._client = GrafeasClient(
            transport=transport,
        )
\g<1>async def ''',
    flags=re.MULTILINE | re.DOTALL,
    )


    # Changes tests

    # Remove hardcoded default endpoint
    s.replace(library / "tests/**/test_grafeas.py", "containeranalysis.googleapis.com", "")

    # remove use of credentials
    s.replace(library / "tests/**/test_grafeas.py", """credentials=ga_credentials.*?,""", "")

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

    excludes = ["README.rst", "setup.py", "docs/index.rst"]
    s.move(library, excludes=excludes)

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=False, microgenerator=True,  # set to True only if there are samples
    cov_level=90  #  some coverage is missing due to manual alterations
)

s.move(
    templated_files,
    excludes=[
        ".coveragerc", # microgenerator has a good .coveragerc file
        ".github/snippet-bot.yml",
        ".github/workflows", # exclude templated gh actions as tests require credentials
	"README.rst",
    ]
)

python.py_samples(skip_readmes=True)
python.configure_previous_major_version_branches()

# Library code is in "grafeas" instead of "google"
s.replace("noxfile.py", """['"]google['"]""", '''"grafeas"''')
s.replace(
    "noxfile.py",
    "--cov=google",
    "--cov=grafeas",
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)

