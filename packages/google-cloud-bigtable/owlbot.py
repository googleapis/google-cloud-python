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
# cater for copying 2 different folders from googleapis-gen
# which are bigtable and bigtable/admin.
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

# This library ships clients for two different APIs,
# BigTable and BigTable Admin
bigtable_default_version = "v2"
bigtable_admin_default_version = "v2"

for library in get_staging_dirs(bigtable_default_version, "bigtable"):
    s.move(library / "google/cloud/bigtable_v*")
    s.move(library / "tests")
    s.move(library / "scripts")

for library in get_staging_dirs(bigtable_admin_default_version, "bigtable_admin"):
    s.move(library / "google/cloud/bigtable_admin_v*")
    s.move(library / "tests")
    s.move(library / "scripts")

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=True,  # set to True only if there are samples
    microgenerator=True,
    cov_level=99
)

s.move(templated_files, excludes=[".coveragerc", "noxfile.py"])

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

sample_files = common.py_samples(samples=True)
for path in sample_files:
    s.move(path, excludes=['noxfile.py'])


s.shell.run(["nox", "-s", "blacken"], hide_output=False)
