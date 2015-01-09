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

"""Connections to gcloud datastore API servers."""

import six

from gcloud import connection
from gcloud.datastore import datastore_v1_pb2 as datastore_pb
from gcloud.datastore import helpers


class Connection(connection.Connection):
    """A connection to the Google Cloud Datastore via the Protobuf API.

    This class should understand only the basic types (and protobufs)
    in method arguments, however should be capable of returning advanced types.

    :type credentials: :class:`oauth2client.client.OAuth2Credentials`
    :param credentials: The OAuth2 Credentials to use for this connection.
    """

    API_VERSION = 'v1beta2'
    """The version of the API, used in building the API call's URL."""

    API_URL_TEMPLATE = ('{api_base}/datastore/{api_version}'
                        '/datasets/{dataset_id}/{method}')
    """A template for the URL of a particular API call."""

    def __init__(self, credentials=None):
        super(Connection, self).__init__(credentials=credentials)
        self._current_transaction = None

    def _request(self, dataset_id, method, data):
        """Make a request over the Http transport to the Cloud Datastore API.

        :type dataset_id: string
        :param dataset_id: The ID of the dataset of which to make the request.

        :type method: string
        :param method: The API call method name (ie, ``runQuery``,
                       ``lookup``, etc)

        :type data: string
        :param data: The data to send with the API call.
                     Typically this is a serialized Protobuf string.

        :rtype: string
        :returns: The string response content from the API call.
        :raises: :class:`six.moves.http_client.HTTPException` if the response
                 code is not 200 OK.
        """
        headers = {
            'Content-Type': 'application/x-protobuf',
            'Content-Length': str(len(data)),
            'User-Agent': self.USER_AGENT,
        }
        headers, content = self.http.request(
            uri=self.build_api_url(dataset_id=dataset_id, method=method),
            method='POST', headers=headers, body=data)

        status = headers['status']
        if status != '200':
            message = ('Request failed with status code %s. '
                       'Error was: %s' % (status, content))
            raise six.moves.http_client.HTTPException(message)

        return content

    def _rpc(self, dataset_id, method, request_pb, response_pb_cls):
        """Make a protobuf RPC request.

        :type dataset_id: string
        :param dataset_id: The ID of the dataset to connect to. This is
                           usually your project name in the cloud console.

        :type method: string
        :param method: The name of the method to invoke.

        :type request_pb: :class:`google.protobuf.message.Message` instance
        :param request_pb: the protobuf instance representing the request.

        :type response_pb_cls: A :class:`google.protobuf.message.Message'
                               subclass.
        :param response_pb_cls: The class used to unmarshall the response
                                protobuf.
        """
        response = self._request(dataset_id=dataset_id, method=method,
                                 data=request_pb.SerializeToString())
        return response_pb_cls.FromString(response)

    @classmethod
    def build_api_url(cls, dataset_id, method, base_url=None,
                      api_version=None):
        """Construct the URL for a particular API call.

        This method is used internally to come up with the URL to use when
        making RPCs to the Cloud Datastore API.

        :type dataset_id: string
        :param dataset_id: The ID of the dataset to connect to. This is
                           usually your project name in the cloud console.

        :type method: string
        :param method: The API method to call (ie, runQuery, lookup, ...).

        :type base_url: string
        :param base_url: The base URL where the API lives.
                         You shouldn't have to provide this.

        :type api_version: string
        :param api_version: The version of the API to connect to.
                            You shouldn't have to provide this.
        """
        return cls.API_URL_TEMPLATE.format(
            api_base=(base_url or cls.API_BASE_URL),
            api_version=(api_version or cls.API_VERSION),
            dataset_id=dataset_id, method=method)

    def transaction(self, transaction=connection.Connection._EMPTY):
        """Getter/setter for the connection's transaction object.

        :type transaction: :class:`gcloud.datastore.transaction.Transaction`,
                           (setting), or omitted (getting).
        :param transaction: The new transaction (if passed).

        :rtype: :class:`gcloud.datastore.transaction.Transaction`, (getting)
                or :class:`gcloud.datastore.connection.Connection` (setting)
        :returns: The current transaction (getting) or self (setting).
        """
        if transaction is self._EMPTY:
            return self._current_transaction
        else:
            self._current_transaction = transaction
            return self

    def mutation(self):
        """Getter for mutation usable with current connection.

        :rtype: :class:`gcloud.datastore.datastore_v1_pb2.Mutation`.
        :returns: The mutation instance associated with the current transaction
                  (if one exists) or or a new mutation instance.
        """
        if self.transaction():
            return self.transaction().mutation
        else:
            return datastore_pb.Mutation()

    def lookup(self, dataset_id, key_pbs,
               missing=None, deferred=None, eventual=False):
        """Lookup keys from a dataset in the Cloud Datastore.

        Maps the ``DatastoreService.Lookup`` protobuf RPC.

        This method deals only with protobufs
        (:class:`gcloud.datastore.datastore_v1_pb2.Key` and
        :class:`gcloud.datastore.datastore_v1_pb2.Entity`) and is used
        under the hood in :func:`gcloud.datastore.get`:

        >>> from gcloud import datastore
        >>> datastore.set_defaults()
        >>> key = datastore.Key('MyKind', 1234, dataset_id='dataset-id')
        >>> datastore.get(key)
        <Entity object>

        Using the ``connection`` class directly:

        >>> connection.lookup('dataset-id', key.to_protobuf())
        <Entity protobuf>

        :type dataset_id: string
        :param dataset_id: The ID of the dataset to look up the keys.

        :type key_pbs: list of :class:`gcloud.datastore.datastore_v1_pb2.Key`
                       (or a single Key)
        :param key_pbs: The key (or keys) to retrieve from the datastore.

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
                        consistency.  If the connection has a current
                        transaction, this value *must* be false.

        :rtype: list of :class:`gcloud.datastore.datastore_v1_pb2.Entity`
                (or a single Entity)
        :returns: The entities corresponding to the keys provided.
                  If a single key was provided and no results matched,
                  this will return None.
                  If multiple keys were provided and no results matched,
                  this will return an empty list.
        :raises: ValueError if ``eventual`` is True
        """
        if missing is not None and missing != []:
            raise ValueError('missing must be None or an empty list')

        if deferred is not None and deferred != []:
            raise ValueError('deferred must be None or an empty list')

        lookup_request = datastore_pb.LookupRequest()
        self._set_read_options(lookup_request, eventual)

        single_key = isinstance(key_pbs, datastore_pb.Key)

        if single_key:
            key_pbs = [key_pbs]

        helpers._add_keys_to_request(lookup_request.key, key_pbs)

        results, missing_found, deferred_found = self._lookup(
            lookup_request, dataset_id, deferred is not None)

        if missing is not None:
            missing.extend(missing_found)

        if deferred is not None:
            deferred.extend(deferred_found)

        if single_key:
            if results:
                return results[0]
            else:
                return None

        return results

    def run_query(self, dataset_id, query_pb, namespace=None, eventual=False):
        """Run a query on the Cloud Datastore.

        Maps the ``DatastoreService.RunQuery`` protobuf RPC.

        Given a Query protobuf, sends a ``runQuery`` request to the
        Cloud Datastore API and returns a list of entity protobufs
        matching the query.

        You typically wouldn't use this method directly, in favor of the
        :meth:`gcloud.datastore.query.Query.fetch` method.

        Under the hood, the :class:`gcloud.datastore.query.Query` class
        uses this method to fetch data:

        >>> from gcloud import datastore

        >>> datastore.set_defaults()

        >>> query = datastore.Query(kind='MyKind')
        >>> query.add_filter('property', '=', 'val')

        Using the query's ``fetch_page`` method...

        >>> entities, cursor, more_results = query.fetch_page()
        >>> entities
        [<list of Entity unmarshalled from protobuf>]
        >>> cursor
        <string containing cursor where fetch stopped>
        >>> more_results
        <boolean of more results>

        Under the hood this is doing...

        >>> connection.run_query('dataset-id', query.to_protobuf())
        [<list of Entity Protobufs>], cursor, more_results, skipped_results

        :type dataset_id: string
        :param dataset_id: The ID of the dataset over which to run the query.

        :type query_pb: :class:`gcloud.datastore.datastore_v1_pb2.Query`
        :param query_pb: The Protobuf representing the query to run.

        :type namespace: string
        :param namespace: The namespace over which to run the query.

        :type eventual: boolean
        :param eventual: If False (the default), request ``STRONG`` read
                         consistency.  If True, request ``EVENTUAL`` read
                         consistency.  If the connection has a current
                         transaction, this value *must* be false.
        """
        request = datastore_pb.RunQueryRequest()
        self._set_read_options(request, eventual)

        if namespace:
            request.partition_id.namespace = namespace

        request.query.CopyFrom(query_pb)
        response = self._rpc(dataset_id, 'runQuery', request,
                             datastore_pb.RunQueryResponse)
        return (
            [e.entity for e in response.batch.entity_result],
            response.batch.end_cursor,  # Assume response always has cursor.
            response.batch.more_results,
            response.batch.skipped_results,
        )

    def begin_transaction(self, dataset_id, serializable=False):
        """Begin a transaction.

        Maps the ``DatastoreService.BeginTransaction`` protobuf RPC.

        :type dataset_id: string
        :param dataset_id: The ID dataset to which the transaction applies.

        :type serializable: boolean
        :param serializable: Boolean indicating if the isolation level of the
                             transaction should be SERIALIZABLE (True) or
                             SNAPSHOT (False).

        :rtype: :class:`.datastore_v1_pb2.BeginTransactionResponse`
        :returns': the result protobuf for the begin transaction request.
        """
        if self.transaction():
            raise ValueError('Cannot start a transaction with another already '
                             'in progress.')

        request = datastore_pb.BeginTransactionRequest()

        if serializable:
            request.isolation_level = (
                datastore_pb.BeginTransactionRequest.SERIALIZABLE)
        else:
            request.isolation_level = (
                datastore_pb.BeginTransactionRequest.SNAPSHOT)

        response = self._rpc(dataset_id, 'beginTransaction', request,
                             datastore_pb.BeginTransactionResponse)

        return response.transaction

    def commit(self, dataset_id, mutation_pb):
        """Commit dataset mutations in context of current transation (if any).

        Maps the ``DatastoreService.Commit`` protobuf RPC.

        :type dataset_id: string
        :param dataset_id: The ID dataset to which the transaction applies.

        :type mutation_pb: :class:`gcloud.datastore.datastore_v1_pb2.Mutation`.
        :param mutation_pb: The protobuf for the mutations being saved.

        :rtype: :class:`gcloud.datastore.datastore_v1_pb2.MutationResult`.
        :returns': the result protobuf for the mutation.
        """
        request = datastore_pb.CommitRequest()

        if self.transaction():
            request.mode = datastore_pb.CommitRequest.TRANSACTIONAL
            request.transaction = self.transaction().id
        else:
            request.mode = datastore_pb.CommitRequest.NON_TRANSACTIONAL

        request.mutation.CopyFrom(mutation_pb)
        response = self._rpc(dataset_id, 'commit', request,
                             datastore_pb.CommitResponse)
        return response.mutation_result

    def rollback(self, dataset_id):
        """Rollback the connection's existing transaction.

        Maps the ``DatastoreService.Rollback`` protobuf RPC.

        :type dataset_id: string
        :param dataset_id: The ID of the dataset to which the transaction
                           belongs.

        :raises: :class:`ValueError` if the connection isn't currently in a
                 transaction.
        """
        if not self.transaction() or not self.transaction().id:
            raise ValueError('No transaction to rollback.')

        request = datastore_pb.RollbackRequest()
        request.transaction = self.transaction().id
        # Nothing to do with this response, so just execute the method.
        self._rpc(dataset_id, 'rollback', request,
                  datastore_pb.RollbackResponse)

    def allocate_ids(self, dataset_id, key_pbs):
        """Obtain backend-generated IDs for a set of keys.

        Maps the ``DatastoreService.AllocateIds`` protobuf RPC.

        :type dataset_id: string
        :param dataset_id: The ID of the dataset to which the transaction
                           belongs.

        :type key_pbs: list of :class:`gcloud.datastore.datastore_v1_pb2.Key`
        :param key_pbs: The keys for which the backend should allocate IDs.

        :rtype: list of :class:`gcloud.datastore.datastore_v1_pb2.Key`
        :returns: An equal number of keys,  with IDs filled in by the backend.
        """
        request = datastore_pb.AllocateIdsRequest()
        helpers._add_keys_to_request(request.key, key_pbs)
        # Nothing to do with this response, so just execute the method.
        response = self._rpc(dataset_id, 'allocateIds', request,
                             datastore_pb.AllocateIdsResponse)
        return list(response.key)

    def save_entity(self, dataset_id, key_pb, properties,
                    exclude_from_indexes=(), mutation=None):
        """Save an entity to the Cloud Datastore with the provided properties.

        .. note::
           Any existing properties for the entity identified by ``key_pb``
           will be replaced by those passed in ``properties``;  properties
           not passed in ``properties`` no longer be set for the entity.

        :type dataset_id: string
        :param dataset_id: The ID of the dataset in which to save the entity.

        :type key_pb: :class:`gcloud.datastore.datastore_v1_pb2.Key`
        :param key_pb: The complete or partial key for the entity.

        :type properties: dict
        :param properties: The properties to store on the entity.

        :type exclude_from_indexes: sequence of string
        :param exclude_from_indexes: Names of properties *not* to be indexed.

        :type mutation: :class:`gcloud.datastore.datastore_v1_pb2.Mutation`
                        or None.
        :param mutation: If passed, the mutation protobuf into which the
                         entity will be saved.  If None, use th result
                         of calling ``self.mutation()``

        :rtype: tuple
        :returns: The pair (``assigned``, ``new_id``) where ``assigned`` is a
                  boolean indicating if a new ID has been assigned and
                  ``new_id`` is either ``None`` or an integer that has been
                  assigned.
        """
        if mutation is not None:
            in_batch = True
        else:
            in_batch = False
            mutation = self.mutation()

        key_pb = helpers._prepare_key_for_request(key_pb)

        # If the Key is complete, we should upsert
        # instead of using insert_auto_id.
        path = key_pb.path_element[-1]
        auto_id = not (path.HasField('id') or path.HasField('name'))

        if auto_id:
            insert = mutation.insert_auto_id.add()
        else:
            insert = mutation.upsert.add()

        insert.key.CopyFrom(key_pb)

        for name, value in properties.items():
            prop = insert.property.add()
            # Set the name of the property.
            prop.name = name

            # Set the appropriate value.
            helpers._set_protobuf_value(prop.value, value)

            if name in exclude_from_indexes:
                if not isinstance(value, list):
                    prop.value.indexed = False

                for sub_value in prop.value.list_value:
                    sub_value.indexed = False

        # If this is in a transaction, we should just return True. The
        # transaction will handle assigning any keys as necessary.
        if in_batch or self.transaction():
            return False, None

        result = self.commit(dataset_id, mutation)
        # If this was an auto-assigned ID, return the new Key. We don't
        # verify that this matches the original `key_pb` but trust the
        # backend to uphold the values sent (e.g. dataset ID).
        if auto_id:
            inserted_key_pb = result.insert_auto_id_key[0]
            # Assumes the backend has set `id` without checking HasField('id').
            return True, inserted_key_pb.path_element[-1].id

        return False, None

    def delete_entities(self, dataset_id, key_pbs, mutation=None):
        """Delete keys from a dataset in the Cloud Datastore.

        This method deals only with
        :class:`gcloud.datastore.datastore_v1_pb2.Key` protobufs and not
        with any of the other abstractions.  For example, it's used
        under the hood in the
        :meth:`gcloud.datastore.entity.Entity.delete` method.

        :type dataset_id: string
        :param dataset_id: The ID of the dataset from which to delete the keys.

        :type key_pbs: list of :class:`gcloud.datastore.datastore_v1_pb2.Key`
        :param key_pbs: The keys to delete from the datastore.

        :type mutation: :class:`gcloud.datastore.datastore_v1_pb2.Mutation`
                        or None.
        :param mutation: If passed, the mutation protobuf into which the
                         deletion will be saved.  If None, use th result
                         of calling ``self.mutation()``

        :rtype: boolean
        :returns: ``True``
        """
        if mutation is not None:
            in_batch = True
        else:
            in_batch = False
            mutation = self.mutation()

        helpers._add_keys_to_request(mutation.delete, key_pbs)

        if not in_batch and not self.transaction():
            self.commit(dataset_id, mutation)

        return True

    def _lookup(self, lookup_request, dataset_id, stop_on_deferred):
        """Repeat lookup until all keys found (unless stop requested).

        Helper method for ``lookup()``.
        """
        results = []
        missing = []
        deferred = []
        while True:  # loop against possible deferred.
            lookup_response = self._rpc(dataset_id, 'lookup', lookup_request,
                                        datastore_pb.LookupResponse)

            results.extend(
                [result.entity for result in lookup_response.found])

            missing.extend(
                [result.entity for result in lookup_response.missing])

            if stop_on_deferred:
                deferred.extend([key for key in lookup_response.deferred])
                break

            if not lookup_response.deferred:
                break

            # We have deferred keys, and the user didn't ask to know about
            # them, so retry (but only with the deferred ones).
            _copy_deferred_keys(lookup_request, lookup_response)
        return results, missing, deferred

    def _set_read_options(self, request, eventual):
        """Validate rules for read options, and assign to the request.

        Helper method for ``lookup()`` and ``run_query``.
        """
        transaction = self.transaction()
        if eventual and transaction:
            raise ValueError('eventual must be False when in a transaction')

        opts = request.read_options
        if eventual:
            opts.read_consistency = datastore_pb.ReadOptions.EVENTUAL
        elif transaction:
            opts.transaction = transaction.id


def _copy_deferred_keys(lookup_request, lookup_response):
    """Clear requested keys and copy deferred keys back in.

    Helper for ``Connection.lookup()``.
    """
    for old_key in list(lookup_request.key):
        lookup_request.key.remove(old_key)
    for def_key in lookup_response.deferred:
        lookup_request.key.add().CopyFrom(def_key)
