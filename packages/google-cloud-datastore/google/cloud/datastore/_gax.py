# Copyright 2017 Google Inc.
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

"""Helpers for making API requests via GAX / gRPC."""


import contextlib

from grpc import StatusCode

from google.cloud._helpers import make_insecure_stub
from google.cloud._helpers import make_secure_stub
from google.cloud import exceptions

from google.cloud.proto.datastore.v1 import datastore_pb2_grpc


_GRPC_ERROR_MAPPING = {
    StatusCode.UNKNOWN: exceptions.InternalServerError,
    StatusCode.INVALID_ARGUMENT: exceptions.BadRequest,
    StatusCode.DEADLINE_EXCEEDED: exceptions.GatewayTimeout,
    StatusCode.NOT_FOUND: exceptions.NotFound,
    StatusCode.ALREADY_EXISTS: exceptions.Conflict,
    StatusCode.PERMISSION_DENIED: exceptions.Forbidden,
    StatusCode.UNAUTHENTICATED: exceptions.Unauthorized,
    StatusCode.RESOURCE_EXHAUSTED: exceptions.TooManyRequests,
    StatusCode.FAILED_PRECONDITION: exceptions.PreconditionFailed,
    StatusCode.ABORTED: exceptions.Conflict,
    StatusCode.OUT_OF_RANGE: exceptions.BadRequest,
    StatusCode.UNIMPLEMENTED: exceptions.MethodNotImplemented,
    StatusCode.INTERNAL: exceptions.InternalServerError,
    StatusCode.UNAVAILABLE: exceptions.ServiceUnavailable,
    StatusCode.DATA_LOSS: exceptions.InternalServerError,
}


@contextlib.contextmanager
def _grpc_catch_rendezvous():
    """Remap gRPC exceptions that happen in context.

    .. _code.proto: https://github.com/googleapis/googleapis/blob/\
                    master/google/rpc/code.proto

    Remaps gRPC exceptions to the classes defined in
    :mod:`~google.cloud.exceptions` (according to the description
    in `code.proto`_).
    """
    try:
        yield
    except exceptions.GrpcRendezvous as exc:
        error_code = exc.code()
        error_class = _GRPC_ERROR_MAPPING.get(error_code)
        if error_class is None:
            raise
        else:
            raise error_class(exc.details())


class _DatastoreAPIOverGRPC(object):
    """Helper mapping datastore API methods.

    Makes requests to send / receive protobuf content over gRPC.

    Methods make bare API requests without any helpers for constructing
    the requests or parsing the responses.

    :type connection: :class:`Connection`
    :param connection: A connection object that contains helpful
                       information for making requests.

    :type secure: bool
    :param secure: Flag indicating if a secure stub connection is needed.
    """

    def __init__(self, connection, secure):
        if secure:
            self._stub = make_secure_stub(connection.credentials,
                                          connection.USER_AGENT,
                                          datastore_pb2_grpc.DatastoreStub,
                                          connection.host)
        else:
            self._stub = make_insecure_stub(datastore_pb2_grpc.DatastoreStub,
                                            connection.host)

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
        request_pb.project_id = project
        with _grpc_catch_rendezvous():
            return self._stub.Lookup(request_pb)

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
        request_pb.project_id = project
        with _grpc_catch_rendezvous():
            return self._stub.RunQuery(request_pb)

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
        request_pb.project_id = project
        with _grpc_catch_rendezvous():
            return self._stub.BeginTransaction(request_pb)

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
        request_pb.project_id = project
        with _grpc_catch_rendezvous():
            return self._stub.Commit(request_pb)

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
        request_pb.project_id = project
        with _grpc_catch_rendezvous():
            return self._stub.Rollback(request_pb)

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
        request_pb.project_id = project
        with _grpc_catch_rendezvous():
            return self._stub.AllocateIds(request_pb)
