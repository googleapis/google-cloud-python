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
import textwrap

import synthtool as s
from synthtool import gcp
from synthtool.languages import python

common = gcp.CommonTemplates()

default_version = "v1"

for library in s.get_staging_dirs(default_version):
    # Work around gapic generator bug https://github.com/googleapis/gapic-generator-python/issues/902
    s.replace(
        library / f"google/pubsub_{library.name}/types/*.py",
        r""".
    Attributes:""",
        r""".\n
    Attributes:""",
    )

    # Work around gapic generator bug https://github.com/googleapis/gapic-generator-python/issues/902
    s.replace(
        library / f"google/pubsub_{library.name}/types/*.py",
        r""".
        Attributes:""",
        r""".\n
        Attributes:""",
    )

    # DEFAULT SCOPES and SERVICE_ADDRESS are being used. so let's force them in.
    s.replace(
        library / f"google/pubsub_{library.name}/services/*er/*client.py",
        r"""DEFAULT_ENDPOINT = \"pubsub\.googleapis\.com\"""",
        """
    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = (
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/pubsub',
    )

    SERVICE_ADDRESS = "pubsub.googleapis.com:443"
    \"""The default address of the service.\"""

    \g<0>""",
    )

    # Modify GRPC options in transports.
    count = s.replace(
        [
            library / f"google/pubsub_{library.name}/services/*/transports/grpc*",
            library / f"tests/unit/gapic/pubsub_{library.name}/*",
        ],
        "options=\[.*?\]",
        """options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                    ("grpc.keepalive_time_ms", 30000),
                ]""",
        flags=re.MULTILINE | re.DOTALL,
    )

    if count < 15:
        raise Exception("Expected replacements for gRPC channel options not made.")

    # If the emulator is used, force an insecure gRPC channel to avoid SSL errors.
    clients_to_patch = [
        library / f"google/pubsub_{library.name}/services/publisher/client.py",
        library / f"google/pubsub_{library.name}/services/subscriber/client.py",
    ]
    err_msg = (
        "Expected replacements for gRPC channel to use with the emulator not made."
    )

    count = s.replace(clients_to_patch, r"import os", "import functools\n\g<0>")

    if count < len(clients_to_patch):
        raise Exception(err_msg)

    count = s.replace(
        clients_to_patch,
        f"from google\.pubsub_{library.name}\.types import pubsub",
        "\g<0>\n\nimport grpc",
    )

    if count < len(clients_to_patch):
        raise Exception(err_msg)

    count = s.replace(
        clients_to_patch,
        r"Transport = type\(self\)\.get_transport_class\(transport\)",
        """\g<0>

            emulator_host = os.environ.get("PUBSUB_EMULATOR_HOST")
            if emulator_host:
                if issubclass(Transport, type(self)._transport_registry["grpc"]):
                    channel = grpc.insecure_channel(target=emulator_host)
                else:
                    channel = grpc.aio.insecure_channel(target=emulator_host)
                Transport = functools.partial(Transport, channel=channel)

    """,
    )

    if count < len(clients_to_patch):
        raise Exception(err_msg)

    # Monkey patch the streaming_pull() GAPIC method to disable pre-fetching stream
    # results.
    s.replace(
        library / f"google/pubsub_{library.name}/services/subscriber/client.py",
        (
            r"# Wrap the RPC method.*\n"
            r"\s+# and friendly error.*\n"
            r"\s+rpc = self\._transport\._wrapped_methods\[self\._transport\.streaming_pull\]"
        ),
        """
        # Wrappers in api-core should not automatically pre-fetch the first
        # stream result, as this breaks the stream when re-opening it.
        # https://github.com/googleapis/python-pubsub/issues/93#issuecomment-630762257
        self._transport.streaming_pull._prefetch_first_result_ = False

        \g<0>""",
    )

    # Emit deprecation warning if return_immediately flag is set with synchronous pull.
    s.replace(
        library / f"google/pubsub_{library.name}/services/subscriber/*client.py",
        r"import pkg_resources",
        "import warnings\n\g<0>",
    )

    count = s.replace(
        library / f"google/pubsub_{library.name}/services/subscriber/*client.py",
        r"""
    ([^\n\S]+(?:async\ )?def\ pull\(.*?->\ pubsub\.PullResponse:.*?)
    ((?P<indent>[^\n\S]+)\#\ Wrap\ the\ RPC\ method)
    """,
        textwrap.dedent(
            """
    \g<1>
    \g<indent>if request.return_immediately:
    \g<indent>    warnings.warn(
    \g<indent>        "The return_immediately flag is deprecated and should be set to False.",
    \g<indent>        category=DeprecationWarning,
    \g<indent>    )

    \g<2>"""
        ),
        flags=re.MULTILINE | re.DOTALL | re.VERBOSE,
    )

    if count != 2:
        raise Exception("Too many or too few replacements in pull() methods.")

    # Silence deprecation warnings in pull() method flattened parameter tests.
    s.replace(
        library / f"tests/unit/gapic/pubsub_{library.name}/test_subscriber.py",
        "import mock",
        "\g<0>\nimport warnings",
    )

    count = s.replace(
        library / f"tests/unit/gapic/pubsub_{library.name}/test_subscriber.py",
        textwrap.dedent(
            r"""
        ([^\n\S]+# Call the method with a truthy value for each flattened field,
        [^\n\S]+# using the keyword arguments to the method\.)
        \s+(client\.pull\(.*?\))"""
        ),
        """\n\g<1>
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=DeprecationWarning)
            \g<2>""",
        flags=re.MULTILINE | re.DOTALL,
    )

    if count < 1:
        raise Exception("Catch warnings replacement failed.")

    count = s.replace(
        library / f"tests/unit/gapic/pubsub_{library.name}/test_subscriber.py",
        textwrap.dedent(
            r"""
        ([^\n\S]+# Call the method with a truthy value for each flattened field,
        [^\n\S]+# using the keyword arguments to the method\.)
        \s+response = (await client\.pull\(.*?\))"""
        ),
        """\n\g<1>
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=DeprecationWarning)
            \g<2>""",
        flags=re.MULTILINE | re.DOTALL,
    )

    if count < 1:
        raise Exception("Catch warnings replacement failed.")

    # Make sure that client library version is present in user agent header.
    s.replace(
        [
            library
            / f"google/pubsub_{library.name}/services/publisher/async_client.py",
            library / f"google/pubsub_{library.name}/services/publisher/client.py",
            library
            / f"google/pubsub_{library.name}/services/publisher/transports/base.py",
            library
            / f"google/pubsub_{library.name}/services/schema_service/async_client.py",
            library / f"google/pubsub_{library.name}/services/schema_service/client.py",
            library
            / f"google/pubsub_{library.name}/services/schema_service/transports/base.py",
            library
            / f"google/pubsub_{library.name}/services/subscriber/async_client.py",
            library / f"google/pubsub_{library.name}/services/subscriber/client.py",
            library
            / f"google/pubsub_{library.name}/services/subscriber/transports/base.py",
        ],
        r"""gapic_version=(pkg_resources\.get_distribution\(\s+)['"]google-pubsub['"]""",
        "client_library_version=\g<1>'google-cloud-pubsub'",
    )

    # Docstrings of *_iam_policy() methods are formatted poorly and must be fixed
    # in order to avoid docstring format warnings in docs.
    s.replace(
        library / f"google/pubsub_{library.name}/services/*er/client.py",
        r"(\s+)Args:",
        "\n\g<1>Args:",
    )
    s.replace(
        library / f"google/pubsub_{library.name}/services/*er/client.py",
        r"(\s+)\*\*JSON Example\*\*\s+::",
        "\n\g<1>**JSON Example**::\n",
    )

    s.replace(
        library / f"google/pubsub_{library.name}/services/*er/client.py",
        r"(\s+)\*\*YAML Example\*\*\s+::",
        "\n\g<1>**YAML Example**::\n",
    )

    s.replace(
        library / f"google/pubsub_{library.name}/services/*er/client.py",
        r"(\s+)For a description of IAM and its features, see",
        "\n\g<0>",
    )

    # Allow timeout to be an instance of google.api_core.timeout.*
    s.replace(
        library / f"google/pubsub_{library.name}/types/__init__.py",
        r"from \.pubsub import \(",
        "from typing import Union\n\n\g<0>",
    )

    s.replace(
        library / f"google/pubsub_{library.name}/types/__init__.py",
        r"__all__ = \(\n",
        textwrap.dedent(
            '''\
            TimeoutType = Union[
                int,
                float,
                "google.api_core.timeout.ConstantTimeout",
                "google.api_core.timeout.ExponentialTimeout",
            ]
            """The type of the timeout parameter of publisher client methods."""

            \g<0>    "TimeoutType",'''
        ),
    )

    s.replace(
        library / f"google/pubsub_{library.name}/services/publisher/*client.py",
        r"from google.api_core import retry as retries.*\n",
        "\g<0>from google.api_core import timeout as timeouts  # type: ignore\n",
    )

    s.replace(
        library / f"google/pubsub_{library.name}/services/publisher/*client.py",
        f"from google\.pubsub_{library.name}\.types import pubsub",
        f"\g<0>\nfrom google.pubsub_{library.name}.types import TimeoutType",
    )

    s.replace(
        library / f"google/pubsub_{library.name}/services/publisher/*client.py",
        r"(\s+)timeout: float = None.*\n",
        f"\g<1>timeout: TimeoutType = gapic_{library.name}.method.DEFAULT,",
    )

    s.replace(
        library / f"google/pubsub_{library.name}/services/publisher/*client.py",
        r"([^\S\r\n]+)timeout \(float\): (.*)\n",
        ("\g<1>timeout (TimeoutType):\n" "\g<1>    \g<2>\n"),
    )

    # The namespace package declaration in google/cloud/__init__.py should be excluded
    # from coverage.
    count = s.replace(
        library / ".coveragerc",
        "google/pubsub/__init__.py",
        """google/cloud/__init__.py
    google/pubsub/__init__.py""",
    )

    if count < 1:
        raise Exception(".coveragerc replacement failed.")

    s.move(
        library,
        excludes=[
            "docs/**/*",
            "nox.py",
            "README.rst",
            "setup.py",
            f"google/cloud/pubsub_{library.name}/__init__.py",
            f"google/cloud/pubsub_{library.name}/types.py",
        ],
    )

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = gcp.CommonTemplates().py_library(
    microgenerator=True,
    samples=True,
    cov_level=100,
    system_test_external_dependencies=["psutil"],
)
s.move(templated_files, excludes=[".coveragerc"])

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------
python.py_samples()

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
