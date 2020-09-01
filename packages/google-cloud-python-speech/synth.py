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

import synthtool as s
from synthtool import gcp
from synthtool.languages import python

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()
versions = ["v1p1beta1", "v1"]


# ----------------------------------------------------------------------------
# Generate speech GAPIC layer
# ----------------------------------------------------------------------------
for version in versions:
    library = gapic.py_library(
        service="speech",
        version=version,
        bazel_target=f"//google/cloud/speech/{version}:speech-{version}-py",
        include_protos=True,
    )

    # Don't move over __init__.py, as we modify it to make the generated client
    # use helpers.py.
    s.move(library / f"google/cloud/speech_{version}/types.py")
    s.move(library / f"google/cloud/speech_{version}/gapic")
    s.move(library / f"google/cloud/speech_{version}/proto")
    s.move(library / f"tests/unit/gapic/{version}")
    s.move(library / f"docs/gapic/{version}")
    s.move(library / f"samples")


# Use the highest version library to generate documentation import alias.
s.move(library / "google/cloud/speech.py")


# Fix tests to use the direct gapic client instead of the wrapped helper
# client.
s.replace(
    "tests/unit/**/test*client*.py",
    r"from google\.cloud import speech_(.+?)$",
    r"from google.cloud.speech_\1.gapic import speech_client as speech_\1",
)


# Fix bad docstring
s.replace(
    "google/**/resource_pb2.py",
    """``\\\\ ``e\.g\.``\\\\
    \$MONTH\\\\ ``\.""",
    """``\ ``e.g.``\$MONTH\ ``."""
)

s.replace(
    "google/**/resource_pb2.py",
    """\(e\.g\. ``\\\\ \{my-
    months\}`\)\.""",
    """(e.g. ``\ {my-months}``)."""
)
# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(cov_level=87, samples=True)
s.move(templated_files)

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

python.py_samples()


# TODO(busunkim): Use latest sphinx after microgenerator transition
s.replace("noxfile.py", """['"]sphinx['"]""", '"sphinx<3.0.0"')


s.shell.run(["nox", "-s", "blacken"], hide_output=False)
