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

from pathlib import Path
import shutil
from typing import List, Optional
import re

import synthtool as s
from synthtool import gcp
from synthtool.languages import python

common = gcp.CommonTemplates()


def get_staging_dirs(
    # This is a customized version of the s.get_staging_dirs() function
    # from synthtool to # cater for copying 3 different folders from
    # googleapis-gen:
    # spanner, spanner/admin/instance and spanner/admin/database.
    # Source:
    # https://github.com/googleapis/synthtool/blob/master/synthtool/transforms.py#L280
    default_version: Optional[str] = None,
    sub_directory: Optional[str] = None,
) -> List[Path]:
    """Returns the list of directories, one per version, copied from
    https://github.com/googleapis/googleapis-gen. Will return in lexical sorting
    order with the exception of the default_version which will be last (if specified).

    Args:
      default_version (str): the default version of the API. The directory for this version
        will be the last item in the returned list if specified.
      sub_directory (str): if a `sub_directory` is provided, only the directories within the
        specified `sub_directory` will be returned.

    Returns: the empty list if no file were copied.
    """

    staging = Path("owl-bot-staging")

    if sub_directory:
        staging /= sub_directory

    if staging.is_dir():
        # Collect the subdirectories of the staging directory.
        versions = [v.name for v in staging.iterdir() if v.is_dir()]
        # Reorder the versions so the default version always comes last.
        versions = [v for v in versions if v != default_version]
        versions.sort()
        if default_version is not None:
            versions += [default_version]
        dirs = [staging / v for v in versions]
        for dir in dirs:
            s._tracked_paths.add(dir)
        return dirs
    else:
        return []


spanner_default_version = "v1"
spanner_admin_instance_default_version = "v1"
spanner_admin_database_default_version = "v1"

clean_up_generated_samples = True

for library in get_staging_dirs(spanner_default_version, "spanner"):
    if clean_up_generated_samples:
        shutil.rmtree("samples/generated_samples", ignore_errors=True)
        clean_up_generated_samples = False

    # Customization for MetricsInterceptor

    assert 6 == s.replace(
        [
            library / "google/cloud/spanner_v1/services/spanner/transports/*.py",
            library / "google/cloud/spanner_v1/services/spanner/client.py",
        ],
        """from google.cloud.spanner_v1.types import transaction""",
        """from google.cloud.spanner_v1.types import transaction
from google.cloud.spanner_v1.metrics.metrics_interceptor import MetricsInterceptor""",
    )

    assert 1 == s.replace(
        library / "google/cloud/spanner_v1/services/spanner/transports/*.py",
        """api_audience: Optional\[str\] = None,
            \*\*kwargs,
            \) -> None:
        \"\"\"Instantiate the transport.""",
"""api_audience: Optional[str] = None,
            metrics_interceptor: Optional[MetricsInterceptor] = None,
            **kwargs,
    ) -> None:
        \"\"\"Instantiate the transport."""
    )

    assert 4 == s.replace(
        library / "google/cloud/spanner_v1/services/spanner/transports/*.py",
        """api_audience: Optional\[str\] = None,
            \) -> None:
        \"\"\"Instantiate the transport.""",
"""api_audience: Optional[str] = None,
            metrics_interceptor: Optional[MetricsInterceptor] = None,
    ) -> None:
        \"\"\"Instantiate the transport."""
    )

    assert 1 == s.replace(
        library / "google/cloud/spanner_v1/services/spanner/transports/grpc.py",
        """\)\n\n        self._interceptor = _LoggingClientInterceptor\(\)""",
        """)

        # Wrap the gRPC channel with the metric interceptor
        if metrics_interceptor is not None:
            self._metrics_interceptor = metrics_interceptor
            self._grpc_channel = grpc.intercept_channel(
                self._grpc_channel, metrics_interceptor
            )

        self._interceptor = _LoggingClientInterceptor()"""
    )

    assert 1 == s.replace(
        library / "google/cloud/spanner_v1/services/spanner/transports/grpc.py",
        """self._stubs: Dict\[str, Callable\] = \{\}\n\n        if api_mtls_endpoint:""",
        """self._stubs: Dict[str, Callable] = {}
        self._metrics_interceptor = None

        if api_mtls_endpoint:"""
    )

    assert 1 == s.replace(
        library / "google/cloud/spanner_v1/services/spanner/client.py",
        """# initialize with the provided callable or the passed in class
            self._transport = transport_init\(
                credentials=credentials,
                credentials_file=self._client_options.credentials_file,
                host=self._api_endpoint,
                scopes=self._client_options.scopes,
                client_cert_source_for_mtls=self._client_cert_source,
                quota_project_id=self._client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=True,
                api_audience=self._client_options.api_audience,
            \)""",
            """# initialize with the provided callable or the passed in class
            self._transport = transport_init(
                credentials=credentials,
                credentials_file=self._client_options.credentials_file,
                host=self._api_endpoint,
                scopes=self._client_options.scopes,
                client_cert_source_for_mtls=self._client_cert_source,
                quota_project_id=self._client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=True,
                api_audience=self._client_options.api_audience,
                metrics_interceptor=MetricsInterceptor(),
            )""",
    )

    assert 12 == s.replace(
        library / "tests/unit/gapic/spanner_v1/test_spanner.py",
        """api_audience=None,\n(\s+)\)""",
        """api_audience=None,
            metrics_interceptor=mock.ANY,
        )"""
    )

    assert 1 == s.replace(
        library / "tests/unit/gapic/spanner_v1/test_spanner.py",
        """api_audience="https://language.googleapis.com"\n(\s+)\)""",
        """api_audience="https://language.googleapis.com",
            metrics_interceptor=mock.ANY,
        )"""
    )

    count = s.replace(
        [
            library / "google/cloud/spanner_v1/services/*/transports/grpc*",
            library / "tests/unit/gapic/spanner_v1/*",
        ],
        "^\s+options=\\[.*?\\]",
        """options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                    ("grpc.keepalive_time_ms", 120000),
                ]""",
        flags=re.MULTILINE | re.DOTALL,
    )
    if count < 1:
        raise Exception("Expected replacements for gRPC channel options not made.")

    s.move(
        library,
        excludes=[
            "google/cloud/spanner/**",
            "*.*",
            "noxfile.py",
            "docs/index.rst",
            "google/cloud/spanner_v1/__init__.py",
            "**/gapic_version.py",
            "testing/constraints-3.7.txt",
        ],
    )

