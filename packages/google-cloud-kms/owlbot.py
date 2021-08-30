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
from synthtool.languages import python
import logging

logging.basicConfig(level=logging.DEBUG)

common = gcp.CommonTemplates()

default_version = "v1"

for library in s.get_staging_dirs(default_version):
    # Escape single '_' which RST treats as target names
    s.replace(library / "google/**/resources.py", '''"(.*?)((SIGN)|(DECRYPT)|(HMAC))_"''', '''"\g<1>\g<2>\_"''')

    # Docstrings of *_iam_policy() methods are formatted poorly and must be fixed
    # in order to avoid docstring format warnings in docs.
    s.replace(library / "google/**/*client.py",
        r"(\s+)Args:",
        "\n\g<1>Args:"
    )
    s.replace(library / "google/**/*client.py",
        r"(\s+)\*\*JSON Example\*\*\s+::",
        "\n\g<1>**JSON Example**::\n",
    )
    s.replace(library / "google/**/*client.py",
        r"(\s+)\*\*YAML Example\*\*\s+::",
        "\n\g<1>**YAML Example**::\n",
    )
    s.replace(library / "google/**/*client.py",
        r"(\s+)For a description of IAM and its features, see",
        "\n\g<0>",
    )

    # Rename `format_` to `format` to avoid breaking change
    s.replace(library / "google/**/types/*.py",
        "format_",
        "format"
    )

    s.move(library, excludes=["README.rst", "setup.py", "nox*.py", "docs/index.rst"])

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    cov_level=98,
    samples=True,
    microgenerator=True,
)
s.move(templated_files, excludes=[".coveragerc"])  # microgenerator has a good .coveragerc file

# Remove the replacements below once https://github.com/googleapis/synthtool/pull/1188 is merged

# Update googleapis/repo-automation-bots repo to main in .kokoro/*.sh files
s.replace(".kokoro/*.sh", "repo-automation-bots/tree/master", "repo-automation-bots/tree/main")

# Customize CONTRIBUTING.rst to replace master with main
s.replace(
    "CONTRIBUTING.rst",
    "fetch and merge changes from upstream into master",
    "fetch and merge changes from upstream into main",
)

s.replace(
    "CONTRIBUTING.rst",
    "git merge upstream/master",
    "git merge upstream/main",
)

s.replace(
    "CONTRIBUTING.rst",
    """export GOOGLE_CLOUD_TESTING_BRANCH=\"master\"""",
    """export GOOGLE_CLOUD_TESTING_BRANCH=\"main\"""",
)

s.replace(
    "CONTRIBUTING.rst",
    "remote \(``master``\)",
    "remote (``main``)",
)

s.replace(
    "CONTRIBUTING.rst",
    "blob/master/CONTRIBUTING.rst",
    "blob/main/CONTRIBUTING.rst",
)

s.replace(
    "CONTRIBUTING.rst",
    "blob/master/noxfile.py",
    "blob/main/noxfile.py",
)

s.replace(
    "docs/conf.py",
    "master_doc",
    "root_doc",
)

s.replace(
    "docs/conf.py",
    "# The master toctree document.",
    "# The root toctree document.",
)

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

sample_files = common.py_samples(unit_cov_level=97, cov_level=99, samples=True)
s.move(sample_files, excludes=['noxfile.py'])

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
