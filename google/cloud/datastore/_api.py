# Copyright 2016 Google Inc. All rights reserved.
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

"""Implementations for HTTP and gRPC

These are connections to Google Cloud Datastore API servers for
each datastore API method.
"""


import os

from google.rpc import status_pb2

from google.cloud._helpers import make_insecure_stub
from google.cloud._helpers import make_secure_stub
from google.cloud.environment_vars import DISABLE_GRPC
from google.cloud.exceptions import Conflict
from google.cloud.exceptions import make_exception
from google.cloud.datastore._generated import datastore_pb2
# pylint: disable=ungrouped-imports
try:
    from grpc import StatusCode
    from grpc._channel import _Rendezvous
    from google.cloud.datastore._generated import datastore_grpc_pb2
except ImportError:  # pragma: NO COVER
    HAVE_GRPC = False
    datastore_grpc_pb2 = None
    StatusCode = None
    _Rendezvous = Exception
else:
    HAVE_GRPC = True
# pylint: enable=ungrouped-imports


USE_GRPC = HAVE_GRPC and not os.getenv(DISABLE_GRPC, False)

API_URL_TEMPLATE = ('{api_base}/{api_version}/projects'
                    '/{project}:{method}')
"""A template for the URL of a particular API call."""

API_VERSION = 'v1'
"""The version of the API, used in building the API call's URL."""


class DatastoreAPIBase(object):
    """Base class for datastore API Implementations."""

    def _lookup(self, project, request_pb):
        """Perform a ``lookup`` request.

        This method is virtual and should be implemented by subclasses.

        :type project: string
        :param project: The project to connect to.

        :type request_pb: :class:`._generated.datastore_pb2.LookupRequest`
        :param request_pb: The request protobuf object.

        :raises: :exc:`NotImplementedError` always
        """
        raise NotImplementedError

    def lookup(self, project, key_pbs,
               eventual=False, transaction_id=None):
        """Lookup keys from a project in the Cloud Datastore.

        Maps the ``DatastoreService.Lookup`` protobuf RPC.

        This uses mostly protobufs
        (:class:`google.cloud.datastore._generated.entity_pb2.Key` as input
        and :class:`google.cloud.datastore._generated.entity_pb2.Entity`
        as output). It is used under the hood in
        :meth:`Client.get() <.datastore.client.Client.get>`:

        >>> from google.cloud import datastore
        >>> client = datastore.Client(project='project')
        >>> key = client.key('MyKind', 1234)
        >>> client.get(key)
        [<Entity object>]

        Using a :class:`Connection` directly:

        >>> connection.lookup('project', [key.to_protobuf()])
        [<Entity protobuf>]

        :type project: string
        :param project: The project to look up the keys in.

        :type key_pbs: list of
                       :class:`google.cloud.datastore._generated.entity_pb2.Key`
        :param key_pbs: The keys to retrieve from the datastore.

        :type eventual: bool
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
                  :class:`google.cloud.datastore._generated.entity_pb2.Entity`
                  and ``deferred`` is a list of
                  :class:`google.cloud.datastore._generated.entity_pb2.Key`.
        """
        lookup_request = datastore_pb2.LookupRequest()
        _set_read_options(lookup_request, eventual, transaction_id)
        _add_keys_to_request(lookup_request.keys, key_pbs)

        lookup_response = self._lookup(project, lookup_request)

        results = [result.entity for result in lookup_response.found]
        missing = [result.entity for result in lookup_response.missing]

        return results, missing, list(lookup_response.deferred)


