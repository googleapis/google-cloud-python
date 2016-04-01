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
"""Convenience wrapper for invoking APIs/factories w/ a project."""

import os

from gcloud._helpers import _LocalStack
from gcloud._helpers import _determine_default_project as _base_default_project
from gcloud.client import _ClientProjectMixin
from gcloud.client import Client as _BaseClient
from gcloud.datastore import helpers
from gcloud.datastore.connection import Connection
from gcloud.datastore.batch import Batch
from gcloud.datastore.entity import Entity
from gcloud.datastore.key import Key
from gcloud.datastore.query import Query
from gcloud.datastore.transaction import Transaction
from gcloud.environment_vars import GCD_DATASET


_MAX_LOOPS = 128
"""Maximum number of iterations to wait for deferred keys."""


def _get_gcd_project():
    """Gets the GCD application ID if it can be inferred."""
    return os.getenv(GCD_DATASET)


def _determine_default_project(project=None):
    """Determine default project explicitly or implicitly as fall-back.

    In implicit case, supports four environments. In order of precedence, the
    implicit environments are:

    * DATASTORE_DATASET environment variable (for ``gcd`` / emulator testing)
    * GCLOUD_PROJECT environment variable
    * Google App Engine application ID
    * Google Compute Engine project ID (from metadata server)

    :type project: string
    :param project: Optional. The project to use as default.

    :rtype: string or ``NoneType``
    :returns: Default project if it can be determined.
    """
    if project is None:
        project = _get_gcd_project()

    if project is None:
        project = _base_default_project(project=project)

    return project


