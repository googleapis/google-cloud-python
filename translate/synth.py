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

gapic = gcp.GAPICGenerator()
common = gcp.CommonTemplates()
versions = ["v3beta1", "v3"]

excludes = [
    "setup.py",
    "nox*.py",
    "README.rst",
    "docs/conf.py",
    "docs/index.rst",
    "translation.py",
]

# ----------------------------------------------------------------------------
# Generate asset GAPIC layer
# ----------------------------------------------------------------------------
for version in versions:
    library = gapic.py_library("translate", version, include_protos=True)

    # s.move(library / f'google/cloud/translation_{version}', f'google/cloud/translate_{version}', excludes=excludes)
    s.move(library / f"google/cloud/translate_{version}", excludes=excludes)
    s.move(library / "tests")
    s.move(library / f"docs/gapic/{version}")

    # translation -> translate
    s.replace(
        "google/**/translation_service_pb2_grpc.py",
        f"google.cloud.translation_{version}.proto",
        f"google.cloud.translate_{version}.proto",
    )

# Use the highest version library to generate documentation import alias.
s.move(library / "google/cloud/translate.py")

s.replace(
    "google/cloud/**/translation_service_pb2.py",
    r"""record delimiters are ':raw-latex:`\\n`' instead of
          ':raw-latex:`\\r`:raw-latex:`\\n`'.""",
    r"""record delimiters are ``\\\\\\\\n`` instead of
          ``\\\\\\\\r\\\\\\\\n``.""",
)

# Fix docstring issue for classes with no summary line
s.replace(
    "google/cloud/**/proto/*_pb2.py",
    '''__doc__ = """Attributes:''',
    '''__doc__ = """
    Attributes:''',
)

# Fix wrapping for literal string
s.replace(
    "google/cloud/**/translation_service_pb2.py",
    r"""This field has the same length as \[``contents`
\s+`\]\[google\.cloud\.translation\.v3beta1\.TranslateTextRequest\.conte
\s+nts\]\.""",
    """This field has the same length as [``contents``][google.cloud.translation.v3beta1.TranslateTextRequest.contents].""",
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = gcp.CommonTemplates().py_library(unit_cov_level=100, cov_level=100)
s.move(templated_files)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
