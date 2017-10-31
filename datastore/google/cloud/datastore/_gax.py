# Copyright 2017 Google LLC
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
import sys

from google.cloud.gapic.datastore.v1 import datastore_client
from google.gax.errors import GaxError
from google.gax.grpc import exc_to_code
from google.gax.utils import metrics
from grpc import insecure_channel
from grpc import StatusCode
import six

from google.cloud._helpers import make_secure_channel
from google.cloud._http import DEFAULT_USER_AGENT
from google.cloud import exceptions

from google.cloud.datastore import __version__


_METRICS_HEADERS = (
    ('gccl', __version__),
)
_HEADER_STR = metrics.stringify(metrics.fill(_METRICS_HEADERS))
_GRPC_EXTRA_OPTIONS = (
    ('x-goog-api-client', _HEADER_STR),
)
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
def _catch_remap_gax_error():
    """Remap GAX exceptions that happen in context.

    .. _code.proto: https://github.com/googleapis/googleapis/blob/\
                    master/google/rpc/code.proto

    Remaps gRPC exceptions to the classes defined in
    :mod:`~google.cloud.exceptions` (according to the description
    in `code.proto`_).
    """
    try:
        yield
    except GaxError as exc:
        error_code = exc_to_code(exc.cause)
        error_class = _GRPC_ERROR_MAPPING.get(error_code)
        if error_class is None:
            raise
        else:
            new_exc = error_class(exc.cause.details())
            six.reraise(error_class, new_exc, sys.exc_info()[2])


class GAPICDatastoreAPI(datastore_client.DatastoreClient):
    """An API object that sends proto-over-gRPC requests.

    A light wrapper around the parent class, with exception re-mapping
    provided (from GaxError to our native errors).

    :type args: tuple
    :param args: Positional arguments to pass to constructor.

    :type kwargs: dict
    :param kwargs: Keyword arguments to pass to constructor.
    """

    def lookup(self, *args, **kwargs):
        """Perform a ``lookup`` request.

        A light wrapper around the the base method from the parent class.
        Intended to provide exception re-mapping (from GaxError to our
        native errors).

        :type args: tuple
        :param args: Positional arguments to pass to base method.

        :type kwargs: dict
        :param kwargs: Keyword arguments to pass to base method.

        :rtype: :class:`.datastore_pb2.LookupResponse`
        :returns: The returned protobuf response object.
        """
        with _catch_remap_gax_error():
            return super(GAPICDatastoreAPI, self).lookup(*args, **kwargs)

    def run_query(self, *args, **kwargs):
        """Perform a ``runQuery`` request.

        A light wrapper around the the base method from the parent class.
        Intended to provide exception re-mapping (from GaxError to our
        native errors).

        :type args: tuple
        :param args: Positional arguments to pass to base method.

        :type kwargs: dict
        :param kwargs: Keyword arguments to pass to base method.

        :rtype: :class:`.datastore_pb2.RunQueryResponse`
        :returns: The returned protobuf response object.
        """
        with _catch_remap_gax_error():
            return super(GAPICDatastoreAPI, self).run_query(*args, **kwargs)

    def begin_transaction(self, *args, **kwargs):
        """Perform a ``beginTransaction`` request.

        A light wrapper around the the base method from the parent class.
        Intended to provide exception re-mapping (from GaxError to our
        native errors).

        :type args: tuple
        :param args: Positional arguments to pass to base method.

        :type kwargs: dict
        :param kwargs: Keyword arguments to pass to base method.

        :rtype: :class:`.datastore_pb2.BeginTransactionResponse`
        :returns: The returned protobuf response object.
        """
        with _catch_remap_gax_error():
            return super(GAPICDatastoreAPI, self).begin_transaction(
                *args, **kwargs)

    def commit(self, *args, **kwargs):
        """Perform a ``commit`` request.

        A light wrapper around the the base method from the parent class.
        Intended to provide exception re-mapping (from GaxError to our
        native errors).

        :type args: tuple
        :param args: Positional arguments to pass to base method.

        :type kwargs: dict
        :param kwargs: Keyword arguments to pass to base method.

        :rtype: :class:`.datastore_pb2.CommitResponse`
        :returns: The returned protobuf response object.
        """
        with _catch_remap_gax_error():
            return super(GAPICDatastoreAPI, self).commit(*args, **kwargs)

    def rollback(self, *args, **kwargs):
        """Perform a ``rollback`` request.

        A light wrapper around the the base method from the parent class.
        Intended to provide exception re-mapping (from GaxError to our
        native errors).

        :type args: tuple
        :param args: Positional arguments to pass to base method.

        :type kwargs: dict
        :param kwargs: Keyword arguments to pass to base method.

        :rtype: :class:`.datastore_pb2.RollbackResponse`
        :returns: The returned protobuf response object.
        """
        with _catch_remap_gax_error():
            return super(GAPICDatastoreAPI, self).rollback(*args, **kwargs)

    def allocate_ids(self, *args, **kwargs):
        """Perform an ``allocateIds`` request.

        A light wrapper around the the base method from the parent class.
        Intended to provide exception re-mapping (from GaxError to our
        native errors).

        :type args: tuple
        :param args: Positional arguments to pass to base method.

        :type kwargs: dict
        :param kwargs: Keyword arguments to pass to base method.

        :rtype: :class:`.datastore_pb2.AllocateIdsResponse`
        :returns: The returned protobuf response object.
        """
        with _catch_remap_gax_error():
            return super(GAPICDatastoreAPI, self).allocate_ids(
                *args, **kwargs)


def make_datastore_api(client):
    """Create an instance of the GAPIC Datastore API.

    :type client: :class:`~google.cloud.datastore.client.Client`
    :param client: The client that holds configuration details.

    :rtype: :class:`.datastore.v1.datastore_client.DatastoreClient`
    :returns: A datastore API instance with the proper credentials.
    """
    parse_result = six.moves.urllib_parse.urlparse(
        client._base_url)
    host = parse_result.netloc
    if parse_result.scheme == 'https':
        channel = make_secure_channel(
            client._credentials, DEFAULT_USER_AGENT, host)
    else:
        channel = insecure_channel(host)

    return GAPICDatastoreAPI(
        channel=channel, lib_name='gccl', lib_version=__version__)
