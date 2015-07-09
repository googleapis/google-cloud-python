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
"""Convenience wrapper for invoking APIs/factories w/ a dataset ID."""

from gcloud.datastore import helpers
from gcloud.datastore.batch import Batch
from gcloud.datastore.entity import Entity
from gcloud.datastore.key import Key
from gcloud.datastore.query import Query
from gcloud.datastore.transaction import Transaction
from gcloud.datastore._implicit_environ import _determine_default_dataset_id
from gcloud.datastore._implicit_environ import get_connection


_MAX_LOOPS = 128
"""Maximum number of iterations to wait for deferred keys."""


def _extended_lookup(connection, dataset_id, key_pbs,
                     missing=None, deferred=None,
                     eventual=False, transaction_id=None):
    """Repeat lookup until all keys found (unless stop requested).

    Helper function for :meth:`Client.get_multi`.

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


class Client(object):
    """Convenience wrapper for invoking APIs/factories w/ a dataset ID.

    :type dataset_id: string
    :param dataset_id: (optional) dataset ID to pass to proxied API methods.

    :type namespace: string
    :param namespace: (optional) namespace to pass to proxied API methods.

    :type connection: :class:`gcloud.datastore.connection.Connection`, or None
    :param connection: (optional) connection to pass to proxied API methods
    """

    def __init__(self, dataset_id=None, namespace=None, connection=None):
        dataset_id = _determine_default_dataset_id(dataset_id)
        if dataset_id is None:
            raise EnvironmentError('Dataset ID could not be inferred.')
        self.dataset_id = dataset_id
        if connection is None:
            connection = get_connection()
        self._connection_stack = [connection]
        self.namespace = namespace

    def _push_connection(self, connection):
        """Push a connection/batch/transaction onto our stack.

        "Protected", intended for use by batch / transaction context mgrs.

        :type connection: :class:`gcloud.datastore.connection.Connection`,
                          or an object implementing its API.
        :param connection: newly-active connection/batch/transaction to
                           pass to proxied API methods
        """
        self._connection_stack.append(connection)

    def _pop_connection(self):
        """Pop a connection/batch/transaction from our stack.

        "Protected", intended for use by batch / transaction context mgrs.

        :raises: IndexError if the stack is empty.
        :rtype: :class:`gcloud.datastore.connection.Connection`, or
                an object implementing its API.
        :returns: the top-most connection/batch/transaction, after removing it.
        """
        return self._connection_stack.pop()

    @property
    def connection(self):
        """Currently-active connection.

        :rtype: :class:`gcloud.datastore.connection.Connection`, or
                an object implementing its API.
        :returns: The connection/batch/transaction at the toop of the
                  connection stack.
        """
        return self._connection_stack[-1]

    def get(self, key, missing=None, deferred=None):
        """Retrieve an entity from a single key (if it exists).

        .. note::

           This is just a thin wrapper over :meth:`get_multi`.
           The backend API does not make a distinction between a single key or
           multiple keys in a lookup request.

        :type key: :class:`gcloud.datastore.key.Key`
        :param key: The key to be retrieved from the datastore.

        :type missing: an empty list or None.
        :param missing: If a list is passed, the key-only entities returned
                        by the backend as "missing" will be copied into it.
                        Use only as a keyword param.

        :type deferred: an empty list or None.
        :param deferred: If a list is passed, the keys returned
                         by the backend as "deferred" will be copied into it.
                         Use only as a keyword param.

        :rtype: :class:`gcloud.datastore.entity.Entity` or ``NoneType``
        :returns: The requested entity if it exists.
        """
        entities = self.get_multi(keys=[key], missing=missing,
                                  deferred=deferred)
        if entities:
            return entities[0]

    def get_multi(self, keys, missing=None, deferred=None):
        """Retrieve entities, along with their attributes.

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

        :rtype: list of :class:`gcloud.datastore.entity.Entity`
        :returns: The requested entities.
        :raises: ValueError if one or more of ``keys`` has a dataset ID which
                 does not match our dataset ID.
        """
        if not keys:
            return []

        ids = list(set([key.dataset_id for key in keys]))
        if ids != [self.dataset_id]:
            raise ValueError('Keys do not match dataset ID')

        transaction = Transaction.current()

        entity_pbs = _extended_lookup(
            connection=self.connection,
            dataset_id=self.dataset_id,
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

        return [helpers.entity_from_protobuf(entity_pb)
                for entity_pb in entity_pbs]

    def put(self, entity):
        """Save an entity in the Cloud Datastore.

        .. note::

           This is just a thin wrapper over :meth:`put_multi`.
           The backend API does not make a distinction between a single
           entity or multiple entities in a commit request.

        :type entity: :class:`gcloud.datastore.entity.Entity`
        :param entity: The entity to be saved to the datastore.
        """
        self.put_multi(entities=[entity])

    def put_multi(self, entities):
        """Save entities in the Cloud Datastore.

        :type entities: list of :class:`gcloud.datastore.entity.Entity`
        :param entities: The entities to be saved to the datastore.

        :raises: ValueError if ``entities`` is a single entity.
        """
        if isinstance(entities, Entity):
            raise ValueError("Pass a sequence of entities")

        if not entities:
            return

        current = Batch.current()
        in_batch = current is not None

        if not in_batch:
            current = Batch(dataset_id=self.dataset_id,
                            connection=self.connection)
        for entity in entities:
            current.put(entity)

        if not in_batch:
            current.commit()

    def delete(self, key):
        """Delete the key in the Cloud Datastore.

        .. note::

           This is just a thin wrapper over :meth:`delete_multi`.
           The backend API does not make a distinction between a single key or
           multiple keys in a commit request.

        :type key: :class:`gcloud.datastore.key.Key`
        :param key: The key to be deleted from the datastore.
        """
        return self.delete_multi(keys=[key])

    def delete_multi(self, keys):
        """Delete keys from the Cloud Datastore.

        :type keys: list of :class:`gcloud.datastore.key.Key`
        :param keys: The keys to be deleted from the datastore.
        """
        if not keys:
            return

        # We allow partial keys to attempt a delete, the backend will fail.
        current = Batch.current()
        in_batch = current is not None

        if not in_batch:
            current = Batch(dataset_id=self.dataset_id,
                            connection=self.connection)
        for key in keys:
            current.delete(key)

        if not in_batch:
            current.commit()

    def allocate_ids(self, incomplete_key, num_ids):
        """Allocate a list of IDs from a partial key.

        :type incomplete_key: A :class:`gcloud.datastore.key.Key`
        :param incomplete_key: Partial key to use as base for allocated IDs.

        :type num_ids: integer
        :param num_ids: The number of IDs to allocate.

        :rtype: list of :class:`gcloud.datastore.key.Key`
        :returns: The (complete) keys allocated with ``incomplete_key`` as
                  root.
        :raises: :class:`ValueError` if ``incomplete_key`` is not a
                 partial key.
        """
        if not incomplete_key.is_partial:
            raise ValueError(('Key is not partial.', incomplete_key))

        incomplete_key_pb = incomplete_key.to_protobuf()
        incomplete_key_pbs = [incomplete_key_pb] * num_ids

        conn = self.connection
        allocated_key_pbs = conn.allocate_ids(incomplete_key.dataset_id,
                                              incomplete_key_pbs)
        allocated_ids = [allocated_key_pb.path_element[-1].id
                         for allocated_key_pb in allocated_key_pbs]
        return [incomplete_key.completed_key(allocated_id)
                for allocated_id in allocated_ids]

    def key(self, *path_args, **kwargs):
        """Proxy to :class:`gcloud.datastore.key.Key`.

        Passes our ``dataset_id``.
        """
        if 'dataset_id' in kwargs:
            raise TypeError('Cannot pass dataset_id')
        kwargs['dataset_id'] = self.dataset_id
        if 'namespace' not in kwargs:
            kwargs['namespace'] = self.namespace
        return Key(*path_args, **kwargs)

    def batch(self):
        """Proxy to :class:`gcloud.datastore.batch.Batch`.

        Passes our ``dataset_id``.
        """
        return Batch(dataset_id=self.dataset_id, connection=self.connection)

    def transaction(self):
        """Proxy to :class:`gcloud.datastore.transaction.Transaction`.

        Passes our ``dataset_id``.
        """
        return Transaction(dataset_id=self.dataset_id,
                           connection=self.connection)

    def query(self, **kwargs):
        """Proxy to :class:`gcloud.datastore.query.Query`.

        Passes our ``dataset_id``.
        """
        if 'dataset_id' in kwargs:
            raise TypeError('Cannot pass dataset_id')
        kwargs['dataset_id'] = self.dataset_id
        if 'namespace' not in kwargs:
            kwargs['namespace'] = self.namespace
        return Query(**kwargs)
