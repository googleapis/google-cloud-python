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

logging.basicConfig(level=logging.DEBUG)

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate Grafeas GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    service="grafeas",
    version="v1",
    bazel_target="//grafeas/v1:grafeas-v1-py",
    proto_output_path="grafeas/grafeas_v1/proto",
    include_protos=True,
)

excludes = ["README.rst", "setup.py", "docs/index.rst"]

s.move(library, excludes=excludes)


# Make package name 'grafeas'
s.replace("grafeas/**/*.py", "grafeas-grafeas", "grafeas")

# ----------------------------------------------------------------------------
# Remove google-specific portions of library
# ----------------------------------------------------------------------------

# Please see this PR for more context
# https://github.com/googleapis/google-cloud-python/pull/8186/

# Remove default service address, default scopes, default credentials
# Users must pass a transport to the client constructor


# Remove default endpoint
s.replace(
    "grafeas/**/*client.py",
    r"""\s+DEFAULT_ENDPOINT\s+=\s+"containeranalysis\.googleapis\.com"
\s+DEFAULT_MTLS_ENDPOINT\s+=\s+_get_default_mtls_endpoint\.__func__\(  # type: ignore
\s+DEFAULT_ENDPOINT
\s+\)""",
    "",
)

s.replace(
    "grafeas/**/transports/*.py", r"""'containeranalysis\.googleapis\.com'""", """''""",
)


# Remove 'from_service_account_file' method
s.replace(
    "grafeas/**/*client.py",
    """@classmethod
    def from_service_account_file.*
    from_service_account_json = from_service_account_file""",
    "",
    flags=re.MULTILINE | re.DOTALL,
)

s.replace(
    "grafeas/**/async_client.py",
    """\s+from_service_account_file = GrafeasClient\.from_service_account_file
\s+from_service_account_json = from_service_account_file""",
    "",
)

# Remove credentials and client options from the service celint
# A transport must be used to initialize the client
s.replace(
    "grafeas/**/client.py",
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
    "grafeas/**/async_client.py",
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

# remove use of credentials
s.replace("tests/**/test_grafeas.py", """credentials=credentials.*?,""", "")

# remove client_options
s.replace("tests/**/test_grafeas.py", """client_options=\{.*?\},""", "")
s.replace("tests/**/test_grafeas.py", """client_options=options,""", "")
s.replace(
    "tests/**/test_grafeas.py",
    """client_options=client_options.ClientOptions(.*?),""",
    "",
)

# Delete irrelevant tests

# client options tests
s.replace(
    "tests/**/test_grafeas.py",
    """def client_cert_source_callback.*?def test_get_occurrence""",
    """def test_get_occurrence""",
    flags=re.MULTILINE | re.DOTALL,
)

# default endpoint test
s.replace(
    "tests/**/test_grafeas.py",
    """def test_grafeas_host_no_port.*?def test_grafeas_grpc_transport_channel""",
    """def test_grafeas_grpc_transport_channel""",
    flags=re.MULTILINE | re.DOTALL,
)

# duplicate credentials tests
s.replace(
    "tests/**/test_grafeas.py",
    """def test_credentials_transport_error.*?def test_transport_instance""",
    """def test_transport_instance""",
    flags=re.MULTILINE | re.DOTALL,
)

s.replace(
    "tests/**/test_grafeas.py",
    """def test_grafeas_base_transport_error.*?def test_grafeas_base_transport""",
    """def test_grafeas_base_transport""",
    flags=re.MULTILINE | re.DOTALL,
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=False, microgenerator=True,  # set to True only if there are samples
    cov_level=90  #  some coverage is missing due to manual alterations
)

s.move(
    templated_files, excludes=[".coveragerc"]
)  # microgenerator has a good .coveragerc file


# Library code is in "grafeas" instead of "google"
s.replace("noxfile.py", """['"]google['"]""", '''"grafeas"''')
s.replace(
    "noxfile.py",
    """"--cov=google.cloud.grafeas",
    \s+"--cov=google.cloud",""",
    """"--cov=grafeas",""",
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
