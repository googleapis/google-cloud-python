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
from synthtool import gcp
from synthtool.languages import python

common = gcp.CommonTemplates()

default_version = "v1"

for library in s.get_staging_dirs(default_version):
    # fix bad indentation
    s.replace(library / "google/**/*service.py",
        r"(\s+)settings resource.\n"
        r"\s+If empty all mutable fields will be updated.",
        r"\g<1>settings resource.\n"
        r"\g<1>If empty all mutable fields will be updated.",
    )

    # Comment out broken assertion in unit test
    # https://github.com/googleapis/gapic-generator-python/issues/897
    s.replace(
        library / "tests/**/*.py",
        "assert args\[0\]\.start_time == timestamp_pb2\.Timestamp\(seconds=751\)",
        "# assert args[0].start_time == timestamp_pb2.Timestamp(seconds=751)"
    )

    s.move(library, excludes=["README.rst", "docs/index.rst", "setup.py"])

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=True,
    microgenerator=True,  # set to True only if there are samples
    cov_level=98,
)
s.move(
    templated_files, excludes=[".coveragerc"]
)  # microgenerator has a good .coveragerc file

python.py_samples(skip_readmes=True)

# Remove the replacements below once
# https://github.com/googleapis/synthtool/pull/1188 is merged

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

s.replace("docs/conf.py", "master", "root")

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
