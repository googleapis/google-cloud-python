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

from pathlib import Path
from typing import List, Optional

import shutil
import synthtool as s
from synthtool.gcp.common import CommonTemplates, detect_versions
from synthtool.languages import python


# This is a customized version of the s.get_staging_dirs() function from synthtool to
# cater for copying 2 different folders from googleapis-gen
# which are workflows and workflows/executions
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
# IAM and IAM credentials
iam_credentials_default_version = "v1"
iam_default_version = "v2beta"

for library in get_staging_dirs(iam_default_version, "iam"):
    s.move([library], excludes=["setup.py", "README.rst", "docs/index.rst", "google/cloud/iam/**",])

for library in get_staging_dirs(iam_credentials_default_version, "iamcredentials"):
    s.move([library], excludes=["setup.py", "README.rst", "docs/index.rst"])

s.remove_staging_dirs()

templated_files = CommonTemplates().py_library(
    microgenerator=True,
    versions=detect_versions(path="./google", default_first=True),
)
s.move(
    [templated_files], excludes=[".coveragerc"]
)  # the microgenerator has a good coveragerc file

python.py_samples(skip_readmes=True)

# run format nox session for all directories which have a noxfile
for noxfile in Path(".").glob("**/noxfile.py"):
    s.shell.run(["nox", "-s", "format"], cwd=noxfile.parent, hide_output=False)

python.configure_previous_major_version_branches()