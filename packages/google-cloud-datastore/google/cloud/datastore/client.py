# Copyright 2014 Google LLC
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

from google.cloud.proto.datastore.v1 import datastore_pb2 as _datastore_pb2

from google.cloud._helpers import _LocalStack
from google.cloud._helpers import (
    _determine_default_project as _base_default_project)
from google.cloud.client import ClientWithProject
from google.cloud.environment_vars import DISABLE_GRPC
from google.cloud.environment_vars import GCD_DATASET
from google.cloud.environment_vars import GCD_HOST

from google.cloud.datastore._http import HTTPDatastoreAPI
from google.cloud.datastore import helpers
from google.cloud.datastore.batch import Batch
from google.cloud.datastore.entity import Entity
from google.cloud.datastore.key import Key
from google.cloud.datastore.query import Query
from google.cloud.datastore.transaction import Transaction
try:
    from google.cloud.datastore._gax import make_datastore_api
    _HAVE_GRPC = True
except ImportError:  # pragma: NO COVER
    make_datastore_api = None
    _HAVE_GRPC = False


_MAX_LOOPS = 128
"""Maximum number of iterations to wait for deferred keys."""
_DATASTORE_BASE_URL = 'https://datastore.googleapis.com'
"""Datastore API request URL base."""

_USE_GRPC = _HAVE_GRPC and not os.getenv(DISABLE_GRPC, False)


def _get_gcd_project():
    """Gets the GCD application ID if it can be inferred."""
    return os.getenv(GCD_DATASET)


def _determine_default_project(project=None):
    """Determine default project explicitly or implicitly as fall-back.

    In implicit case, supports four environments. In order of precedence, the
    implicit environments are:

    * DATASTORE_DATASET environment variable (for ``gcd`` / emulator testing)
    * GOOGLE_CLOUD_PROJECT environment variable
    * Google App Engine application ID
    * Google Compute Engine project ID (from metadata server)

    :type project: str
    :param project: Optional. The project to use as default.

    :rtype: str or ``NoneType``
    :returns: Default project if it can be determined.
    """
    if project is None:
        project = _get_gcd_project()

    if project is None:
        project = _base_default_project(project=project)

    return project


