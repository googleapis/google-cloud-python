# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import google.api_core.grpc_helpers

from google.cloud.bigquery_storage_v1beta1.proto import storage_pb2_grpc


class BigQueryStorageGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.cloud.bigquery.storage.v1beta1 BigQueryStorage API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = (
        "https://www.googleapis.com/auth/bigquery",
        "https://www.googleapis.com/auth/cloud-platform",
    )

    def __init__(
        self,
        channel=None,
        credentials=None,
        address="bigquerystorage.googleapis.com:443",
    ):
        """Instantiate the transport class.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            address (str): The address where the service is hosted.
        """
        # If both `channel` and `credentials` are specified, raise an
        # exception (channels come with credentials baked in already).
        if channel is not None and credentials is not None:  # pragma: no cover
            raise ValueError(
                "The `channel` and `credentials` arguments are mutually " "exclusive."
            )

        # Create the channel.
        if channel is None:  # pragma: no cover
            channel = self.create_channel(address=address, credentials=credentials)

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {
            "big_query_storage_stub": storage_pb2_grpc.BigQueryStorageStub(channel)
        }

    @classmethod
    def create_channel(
        cls, address="bigquerystorage.googleapis.com:443", credentials=None
    ):
        """Create and return a gRPC channel object.

        Args:
            address (str): The host for the channel to use.
            credentials (~.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return google.api_core.grpc_helpers.create_channel(  # pragma: no cover
            address, credentials=credentials, scopes=cls._OAUTH_SCOPES
        )

    @property
    def channel(self):
        """The gRPC channel used by the transport.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return self._channel

    @property
    def create_read_session(self):
        """Return the gRPC stub for :meth:`BigQueryStorageClient.create_read_session`.

        Creates a new read session. A read session divides the contents of a
        BigQuery table into one or more streams, which can then be used to read
        data from the table. The read session also specifies properties of the
        data to be read, such as a list of columns or a push-down filter describing
        the rows to be returned.

        A particular row can be read by at most one stream. When the caller has
        reached the end of each stream in the session, then all the data in the
        table has been read.

        Read sessions automatically expire 24 hours after they are created and do
        not require manual clean-up by the caller.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["big_query_storage_stub"].CreateReadSession

    @property
    def read_rows(self):
        """Return the gRPC stub for :meth:`BigQueryStorageClient.read_rows`.

        Reads rows from the table in the format prescribed by the read session.
        Each response contains one or more table rows, up to a maximum of 10 MiB
        per response; read requests which attempt to read individual rows larger
        than this will fail.

        Each request also returns a set of stream statistics reflecting the
        estimated total number of rows in the read stream. This number is computed
        based on the total table size and the number of active streams in the read
        session, and may change as other streams continue to read data.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["big_query_storage_stub"].ReadRows

    @property
    def batch_create_read_session_streams(self):
        """Return the gRPC stub for :meth:`BigQueryStorageClient.batch_create_read_session_streams`.

        Creates additional streams for a ReadSession. This API can be used to
        dynamically adjust the parallelism of a batch processing task upwards by
        adding additional workers.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["big_query_storage_stub"].BatchCreateReadSessionStreams

    @property
    def finalize_stream(self):
        """Return the gRPC stub for :meth:`BigQueryStorageClient.finalize_stream`.

        Triggers the graceful termination of a single stream in a ReadSession. This
        API can be used to dynamically adjust the parallelism of a batch processing
        task downwards without losing data.

        This API does not delete the stream -- it remains visible in the
        ReadSession, and any data processed by the stream is not released to other
        streams. However, no additional data will be assigned to the stream once
        this call completes. Callers must continue reading data on the stream until
        the end of the stream is reached so that data which has already been
        assigned to the stream will be processed.

        This method will return an error if there are no other live streams
        in the Session, or if SplitReadStream() has been called on the given
        Stream.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["big_query_storage_stub"].FinalizeStream

    @property
    def split_read_stream(self):
        """Return the gRPC stub for :meth:`BigQueryStorageClient.split_read_stream`.

        Splits a given read stream into two Streams. These streams are referred
        to as the primary and the residual of the split. The original stream can
        still be read from in the same manner as before. Both of the returned
        streams can also be read from, and the total rows return by both child
        streams will be the same as the rows read from the original stream.

        Moreover, the two child streams will be allocated back to back in the
        original Stream. Concretely, it is guaranteed that for streams Original,
        Primary, and Residual, that Original[0-j] = Primary[0-j] and
        Original[j-n] = Residual[0-m] once the streams have been read to
        completion.

        This method is guaranteed to be idempotent.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["big_query_storage_stub"].SplitReadStream
