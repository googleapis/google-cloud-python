# Copyright 2019 Google LLC
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
import re

import synthtool as s
from synthtool import gcp
from synthtool.languages import python

common = gcp.CommonTemplates()

default_version = "v1"

for library in s.get_staging_dirs(default_version):
    # Fix docstring with regex pattern that breaks docgen
    s.replace(library / "google/**/*client.py", "(/\^.*\$/)", "``\g<1>``")

    # Fix more regex in docstrings
    s.replace(library / "google/**/types/*.py",
        "(regex\s+)(/.*?/)\.",
        "\g<1>``\g<2>``.",
        flags=re.MULTILINE | re.DOTALL,
    )

    # Fix docstring with JSON example by wrapping with backticks
    s.replace(library / "google/**/types/recommendation.py",
        "( -  Example: )(\{.*?\})",
        "\g<1>``\g<2>``",
        flags=re.MULTILINE | re.DOTALL,
    )

    s.move(library, excludes=["docs/index.rst", "README.rst", "setup.py"])

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=False,  # set to True only if there are samples
    microgenerator=True,
    cov_level=98,
)
s.move(
    templated_files, excludes=[".coveragerc"]
)  # microgenerator has a good .coveragerc file

s.shell.run(["nox", "-s", "blacken"], hide_output=False)