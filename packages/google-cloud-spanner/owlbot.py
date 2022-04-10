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
from typing import List, Optional

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

for library in get_staging_dirs(spanner_default_version, "spanner"):
    # Work around gapic generator bug https://github.com/googleapis/gapic-generator-python/issues/902
    s.replace(
        library / f"google/cloud/spanner_{library.name}/types/transaction.py",
        r""".
        Attributes:""",
        r""".\n
        Attributes:""",
    )

    # Work around gapic generator bug https://github.com/googleapis/gapic-generator-python/issues/902
    s.replace(
        library / f"google/cloud/spanner_{library.name}/types/transaction.py",
        r""".
    Attributes:""",
        r""".\n
    Attributes:""",
    )

    # Remove headings from docstring. Requested change upstream in cl/377290854 due to https://google.aip.dev/192#formatting.
    s.replace(
        library / f"google/cloud/spanner_{library.name}/types/transaction.py",
        """\n    ==.*?==\n""",
        ":",
    )

    # Remove headings from docstring. Requested change upstream in cl/377290854 due to https://google.aip.dev/192#formatting.
    s.replace(
        library / f"google/cloud/spanner_{library.name}/types/transaction.py",
        """\n    --.*?--\n""",
        ":",
    )

    s.move(
        library,
        excludes=[
            "google/cloud/spanner/**",
            "*.*",
            "docs/index.rst",
            "google/cloud/spanner_v1/__init__.py",
        ],
    )

for library in get_staging_dirs(
    spanner_admin_instance_default_version, "spanner_admin_instance"
):
    s.move(
        library,
        excludes=["google/cloud/spanner_admin_instance/**", "*.*", "docs/index.rst"],
    )

for library in get_staging_dirs(
    spanner_admin_database_default_version, "spanner_admin_database"
):
    s.move(
        library,
        excludes=["google/cloud/spanner_admin_database/**", "*.*", "docs/index.rst"],
    )

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    microgenerator=True,
    samples=True,
    cov_level=99,
    split_system_tests=True,
    system_test_extras=["tracing"],
)
s.move(
    templated_files,
    excludes=[
        ".coveragerc",
        ".github/workflows",  # exclude gh actions as credentials are needed for tests
    ],
)

# Ensure CI runs on a new instance each time
s.replace(
    ".kokoro/build.sh",
    "# Remove old nox",
    """\
# Set up creating a new instance for each system test run
export GOOGLE_CLOUD_TESTS_CREATE_SPANNER_INSTANCE=true

# Remove old nox""",
)

# Update samples folder in CONTRIBUTING.rst
s.replace("CONTRIBUTING.rst", "samples/snippets", "samples/samples")

python.configure_previous_major_version_branches()
# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

python.py_samples()

# ----------------------------------------------------------------------------
# Customize noxfile.py
# ----------------------------------------------------------------------------


def place_before(path, text, *before_text, escape=None):
    replacement = "\n".join(before_text) + "\n" + text
    if escape:
        for c in escape:
            text = text.replace(c, "\\" + c)
    s.replace([path], text, replacement)


open_telemetry_test = """
    # XXX Work around Kokoro image's older pip, which borks the OT install.
    session.run("pip", "install", "--upgrade", "pip")
    session.install("-e", ".[tracing]", "-c", constraints_path)
    # XXX: Dump installed versions to debug OT issue
    session.run("pip", "list")

    # Run py.test against the unit tests with OpenTelemetry.
    session.run(
        "py.test",
        "--quiet",
        "--cov=google.cloud.spanner",
        "--cov=google.cloud",
        "--cov=tests.unit",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=",
        "--cov-fail-under=0",
        os.path.join("tests", "unit"),
        *session.posargs,
    )
"""

place_before(
    "noxfile.py",
    "@nox.session(python=UNIT_TEST_PYTHON_VERSIONS)",
    open_telemetry_test,
    escape="()",
)

skip_tests_if_env_var_not_set = """# Sanity check: Only run tests if the environment variable is set.
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "") and not os.environ.get(
        "SPANNER_EMULATOR_HOST", ""
    ):
        session.skip(
            "Credentials or emulator host must be set via environment variable"
        )
"""

place_before(
    "noxfile.py",
    "# Install pyopenssl for mTLS testing.",
    skip_tests_if_env_var_not_set,
    escape="()",
)

s.replace(
    "noxfile.py",
    """f"--junitxml=unit_{session.python}_sponge_log.xml",
        "--cov=google",
        "--cov=tests/unit",""",
    """\"--cov=google.cloud.spanner",
        "--cov=google.cloud",
        "--cov=tests.unit",""",
)

s.replace(
    "noxfile.py",
    r"""session.install\("-e", "."\)""",
    """session.install("-e", ".[tracing]")""",
)

s.replace(
    "noxfile.py",
    r"""# Install all test dependencies, then install this package into the
    # virtualenv's dist-packages.
    session.install\("mock", "pytest", "google-cloud-testutils", "-c", constraints_path\)
    session.install\("-e", ".", "-c", constraints_path\)""",
    """# Install all test dependencies, then install this package into the
    # virtualenv's dist-packages.
    session.install("mock", "pytest", "google-cloud-testutils", "-c", constraints_path)
    session.install("-e", ".[tracing]", "-c", constraints_path)""",
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
