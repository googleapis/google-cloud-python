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

import re

import synthtool as s
from synthtool import gcp
from synthtool.languages import python

common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    microgenerator=True,
    default_python_version="3.10",
    system_test_python_versions=["3.10"],
)
s.move(templated_files, excludes=["docs/multiprocessing.rst", "README.rst"])

s.replace(
    ".github/workflows/lint.yml",
    'python-version: "3.8"',
    'python-version: "3.10"'
)

s.replace(
    ".kokoro/presubmit/presubmit.cfg",
    """# Format: //devtools/kokoro/config/proto/build.proto""",
    """# Format: //devtools/kokoro/config/proto/build.proto

env_vars: {
    key: "NOX_SESSION"
    value: "system blacken format"
}""",
)

python.py_samples(skip_readmes=True)

s.replace(
    "noxfile.py",
    """    # Use pre-release gRPC for system tests.
    # Exclude version 1.52.0rc1 which has a known issue.
    # See https://github.com/grpc/grpc/issues/32163
    session.install\("--pre", "grpcio!=1.52.0rc1"\)""",
    ""
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)

