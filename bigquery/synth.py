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

version = 'v2'

library = gapic.py_library(
    'bigquery',
    version,
    config_path='/google/cloud/bigquery/'
                'artman_bigquery_v2.yaml',
    artman_output_name='bigquery-v2',
    include_protos=True,
)

s.move(
    [
        library / "google/cloud/bigquery_v2/gapic/enums.py",
        library / "google/cloud/bigquery_v2/types.py",
        library / "google/cloud/bigquery_v2/proto/location*",
        library / "google/cloud/bigquery_v2/proto/model*",
        library / "google/cloud/bigquery_v2/proto/standard_sql*",
    ],
)

# Fix up proto docs that are missing summary line.
s.replace(
    "google/cloud/bigquery_v2/proto/model_pb2.py",
    '"""Attributes:',
    '"""Protocol buffer.\n\n  Attributes:',
)

# Remove non-ascii characters from docstrings for Python 2.7.
# Format quoted strings as plain text.
s.replace("google/cloud/bigquery_v2/proto/*.py", "[“”]", '``')

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
