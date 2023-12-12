# Copyright 2021 Google LLC
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
import re

from synthtool import gcp
import synthtool as s
from synthtool.languages import python

REPO_ROOT = pathlib.Path(__file__).parent.absolute()

common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    unit_test_python_versions=["3.9", "3.10", "3.11"],
    system_test_python_versions=["3.9", "3.11"],
    cov_level=35,
    intersphinx_dependencies={
        "pandas": "https://pandas.pydata.org/pandas-docs/stable/",
        "pydata-google-auth": "https://pydata-google-auth.readthedocs.io/en/latest/",
    },
)
s.move(
    templated_files,
    excludes=[
        # Multi-processing note isn't relevant, as bigframes is responsible for
        # creating clients, not the end user.
        "docs/multiprocessing.rst",
        "noxfile.py",
        ".pre-commit-config.yaml",
        "README.rst",
        "CONTRIBUTING.rst",
        ".github/release-trigger.yml",
        # BigQuery DataFrames manages its own Kokoro cluster for presubmit & continuous tests.
        ".kokoro/build.sh",
        ".kokoro/continuous/common.cfg",
        ".kokoro/presubmit/common.cfg",
    ],
)

# ----------------------------------------------------------------------------
# Fixup files
# ----------------------------------------------------------------------------

# Make sure build includes all necessary files.
s.replace(
    ["MANIFEST.in"],
    re.escape("recursive-include google"),
    "recursive-include third_party *\nrecursive-include bigframes",
)

# Even though BigQuery DataFrames isn't technically a client library, we are
# opting into Cloud RAD for docs hosting.
s.replace(
    [".kokoro/docs/common.cfg"],
    re.escape('value: "docs-staging-v2-staging"'),
    'value: "docs-staging-v2"',
)

# Use a custom table of contents since the default one isn't organized well
# enough for the number of classes we have.
s.replace(
    [".kokoro/publish-docs.sh"],
    (
        re.escape("# upload docs")
        + "\n"
        + re.escape(
            'python3 -m docuploader upload docs/_build/html/docfx_yaml --metadata-file docs.metadata --destination-prefix docfx --staging-bucket "${V2_STAGING_BUCKET}"'
        )
    ),
    (
        "# Replace toc.yml template file\n"
        + "mv docs/templates/toc.yml docs/_build/html/docfx_yaml/toc.yml\n\n"
        + "# upload docs\n"
        + 'python3 -m docuploader upload docs/_build/html/docfx_yaml --metadata-file docs.metadata --destination-prefix docfx --staging-bucket "${V2_STAGING_BUCKET}"'
    ),
)

# Fixup the documentation.
s.replace(
    ["docs/conf.py"],
    re.escape("Google Cloud Client Libraries for bigframes"),
    "BigQuery DataFrames provides DataFrame APIs on the BigQuery engine",
)

# Update the contributing guide to reflect some differences in this repo.
s.replace(
    ["CONTRIBUTING.rst"],
    re.escape("blacken"),
    "format",
)

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

python.py_samples(skip_readmes=True)

# ----------------------------------------------------------------------------
# Final cleanup
# ----------------------------------------------------------------------------

s.shell.run(["nox", "-s", "format"], hide_output=False)
