# Copyright 2016 Google Inc. All rights reserved.
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

"""Cloud Spanner API package."""


import pkg_resources
__version__ = pkg_resources.get_distribution('google-cloud-spanner').version

from google.cloud.spanner.client import Client

from google.cloud.spanner.keyset import KeyRange
from google.cloud.spanner.keyset import KeySet

from google.cloud.spanner.pool import AbstractSessionPool
from google.cloud.spanner.pool import BurstyPool
from google.cloud.spanner.pool import FixedSizePool

from google.cloud.spanner.types import ArrayParamType
from google.cloud.spanner.types import BOOL_PARAM_TYPE
from google.cloud.spanner.types import BYTES_PARAM_TYPE
from google.cloud.spanner.types import DATE_PARAM_TYPE
from google.cloud.spanner.types import FLOAT64_PARAM_TYPE
from google.cloud.spanner.types import INT64_PARAM_TYPE
from google.cloud.spanner.types import STRING_PARAM_TYPE
from google.cloud.spanner.types import StructField
from google.cloud.spanner.types import StructParamType
from google.cloud.spanner.types import TIMESTAMP_PARAM_TYPE


__all__ = [
    '__version__',
    'AbstractSessionPool',
    'ArrayParamType',
    'BOOL_PARAM_TYPE',
    'BYTES_PARAM_TYPE',
    'BurstyPool',
    'Client',
    'DATE_PARAM_TYPE',
    'FLOAT64_PARAM_TYPE',
    'FixedSizePool',
    'INT64_PARAM_TYPE',
    'KeyRange',
    'KeySet',
    'STRING_PARAM_TYPE',
    'StructField',
    'StructParamType',
    'TIMESTAMP_PARAM_TYPE',
]
