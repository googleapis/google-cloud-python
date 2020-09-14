# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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

from google.cloud.bigquery_storage_v1beta2.proto import storage_pb2_grpc


class BigQueryReadGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.cloud.bigquery.storage.v1beta2 BigQueryRead API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = (
        "https://www.googleapis.com/auth/bigquery",
        "https://www.googleapis.com/auth/bigquery.readonly",
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
                "The `channel` and `credentials` arguments are mutually " "exclusive.",
            )

        # Create the channel.
        if channel is None:  # pragma: no cover
            channel = self.create_channel(
                address=address,
                credentials=credentials,
                options={
                    "grpc.max_send_message_length": -1,
                    "grpc.max_receive_message_length": -1,
                }.items(),
            )

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {
            "big_query_read_stub": storage_pb2_grpc.BigQueryReadStub(channel),
        }

    @classmethod
    def create_channel(
        cls, address="bigquerystorage.googleapis.com:443", credentials=None, **kwargs
    ):
        """Create and return a gRPC channel object.

        Args:
            address (str): The host for the channel to use.
            credentials (~.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            kwargs (dict): Keyword arguments, which are passed to the
                channel creation.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return google.api_core.grpc_helpers.create_channel(  # pragma: no cover
            address, credentials=credentials, scopes=cls._OAUTH_SCOPES, **kwargs
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
        """Return the gRPC stub for :meth:`BigQueryReadClient.create_read_session`.

        Creates a new read session. A read session divides the contents of a
        BigQuery table into one or more streams, which can then be used to read
        data from the table. The read session also specifies properties of the
        data to be read, such as a list of columns or a push-down filter describing
        the rows to be returned.

        A particular row can be read by at most one stream. When the caller has
        reached the end of each stream in the session, then all the data in the
        table has been read.

        Data is assigned to each stream such that roughly the same number of
        rows can be read from each stream. Because the server-side unit for
        assigning data is collections of rows, the API does not guarantee that
        each stream will return the same number or rows. Additionally, the
        limits are enforced based on the number of pre-filtered rows, so some
        filters can lead to lopsided assignments.

        Read sessions automatically expire 24 hours after they are created and do
        not require manual clean-up by the caller.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["big_query_read_stub"].CreateReadSession

    @property
    def read_rows(self):
        """Return the gRPC stub for :meth:`BigQueryReadClient.read_rows`.

        Reads rows from the stream in the format prescribed by the ReadSession.
        Each response contains one or more table rows, up to a maximum of 100 MiB
        per response; read requests which attempt to read individual rows larger
        than 100 MiB will fail.

        Each request also returns a set of stream statistics reflecting the current
        state of the stream.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["big_query_read_stub"].ReadRows

    @property
    def split_read_stream(self):
        """Return the gRPC stub for :meth:`BigQueryReadClient.split_read_stream`.

        An indicator of the behavior of a given field (for example, that a
        field is required in requests, or given as output but ignored as input).
        This **does not** change the behavior in protocol buffers itself; it
        only denotes the behavior and may affect how API tooling handles the
        field.

        Note: This enum **may** receive new values in the future.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["big_query_read_stub"].SplitReadStream
