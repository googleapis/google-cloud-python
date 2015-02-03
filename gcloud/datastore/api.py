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
from gcloud.datastore.batch import Batch
from gcloud.datastore.transaction import Transaction
from gcloud.datastore import helpers


_MAX_LOOPS = 128
"""Maximum number of iterations to wait for deferred keys."""


def _require_dataset_id(dataset_id=None, first_key=None):
    """Infer a dataset ID from the environment, if not passed explicitly.

    Order of precedence:

    - Passed `dataset_id` (if not None).
    - `dataset_id` of current batch / transaction (if current exists).
    - `dataset_id` of first key
    - `dataset_id` inferred from the environment (if `set_default_dataset_id`
      has been called).

    :type dataset_id: string
    :param dataset_id: Optional.

    :type first_key: :class:`gcloud.datastore.key.Key` or None
    :param first_key: Optional: first key being manipulated.

    :rtype: string
    :returns: A dataset ID based on the current environment.
    :raises: :class:`EnvironmentError` if ``dataset_id`` is ``None``,
             and cannot be inferred from the environment.
    """
    if dataset_id is not None:
        return dataset_id
    top = Batch.current()
    if top is not None:
        return top.dataset_id
    if first_key is not None:
        return first_key.dataset_id
    if _implicit_environ.DATASET_ID is None:
        raise EnvironmentError('Dataset ID could not be inferred.')
    return _implicit_environ.DATASET_ID


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
        top = Batch.current()
        if top is not None:
            connection = top.connection
        else:
            if _implicit_environ.CONNECTION is None:
                raise EnvironmentError('Connection could not be inferred.')
            connection = _implicit_environ.CONNECTION
    return connection


def _extended_lookup(connection, dataset_id, key_pbs,
                     missing=None, deferred=None,
                     eventual=False, transaction_id=None):
    """Repeat lookup until all keys found (unless stop requested).

    Helper method for :func:`get`.

    :type connection: :class:`gcloud.datastore.connection.Connection`
    :param connection: The connection used to connect to datastore.

    :type dataset_id: string
    :param dataset_id: The ID of the dataset of which to make the request.

    :type key_pbs: list of :class:`gcloud.datastore._datastore_v1_pb2.Key`
    :param key_pbs: The keys to retrieve from the datastore.

    :type missing: an empty list or None.
    :param missing: If a list is passed, the key-only entity protobufs
                    returned by the backend as "missing" will be copied
                    into it.  Use only as a keyword param.

    :type deferred: an empty list or None.
    :param deferred: If a list is passed, the key protobufs returned
                     by the backend as "deferred" will be copied into it.
                     Use only as a keyword param.

    :type eventual: boolean
    :param eventual: If False (the default), request ``STRONG`` read
                     consistency.  If True, request ``EVENTUAL`` read
                     consistency.

    :type transaction_id: string
    :param transaction_id: If passed, make the request in the scope of
                           the given transaction.  Incompatible with
                           ``eventual==True``.

    :rtype: list of :class:`gcloud.datastore._datastore_v1_pb2.Entity`
    :returns: The requested entities.
    :raises: :class:`ValueError` if missing / deferred are not null or
             empty list.
    """
    if missing is not None and missing != []:
        raise ValueError('missing must be None or an empty list')

    if deferred is not None and deferred != []:
        raise ValueError('deferred must be None or an empty list')

    results = []

    loop_num = 0
    while loop_num < _MAX_LOOPS:  # loop against possible deferred.
        loop_num += 1

        results_found, missing_found, deferred_found = connection.lookup(
            dataset_id=dataset_id,
            key_pbs=key_pbs,
            eventual=eventual,
            transaction_id=transaction_id,
        )

        results.extend(results_found)

        if missing is not None:
            missing.extend(missing_found)

        if deferred is not None:
            deferred.extend(deferred_found)
            break

        if len(deferred_found) == 0:
            break

        # We have deferred keys, and the user didn't ask to know about
        # them, so retry (but only with the deferred ones).
        key_pbs = deferred_found

    return results


