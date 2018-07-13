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

import re

import synthtool as s
from synthtool import gcp

gapic = gcp.GAPICGenerator()

versions = ['v1p1beta1', 'v1']


for version in versions:
    library = gapic.py_library('speech', version)

    # Don't move over __init__.py, as we modify it to make the generated client
    # use helpers.py.
    s.move(library / f'google/cloud/speech_{version}/types.py')
    s.move(library / f'google/cloud/speech_{version}/gapic')
    s.move(library / f'google/cloud/speech_{version}/proto')
    s.move(library / f'tests/unit/gapic/{version}')
    s.move(library / f'docs/gapic/{version}')


# Use the highest version library to generate documentation index, README, and
# import alias.
s.move(library / 'google/cloud/speech.py')
s.move(library / 'docs/index.rst')
s.move(library / 'README.rst')


# Make the docs multiversion
s.replace(
    'docs/index.rst',
    r'    gapic/v1/api(.+?)\Z',
    """\
    gapic/v1/api
    gapic/v1/types
    gapic/v1p1beta1/api
    gapic/v1p1beta1/types
    changelog
""", re.DOTALL | re.MULTILINE)


# The release stage is Beta, not Alpha.
s.replace(
    ['README.rst', 'docs/index.rst'],
    r'Google Cloud Speech API \(`Alpha`_\)',
    'Google Cloud Speech API (`Beta`_)')


# Fix bad reference to operations_v1
s.replace(
    '**/gapic/**/*_transport.py',
    r' \= operations_v1\.',
    ' = google.api_core.operations_v1.')


# Fix bad docstrings.
s.replace(
    '**/gapic/*_client.py',
    r'\\"(.+?)-\*\\"',
    r'"\1-\\*"')


# Issues exist where python files should define the source encoding
# https://github.com/googleapis/gapic-generator/issues/2097
s.replace(
    '**/proto/*_pb2.py',
    r"(^.*$\n)*",
    r"# -*- coding: utf-8 -*-\n\g<0>")


# Fix tests to use the direct gapic client instead of the wrapped helper
# client.
s.replace(
    'tests/unit/**/test*client*.py',
    r'from google\.cloud import speech_(.+?)$',
    r'from google.cloud.speech_\1.gapic import speech_client as speech_\1')
