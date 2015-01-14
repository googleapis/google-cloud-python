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
from gcloud.datastore import _datastore_v1_pb2 as datastore_pb
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

    def lookup(self, dataset_id, key_pbs,
               missing=None, deferred=None,
               eventual=False, transaction_id=None):
        """Lookup keys from a dataset in the Cloud Datastore.

        Maps the ``DatastoreService.Lookup`` protobuf RPC.

        This method deals only with protobufs
        (:class:`gcloud.datastore._datastore_v1_pb2.Key` and
        :class:`gcloud.datastore._datastore_v1_pb2.Entity`) and is used
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

        :type key_pbs: list of :class:`gcloud.datastore._datastore_v1_pb2.Key`
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
                        consistency.

        :type transaction_id: string
        :param transaction_id: If passed, make the request in the scope of
                               the given transaction.  Incompatible with
                               ``eventual==True``.

        :rtype: list of :class:`gcloud.datastore._datastore_v1_pb2.Entity`
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
        _set_read_options(lookup_request, eventual, transaction_id)

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

    def run_query(self, dataset_id, query_pb, namespace=None,
                  eventual=False, transaction_id=None):
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

        :type query_pb: :class:`gcloud.datastore._datastore_v1_pb2.Query`
        :param query_pb: The Protobuf representing the query to run.

        :type namespace: string
        :param namespace: The namespace over which to run the query.

        :type eventual: boolean
        :param eventual: If False (the default), request ``STRONG`` read
                         consistency.  If True, request ``EVENTUAL`` read
                         consistency.

        :type transaction_id: string
        :param transaction_id: If passed, make the request in the scope of
                               the given transaction.  Incompatible with
                               ``eventual==True``.
        """
        request = datastore_pb.RunQueryRequest()
        _set_read_options(request, eventual, transaction_id)

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

        :rtype: :class:`._datastore_v1_pb2.BeginTransactionResponse`
        :returns': the result protobuf for the begin transaction request.
        """
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

    def commit(self, dataset_id, mutation_pb, transaction_id=None):
        """Commit dataset mutations in context of current transation (if any).

        Maps the ``DatastoreService.Commit`` protobuf RPC.

        :type dataset_id: string
        :param dataset_id: The ID dataset to which the transaction applies.

        :type mutation_pb: :class:`datastore_pb.Mutation`.
        :param mutation_pb: The protobuf for the mutations being saved.

        :type transaction_id: string
        :param transaction_id: The transaction ID returned from
                               :meth:`begin_transaction`.  If not passed, the
                               commit will be non-transactional.

        :rtype: :class:`gcloud.datastore._datastore_v1_pb2.MutationResult`.
        :returns': the result protobuf for the mutation.
        """
        request = datastore_pb.CommitRequest()

        if transaction_id:
            request.mode = datastore_pb.CommitRequest.TRANSACTIONAL
            request.transaction = transaction_id
        else:
            request.mode = datastore_pb.CommitRequest.NON_TRANSACTIONAL

        request.mutation.CopyFrom(mutation_pb)
        response = self._rpc(dataset_id, 'commit', request,
                             datastore_pb.CommitResponse)
        return response.mutation_result

    def rollback(self, dataset_id, transaction_id):
        """Rollback the connection's existing transaction.

        Maps the ``DatastoreService.Rollback`` protobuf RPC.

        :type dataset_id: string
        :param dataset_id: The ID of the dataset to which the transaction
                           belongs.

        :type transaction_id: string
        :param transaction_id: The transaction ID returned from
                               :meth:`begin_transaction`.
        """
        request = datastore_pb.RollbackRequest()
        request.transaction = transaction_id
        # Nothing to do with this response, so just execute the method.
        self._rpc(dataset_id, 'rollback', request,
                  datastore_pb.RollbackResponse)

    def allocate_ids(self, dataset_id, key_pbs):
        """Obtain backend-generated IDs for a set of keys.

        Maps the ``DatastoreService.AllocateIds`` protobuf RPC.

        :type dataset_id: string
        :param dataset_id: The ID of the dataset to which the transaction
                           belongs.

        :type key_pbs: list of :class:`gcloud.datastore._datastore_v1_pb2.Key`
        :param key_pbs: The keys for which the backend should allocate IDs.

        :rtype: list of :class:`gcloud.datastore._datastore_v1_pb2.Key`
        :returns: An equal number of keys,  with IDs filled in by the backend.
        """
        request = datastore_pb.AllocateIdsRequest()
        helpers._add_keys_to_request(request.key, key_pbs)
        # Nothing to do with this response, so just execute the method.
        response = self._rpc(dataset_id, 'allocateIds', request,
                             datastore_pb.AllocateIdsResponse)
        return list(response.key)

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


def _set_read_options(request, eventual, transaction_id):
    """Validate rules for read options, and assign to the request.

    Helper method for ``lookup()`` and ``run_query``.
    """
    if eventual and (transaction_id is not None):
        raise ValueError('eventual must be False when in a transaction')

    opts = request.read_options
    if eventual:
        opts.read_consistency = datastore_pb.ReadOptions.EVENTUAL
    elif transaction_id:
        opts.transaction = transaction_id


def _copy_deferred_keys(lookup_request, lookup_response):
    """Clear requested keys and copy deferred keys back in.

    Helper for ``Connection.lookup()``.
    """
    for old_key in list(lookup_request.key):
        lookup_request.key.remove(old_key)
    for def_key in lookup_response.deferred:
        lookup_request.key.add().CopyFrom(def_key)
