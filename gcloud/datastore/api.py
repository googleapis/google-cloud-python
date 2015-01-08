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

"""Methods for interacting with Google Cloud Datastore.

Allows interacting with the datastore via user-friendly Key, Entity and
Query objects rather than via protobufs.
"""

from gcloud.datastore import _implicit_environ
from gcloud.datastore import helpers


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
