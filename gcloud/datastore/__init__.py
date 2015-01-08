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
from gcloud.datastore.connection import Connection
from gcloud.datastore import helpers


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


def _require_dataset_id(dataset_id=None):
    """Infer a dataset ID from the environment, if not passed explicitly.

    :type dataset_id: string
    :param dataset_id: Optional.

    :rtype: string
    :returns: A dataset ID based on the current environment.
    :raises: :class:`EnvironmentError` if ``dataset_id`` is ``None``,
             and cannot be inferred from the environment.
    """
    if dataset_id is None:
        if _implicit_environ.DATASET_ID is None:
            raise EnvironmentError('Dataset ID could not be inferred.')
        dataset_id = _implicit_environ.DATASET_ID
    return dataset_id


def _require_connection(connection=None):
    """Infer a connection from the environment, if not passed explicitly.

    :type connection: :class:`gcloud.datastore.connection.Connection`
    :param connection: Optional.

    :rtype: :class:`gcloud.datastore.connection.Connection`
    :returns: A connection based on the current environment.
    :raises: :class:`EnvironmentError` if ``connection`` is ``None``, and
             cannot be inferred from the environment.
    """
    if connection is None:
        if _implicit_environ.CONNECTION is None:
            raise EnvironmentError('Connection could not be inferred.')
        connection = _implicit_environ.CONNECTION
    return connection


def get_entities(keys, missing=None, deferred=None, connection=None):
    """Retrieves entities, along with their attributes.

    :type keys: list of :class:`gcloud.datastore.key.Key`
    :param keys: The name of the item to retrieve.

    :type missing: an empty list or None.
    :param missing: If a list is passed, the key-only entities returned
                    by the backend as "missing" will be copied into it.
                    Use only as a keyword param.

    :type deferred: an empty list or None.
    :param deferred: If a list is passed, the keys returned
                     by the backend as "deferred" will be copied into it.
                     Use only as a keyword param.

    :type connection: :class:`gcloud.datastore.connection.Connection`
    :param connection: Optional. The connection used to connect to datastore.

    :rtype: list of :class:`gcloud.datastore.entity.Entity`
    :returns: The requested entities.
    :raises: :class:`ValueError` if the key dataset IDs don't agree.
    """
    if not keys:
        return []

    connection = _require_connection(connection)
    dataset_id = keys[0].dataset_id
    # Rather than creating a list or set of all dataset IDs, we iterate
    # and check. We could allow the backend to check this for us if IDs
    # with no prefix worked (GoogleCloudPlatform/google-cloud-datastore#59)
    # or if we made sure that a prefix s~ or e~ was on each key.
    for key in keys[1:]:
        if key.dataset_id != dataset_id:
            raise ValueError('All keys in get_entities must be from the '
                             'same dataset.')

    entity_pbs = connection.lookup(
        dataset_id=dataset_id,
        key_pbs=[k.to_protobuf() for k in keys],
        missing=missing, deferred=deferred,
    )

    if missing is not None:
        missing[:] = [
            helpers.entity_from_protobuf(missed_pb)
            for missed_pb in missing]

    if deferred is not None:
        deferred[:] = [
            helpers.key_from_protobuf(deferred_pb)
            for deferred_pb in deferred]

    entities = []
    for entity_pb in entity_pbs:
        entities.append(helpers.entity_from_protobuf(entity_pb))

    return entities


def allocate_ids(incomplete_key, num_ids, connection=None):
    """Allocates a list of IDs from a partial key.

    :type incomplete_key: A :class:`gcloud.datastore.key.Key`
    :param incomplete_key: Partial key to use as base for allocated IDs.

    :type num_ids: integer
    :param num_ids: The number of IDs to allocate.

    :type connection: :class:`gcloud.datastore.connection.Connection`
    :param connection: Optional. The connection used to connect to datastore.

    :rtype: list of :class:`gcloud.datastore.key.Key`
    :returns: The (complete) keys allocated with ``incomplete_key`` as root.
    :raises: :class:`ValueError` if ``incomplete_key`` is not a partial key.
    """
    connection = _require_connection(connection)

    if not incomplete_key.is_partial:
        raise ValueError(('Key is not partial.', incomplete_key))

    incomplete_key_pb = incomplete_key.to_protobuf()
    incomplete_key_pbs = [incomplete_key_pb] * num_ids

    allocated_key_pbs = connection.allocate_ids(incomplete_key.dataset_id,
                                                incomplete_key_pbs)
    allocated_ids = [allocated_key_pb.path_element[-1].id
                     for allocated_key_pb in allocated_key_pbs]
    return [incomplete_key.completed_key(allocated_id)
            for allocated_id in allocated_ids]