for library in get_staging_dirs(
    spanner_admin_instance_default_version, "spanner_admin_instance"
):
    count = s.replace(
        [
            library / "google/cloud/spanner_admin_instance_v1/services/*/transports/grpc*",
            library / "tests/unit/gapic/spanner_admin_instance_v1/*",
        ],
        "^\s+options=\\[.*?\\]",
        """options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                    ("grpc.keepalive_time_ms", 120000),
                ]""",
        flags=re.MULTILINE | re.DOTALL,
    )
    if count < 1:
        raise Exception("Expected replacements for gRPC channel options not made.")
    s.move(
        library,
        excludes=["google/cloud/spanner_admin_instance/**", "*.*", "docs/index.rst", "noxfile.py", "**/gapic_version.py", "testing/constraints-3.7.txt",],
    )

for library in get_staging_dirs(
    spanner_admin_database_default_version, "spanner_admin_database"
):
    count = s.replace(
        [
            library / "google/cloud/spanner_admin_database_v1/services/*/transports/grpc*",
            library / "tests/unit/gapic/spanner_admin_database_v1/*",
        ],
        "^\s+options=\\[.*?\\]",
        """options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                    ("grpc.keepalive_time_ms", 120000),
                ]""",
        flags=re.MULTILINE | re.DOTALL,
    )
    if count < 1:
        raise Exception("Expected replacements for gRPC channel options not made.")
    s.move(
        library,
        excludes=["google/cloud/spanner_admin_database/**", "*.*", "docs/index.rst", "noxfile.py", "**/gapic_version.py", "testing/constraints-3.7.txt",],
    )

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    microgenerator=True,
    samples=True,
    cov_level=98,
    split_system_tests=True,
    system_test_extras=["tracing"],
    system_test_python_versions=["3.12"]
)
s.move(
    templated_files,
    excludes=[
        ".coveragerc",
        ".github/workflows",  # exclude gh actions as credentials are needed for tests
        "README.rst",
        ".github/release-please.yml",
        ".kokoro/test-samples-impl.sh",
        ".kokoro/presubmit/presubmit.cfg",
        ".kokoro/samples/python3.7/**",
        ".kokoro/samples/python3.8/**",
    ],
)

# Ensure CI runs on a new instance each time
s.replace(
    ".kokoro/build.sh",
    "# Setup project id.",
    """\
# Set up creating a new instance for each system test run
export GOOGLE_CLOUD_TESTS_CREATE_SPANNER_INSTANCE=true

# Setup project id.""",
)

# Update samples folder in CONTRIBUTING.rst
s.replace("CONTRIBUTING.rst", "samples/snippets", "samples/samples")

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

python.py_samples()

s.replace(
    "samples/**/noxfile.py",
    'BLACK_VERSION = "black==22.3.0"',
    'BLACK_VERSION = "black==23.7.0"',
)
s.replace(
    "samples/**/noxfile.py",
    r'ALL_VERSIONS = \["3.7", "3.8", "3.9", "3.10", "3.11", "3.12", "3.13"\]',
    'ALL_VERSIONS = ["3.9", "3.10", "3.11", "3.12", "3.13"]',
)

# Use a python runtime which is available in the owlbot post processor here
# https://github.com/googleapis/synthtool/blob/master/docker/owlbot/python/Dockerfile
s.shell.run(["nox", "-s", "blacken-3.10"], hide_output=False)
