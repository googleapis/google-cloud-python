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

versions = ['v1beta1', 'v1beta2', 'v1p1beta1', 'v1p2beta1', 'v1']


for version in versions:
    library = gapic.py_library(
        'videointelligence',
        version,
        artman_output_name=f'video-intelligence-{version}')

    # TODO: stop excluding tests and nox.py (excluded as we lack system tests)
    s.move(
        library,
        excludes=[
            'setup.py',
            'nox*.py',
            'README.rst',
            'docs/index.rst', 
            f'tests/system/gapic/{version}/'
            f'test_system_video_intelligence_service_{version}.py',
            #f'tests/unit/gapic/{version}/'
            #f'test_video_intelligence_service_client_{version}.py',
        ])

s.replace(
    "**/*/video_intelligence_service_client.py",
    "'google-cloud-video-intelligence', \).version",
    "'google-cloud-videointelligence', ).version",
)

s.replace(
    "tests/unit/gapic/**/test_video_intelligence_service_client_*.py",
    "^(\s+)expected_request = video_intelligence_pb2.AnnotateVideoRequest\(\)",
    "\g<1>expected_request = video_intelligence_pb2.AnnotateVideoRequest(\n"
        "\g<1>    input_uri=input_uri, features=features)",
)
