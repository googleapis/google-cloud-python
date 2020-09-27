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

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()
versions = ["v1beta2", "v1"]


# ----------------------------------------------------------------------------
# Generate language GAPIC layer
# ----------------------------------------------------------------------------
for version in versions:
    library = gapic.py_library(
        service="language",
        version=version,
        bazel_target=f"//google/cloud/language/{version}:language-{version}-py",
        include_protos=True,
    )

    s.move(library / f"google/cloud/language_{version}/proto")
    s.move(library / f"google/cloud/language_{version}/gapic")
    s.move(library / f"tests/unit/gapic/{version}")
    s.move(library / f"tests/system/gapic/{version}")
    s.move(library / f"samples")

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=97, cov_level=100, samples=True)

s.move(templated_files, excludes=['noxfile.py'])

s.replace("google/cloud/**/language_service_pb2.py",
'''__doc__ = """################################################################
  #
  
  Represents the input to API methods.''',
'''__doc__="""Represents the input to API methods.'''
)
s.replace(
    f"google/cloud/**/gapic/language_service_client.py",
    r"types\.EncodingType",
    "enums.EncodingType",
)

# TODO(busunkim): Use latest sphinx after microgenerator transition
s.replace("noxfile.py", """['"]sphinx['"]""", '"sphinx<3.0.0"')

s.shell.run(["nox", "-s", "blacken"], hide_output=False)

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

python.py_samples(skip_readmes=True)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)