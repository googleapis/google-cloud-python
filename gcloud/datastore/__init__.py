# Copyright 2014 Google Inc. All rights reserved.
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

"""Shortcut methods for getting set up with Google Cloud Datastore.

You'll typically use these to get started with the API:

>>> from gcloud import datastore
>>>
>>> client = datastore.Client()
>>> key = client.key('EntityKind', 1234)
>>> entity = datastore.Entity(key)
>>> query = client.query(kind='EntityKind')

The main concepts with this API are:

- :class:`gcloud.datastore.connection.Connection`
  which represents a connection between your machine and the Cloud Datastore
  API.

- :class:`gcloud.datastore.client.Client`
  which represents a project (string) and namespace (string) bundled with
  a connection and has convenience methods for constructing objects with that
  project / namespace.

- :class:`gcloud.datastore.entity.Entity`
  which represents a single entity in the datastore
  (akin to a row in relational database world).

- :class:`gcloud.datastore.key.Key`
  which represents a pointer to a particular entity in the datastore
  (akin to a unique identifier in relational database world).

- :class:`gcloud.datastore.query.Query`
  which represents a lookup or search over the rows in the datastore.

- :class:`gcloud.datastore.transaction.Transaction`
  which represents an all-or-none transaction and enables consistency
  when race conditions may occur.
"""

from gcloud.datastore.batch import Batch
from gcloud.datastore.connection import Connection
from gcloud.datastore.client import Client
from gcloud.datastore.entity import Entity
from gcloud.datastore.key import Key
from gcloud.datastore.query import Query
from gcloud.datastore.transaction import Transaction


SCOPE = Connection.SCOPE
