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
import logging
import re

import synthtool as s

from synthtool import gcp
from synthtool.languages import python

logging.basicConfig(level=logging.DEBUG)

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()
versions = ["v1beta2", "v1p1beta1", "v1p2beta1", "v1p3beta1", "v1"]


# ----------------------------------------------------------------------------
# Generate videointelligence GAPIC layer
# ----------------------------------------------------------------------------
for version in versions:
    library = gapic.py_library(
        service="videointelligence",
        version=version,
        bazel_target=f"//google/cloud/videointelligence/{version}:videointelligence-{version}-py",
        include_protos=True,
    )

    # TODO: stop excluding tests and nox.py (excluded as we lack system tests)
    s.move(
        library,
        excludes=[
            "setup.py",
            "nox*.py",
            "README.rst",
            "docs/index.rst",
            f"tests/system/gapic/{version}/"
            f"test_system_video_intelligence_service_{version}.py",
            # f'tests/unit/gapic/{version}/'
            # f'test_video_intelligence_service_client_{version}.py',
        ],
    )
    s.replace(
        f"google/cloud/videointelligence_{version}/gapic/"
        f"*video_intelligence_service_client.py",
        "google-cloud-video-intelligence",
        "google-cloud-videointelligence",
    )

s.replace(
    "tests/unit/gapic/**/test_video_intelligence_service_client_*.py",
    "^(\s+)expected_request = video_intelligence_pb2.AnnotateVideoRequest\(\)",
    "\g<1>expected_request = video_intelligence_pb2.AnnotateVideoRequest(\n"
    "\g<1>    input_uri=input_uri, features=features)",
)

# Keep features a keyword param until the microgenerator migration
# https://github.com/googleapis/python-videointelligence/issues/7
# -------------------------------------------------------------------------------
s.replace(
    "google/cloud/videointelligence_v1/gapic/video_intelligence_service_client.py",
    ">>> response = client\.annotate_video\(features, input_uri=input_uri\)",
    ">>> response = client.annotate_video(input_uri=input_uri, features=features)",
)
s.replace(
    "google/cloud/videointelligence_v1/gapic/video_intelligence_service_client.py",
    """(?P<features>\s+features \(list.+?)\n"""
    """(?P<input_uri>\s+input_uri \(str\).+?should be unset\.\n)"""
    """(?P<input_content>\s+input_content \(bytes\).+?should be unset\.)""",
    """\n\g<input_uri>\g<input_content>\g<features>""",
    re.DOTALL | re.MULTILINE,
)

s.replace(
    "google/cloud/videointelligence_v1/gapic/video_intelligence_service_client.py",
    """            self,
            features,
            input_uri=None,
            input_content=None,
            video_context=None,
            output_uri=None,
            location_id=None,
            retry=google\.api_core\.gapic_v1\.method\.DEFAULT,
            timeout=google\.api_core\.gapic_v1\.method\.DEFAULT,
            metadata=None""",
    """            self,
            input_uri=None,
            input_content=None,
            # NOTE: Keep features a keyword param that comes after `input_uri` until
            # the microgenerator migration to avoid breaking users.
            # See https://github.com/googleapis/python-videointelligence/issues/7.
            features=None,
            video_context=None,
            output_uri=None,
            location_id=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None""",
)

s.replace(
    "tests/**/test_video_intelligence_service_client_v1.py",
    "response = client\.annotate_video\(features, input_uri=input_uri\)",
    "response = client.annotate_video(input_uri=input_uri, features=features)",
)

# Add missing blank line before Attributes: in generated docstrings
# Remove after
# https://github.com/googleapis/protoc-docs-plugin/pull/31
s.replace("google/cloud/**/*_pb2.py", "(\s+)Attributes:", "\n\g<1>Attributes:")

# Add noindex to types docs to silence warnings about duplicates
# TODO: Remove during microgenerator transition
s.replace("docs/gapic/**/types.rst", "(\s+):members:", "\g<1>:members:\g<1>:noindex:")

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(cov_level=70, samples=True)
s.move(templated_files)

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------
python.py_samples()

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
