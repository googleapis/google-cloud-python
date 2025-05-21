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
import textwrap

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
                    ("grpc.max_metadata_size", 4 * 1024 * 1024),
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
        library / f"google/pubsub_{library.name}/services/schema_service/client.py",
    ]
    err_msg = (
        "Expected replacements for gRPC channel to use with the emulator not made."
    )

    count = s.replace(clients_to_patch, r"import os", "import functools\n\g<0>")

    if count < len(clients_to_patch):
        raise Exception(err_msg)

    count = s.replace(
        clients_to_patch,
        f"from \.transports\.base",
        "\nimport grpc\n\g<0>",
    )

    if count < len(clients_to_patch):
        raise Exception(err_msg)

    # TODO(https://github.com/googleapis/python-pubsub/issues/1349): Move the emulator
    # code below to test files.
    count = s.replace(
        clients_to_patch,
        r"# initialize with the provided callable or the passed in class",
        """\g<0>

            emulator_host = os.environ.get("PUBSUB_EMULATOR_HOST")
            if emulator_host:
                if issubclass(transport_init, type(self)._transport_registry["grpc"]):
                    channel = grpc.insecure_channel(target=emulator_host)
                else:
                    channel = grpc.aio.insecure_channel(target=emulator_host)
                transport_init = functools.partial(transport_init, channel=channel)

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
        r"from google.pubsub_v1 import gapic_version as package_version",
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
        "import os",
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
    count = s.replace(
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
        r"""gapic_version=package_version.__version__""",
        "client_library_version=package_version.__version__",
    )

    if count < 1:
        raise Exception("client_library_version replacement failed.")

    # Allow timeout to be an instance of google.api_core.timeout.*
    count = s.replace(
        library / f"google/pubsub_{library.name}/types/__init__.py",
        r"from \.pubsub import \(",
        "from typing import Union\n\n\g<0>",
    )

    if count < 1:
        raise Exception("Catch timeout replacement 1 failed.")

    count = s.replace(
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

    if count < 1:
        raise Exception("Catch timeout replacement 2 failed.")

    count = s.replace(
        library / f"google/pubsub_{library.name}/services/publisher/*client.py",
        r"from google.api_core import retry as retries.*\n",
        "\g<0>from google.api_core import timeout as timeouts  # type: ignore\n",
    )

    if count < 1:
        raise Exception("Catch timeout replacement 3 failed.")

    count = s.replace(
        library / f"google/pubsub_{library.name}/services/publisher/*client.py",
        f"from google\.pubsub_{library.name}\.types import pubsub",
        f"\g<0>\nfrom google.pubsub_{library.name}.types import TimeoutType",
    )

    if count < 1:
        raise Exception("Catch timeout replacement 4 failed.")

    count = s.replace(
        library / f"google/pubsub_{library.name}/services/publisher/*client.py",
        r"(\s+)timeout: Union\[float, object\] = gapic_v1.method.DEFAULT.*\n",
        f"\g<1>timeout: TimeoutType = gapic_{library.name}.method.DEFAULT,",
    )

    if count < 1:
        raise Exception("Catch timeout replacement 5 failed.")

    count = s.replace(
        library / f"google/pubsub_{library.name}/services/publisher/*client.py",
        r"([^\S\r\n]+)timeout \(float\): (.*)\n",
        ("\g<1>timeout (TimeoutType):\n" "\g<1>    \g<2>\n"),
    )

    if count < 1:
        raise Exception("Catch timeout replacement 6 failed.")

    # Override the default max retry deadline for publisher methods.
    count = s.replace(
        library / f"google/pubsub_{library.name}/services/publisher/transports/base.py",
        r"deadline=60\.0",
        "deadline=600.0",
    )
    if count < 9:
        raise Exception(
            "Default retry deadline not overriden for all publisher methods."
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

    s.move([library], excludes=["**/gapic_version.py", "noxfile.py", "README.rst", "docs/**/*", "setup.py", "testing/constraints-3.7.txt", "testing/constraints-3.8.txt"])
s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------

templated_files = gcp.CommonTemplates().py_library(
    microgenerator=True,
    samples=True,
    cov_level=99,
    versions=gcp.common.detect_versions(path="./google", default_first=True),
    unit_test_python_versions=["3.7", "3.8", "3.9", "3.10", "3.11", "3.12", "3.13"],
    unit_test_dependencies=["flaky"],
    system_test_python_versions=["3.12"],
    system_test_external_dependencies=["psutil","flaky"],
)
s.move(templated_files, excludes=[".coveragerc", ".github/blunderbuss.yml", ".github/release-please.yml", "README.rst", "docs/index.rst"])

python.py_samples(skip_readmes=True)

# run format session for all directories which have a noxfile
for noxfile in Path(".").glob("**/noxfile.py"):
    s.shell.run(["nox", "-s", "blacken"], cwd=noxfile.parent, hide_output=False)
