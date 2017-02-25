# Copyright 2014 Google Inc.
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

"""Connections to Google Cloud Datastore API servers."""

import os

from google.rpc import status_pb2

from google.cloud import _http as connection_module
from google.cloud.environment_vars import DISABLE_GRPC
from google.cloud.environment_vars import GCD_HOST
from google.cloud import exceptions
from google.cloud.proto.datastore.v1 import datastore_pb2 as _datastore_pb2

from google.cloud.datastore import __version__
try:
    from google.cloud.datastore._gax import _DatastoreAPIOverGRPC
    _HAVE_GRPC = True
except ImportError:  # pragma: NO COVER
    _DatastoreAPIOverGRPC = None
    _HAVE_GRPC = False


DATASTORE_API_HOST = 'datastore.googleapis.com'
"""Datastore API request host."""

_DISABLE_GRPC = os.getenv(DISABLE_GRPC, False)
_USE_GRPC = _HAVE_GRPC and not _DISABLE_GRPC
_CLIENT_INFO = connection_module.CLIENT_INFO_TEMPLATE.format(__version__)


class _DatastoreAPIOverHttp(object):
    """Helper mapping datastore API methods.

    Makes requests to send / receive protobuf content over HTTP/1.1.

    Methods make bare API requests without any helpers for constructing
    the requests or parsing the responses.

    :type connection: :class:`Connection`
    :param connection: A connection object that contains helpful
                       information for making requests.
    """

    def __init__(self, connection):
        self.connection = connection

    def _request(self, project, method, data):
        """Make a request over the Http transport to the Cloud Datastore API.

        :type project: str
        :param project: The project to make the request for.

        :type method: str
        :param method: The API call method name (ie, ``runQuery``,
                       ``lookup``, etc)

        :type data: str
        :param data: The data to send with the API call.
                     Typically this is a serialized Protobuf string.

        :rtype: str
        :returns: The string response content from the API call.
        :raises: :class:`google.cloud.exceptions.GoogleCloudError` if the
                 response code is not 200 OK.
        """
        headers = {
            'Content-Type': 'application/x-protobuf',
            'Content-Length': str(len(data)),
            'User-Agent': self.connection.USER_AGENT,
            connection_module.CLIENT_INFO_HEADER: _CLIENT_INFO,
        }
        headers, content = self.connection.http.request(
            uri=self.connection.build_api_url(project=project, method=method),
            method='POST', headers=headers, body=data)

        status = headers['status']
        if status != '200':
            error_status = status_pb2.Status.FromString(content)
            raise exceptions.make_exception(
                headers, error_status.message, use_json=False)

        return content

    def _rpc(self, project, method, request_pb, response_pb_cls):
        """Make a protobuf RPC request.

        :type project: str
        :param project: The project to connect to. This is
                        usually your project name in the cloud console.

        :type method: str
        :param method: The name of the method to invoke.

        :type request_pb: :class:`google.protobuf.message.Message` instance
        :param request_pb: the protobuf instance representing the request.

        :type response_pb_cls: A :class:`google.protobuf.message.Message`
                               subclass.
        :param response_pb_cls: The class used to unmarshall the response
                                protobuf.

        :rtype: :class:`google.protobuf.message.Message`
        :returns: The RPC message parsed from the response.
        """
        response = self._request(project=project, method=method,
                                 data=request_pb.SerializeToString())
        return response_pb_cls.FromString(response)

    def lookup(self, project, request_pb):
        """Perform a ``lookup`` request.

        :type project: str
        :param project: The project to connect to. This is
                        usually your project name in the cloud console.

        :type request_pb: :class:`.datastore_pb2.LookupRequest`
        :param request_pb: The request protobuf object.

        :rtype: :class:`.datastore_pb2.LookupResponse`
        :returns: The returned protobuf response object.
        """
        return self._rpc(project, 'lookup', request_pb,
                         _datastore_pb2.LookupResponse)

    def run_query(self, project, request_pb):
        """Perform a ``runQuery`` request.

        :type project: str
        :param project: The project to connect to. This is
                        usually your project name in the cloud console.

        :type request_pb: :class:`.datastore_pb2.RunQueryRequest`
        :param request_pb: The request protobuf object.

        :rtype: :class:`.datastore_pb2.RunQueryResponse`
        :returns: The returned protobuf response object.
        """
        return self._rpc(project, 'runQuery', request_pb,
                         _datastore_pb2.RunQueryResponse)

    def begin_transaction(self, project, request_pb):
        """Perform a ``beginTransaction`` request.

        :type project: str
        :param project: The project to connect to. This is
                        usually your project name in the cloud console.

        :type request_pb:
            :class:`.datastore_pb2.BeginTransactionRequest`
        :param request_pb: The request protobuf object.

        :rtype: :class:`.datastore_pb2.BeginTransactionResponse`
        :returns: The returned protobuf response object.
        """
        return self._rpc(project, 'beginTransaction', request_pb,
                         _datastore_pb2.BeginTransactionResponse)

    def commit(self, project, request_pb):
        """Perform a ``commit`` request.

        :type project: str
        :param project: The project to connect to. This is
                        usually your project name in the cloud console.

        :type request_pb: :class:`.datastore_pb2.CommitRequest`
        :param request_pb: The request protobuf object.

        :rtype: :class:`.datastore_pb2.CommitResponse`
        :returns: The returned protobuf response object.
        """
        return self._rpc(project, 'commit', request_pb,
                         _datastore_pb2.CommitResponse)

    def rollback(self, project, request_pb):
        """Perform a ``rollback`` request.

        :type project: str
        :param project: The project to connect to. This is
                        usually your project name in the cloud console.

        :type request_pb: :class:`.datastore_pb2.RollbackRequest`
        :param request_pb: The request protobuf object.

        :rtype: :class:`.datastore_pb2.RollbackResponse`
        :returns: The returned protobuf response object.
        """
        return self._rpc(project, 'rollback', request_pb,
                         _datastore_pb2.RollbackResponse)

    def allocate_ids(self, project, request_pb):
        """Perform an ``allocateIds`` request.

        :type project: str
        :param project: The project to connect to. This is
                        usually your project name in the cloud console.

        :type request_pb: :class:`.datastore_pb2.AllocateIdsRequest`
        :param request_pb: The request protobuf object.

        :rtype: :class:`.datastore_pb2.AllocateIdsResponse`
        :returns: The returned protobuf response object.
        """
        return self._rpc(project, 'allocateIds', request_pb,
                         _datastore_pb2.AllocateIdsResponse)


