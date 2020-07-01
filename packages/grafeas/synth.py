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
    include_protos=True
)

excludes = ["README.rst", "nox.py", "setup.py", "docs/index.rst"]

# Make 'grafeas' a namespace
s.move(library / "grafeas", excludes=["__init__.py"])
s.move(library / "docs", excludes=["conf.py", "index.rst"])
s.move(
    library / "google/cloud/grafeas_v1/proto",
    "grafeas/grafeas_v1/proto",
    excludes=excludes,
)
s.move(library / "tests")


# Fix proto imports
s.replace(
    ["grafeas/**/*.py", "tests/**/*.py"],
    "from grafeas\.v1( import \w*_pb2)",
    "from grafeas.grafeas_v1.proto\g<1>",
)
s.replace(
    "grafeas/**/*_pb2.py",
    "from grafeas_v1\.proto( import \w*_pb2)",
    "from grafeas.grafeas_v1.proto\g<1>",
)
s.replace(
    "grafeas/**/grafeas_pb2_grpc.py",
    "from grafeas_v1\.proto",
    "from grafeas.grafeas_v1.proto",
)

# Make package name 'grafeas'
s.replace(
    "grafeas/grafeas_v1/gapic/grafeas_client.py", "google-cloud-grafeas", "grafeas"
)

# Fix docstrings with no summary lines
s.replace(
    "grafeas/grafeas_v1/proto/vulnerability_pb2.py",
    r"""(\s+)["']__doc__["']: \"\"\"Attributes:""",
    """\g<1>"__doc__": \"\"\"
    Attributes:""",
)

# Replace mentions of 'Container Analysis' with 'Grafeas' in the docs
s.replace("docs/**/v*/*.rst", "Container Analysis", "Grafeas")


# ----------------------------------------------------------------------------
# Remove google-specific portions of library
# ----------------------------------------------------------------------------

# Please see this PR https://github.com/googleapis/google-cloud-python/pull/8186/

# Remove default service address, default scopes, default credentials
# Update tests and code in docstrings showing client instantiation.


s.replace(
    "grafeas/**/grafeas_client.py",
    r"""    SERVICE_ADDRESS = 'containeranalysis\.googleapis\.com:443'
    \"\"\"The default address of the service\.\"\"\"""",
    "",
)

s.replace(
    "grafeas/**/grafeas_client.py",
    r"""    def __init__\(self, transport=None, channel=None, credentials=None,
            client_config=None, client_info=None, client_options=None\):""",
    "    def __init__(self, transport, client_config=None, client_info=None):",
)

s.replace(
    "grafeas/**/grafeas_client.py",
    r"""Union\[~\.GrafeasGrpcTransport,
                    Callable\[\[~\.Credentials, type], ~\.GrafeasGrpcTransport\]""",
    """~.GrafeasGrpcTransport""",
)

s.replace(
    "grafeas/**/grafeas_client.py",
    r"""            channel \(grpc\.Channel\): DEPRECATED\. A ``Channel`` instance
                through which to make calls\. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception\.
            credentials \(google\.auth\.credentials\.Credentials\): The
                authorization credentials to attach to requests\. These
                credentials identify this application to the service\. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment\.
                This argument is mutually exclusive with providing a
                transport instance to ``transport``; doing so will raise
                an exception\.""",
    "",
)

# Remove client_options
# api_endpoint is currently the only option and doesn't make sense for Grafeas.
s.replace("grafeas/**/grafeas_client.py", "import google.api_core.client_options\n", "")
s.replace(
    "grafeas/**/grafeas_client.py",
    r"""            client_options \(Union\[dict, google\.api_core\.client_options\.ClientOptions\]\):
                Client options used to set user options on the client\. API Endpoint
                should be set through client_options\.
        \"\"\"""",
    "        \"\"\""
)

s.replace(
    "grafeas/**/grafeas_client.py",
    r"""if channel:
            warnings\.warn\('The `channel` argument is deprecated; use '
                          '`transport` instead\.',
                          PendingDeprecationWarning, stacklevel=2\)

        api_endpoint = self\.SERVICE_ADDRESS
        if client_options:
            if type\(client_options\) == dict:
                client_options = google\.api_core\.client_options\.from_dict\(client_options\)
            if client_options\.api_endpoint:
                api_endpoint = client_options\.api_endpoint

        \# Instantiate the transport\.
        \# The transport is responsible for handling serialization and
        \# deserialization and actually sending data to the service\.
        if transport:
            if callable\(transport\):
                self\.transport = transport\(
                    credentials=credentials,
                    default_class=grafeas_grpc_transport\.GrafeasGrpcTransport,
                    address=api_endpoint,
                \)
            else:
                if credentials:
                    raise ValueError\(
                        'Received both a transport instance and '
                        'credentials; these are mutually exclusive\.'
                    \)
                self\.transport = transport
        else:
            self\.transport = grafeas_grpc_transport\.GrafeasGrpcTransport\(
                address=api_endpoint,
                channel=channel,
                credentials=credentials,
            \)""",
    """# Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        self.transport = transport""",
)

