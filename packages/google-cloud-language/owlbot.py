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
    # Work around generator issue https://github.com/googleapis/gapic-generator-python/issues/902
    s.replace(library / f"google/cloud/language_{library.name}/types/language_service.py",
        r"""Represents the input to API methods.
    Attributes:""",
        r"""Represents the input to API methods.\n
    Attributes:""")

    s.move(library, excludes=["docs/index.rst", "README.rst", "setup.py"])

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(cov_level=98, samples=True, microgenerator=True,)

s.move(templated_files, excludes=['.coveragerc'])

s.shell.run(["nox", "-s", "blacken"], hide_output=False)

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

python.py_samples(skip_readmes=True)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
