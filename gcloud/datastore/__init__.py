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
>>> from gcloud.datastore.entity import Entity
>>> from gcloud.datastore.key import Key
>>> from gcloud.datastore.query import Query

>>> datastore.set_default_connection()
>>> datastore.set_default_dataset_id()

>>> key = Key('EntityKind', 1234)
>>> entity = Entity(key)
>>> query = Query(kind='EntityKind')

The main concepts with this API are:

- :class:`gcloud.datastore.connection.Connection`
  which represents a connection between your machine and the Cloud Datastore
  API.

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

import os

from gcloud import credentials
from gcloud.datastore import _implicit_environ
from gcloud.datastore.api import allocate_ids
from gcloud.datastore.api import get_entities
from gcloud.datastore.connection import Connection


SCOPE = ('https://www.googleapis.com/auth/datastore',
         'https://www.googleapis.com/auth/userinfo.email')
"""The scopes required for authenticating as a Cloud Datastore consumer."""

_DATASET_ENV_VAR_NAME = 'GCLOUD_DATASET_ID'


def set_default_dataset_id(dataset_id=None):
    """Set default dataset ID either explicitly or implicitly as fall-back.

    In implicit case, currently only supports enviroment variable but will
    support App Engine, Compute Engine and other environments in the future.

    Local environment variable used is:
    - GCLOUD_DATASET_ID

    :type dataset_id: string
    :param dataset_id: Optional. The dataset ID to use as default.
    """
    if dataset_id is None:
        dataset_id = os.getenv(_DATASET_ENV_VAR_NAME)

    if dataset_id is not None:
        _implicit_environ.DATASET_ID = dataset_id


def set_default_connection(connection=None):
    """Set default connection either explicitly or implicitly as fall-back.

    :type connection: :class:`gcloud.datastore.connection.Connection`
    :param connection: A connection provided to be the default.
    """
    connection = connection or get_connection()
    _implicit_environ.CONNECTION = connection


def get_connection():
    """Shortcut method to establish a connection to the Cloud Datastore.

    Use this if you are going to access several datasets
    with the same set of credentials (unlikely):

    >>> from gcloud import datastore
    >>> from gcloud.datastore import Key

    >>> connection = datastore.get_connection()
    >>> key1 = Key('Kind', 1234, dataset_id='dataset1')
    >>> key2 = Key('Kind', 1234, dataset_id='dataset2')
    >>> entity1 = key1.get(connection=connection)
    >>> entity2 = key2.get(connection=connection)

    :rtype: :class:`gcloud.datastore.connection.Connection`
    :returns: A connection defined with the proper credentials.
    """
    implicit_credentials = credentials.get_credentials()
    scoped_credentials = implicit_credentials.create_scoped(SCOPE)
    return Connection(credentials=scoped_credentials)