s.replace(
    "grafeas/**/grafeas_client.py",
    r"""        Example:
            >>> from grafeas import grafeas_v1
            >>>
            >>> client = grafeas_v1\.GrafeasClient\(\)""",
    """        Example:
            >>> from grafeas import grafeas_v1
            >>> from grafeas.grafeas_v1.gapic.transports import grafeas_grpc_transport
            >>> 
            >>> address = "[SERVICE_ADDRESS]"
            >>> scopes = ("[SCOPE]")
            >>> transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)
            >>> client = grafeas_v1.GrafeasClient(transport)""",
)

s.replace(
    "grafeas/**/grafeas_client.py",
    r'''    @classmethod
    def from_service_account_file\(cls, filename, \*args, \*\*kwargs\):
        """Creates an instance of this client using the provided credentials
        file\.

        Args:
            filename \(str\): The path to the service account private key json
                file\.
            args: Additional arguments to pass to the constructor\.
            kwargs: Additional arguments to pass to the constructor\.

        Returns:
            GrafeasClient: The constructed client\.
        """
        credentials = service_account\.Credentials\.from_service_account_file\(
            filename\)
        kwargs\['credentials'\] = credentials
        return cls\(\*args, \*\*kwargs\)

    from_service_account_json = from_service_account_file''',
    "")

s.replace(
    "grafeas/**/grafeas_grpc_transport.py",
    r"""    \# The scopes needed to make gRPC calls to all of the methods defined
    \# in this service\.
    _OAUTH_SCOPES = \(
        'https://www\.googleapis\.com/auth/cloud-platform',
    \)""",
    "",
)

s.replace(
    "grafeas/**/grafeas_grpc_transport.py",
    r"""    def __init__\(self, channel=None, credentials=None,
                 address='containeranalysis\.googleapis\.com:443'\):""",
    """    def __init__(self, address, scopes, channel=None, credentials=None):""",
)

s.replace(
    "grafeas/**/grafeas_grpc_transport.py",
    r"""        \# Create the channel\.
        if channel is None:
            channel = self\.create_channel\(
                address=address,
                credentials=credentials,
""",
    """        # Create the channel.
        if channel is None:
            channel = self.create_channel(
                address,
                scopes,
                credentials=credentials,
""",
)

s.replace(
    "grafeas/**/grafeas_grpc_transport.py",
    r"""    def create_channel\(
                cls,
                address='containeranalysis\.googleapis\.com:443',
                credentials=None,
                \*\*kwargs\):""",
    """    def create_channel(
                cls,
                address,
                scopes,
                credentials=None,
                **kwargs):""",
)

s.replace(
    "grafeas/**/grafeas_grpc_transport.py",
    r"""        Args:
            address \(str\): The host for the channel to use\.
            credentials \(~\.Credentials\): The
                authorization credentials to attach to requests\. These
                credentials identify this application to the service\. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment\.""",
    """        Args:
            address (str): The host for the channel to use.
            scopes (Sequence[str]): The scopes needed to make gRPC calls.
            credentials (~.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.""",
)

s.replace(
    "grafeas/**/grafeas_grpc_transport.py",
    r"""        return google\.api_core\.grpc_helpers\.create_channel\(
            address,
            credentials=credentials,
            scopes=cls\._OAUTH_SCOPES,
            \*\*kwargs
        \)""",
    """        return google.api_core.grpc_helpers.create_channel(
            address,
            credentials=credentials,
            scopes=scopes,
            **kwargs
        )""",
)

s.replace(
    "grafeas/**/grafeas_grpc_transport.py",
    r"""        \"\"\"Instantiate the transport class\.

        Args:
            channel \(grpc\.Channel\): A ``Channel`` instance through
                which to make calls\. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception\.
            credentials \(google\.auth\.credentials\.Credentials\): The
                authorization credentials to attach to requests\. These
                credentials identify this application to the service\. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment\.
            address \(str\): The address where the service is hosted\.""",
    '''        """Instantiate the transport class.

        Args:
            address (str): The address where the service is hosted.
            scopes (Sequence[str]): The scopes needed to make gRPC calls.
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
        ''',
)

s.replace(
    "tests/**/test_grafeas_client_v1.py",
    r"""from grafeas\.grafeas_v1\.proto import grafeas_pb2""",
    r"""from grafeas.grafeas_v1.proto import grafeas_pb2
from grafeas.grafeas_v1.gapic.transports import grafeas_grpc_transport""",
)

s.replace(
    "tests/**/test_grafeas_client_v1.py",
    r"(\s+)client = grafeas_v1\.GrafeasClient\(\)",
    r"""\g<1>address = "[SERVICE_ADDRESS]"
\g<1>scopes = ("SCOPE")
\g<1>transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)
\g<1>client=grafeas_v1.GrafeasClient(transport)""",
)


# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(cov_level=76)
s.move(templated_files)

# TODO(busunkim): Use latest sphinx after microgenerator transition
s.replace("noxfile.py", """['"]sphinx['"]""", '"sphinx<3.0.0"')

# Library code is in "grafeas" instead of "google"
s.replace("noxfile.py", """['"]google['"]""", '''"grafeas"''')
s.replace("noxfile.py",
    '''"--cov=google.cloud.grafeas",
    \s+"--cov=google.cloud",''',
    '''"--cov=grafeas",'''
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