class Connection(connection_module.Connection):
    """A connection to the Google Cloud Datastore via the Protobuf API.

    This class should understand only the basic types (and protobufs)
    in method arguments, however it should be capable of returning advanced
    types.

    :type client: :class:`~google.cloud.datastore.client.Client`
    :param client: The client that owns the current connection.
    """

    API_BASE_URL = 'https://' + DATASTORE_API_HOST
    """The base of the API call URL."""

    API_VERSION = 'v1'
    """The version of the API, used in building the API call's URL."""

    API_URL_TEMPLATE = ('{api_base}/{api_version}/projects'
                        '/{project}:{method}')
    """A template for the URL of a particular API call."""

    def __init__(self, client):
        super(Connection, self).__init__(client)
        try:
            self.host = os.environ[GCD_HOST]
            self.api_base_url = 'http://' + self.host
            secure = False
        except KeyError:
            self.host = DATASTORE_API_HOST
            self.api_base_url = self.__class__.API_BASE_URL
            secure = True
        if _USE_GRPC:
            self._datastore_api = _DatastoreAPIOverGRPC(self, secure=secure)
        else:
            self._datastore_api = _DatastoreAPIOverHttp(self)

    def build_api_url(self, project, method, base_url=None,
                      api_version=None):
        """Construct the URL for a particular API call.

        This method is used internally to come up with the URL to use when
        making RPCs to the Cloud Datastore API.

        :type project: str
        :param project: The project to connect to. This is
                        usually your project name in the cloud console.

        :type method: str
        :param method: The API method to call (e.g. 'runQuery', 'lookup').

        :type base_url: str
        :param base_url: The base URL where the API lives.
                         You shouldn't have to provide this.

        :type api_version: str
        :param api_version: The version of the API to connect to.
                            You shouldn't have to provide this.

        :rtype: str
        :returns: The API URL created.
        """
        return self.API_URL_TEMPLATE.format(
            api_base=(base_url or self.api_base_url),
            api_version=(api_version or self.API_VERSION),
            project=project, method=method)

    def lookup(self, project, key_pbs,
               eventual=False, transaction_id=None):
        """Lookup keys from a project in the Cloud Datastore.

        Maps the ``DatastoreService.Lookup`` protobuf RPC.

        This uses mostly protobufs
        (:class:`.entity_pb2.Key` as input and :class:`.entity_pb2.Entity`
        as output). It is used under the hood in
        :meth:`Client.get() <.datastore.client.Client.get>`:

        .. code-block:: python

          >>> from google.cloud import datastore
          >>> client = datastore.Client(project='project')
          >>> key = client.key('MyKind', 1234)
          >>> client.get(key)
          [<Entity object>]

        Using a :class:`Connection` directly:

        .. code-block:: python

          >>> connection.lookup('project', [key.to_protobuf()])
          [<Entity protobuf>]

        :type project: str
        :param project: The project to look up the keys in.

        :type key_pbs: list of
                       :class:`.entity_pb2.Key`
        :param key_pbs: The keys to retrieve from the datastore.

        :type eventual: bool
        :param eventual: If False (the default), request ``STRONG`` read
                         consistency.  If True, request ``EVENTUAL`` read
                         consistency.

        :type transaction_id: str
        :param transaction_id: If passed, make the request in the scope of
                               the given transaction.  Incompatible with
                               ``eventual==True``.

        :rtype: tuple
        :returns: A triple of (``results``, ``missing``, ``deferred``) where
                  both ``results`` and ``missing`` are lists of
                  :class:`.entity_pb2.Entity`
                  and ``deferred`` is a list of
                  :class:`.entity_pb2.Key`.
        """
        lookup_request = _datastore_pb2.LookupRequest()
        _set_read_options(lookup_request, eventual, transaction_id)
        _add_keys_to_request(lookup_request.keys, key_pbs)

        lookup_response = self._datastore_api.lookup(project, lookup_request)

        results = [result.entity for result in lookup_response.found]
        missing = [result.entity for result in lookup_response.missing]

        return results, missing, list(lookup_response.deferred)

    def run_query(self, project, query_pb, namespace=None,
                  eventual=False, transaction_id=None):
        """Run a query on the Cloud Datastore.

        Maps the ``DatastoreService.RunQuery`` protobuf RPC.

        Given a Query protobuf, sends a ``runQuery`` request to the
        Cloud Datastore API and returns a list of entity protobufs
        matching the query.

        You typically wouldn't use this method directly, in favor of the
        :meth:`google.cloud.datastore.query.Query.fetch` method.

        Under the hood, the :class:`google.cloud.datastore.query.Query` class
        uses this method to fetch data.

        :type project: str
        :param project: The project over which to run the query.

        :type query_pb: :class:`.query_pb2.Query`
        :param query_pb: The Protobuf representing the query to run.

        :type namespace: str
        :param namespace: The namespace over which to run the query.

        :type eventual: bool
        :param eventual: If False (the default), request ``STRONG`` read
                         consistency.  If True, request ``EVENTUAL`` read
                         consistency.

        :type transaction_id: str
        :param transaction_id: If passed, make the request in the scope of
                               the given transaction.  Incompatible with
                               ``eventual==True``.

        :rtype: :class:`.datastore_pb2.RunQueryResponse`
        :returns: The protobuf response from a ``runQuery`` request.
        """
        request = _datastore_pb2.RunQueryRequest()
        _set_read_options(request, eventual, transaction_id)

        if namespace:
            request.partition_id.namespace_id = namespace

        request.query.CopyFrom(query_pb)
        return self._datastore_api.run_query(project, request)

    def begin_transaction(self, project):
        """Begin a transaction.

        Maps the ``DatastoreService.BeginTransaction`` protobuf RPC.

        :type project: str
        :param project: The project to which the transaction applies.

        :rtype: bytes
        :returns: The serialized transaction that was begun.
        """
        request = _datastore_pb2.BeginTransactionRequest()
        response = self._datastore_api.begin_transaction(project, request)
        return response.transaction

    def commit(self, project, request, transaction_id):
        """Commit mutations in context of current transaction (if any).

        Maps the ``DatastoreService.Commit`` protobuf RPC.

        :type project: str
        :param project: The project to which the transaction applies.

        :type request: :class:`.datastore_pb2.CommitRequest`
        :param request: The protobuf with the mutations being committed.

        :type transaction_id: str
        :param transaction_id: (Optional) The transaction ID returned from
                               :meth:`begin_transaction`.  Non-transactional
                               batches must pass ``None``.

        .. note::

            This method will mutate ``request`` before using it.

        :rtype: :class:`.datastore_pb2.CommitResponse`
        :returns: The protobuf response from a commit request.
        """
        if transaction_id:
            request.mode = _datastore_pb2.CommitRequest.TRANSACTIONAL
            request.transaction = transaction_id
        else:
            request.mode = _datastore_pb2.CommitRequest.NON_TRANSACTIONAL

        return self._datastore_api.commit(project, request)

    def rollback(self, project, transaction_id):
        """Rollback the connection's existing transaction.

        Maps the ``DatastoreService.Rollback`` protobuf RPC.

        :type project: str
        :param project: The project to which the transaction belongs.

        :type transaction_id: str
        :param transaction_id: The transaction ID returned from
                               :meth:`begin_transaction`.
        """
        request = _datastore_pb2.RollbackRequest()
        request.transaction = transaction_id
        # Nothing to do with this response, so just execute the method.
        self._datastore_api.rollback(project, request)

    def allocate_ids(self, project, key_pbs):
        """Obtain backend-generated IDs for a set of keys.

        Maps the ``DatastoreService.AllocateIds`` protobuf RPC.

        :type project: str
        :param project: The project to which the transaction belongs.

        :type key_pbs: list of
                       :class:`.entity_pb2.Key`
        :param key_pbs: The keys for which the backend should allocate IDs.

        :rtype: list of :class:`.entity_pb2.Key`
        :returns: An equal number of keys,  with IDs filled in by the backend.
        """
        request = _datastore_pb2.AllocateIdsRequest()
        _add_keys_to_request(request.keys, key_pbs)
        # Nothing to do with this response, so just execute the method.
        response = self._datastore_api.allocate_ids(project, request)
        return list(response.keys)


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
        opts.read_consistency = _datastore_pb2.ReadOptions.EVENTUAL
    elif transaction_id:
        opts.transaction = transaction_id


def _add_keys_to_request(request_field_pb, key_pbs):
    """Add protobuf keys to a request object.

    :type request_field_pb: `RepeatedCompositeFieldContainer`
    :param request_field_pb: A repeated proto field that contains keys.

    :type key_pbs: list of :class:`.entity_pb2.Key`
    :param key_pbs: The keys to add to a request.
    """
    for key_pb in key_pbs:
        request_field_pb.add().CopyFrom(key_pb)
