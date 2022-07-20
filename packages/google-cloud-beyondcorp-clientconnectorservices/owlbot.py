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

import synthtool as s
import synthtool.gcp as gcp
from synthtool.languages import python

# ----------------------------------------------------------------------------
# Copy the generated client from the owl-bot staging directory
# ----------------------------------------------------------------------------

default_version = "v1"

for library in s.get_staging_dirs(default_version):
    # work around issues with docstrings
    s.replace(
        library / "google/cloud/**/*.py",
        """resource.
                \*\*JSON Example\*\*
                ::""",
        """resource. JSON Example.

                .. code-block:: python\n""",
    )

    s.replace(
        library / "google/cloud/**/*.py",
        """\*\*YAML Example\*\*
                ::""",
        """\n                **YAML Example**

                ::\n""",
    )

    s.replace(library / "google/cloud/**/*.py",
        """                For a description of IAM and its features, see the `IAM
                developer's""",
        """\n                For a description of IAM and its features, see the `IAM
                developer's"""
    )
    s.replace(library / "google/cloud/**/*.py","\n    ------------\n\n   ",":")
    s.replace(library / "google/cloud/**/*.py","\n    ----------\n\n   ",":")
    s.move(library, excludes=["google/cloud/beyondcorp_clientconnectorservices", "setup.py"])
s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------

templated_files = gcp.CommonTemplates().py_library(
    cov_level=98,
    microgenerator=True,
    versions=gcp.common.detect_versions(path="./google", default_first=True),
)
s.move(templated_files, excludes=[".coveragerc"]) # the microgenerator has a good coveragerc file

python.py_samples(skip_readmes=True)


# run blacken session for all directories which have a noxfile
for noxfile in Path(".").glob("**/noxfile.py"):
    s.shell.run(["nox", "-s", "blacken"], cwd=noxfile.parent, hide_output=False)