def get(keys, missing=None, deferred=None, connection=None, dataset_id=None):
    """Retrieves entities, along with their attributes.

    :type keys: list of :class:`gcloud.datastore.key.Key`
    :param keys: The keys to be retrieved from the datastore.

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
                       If not passed, inferred from the environment.

    :type dataset_id: :class:`gcloud.datastore.connection.Connection`
    :param dataset_id: Optional. The dataset ID used to connect to datastore.
                       If not passed, inferred from the environment.

    :rtype: list of :class:`gcloud.datastore.entity.Entity`
    :returns: The requested entities.
    :raises: EnvironmentError if ``connection`` or ``dataset_id`` not passed,
             and cannot be inferred from the environment.  ValueError if
             one or more of ``keys`` has a dataset ID which does not match
             the passed / inferred dataset ID.
    """
    if not keys:
        return []

    connection = _require_connection(connection)
    dataset_id = _require_dataset_id(dataset_id, keys[0])

    if list(set([key.dataset_id for key in keys])) != [dataset_id]:
        raise ValueError('Keys do not match dataset ID')

    transaction = Transaction.current()

    entity_pbs = _extended_lookup(
        connection,
        dataset_id=dataset_id,
        key_pbs=[k.to_protobuf() for k in keys],
        missing=missing,
        deferred=deferred,
        transaction_id=transaction and transaction.id,
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


def put(entities, connection=None, dataset_id=None):
    """Save the entities in the Cloud Datastore.

    :type entities: list of :class:`gcloud.datastore.entity.Entity`
    :param entities: The entities to be saved to the datastore.

    :type connection: :class:`gcloud.datastore.connection.Connection`
    :param connection: Optional connection used to connect to datastore.
                       If not passed, inferred from the environment.

    :type dataset_id: :class:`gcloud.datastore.connection.Connection`
    :param dataset_id: Optional. The dataset ID used to connect to datastore.
                       If not passed, inferred from the environment.

    :raises: EnvironmentError if ``connection`` or ``dataset_id`` not passed,
             and cannot be inferred from the environment.  ValueError if
             one or more entities has a key with a dataset ID not matching
             the passed / inferred dataset ID.
    """
    if not entities:
        return

    connection = _require_connection(connection)
    dataset_id = _require_dataset_id(dataset_id, entities[0].key)

    current = Batch.current()
    in_batch = current is not None
    if not in_batch:
        current = Batch(dataset_id=dataset_id, connection=connection)
    for entity in entities:
        current.put(entity)
    if not in_batch:
        current.commit()


def delete(keys, connection=None, dataset_id=None):
    """Delete the keys in the Cloud Datastore.

    :type keys: list of :class:`gcloud.datastore.key.Key`
    :param keys: The keys to be deleted from the datastore.

    :type connection: :class:`gcloud.datastore.connection.Connection`
    :param connection: Optional connection used to connect to datastore.
                       If not passed, inferred from the environment.

    :type dataset_id: :class:`gcloud.datastore.connection.Connection`
    :param dataset_id: Optional. The dataset ID used to connect to datastore.
                       If not passed, inferred from the environment.

    :raises: EnvironmentError if ``connection`` or ``dataset_id`` not passed,
             and cannot be inferred from the environment.  ValueError if
             one or more keys has a dataset ID not matching the passed /
             inferred dataset ID.
    """
    if not keys:
        return

    connection = _require_connection(connection)
    dataset_id = _require_dataset_id(dataset_id, keys[0])

    # We allow partial keys to attempt a delete, the backend will fail.
    current = Batch.current()
    in_batch = current is not None
    if not in_batch:
        current = Batch(dataset_id=dataset_id, connection=connection)
    for key in keys:
        current.delete(key)
    if not in_batch:
        current.commit()


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
