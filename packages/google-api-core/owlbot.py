# Copyright 2020 Google LLC
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
from synthtool import gcp

common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
excludes = [
    "noxfile.py",  # pytype
    "setup.cfg",  # pytype
    ".flake8",  # flake8-import-order, layout
    ".coveragerc",  # layout
    "CONTRIBUTING.rst",  # no systests
]
templated_files = common.py_library(microgenerator=True, cov_level=100)
s.move(templated_files, excludes=excludes)

# Add pytype support
s.replace(
    ".gitignore",
    """\
.pytest_cache
""",
    """\
.pytest_cache
.pytype
""",
)

# Remove the replacements below once https://github.com/googleapis/synthtool/pull/1188 is merged

# Update googleapis/repo-automation-bots repo to main in .kokoro/*.sh files
s.replace(
    ".kokoro/*.sh", "repo-automation-bots/tree/master", "repo-automation-bots/tree/main"
)

# Customize CONTRIBUTING.rst to replace master with main
s.replace(
    "CONTRIBUTING.rst",
    "fetch and merge changes from upstream into master",
    "fetch and merge changes from upstream into main",
)

s.replace(
    "CONTRIBUTING.rst", "git merge upstream/master", "git merge upstream/main",
)

s.replace(
    "CONTRIBUTING.rst",
    """export GOOGLE_CLOUD_TESTING_BRANCH=\"master\"""",
    """export GOOGLE_CLOUD_TESTING_BRANCH=\"main\"""",
)

s.replace(
    "CONTRIBUTING.rst", r"remote \(``master``\)", "remote (``main``)",
)

s.replace(
    "CONTRIBUTING.rst", "blob/master/CONTRIBUTING.rst", "blob/main/CONTRIBUTING.rst",
)

s.replace(
    "CONTRIBUTING.rst", "blob/master/noxfile.py", "blob/main/noxfile.py",
)

s.replace(
    "docs/conf.py", "master_doc", "root_doc",
)

s.replace(
    "docs/conf.py", "# The master toctree document.", "# The root toctree document.",
)


s.shell.run(["nox", "-s", "blacken"], hide_output=False)
