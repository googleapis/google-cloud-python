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

import synthtool as s
import synthtool.gcp as gcp
from synthtool.languages import python

# ----------------------------------------------------------------------------
# Copy the generated client from the owl-bot staging directory
# ----------------------------------------------------------------------------

default_version = "v1"

for library in s.get_staging_dirs(default_version):
    # work around bug in generator
    # `set_` is a reserved term in protobuf
    # https://github.com/googleapis/gapic-generator-python/issues/1348
    s.replace(
        library / "google/cloud/**/*.py",
        "set_ ",
        "set ",
    )

    # work around issue with generated docstring
    s.replace(
        library / "google/cloud/**/*.py",
        "A hostname may be prefixed with a wildcard label \(\*.\).",
        "A hostname may be prefixed with a wildcard label (\*.)."
    )

    s.replace(
        library / "google/cloud/**/*.py",
        """\"\*.""",
        """\"\*.""",
    )

    s.move(
        library, excludes=["setup.py", "README.rst", "google/cloud/network_services"]
    )
s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------

templated_files = gcp.CommonTemplates().py_library(
    microgenerator=True,
    versions=gcp.common.detect_versions(path="./google", default_first=True),
)
s.move(
    templated_files, excludes=[".coveragerc"]
)  # the microgenerator has a good coveragerc file

python.py_samples(skip_readmes=True)

# ----------------------------------------------------------------------------
# Run blacken session
# ----------------------------------------------------------------------------

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
