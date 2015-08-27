# Copyright 2015 Google Inc. All rights reserved.
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

"""Google Cloud BigQuery API wrapper.

The main concepts with this API are:

- :class:`gcloud.bigquery.dataset.Dataset` represents an collection of tables.

- :class:`gcloud.bigquery.table.Table` represents a single "relation".
"""

from gcloud.bigquery.client import Client
from gcloud.bigquery.connection import Connection
from gcloud.bigquery.dataset import Dataset
from gcloud.bigquery.table import SchemaField
from gcloud.bigquery.table import Table


SCOPE = Connection.SCOPE
