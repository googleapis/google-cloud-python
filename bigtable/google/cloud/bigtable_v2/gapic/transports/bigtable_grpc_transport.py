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

from google.cloud.bigtable_v2.proto import bigtable_pb2_grpc


class BigtableGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.bigtable.v2 Bigtable API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = (
        "https://www.googleapis.com/auth/bigtable.data",
        "https://www.googleapis.com/auth/bigtable.data.readonly",
        "https://www.googleapis.com/auth/cloud-bigtable.data",
        "https://www.googleapis.com/auth/cloud-bigtable.data.readonly",
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/cloud-platform.read-only",
    )

    def __init__(
        self, channel=None, credentials=None, address="bigtable.googleapis.com:443"
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
        if channel is not None and credentials is not None:
            raise ValueError(
                "The `channel` and `credentials` arguments are mutually " "exclusive."
            )

        # Create the channel.
        if channel is None:
            channel = self.create_channel(address=address, credentials=credentials)

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {"bigtable_stub": bigtable_pb2_grpc.BigtableStub(channel)}

    @classmethod
    def create_channel(cls, address="bigtable.googleapis.com:443", credentials=None):
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
        return google.api_core.grpc_helpers.create_channel(
            address,
            credentials=credentials,
            scopes=cls._OAUTH_SCOPES,
            options={
                "grpc.max_send_message_length": -1,
                "grpc.max_receive_message_length": -1,
            }.items(),
        )

    @property
    def channel(self):
        """The gRPC channel used by the transport.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return self._channel

    @property
    def read_rows(self):
        """Return the gRPC stub for :meth:`BigtableClient.read_rows`.

        Streams back the contents of all requested rows in key order, optionally
        applying the same Reader filter to each. Depending on their size,
        rows and cells may be broken up across multiple responses, but
        atomicity of each row will still be preserved. See the
        ReadRowsResponse documentation for details.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_stub"].ReadRows

    @property
    def sample_row_keys(self):
        """Return the gRPC stub for :meth:`BigtableClient.sample_row_keys`.

        Returns a sample of row keys in the table. The returned row keys will
        delimit contiguous sections of the table of approximately equal size,
        which can be used to break up the data for distributed tasks like
        mapreduces.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_stub"].SampleRowKeys

    @property
    def mutate_row(self):
        """Return the gRPC stub for :meth:`BigtableClient.mutate_row`.

        Mutates a row atomically. Cells already present in the row are left
        unchanged unless explicitly changed by ``mutation``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_stub"].MutateRow

    @property
    def mutate_rows(self):
        """Return the gRPC stub for :meth:`BigtableClient.mutate_rows`.

        Mutates multiple rows in a batch. Each individual row is mutated
        atomically as in MutateRow, but the entire batch is not executed
        atomically.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_stub"].MutateRows

    @property
    def check_and_mutate_row(self):
        """Return the gRPC stub for :meth:`BigtableClient.check_and_mutate_row`.

        Mutates a row atomically based on the output of a predicate Reader filter.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_stub"].CheckAndMutateRow

    @property
    def read_modify_write_row(self):
        """Return the gRPC stub for :meth:`BigtableClient.read_modify_write_row`.

        Modifies a row atomically on the server. The method reads the latest
        existing timestamp and value from the specified columns and writes a new
        entry based on pre-defined read/modify/write rules. The new value for the
        timestamp is the greater of the existing timestamp or the current server
        time. The method returns the new contents of all modified cells.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["bigtable_stub"].ReadModifyWriteRow
