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
>>> dataset = datastore.get_dataset('dataset-id-here')
>>> # Then do other things...
>>> query = dataset.query().kind('EntityKind')
>>> entity = dataset.entity('EntityKind')

The main concepts with this API are:

- :class:`gcloud.datastore.connection.Connection`
  which represents a connection between your machine and the Cloud Datastore
  API.

- :class:`gcloud.datastore.dataset.Dataset`
  which represents a particular dataset
  (akin to a database name in relational database world).

- :class:`gcloud.datastore.entity.Entity`
  which represents a single entity in the datastore
  (akin to a row in relational database world).

- :class:`gcloud.datastore.key.Key`
  which represents a pointer to a particular entity in the datastore
  (akin to a unique identifier in relational database world).

- :class:`gcloud.datastore.query.Query`
  which represents a lookup or search over the rows in the datastore.
"""

import os

from gcloud import credentials
from gcloud.datastore import _implicit_environ
from gcloud.datastore.connection import Connection


SCOPE = ('https://www.googleapis.com/auth/datastore ',
         'https://www.googleapis.com/auth/userinfo.email')
"""The scope required for authenticating as a Cloud Datastore consumer."""

_DATASET_ENV_VAR_NAME = 'GCLOUD_DATASET_ID'


def _set_dataset_from_environ():
    """Determines auth settings from local enviroment.

    Currently only supports enviroment variable but will implicitly
    support App Engine, Compute Engine and other environments in
    the future.

    Local environment variable used is:
    - GCLOUD_DATASET_ID
    """
    local_dataset_id = os.getenv(_DATASET_ENV_VAR_NAME)
    if local_dataset_id is not None:
        _implicit_environ.DATASET = get_dataset(local_dataset_id)


def get_connection():
    """Shortcut method to establish a connection to the Cloud Datastore.

    Use this if you are going to access several datasets
    with the same set of credentials (unlikely):

    >>> from gcloud import datastore
    >>> connection = datastore.get_connection()
    >>> dataset1 = connection.dataset('dataset1')
    >>> dataset2 = connection.dataset('dataset2')

    :rtype: :class:`gcloud.datastore.connection.Connection`
    :returns: A connection defined with the proper credentials.
    """
    implicit_credentials = credentials.get_credentials()
    scoped_credentials = implicit_credentials.create_scoped(SCOPE)
    return Connection(credentials=scoped_credentials)


def get_dataset(dataset_id):
    """Establish a connection to a particular dataset in the Cloud Datastore.

    This is a shortcut method for creating a connection and using it
    to connect to a dataset.

    You'll generally use this as the first call to working with the API:

    >>> from gcloud import datastore
    >>> dataset = datastore.get_dataset('dataset-id')
    >>> # Now you can do things with the dataset.
    >>> dataset.query().kind('TestKind').fetch()
    [...]

    :type dataset_id: string
    :param dataset_id: The id of the dataset you want to use.
                       This is akin to a database name
                       and is usually the same as your Cloud Datastore project
                       name.

    :rtype: :class:`gcloud.datastore.dataset.Dataset`
    :returns: A dataset with a connection using the provided credentials.
    """
    connection = get_connection()
    return connection.dataset(dataset_id)


def _require_dataset():
    """Convenience method to ensure DATASET is set.

    :rtype: :class:`gcloud.datastore.dataset.Dataset`
    :returns: A dataset based on the current environment.
    :raises: :class:`EnvironmentError` if DATASET is not set.
    """
    if _implicit_environ.DATASET is None:
        raise EnvironmentError('Dataset could not be implied.')
    return _implicit_environ.DATASET


def get_entity(key):
    """Retrieves entity from implicit dataset, along with its attributes.

    :type key: :class:`gcloud.datastore.key.Key`
    :param key: The name of the item to retrieve.

    :rtype: :class:`gcloud.datastore.entity.Entity` or ``None``
    :return: The requested entity, or ``None`` if there was no match found.
    """
    return _require_dataset().get_entity(key)


def get_entities(keys):
    """Retrieves entities from implied dataset, along with their attributes.

    :type keys: list of :class:`gcloud.datastore.key.Key`
    :param keys: The name of the item to retrieve.

    :rtype: list of :class:`gcloud.datastore.entity.Entity`
    :return: The requested entities.
    """
    return _require_dataset().get_entities(keys)


def allocate_ids(incomplete_key, num_ids):
    """Allocates a list of IDs from a partial key.

    :type incomplete_key: A :class:`gcloud.datastore.key.Key`
    :param incomplete_key: The partial key to use as base for allocated IDs.

    :type num_ids: A :class:`int`.
    :param num_ids: The number of IDs to allocate.

    :rtype: list of :class:`gcloud.datastore.key.Key`
    :return: The (complete) keys allocated with `incomplete_key` as root.
    """
    return _require_dataset().allocate_ids(incomplete_key, num_ids)


# Set DATASET if it can be implied from the environment.
_set_dataset_from_environ()