class _DatastoreAPIOverHttp(DatastoreAPIBase):
    """Helper mapping datastore API methods.

    Makes requests to send / receive protobuf content over HTTP/1.1.

    Methods make bare API requests without any helpers for constructing
    the requests or parsing the responses.

    :type connection: :class:`google.cloud.datastore.connection.Connection`
    :param connection: A connection object that contains helpful
                       information for making requests.
    """

    def __init__(self, connection):
        self.connection = connection

    def _request(self, project, method, data):
        """Make a request over the Http transport to the Cloud Datastore API.

        :type project: string
        :param project: The project to make the request for.

        :type method: string
        :param method: The API call method name (ie, ``runQuery``,
                       ``lookup``, etc)

        :type data: string
        :param data: The data to send with the API call.
                     Typically this is a serialized Protobuf string.

        :rtype: string
        :returns: The string response content from the API call.
        :raises: :class:`google.cloud.exceptions.GoogleCloudError` if the
                 response code is not 200 OK.
        """
        headers = {
            'Content-Type': 'application/x-protobuf',
            'Content-Length': str(len(data)),
            'User-Agent': self.connection.USER_AGENT,
        }
        base_url = self.connection.api_base_url
        api_url = build_api_url(project, method, base_url)
        headers, content = self.connection.http.request(
            uri=api_url, method='POST', headers=headers, body=data)

        status = headers['status']
        if status != '200':
            error_status = status_pb2.Status.FromString(content)
            raise make_exception(headers, error_status.message, use_json=False)

        return content

    def _rpc(self, project, method, request_pb, response_pb_cls):
        """Make a protobuf RPC request.

        :type project: string
        :param project: The project to connect to. This is
                        usually your project name in the cloud console.

        :type method: string
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

    def _lookup(self, project, request_pb):
        """Perform a ``lookup`` request.

        :type project: string
        :param project: The project to connect to. This is
                        usually your project name in the cloud console.

        :type request_pb: :class:`._generated.datastore_pb2.LookupRequest`
        :param request_pb: The request protobuf object.

        :rtype: :class:`._generated.datastore_pb2.LookupResponse`
        :returns: The returned protobuf response object.
        """
        return self._rpc(project, 'lookup', request_pb,
                         datastore_pb2.LookupResponse)

    def run_query(self, project, request_pb):
        """Perform a ``runQuery`` request.

        :type project: string
        :param project: The project to connect to. This is
                        usually your project name in the cloud console.

        :type request_pb: :class:`._generated.datastore_pb2.RunQueryRequest`
        :param request_pb: The request protobuf object.

        :rtype: :class:`._generated.datastore_pb2.RunQueryResponse`
        :returns: The returned protobuf response object.
        """
        return self._rpc(project, 'runQuery', request_pb,
                         datastore_pb2.RunQueryResponse)

    def begin_transaction(self, project, request_pb):
        """Perform a ``beginTransaction`` request.

        :type project: string
        :param project: The project to connect to. This is
                        usually your project name in the cloud console.

        :type request_pb:
            :class:`._generated.datastore_pb2.BeginTransactionRequest`
        :param request_pb: The request protobuf object.

        :rtype: :class:`._generated.datastore_pb2.BeginTransactionResponse`
        :returns: The returned protobuf response object.
        """
        return self._rpc(project, 'beginTransaction', request_pb,
                         datastore_pb2.BeginTransactionResponse)

    def commit(self, project, request_pb):
        """Perform a ``commit`` request.

        :type project: string
        :param project: The project to connect to. This is
                        usually your project name in the cloud console.

        :type request_pb: :class:`._generated.datastore_pb2.CommitRequest`
        :param request_pb: The request protobuf object.

        :rtype: :class:`._generated.datastore_pb2.CommitResponse`
        :returns: The returned protobuf response object.
        """
        return self._rpc(project, 'commit', request_pb,
                         datastore_pb2.CommitResponse)

    def rollback(self, project, request_pb):
        """Perform a ``rollback`` request.

        :type project: string
        :param project: The project to connect to. This is
                        usually your project name in the cloud console.

        :type request_pb: :class:`._generated.datastore_pb2.RollbackRequest`
        :param request_pb: The request protobuf object.

        :rtype: :class:`._generated.datastore_pb2.RollbackResponse`
        :returns: The returned protobuf response object.
        """
        return self._rpc(project, 'rollback', request_pb,
                         datastore_pb2.RollbackResponse)

    def allocate_ids(self, project, request_pb):
        """Perform an ``allocateIds`` request.

        :type project: string
        :param project: The project to connect to. This is
                        usually your project name in the cloud console.

        :type request_pb: :class:`._generated.datastore_pb2.AllocateIdsRequest`
        :param request_pb: The request protobuf object.

        :rtype: :class:`._generated.datastore_pb2.AllocateIdsResponse`
        :returns: The returned protobuf response object.
        """
        return self._rpc(project, 'allocateIds', request_pb,
                         datastore_pb2.AllocateIdsResponse)


class _DatastoreAPIOverGRPC(DatastoreAPIBase):
    """Helper mapping datastore API methods.

    Makes requests to send / receive protobuf content over gRPC.

    Methods make bare API requests without any helpers for constructing
    the requests or parsing the responses.

    :type connection: :class:`google.cloud.datastore.connection.Connection`
    :param connection: A connection object that contains helpful
                       information for making requests.

    :type secure: bool
    :param secure: Flag indicating if a secure stub connection is needed.
    """

    def __init__(self, connection, secure):
        if secure:
            self._stub = make_secure_stub(connection.credentials,
                                          connection.USER_AGENT,
                                          datastore_grpc_pb2.DatastoreStub,
                                          connection.host)
        else:
            self._stub = make_insecure_stub(datastore_grpc_pb2.DatastoreStub,
                                            connection.host)

    def _lookup(self, project, request_pb):
        """Perform a ``lookup`` request.

        :type project: string
        :param project: The project to connect to. This is
                        usually your project name in the cloud console.

        :type request_pb: :class:`._generated.datastore_pb2.LookupRequest`
        :param request_pb: The request protobuf object.

        :rtype: :class:`._generated.datastore_pb2.LookupResponse`
        :returns: The returned protobuf response object.
        """
        request_pb.project_id = project
        return self._stub.Lookup(request_pb)

    def run_query(self, project, request_pb):
        """Perform a ``runQuery`` request.

        :type project: string
        :param project: The project to connect to. This is
                        usually your project name in the cloud console.

        :type request_pb: :class:`._generated.datastore_pb2.RunQueryRequest`
        :param request_pb: The request protobuf object.

        :rtype: :class:`._generated.datastore_pb2.RunQueryResponse`
        :returns: The returned protobuf response object.
        """
        request_pb.project_id = project
        return self._stub.RunQuery(request_pb)

    def begin_transaction(self, project, request_pb):
        """Perform a ``beginTransaction`` request.

        :type project: string
        :param project: The project to connect to. This is
                        usually your project name in the cloud console.

        :type request_pb:
            :class:`._generated.datastore_pb2.BeginTransactionRequest`
        :param request_pb: The request protobuf object.

        :rtype: :class:`._generated.datastore_pb2.BeginTransactionResponse`
        :returns: The returned protobuf response object.
        """
        request_pb.project_id = project
        return self._stub.BeginTransaction(request_pb)

    def commit(self, project, request_pb):
        """Perform a ``commit`` request.

        :type project: string
        :param project: The project to connect to. This is
                        usually your project name in the cloud console.

        :type request_pb: :class:`._generated.datastore_pb2.CommitRequest`
        :param request_pb: The request protobuf object.

        :rtype: :class:`._generated.datastore_pb2.CommitResponse`
        :returns: The returned protobuf response object.
        """
        request_pb.project_id = project
        try:
            return self._stub.Commit(request_pb)
        except _Rendezvous as exc:
            if exc.code() == StatusCode.ABORTED:
                raise Conflict(exc.details())
            raise

    def rollback(self, project, request_pb):
        """Perform a ``rollback`` request.

        :type project: string
        :param project: The project to connect to. This is
                        usually your project name in the cloud console.

        :type request_pb: :class:`._generated.datastore_pb2.RollbackRequest`
        :param request_pb: The request protobuf object.

        :rtype: :class:`._generated.datastore_pb2.RollbackResponse`
        :returns: The returned protobuf response object.
        """
        request_pb.project_id = project
        return self._stub.Rollback(request_pb)

    def allocate_ids(self, project, request_pb):
        """Perform an ``allocateIds`` request.

        :type project: string
        :param project: The project to connect to. This is
                        usually your project name in the cloud console.

        :type request_pb: :class:`._generated.datastore_pb2.AllocateIdsRequest`
        :param request_pb: The request protobuf object.

        :rtype: :class:`._generated.datastore_pb2.AllocateIdsResponse`
        :returns: The returned protobuf response object.
        """
        request_pb.project_id = project
        return self._stub.AllocateIds(request_pb)


def build_api_url(project, method, base_url):
    """Construct the URL for a particular API call.

    This method is used internally to come up with the URL to use when
    making RPCs to the Cloud Datastore API.

    :type project: string
    :param project: The project to connect to. This is
                    usually your project name in the cloud console.

    :type method: string
    :param method: The API method to call (e.g. 'runQuery', 'lookup').

    :type base_url: string
    :param base_url: The base URL where the API lives.

    :rtype: str
    :returns: The API URL created.
    """
    return API_URL_TEMPLATE.format(
        api_base=base_url, api_version=API_VERSION,
        project=project, method=method)


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
        opts.read_consistency = datastore_pb2.ReadOptions.EVENTUAL
    elif transaction_id:
        opts.transaction = transaction_id


def _add_keys_to_request(request_field_pb, key_pbs):
    """Add protobuf keys to a request object.

    :type request_field_pb: `RepeatedCompositeFieldContainer`
    :param request_field_pb: A repeated proto field that contains keys.

    :type key_pbs: list of :class:`.datastore._generated.entity_pb2.Key`
    :param key_pbs: The keys to add to a request.
    """
    for key_pb in key_pbs:
        request_field_pb.add().CopyFrom(key_pb)
