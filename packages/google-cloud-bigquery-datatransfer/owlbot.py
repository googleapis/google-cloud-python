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

import pathlib

import synthtool as s

from synthtool import gcp
from synthtool.languages import python


REPO_ROOT = pathlib.Path(__file__).parent.absolute()

common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate bigquery_datatransfer GAPIC layer
# ----------------------------------------------------------------------------
for library in s.get_staging_dirs("v1"):

    # Fix incorrect DeprecationWarning
    # Fixed in https://github.com/googleapis/gapic-generator-python/pull/943
    s.replace(
        "google/**/*client.py",
        "warnings\.DeprecationWarning",
        "DeprecationWarning"
    )

    s.move(library, excludes=["*.tar.gz", "docs/index.rst", "README.rst", "setup.py"])

s.remove_staging_dirs()


# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(microgenerator=True, samples=True, cov_level=99)
s.move(templated_files, excludes=[".coveragerc"])

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

python.py_samples(skip_readmes=True)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
for noxfile in REPO_ROOT.glob("samples/**/noxfile.py"):
    s.shell.run(["nox", "-s", "blacken"], cwd=noxfile.parent, hide_output=False)
