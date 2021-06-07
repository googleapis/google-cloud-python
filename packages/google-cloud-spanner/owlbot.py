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

# This is a customized version of the s.get_staging_dirs() function from synthtool to
# cater for copying 3 different folders from googleapis-gen
# which are spanner, spanner/admin/instance and spanner/admin/database.
# Source https://github.com/googleapis/synthtool/blob/master/synthtool/transforms.py#L280
def get_staging_dirs(
    default_version: Optional[str] = None, sub_directory: Optional[str] = None
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
    s.replace(library / f"google/cloud/spanner_{library.name}/types/transaction.py",
            r""".
        Attributes:""",
            r""".\n
        Attributes:""",
    )

    # Work around gapic generator bug https://github.com/googleapis/gapic-generator-python/issues/902
    s.replace(library / f"google/cloud/spanner_{library.name}/types/transaction.py",
            r""".
    Attributes:""",
            r""".\n
    Attributes:""",
    )

    # Remove headings from docstring. Requested change upstream in cl/377290854 due to https://google.aip.dev/192#formatting.
    s.replace(library / f"google/cloud/spanner_{library.name}/types/transaction.py",
        """\n    ==.*?==\n""",
        ":",
    )

    # Remove headings from docstring. Requested change upstream in cl/377290854 due to https://google.aip.dev/192#formatting.
    s.replace(library / f"google/cloud/spanner_{library.name}/types/transaction.py",
        """\n    --.*?--\n""",
        ":",
    )

    s.move(library, excludes=["google/cloud/spanner/**", "*.*", "docs/index.rst", "google/cloud/spanner_v1/__init__.py"])

for library in get_staging_dirs(spanner_admin_instance_default_version, "spanner_admin_instance"):
    s.move(library, excludes=["google/cloud/spanner_admin_instance/**", "*.*", "docs/index.rst"])

for library in get_staging_dirs(spanner_admin_database_default_version, "spanner_admin_database"):
    s.move(library, excludes=["google/cloud/spanner_admin_database/**", "*.*", "docs/index.rst"])

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(microgenerator=True, samples=True)
s.move(templated_files, excludes=[".coveragerc", "noxfile.py"])

# Ensure CI runs on a new instance each time
s.replace(
    ".kokoro/build.sh",
    "# Remove old nox",
    "# Set up creating a new instance for each system test run\n"
    "export GOOGLE_CLOUD_TESTS_CREATE_SPANNER_INSTANCE=true\n"
    "\n\g<0>",
)

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

python.py_samples()

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
