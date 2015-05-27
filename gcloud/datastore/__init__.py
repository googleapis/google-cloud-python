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

>>> key = datastore.Key('EntityKind', 1234)
>>> entity = datastore.Entity(key)
>>> query = datastore.Query(kind='EntityKind')

The main concepts with this API are:

- :class:`gcloud.datastore.connection.Connection`
  which represents a connection between your machine and the Cloud Datastore
  API.

- :class:`gcloud.datastore.dataset.Dataset`
  which represents a dataset ID (string) bundled with a connection and has
  convenience methods for constructing objects with that dataset ID.

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

from gcloud.datastore._implicit_environ import get_connection
from gcloud.datastore._implicit_environ import get_default_connection
from gcloud.datastore._implicit_environ import get_default_dataset_id
from gcloud.datastore._implicit_environ import set_default_connection
from gcloud.datastore._implicit_environ import set_default_dataset_id
from gcloud.datastore.api import allocate_ids
from gcloud.datastore.api import delete
from gcloud.datastore.api import delete_multi
from gcloud.datastore.api import get
from gcloud.datastore.api import get_multi
from gcloud.datastore.api import put
from gcloud.datastore.api import put_multi
from gcloud.datastore.batch import Batch
from gcloud.datastore.connection import SCOPE
from gcloud.datastore.connection import Connection
from gcloud.datastore.dataset import Dataset
from gcloud.datastore.entity import Entity
from gcloud.datastore.key import Key
from gcloud.datastore.query import Query
from gcloud.datastore.transaction import Transaction


def set_defaults(dataset_id=None, connection=None):
    """Set defaults either explicitly or implicitly as fall-back.

    Uses the arguments to call the individual default methods

    - set_default_dataset_id
    - set_default_connection

    In the future we will likely enable methods like

    - set_default_namespace

    :type dataset_id: string
    :param dataset_id: Optional. The dataset ID to use as default.

    :type connection: :class:`gcloud.datastore.connection.Connection`
    :param connection: A connection provided to be the default.
    """
    set_default_dataset_id(dataset_id=dataset_id)
    set_default_connection(connection=connection)
