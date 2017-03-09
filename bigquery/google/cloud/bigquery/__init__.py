# Copyright 2015 Google Inc.
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

"""Google BigQuery API wrapper.

The main concepts with this API are:

- :class:`~google.cloud.bigquery.dataset.Dataset` represents a
  collection of tables.

- :class:`~google.cloud.bigquery.table.Table` represents a single "relation".
"""


from pkg_resources import get_distribution
__version__ = get_distribution('google-cloud-bigquery').version

from google.cloud.bigquery._helpers import ArrayQueryParameter
from google.cloud.bigquery._helpers import ScalarQueryParameter
from google.cloud.bigquery._helpers import StructQueryParameter
from google.cloud.bigquery.client import Client
from google.cloud.bigquery.dataset import AccessGrant
from google.cloud.bigquery.dataset import Dataset
from google.cloud.bigquery.schema import SchemaField
from google.cloud.bigquery.table import Table

__all__ = [
    '__version__', 'AccessGrant', 'ArrayQueryParameter', 'Client',
    'Dataset', 'ScalarQueryParameter', 'SchemaField', 'StructQueryParameter',
    'Table',
]
