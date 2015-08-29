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

import os

from gcloud import connection
from gcloud.environment_vars import GCD_HOST
from gcloud.exceptions import make_exception
from gcloud.datastore import _datastore_v1_pb2 as datastore_pb


class Connection(connection.Connection):
    """A connection to the Google Cloud Datastore via the Protobuf API.

    This class should understand only the basic types (and protobufs)
    in method arguments, however should be capable of returning advanced types.

    :type credentials: :class:`oauth2client.client.OAuth2Credentials`
    :param credentials: The OAuth2 Credentials to use for this connection.

    :type http: :class:`httplib2.Http` or class that defines ``request()``.
    :param http: An optional HTTP object to make requests.

    :type api_base_url: string
    :param api_base_url: The base of the API call URL. Defaults to the value
                         from :mod:`gcloud.connection`.
    """

    API_VERSION = 'v1beta2'
    """The version of the API, used in building the API call's URL."""

    API_URL_TEMPLATE = ('{api_base}/datastore/{api_version}'
                        '/datasets/{dataset_id}/{method}')
    """A template for the URL of a particular API call."""

    SCOPE = ('https://www.googleapis.com/auth/datastore',
             'https://www.googleapis.com/auth/userinfo.email')
    """The scopes required for authenticating as a Cloud Datastore consumer."""

    def __init__(self, credentials=None, http=None, api_base_url=None):
        super(Connection, self).__init__(credentials=credentials, http=http)
        if api_base_url is None:
            api_base_url = os.getenv(GCD_HOST,
                                     connection.API_BASE_URL)
        self.api_base_url = api_base_url

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
        :raises: :class:`gcloud.exceptions.GCloudError` if the response
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
            raise make_exception(headers, content, use_json=False)

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

    def build_api_url(self, dataset_id, method, base_url=None,
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
        return self.API_URL_TEMPLATE.format(
            api_base=(base_url or self.api_base_url),
            api_version=(api_version or self.API_VERSION),
            dataset_id=dataset_id, method=method)

    def lookup(self, dataset_id, key_pbs,
               eventual=False, transaction_id=None):
        """Lookup keys from a dataset in the Cloud Datastore.

        Maps the ``DatastoreService.Lookup`` protobuf RPC.

        This method deals only with protobufs
        (:class:`gcloud.datastore._datastore_v1_pb2.Key` and
        :class:`gcloud.datastore._datastore_v1_pb2.Entity`) and is used
        under the hood in :func:`gcloud.datastore.get`:

        >>> from gcloud import datastore
        >>> key = datastore.Key('MyKind', 1234, dataset_id='dataset-id')
        >>> datastore.get(key)
        [<Entity object>]

        Using the ``connection`` class directly:

        >>> connection.lookup('dataset-id', [key.to_protobuf()])
        [<Entity protobuf>]

        :type dataset_id: string
        :param dataset_id: The ID of the dataset to look up the keys.

        :type key_pbs: list of :class:`gcloud.datastore._datastore_v1_pb2.Key`
        :param key_pbs: The keys to retrieve from the datastore.

        :type eventual: boolean
        :param eventual: If False (the default), request ``STRONG`` read
                        consistency.  If True, request ``EVENTUAL`` read
                        consistency.

        :type transaction_id: string
        :param transaction_id: If passed, make the request in the scope of
                               the given transaction.  Incompatible with
                               ``eventual==True``.

        :rtype: tuple
        :returns: A triple of (``results``, ``missing``, ``deferred``) where
                  both ``results`` and ``missing`` are lists of
                  :class:`gcloud.datastore._datastore_v1_pb2.Entity` and
                  ``deferred`` is a list of
                  :class:`gcloud.datastore._datastore_v1_pb2.Key`.
        """
        lookup_request = datastore_pb.LookupRequest()
        _set_read_options(lookup_request, eventual, transaction_id)
        _add_keys_to_request(lookup_request.key, key_pbs)

        lookup_response = self._rpc(dataset_id, 'lookup', lookup_request,
                                    datastore_pb.LookupResponse)

        results = [result.entity for result in lookup_response.found]
        missing = [result.entity for result in lookup_response.missing]

        return results, missing, list(lookup_response.deferred)

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

    def commit(self, dataset_id, mutation_pb, transaction_id):
        """Commit dataset mutations in context of current transation (if any).

        Maps the ``DatastoreService.Commit`` protobuf RPC.

        :type dataset_id: string
        :param dataset_id: The ID dataset to which the transaction applies.

        :type mutation_pb: :class:`datastore_pb.Mutation`.
        :param mutation_pb: The protobuf for the mutations being saved.

        :type transaction_id: string or None
        :param transaction_id: The transaction ID returned from
                               :meth:`begin_transaction`.  Non-transactional
                               batches must pass ``None``.

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
        _add_keys_to_request(request.key, key_pbs)
        # Nothing to do with this response, so just execute the method.
        response = self._rpc(dataset_id, 'allocateIds', request,
                             datastore_pb.AllocateIdsResponse)
        return list(response.key)


def _set_read_options(request, eventual, transaction_id):
    """Validate rules for read options, and assign to the request.

    Helper method for ``lookup()`` and ``run_query``.

    :raises: :class:`ValueError` if ``eventual`` is ``True`` and the
             ``transaction_id`` is not ``None``.
    """
    if eventual and (transaction_id is not None):
        raise ValueError('eventual must be False when in a transaction')

    opts = request.read_options
    if eventual:
        opts.read_consistency = datastore_pb.ReadOptions.EVENTUAL
    elif transaction_id:
        opts.transaction = transaction_id


def _prepare_key_for_request(key_pb):  # pragma: NO COVER copied from helpers
    """Add protobuf keys to a request object.

    .. note::
      This is copied from `helpers` to avoid a cycle:
      _implicit_environ -> connection -> helpers -> key -> _implicit_environ

    :type key_pb: :class:`gcloud.datastore._datastore_v1_pb2.Key`
    :param key_pb: A key to be added to a request.

    :rtype: :class:`gcloud.datastore._datastore_v1_pb2.Key`
    :returns: A key which will be added to a request. It will be the
              original if nothing needs to be changed.
    """
    if key_pb.partition_id.HasField('dataset_id'):
        new_key_pb = datastore_pb.Key()
        new_key_pb.CopyFrom(key_pb)
        new_key_pb.partition_id.ClearField('dataset_id')
        key_pb = new_key_pb
    return key_pb


def _add_keys_to_request(request_field_pb, key_pbs):
    """Add protobuf keys to a request object.

    :type request_field_pb: `RepeatedCompositeFieldContainer`
    :param request_field_pb: A repeated proto field that contains keys.

    :type key_pbs: list of :class:`gcloud.datastore._datastore_v1_pb2.Key`
    :param key_pbs: The keys to add to a request.
    """
    for key_pb in key_pbs:
        key_pb = _prepare_key_for_request(key_pb)
        request_field_pb.add().CopyFrom(key_pb)