def _extended_lookup(connection, project, key_pbs,
                     missing=None, deferred=None,
                     eventual=False, transaction_id=None):
    """Repeat lookup until all keys found (unless stop requested).

    Helper function for :meth:`Client.get_multi`.

    :type connection: :class:`gcloud.datastore.connection.Connection`
    :param connection: The connection used to connect to datastore.

    :type project: string
    :param project: The project to make the request for.

    :type key_pbs: list of :class:`gcloud.datastore._generated.entity_pb2.Key`
    :param key_pbs: The keys to retrieve from the datastore.

    :type missing: list
    :param missing: (Optional) If a list is passed, the key-only entity
                    protobufs returned by the backend as "missing" will be
                    copied into it.

    :type deferred: list
    :param deferred: (Optional) If a list is passed, the key protobufs returned
                     by the backend as "deferred" will be copied into it.

    :type eventual: bool
    :param eventual: If False (the default), request ``STRONG`` read
                     consistency.  If True, request ``EVENTUAL`` read
                     consistency.

    :type transaction_id: string
    :param transaction_id: If passed, make the request in the scope of
                           the given transaction.  Incompatible with
                           ``eventual==True``.

    :rtype: list of :class:`gcloud.datastore._generated.entity_pb2.Entity`
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
            project=project,
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


class Client(_BaseClient, _ClientProjectMixin):
    """Convenience wrapper for invoking APIs/factories w/ a project.

    :type project: string
    :param project: (optional) The project to pass to proxied API methods.

    :type namespace: string
    :param namespace: (optional) namespace to pass to proxied API methods.

    :type credentials: :class:`oauth2client.client.OAuth2Credentials` or
                       :class:`NoneType`
    :param credentials: The OAuth2 Credentials to use for the connection
                        owned by this client. If not passed (and if no ``http``
                        object is passed), falls back to the default inferred
                        from the environment.

    :type http: :class:`httplib2.Http` or class that defines ``request()``.
    :param http: An optional HTTP object to make requests. If not passed, an
                 ``http`` object is created that is bound to the
                 ``credentials`` for the current object.
    """
    _connection_class = Connection

    def __init__(self, project=None, namespace=None,
                 credentials=None, http=None):
        _ClientProjectMixin.__init__(self, project=project)
        self.namespace = namespace
        self._batch_stack = _LocalStack()
        super(Client, self).__init__(credentials, http)

    @staticmethod
    def _determine_default(project):
        return _determine_default_project(project)

    def _push_batch(self, batch):
        """Push a batch/transaction onto our stack.

        "Protected", intended for use by batch / transaction context mgrs.

        :type batch: :class:`gcloud.datastore.batch.Batch`, or an object
                     implementing its API.
        :param batch: newly-active batch/transaction.
        """
        self._batch_stack.push(batch)

    def _pop_batch(self):
        """Pop a batch/transaction from our stack.

        "Protected", intended for use by batch / transaction context mgrs.

        :raises: IndexError if the stack is empty.
        :rtype: :class:`gcloud.datastore.batch.Batch`, or an object
                 implementing its API.
        :returns: the top-most batch/transaction, after removing it.
        """
        return self._batch_stack.pop()

    @property
    def current_batch(self):
        """Currently-active batch.

        :rtype: :class:`gcloud.datastore.batch.Batch`, or an object
                implementing its API, or ``NoneType`` (if no batch is active).
        :returns: The batch/transaction at the top of the batch stack.
        """
        return self._batch_stack.top

    @property
    def current_transaction(self):
        """Currently-active transaction.

        :rtype: :class:`gcloud.datastore.transaction.Transaction`, or an object
                implementing its API, or ``NoneType`` (if no transaction is
                active).
        :returns: The transaction at the top of the batch stack.
        """
        transaction = self.current_batch
        if isinstance(transaction, Transaction):
            return transaction

    def get(self, key, missing=None, deferred=None):
        """Retrieve an entity from a single key (if it exists).

        .. note::

           This is just a thin wrapper over :meth:`get_multi`.
           The backend API does not make a distinction between a single key or
           multiple keys in a lookup request.

        :type key: :class:`gcloud.datastore.key.Key`
        :param key: The key to be retrieved from the datastore.

        :type missing: list
        :param missing: (Optional) If a list is passed, the key-only entities
                        returned by the backend as "missing" will be copied
                        into it.

        :type deferred: list
        :param deferred: (Optional) If a list is passed, the keys returned
                         by the backend as "deferred" will be copied into it.

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

        :type missing: list
        :param missing: (Optional) If a list is passed, the key-only entities
                        returned by the backend as "missing" will be copied
                        into it. If the list is not empty, an error will occur.

        :type deferred: list
        :param deferred: (Optional) If a list is passed, the keys returned
                         by the backend as "deferred" will be copied into it.
                         If the list is not empty, an error will occur.

        :rtype: list of :class:`gcloud.datastore.entity.Entity`
        :returns: The requested entities.
        :raises: :class:`ValueError` if one or more of ``keys`` has a project
                 which does not match our project.
        """
        if not keys:
            return []

        ids = set(key.project for key in keys)
        for current_id in ids:
            if current_id != self.project:
                raise ValueError('Keys do not match project')

        transaction = self.current_transaction

        entity_pbs = _extended_lookup(
            connection=self.connection,
            project=self.project,
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

        :raises: :class:`ValueError` if ``entities`` is a single entity.
        """
        if isinstance(entities, Entity):
            raise ValueError("Pass a sequence of entities")

        if not entities:
            return

        current = self.current_batch
        in_batch = current is not None

        if not in_batch:
            current = self.batch()

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
        current = self.current_batch
        in_batch = current is not None

        if not in_batch:
            current = self.batch()

        for key in keys:
            current.delete(key)

        if not in_batch:
            current.commit()

    def allocate_ids(self, incomplete_key, num_ids):
        """Allocate a list of IDs from a partial key.

        :type incomplete_key: :class:`gcloud.datastore.key.Key`
        :param incomplete_key: Partial key to use as base for allocated IDs.

        :type num_ids: int
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
        allocated_key_pbs = conn.allocate_ids(incomplete_key.project,
                                              incomplete_key_pbs)
        allocated_ids = [allocated_key_pb.path[-1].id
                         for allocated_key_pb in allocated_key_pbs]
        return [incomplete_key.completed_key(allocated_id)
                for allocated_id in allocated_ids]

    def key(self, *path_args, **kwargs):
        """Proxy to :class:`gcloud.datastore.key.Key`.

        Passes our ``project``.
        """
        if 'project' in kwargs:
            raise TypeError('Cannot pass project')
        kwargs['project'] = self.project
        if 'namespace' not in kwargs:
            kwargs['namespace'] = self.namespace
        return Key(*path_args, **kwargs)

    def batch(self):
        """Proxy to :class:`gcloud.datastore.batch.Batch`."""
        return Batch(self)

    def transaction(self):
        """Proxy to :class:`gcloud.datastore.transaction.Transaction`."""
        return Transaction(self)

    def query(self, **kwargs):
        """Proxy to :class:`gcloud.datastore.query.Query`.

        Passes our ``project``.
        """
        if 'client' in kwargs:
            raise TypeError('Cannot pass client')
        if 'project' in kwargs:
            raise TypeError('Cannot pass project')
        kwargs['project'] = self.project
        if 'namespace' not in kwargs:
            kwargs['namespace'] = self.namespace
        return Query(self, **kwargs)