def _extended_lookup(datastore_api, project, key_pbs,
                     missing=None, deferred=None,
                     eventual=False, transaction_id=None):
    """Repeat lookup until all keys found (unless stop requested).

    Helper function for :meth:`Client.get_multi`.

    :type datastore_api:
        :class:`google.cloud.datastore._http.HTTPDatastoreAPI`
        or :class:`google.cloud.datastore._gax.GAPICDatastoreAPI`
    :param datastore_api: The datastore API object used to connect
                          to datastore.

    :type project: str
    :param project: The project to make the request for.

    :type key_pbs: list of :class:`.entity_pb2.Key`
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

    :type transaction_id: str
    :param transaction_id: If passed, make the request in the scope of
                           the given transaction.  Incompatible with
                           ``eventual==True``.

    :rtype: list of :class:`.entity_pb2.Entity`
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
    read_options = _get_read_options(eventual, transaction_id)
    while loop_num < _MAX_LOOPS:  # loop against possible deferred.
        loop_num += 1
        lookup_response = datastore_api.lookup(
            project, read_options, key_pbs)

        # Accumulate the new results.
        results.extend(result.entity for result in lookup_response.found)

        if missing is not None:
            missing.extend(result.entity for result in lookup_response.missing)

        if deferred is not None:
            deferred.extend(lookup_response.deferred)
            break

        if len(lookup_response.deferred) == 0:
            break

        # We have deferred keys, and the user didn't ask to know about
        # them, so retry (but only with the deferred ones).
        key_pbs = lookup_response.deferred

    return results


class Client(ClientWithProject):
    """Convenience wrapper for invoking APIs/factories w/ a project.

    .. doctest::

       >>> from google.cloud import datastore
       >>> client = datastore.Client()

    :type project: str
    :param project: (optional) The project to pass to proxied API methods.

    :type namespace: str
    :param namespace: (optional) namespace to pass to proxied API methods.

    :type credentials: :class:`~google.auth.credentials.Credentials`
    :param credentials: (Optional) The OAuth2 Credentials to use for this
                        client. If not passed (and if no ``_http`` object is
                        passed), falls back to the default inferred from the
                        environment.

    :type _http: :class:`~requests.Session`
    :param _http: (Optional) HTTP object to make requests. Can be any object
                  that defines ``request()`` with the same interface as
                  :meth:`requests.Session.request`. If not passed, an
                  ``_http`` object is created that is bound to the
                  ``credentials`` for the current object.
                  This parameter should be considered private, and could
                  change in the future.

    :type _use_grpc: bool
    :param _use_grpc: (Optional) Explicitly specifies whether
                      to use the gRPC transport (via GAX) or HTTP. If unset,
                      falls back to the ``GOOGLE_CLOUD_DISABLE_GRPC``
                      environment variable.
                      This parameter should be considered private, and could
                      change in the future.
    """

    SCOPE = ('https://www.googleapis.com/auth/datastore',)
    """The scopes required for authenticating as a Cloud Datastore consumer."""

    def __init__(self, project=None, namespace=None,
                 credentials=None, _http=None, _use_grpc=None):
        super(Client, self).__init__(
            project=project, credentials=credentials, _http=_http)
        self.namespace = namespace
        self._batch_stack = _LocalStack()
        self._datastore_api_internal = None
        if _use_grpc is None:
            self._use_grpc = _USE_GRPC
        else:
            self._use_grpc = _use_grpc
        try:
            host = os.environ[GCD_HOST]
            self._base_url = 'http://' + host
        except KeyError:
            self._base_url = _DATASTORE_BASE_URL

    @staticmethod
    def _determine_default(project):
        """Helper:  override default project detection."""
        return _determine_default_project(project)

    @property
    def _datastore_api(self):
        """Getter for a wrapped API object."""
        if self._datastore_api_internal is None:
            if self._use_grpc:
                self._datastore_api_internal = make_datastore_api(self)
            else:
                self._datastore_api_internal = HTTPDatastoreAPI(self)
        return self._datastore_api_internal

    def _push_batch(self, batch):
        """Push a batch/transaction onto our stack.

        "Protected", intended for use by batch / transaction context mgrs.

        :type batch: :class:`google.cloud.datastore.batch.Batch`, or an object
                     implementing its API.
        :param batch: newly-active batch/transaction.
        """
        self._batch_stack.push(batch)

    def _pop_batch(self):
        """Pop a batch/transaction from our stack.

        "Protected", intended for use by batch / transaction context mgrs.

        :raises: IndexError if the stack is empty.
        :rtype: :class:`google.cloud.datastore.batch.Batch`, or an object
                 implementing its API.
        :returns: the top-most batch/transaction, after removing it.
        """
        return self._batch_stack.pop()

    @property
    def current_batch(self):
        """Currently-active batch.

        :rtype: :class:`google.cloud.datastore.batch.Batch`, or an object
                implementing its API, or ``NoneType`` (if no batch is active).
        :returns: The batch/transaction at the top of the batch stack.
        """
        return self._batch_stack.top

    @property
    def current_transaction(self):
        """Currently-active transaction.

        :rtype: :class:`google.cloud.datastore.transaction.Transaction`, or an
                object implementing its API, or ``NoneType`` (if no transaction
                is active).
        :returns: The transaction at the top of the batch stack.
        """
        transaction = self.current_batch
        if isinstance(transaction, Transaction):
            return transaction

    def get(self, key, missing=None, deferred=None, transaction=None):
        """Retrieve an entity from a single key (if it exists).

        .. note::

           This is just a thin wrapper over :meth:`get_multi`.
           The backend API does not make a distinction between a single key or
           multiple keys in a lookup request.

        :type key: :class:`google.cloud.datastore.key.Key`
        :param key: The key to be retrieved from the datastore.

        :type missing: list
        :param missing: (Optional) If a list is passed, the key-only entities
                        returned by the backend as "missing" will be copied
                        into it.

        :type deferred: list
        :param deferred: (Optional) If a list is passed, the keys returned
                         by the backend as "deferred" will be copied into it.

        :type transaction:
            :class:`~google.cloud.datastore.transaction.Transaction`
        :param transaction: (Optional) Transaction to use for read consistency.
                            If not passed, uses current transaction, if set.

        :rtype: :class:`google.cloud.datastore.entity.Entity` or ``NoneType``
        :returns: The requested entity if it exists.
        """
        entities = self.get_multi(keys=[key], missing=missing,
                                  deferred=deferred, transaction=transaction)
        if entities:
            return entities[0]

    def get_multi(self, keys, missing=None, deferred=None, transaction=None):
        """Retrieve entities, along with their attributes.

        :type keys: list of :class:`google.cloud.datastore.key.Key`
        :param keys: The keys to be retrieved from the datastore.

        :type missing: list
        :param missing: (Optional) If a list is passed, the key-only entities
                        returned by the backend as "missing" will be copied
                        into it. If the list is not empty, an error will occur.

        :type deferred: list
        :param deferred: (Optional) If a list is passed, the keys returned
                         by the backend as "deferred" will be copied into it.
                         If the list is not empty, an error will occur.

        :type transaction:
            :class:`~google.cloud.datastore.transaction.Transaction`
        :param transaction: (Optional) Transaction to use for read consistency.
                            If not passed, uses current transaction, if set.

        :rtype: list of :class:`google.cloud.datastore.entity.Entity`
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

        if transaction is None:
            transaction = self.current_transaction

        entity_pbs = _extended_lookup(
            datastore_api=self._datastore_api,
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

        :type entity: :class:`google.cloud.datastore.entity.Entity`
        :param entity: The entity to be saved to the datastore.
        """
        self.put_multi(entities=[entity])

    def put_multi(self, entities):
        """Save entities in the Cloud Datastore.

        :type entities: list of :class:`google.cloud.datastore.entity.Entity`
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
            current.begin()

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

        :type key: :class:`google.cloud.datastore.key.Key`
        :param key: The key to be deleted from the datastore.
        """
        self.delete_multi(keys=[key])

    def delete_multi(self, keys):
        """Delete keys from the Cloud Datastore.

        :type keys: list of :class:`google.cloud.datastore.key.Key`
        :param keys: The keys to be deleted from the Datastore.
        """
        if not keys:
            return

        # We allow partial keys to attempt a delete, the backend will fail.
        current = self.current_batch
        in_batch = current is not None

        if not in_batch:
            current = self.batch()
            current.begin()

        for key in keys:
            current.delete(key)

        if not in_batch:
            current.commit()

    def allocate_ids(self, incomplete_key, num_ids):
        """Allocate a list of IDs from a partial key.

        :type incomplete_key: :class:`google.cloud.datastore.key.Key`
        :param incomplete_key: Partial key to use as base for allocated IDs.

        :type num_ids: int
        :param num_ids: The number of IDs to allocate.

        :rtype: list of :class:`google.cloud.datastore.key.Key`
        :returns: The (complete) keys allocated with ``incomplete_key`` as
                  root.
        :raises: :class:`ValueError` if ``incomplete_key`` is not a
                 partial key.
        """
        if not incomplete_key.is_partial:
            raise ValueError(('Key is not partial.', incomplete_key))

        incomplete_key_pb = incomplete_key.to_protobuf()
        incomplete_key_pbs = [incomplete_key_pb] * num_ids

        response_pb = self._datastore_api.allocate_ids(
            incomplete_key.project, incomplete_key_pbs)
        allocated_ids = [allocated_key_pb.path[-1].id
                         for allocated_key_pb in response_pb.keys]
        return [incomplete_key.completed_key(allocated_id)
                for allocated_id in allocated_ids]

    def key(self, *path_args, **kwargs):
        """Proxy to :class:`google.cloud.datastore.key.Key`.

        Passes our ``project``.
        """
        if 'project' in kwargs:
            raise TypeError('Cannot pass project')
        kwargs['project'] = self.project
        if 'namespace' not in kwargs:
            kwargs['namespace'] = self.namespace
        return Key(*path_args, **kwargs)

    def batch(self):
        """Proxy to :class:`google.cloud.datastore.batch.Batch`."""
        return Batch(self)

    def transaction(self):
        """Proxy to :class:`google.cloud.datastore.transaction.Transaction`."""
        return Transaction(self)

    def query(self, **kwargs):
        """Proxy to :class:`google.cloud.datastore.query.Query`.

        Passes our ``project``.

        Using query to search a datastore:

        .. testsetup:: query

            import os
            import uuid

            from google.cloud import datastore

            unique = os.getenv('CIRCLE_BUILD_NUM', str(uuid.uuid4())[0:8])
            client = datastore.Client(namespace='ns{}'.format(unique))
            query = client.query(kind='_Doctest')

            def do_something(entity):
                pass

        .. doctest:: query

            >>> query = client.query(kind='MyKind')
            >>> query.add_filter('property', '=', 'val')

        Using the query iterator

        .. doctest:: query

            >>> query_iter = query.fetch()
            >>> for entity in query_iter:
            ...     do_something(entity)

        or manually page through results

        .. testsetup:: query-page

            import os
            import uuid

            from google.cloud import datastore
            from tests.system.test_system import Config  # system tests

            unique = os.getenv('CIRCLE_BUILD_NUM', str(uuid.uuid4())[0:8])
            client = datastore.Client(namespace='ns{}'.format(unique))

            key = client.key('_Doctest')
            entity1 = datastore.Entity(key=key)
            entity1['foo'] = 1337
            entity2 = datastore.Entity(key=key)
            entity2['foo'] = 42
            Config.TO_DELETE.extend([entity1, entity2])
            client.put_multi([entity1, entity2])

            query = client.query(kind='_Doctest')
            cursor = None

        .. doctest:: query-page

            >>> query_iter = query.fetch(start_cursor=cursor)
            >>> pages = query_iter.pages
            >>>
            >>> first_page = next(pages)
            >>> first_page_entities = list(first_page)
            >>> query_iter.next_page_token
            b'...'

        :type kwargs: dict
        :param kwargs: Parameters for initializing and instance of
                       :class:`~google.cloud.datastore.query.Query`.

        :rtype: :class:`~google.cloud.datastore.query.Query`
        :returns: A query object.
        """
        if 'client' in kwargs:
            raise TypeError('Cannot pass client')
        if 'project' in kwargs:
            raise TypeError('Cannot pass project')
        kwargs['project'] = self.project
        if 'namespace' not in kwargs:
            kwargs['namespace'] = self.namespace
        return Query(self, **kwargs)


def _get_read_options(eventual, transaction_id):
    """Validate rules for read options, and assign to the request.

    Helper method for ``lookup()`` and ``run_query``.

    :type eventual: bool
    :param eventual: Flag indicating if ``EVENTUAL`` or ``STRONG``
                     consistency should be used.

    :type transaction_id: bytes
    :param transaction_id: A transaction identifier (may be null).

    :rtype: :class:`.datastore_pb2.ReadOptions`
    :returns: The read options corresponding to the inputs.
    :raises: :class:`ValueError` if ``eventual`` is ``True`` and the
             ``transaction_id`` is not ``None``.
    """
    if transaction_id is None:
        if eventual:
            return _datastore_pb2.ReadOptions(
                read_consistency=_datastore_pb2.ReadOptions.EVENTUAL)
        else:
            return _datastore_pb2.ReadOptions()
    else:
        if eventual:
            raise ValueError('eventual must be False when in a transaction')
        else:
            return _datastore_pb2.ReadOptions(
                transaction=transaction_id)
