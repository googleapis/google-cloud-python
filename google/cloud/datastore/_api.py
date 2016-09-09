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


class _DatastoreAPIOverHttp(object):
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
        headers, content = self.connection.http.request(
            uri=self.connection.build_api_url(project=project, method=method),
            method='POST', headers=headers, body=data)

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

    def lookup(self, project, request_pb):
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


class _DatastoreAPIOverGRPC(object):
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

    def lookup(self, project, request_pb):
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
