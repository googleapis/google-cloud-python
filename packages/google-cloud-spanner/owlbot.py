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
    s.replace(
        library / "google/cloud/spanner_admin_instance_v*/__init__.py",
        "from google.cloud.spanner_admin_instance import gapic_version as package_version",
        f"from google.cloud.spanner_admin_instance_{library.name} import gapic_version as package_version",
    )
    s.move(
        library,
        excludes=["google/cloud/spanner_admin_instance/**", "*.*", "docs/index.rst", "noxfile.py", "**/gapic_version.py", "testing/constraints-3.7.txt",],
    )

for library in get_staging_dirs(
    spanner_admin_database_default_version, "spanner_admin_database"
):
    s.replace(
        library / "google/cloud/spanner_admin_database_v*/__init__.py",
        "from google.cloud.spanner_admin_database import gapic_version as package_version",
        f"from google.cloud.spanner_admin_database_{library.name} import gapic_version as package_version",
    )
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
)
s.move(
    templated_files,
    excludes=[
        ".coveragerc",
        ".github/workflows",  # exclude gh actions as credentials are needed for tests
        "README.rst",
        ".github/release-please.yml",
        ".kokoro/test-samples-impl.sh",
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

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
