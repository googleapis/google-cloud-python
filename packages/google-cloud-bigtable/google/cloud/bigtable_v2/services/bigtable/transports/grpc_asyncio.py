# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
#
import warnings
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import gapic_v1
from google.api_core import grpc_helpers_async
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.bigtable_v2.types import bigtable
from .base import BigtableTransport, DEFAULT_CLIENT_INFO
from .grpc import BigtableGrpcTransport


class BigtableGrpcAsyncIOTransport(BigtableTransport):
    """gRPC AsyncIO backend transport for Bigtable.

    Service for reading from and writing to existing Bigtable
    tables.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _grpc_channel: aio.Channel
    _stubs: Dict[str, Callable] = {}

    @classmethod
    def create_channel(
        cls,
        host: str = "bigtable.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> aio.Channel:
        """Create and return a gRPC AsyncIO channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            aio.Channel: A gRPC AsyncIO channel object.
        """

        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    def __init__(
        self,
        *,
        host: str = "bigtable.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: aio.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        ssl_channel_credentials: grpc.ChannelCredentials = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id=None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[aio.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if ``channel`` or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if channel:
            # Ignore credentials if a channel was passed.
            credentials = False
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None
        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                else:
                    self._ssl_channel_credentials = SslCredentials().ssl_credentials

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
        )

        if not self._grpc_channel:
            self._grpc_channel = type(self).create_channel(
                self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                # Set ``credentials_file`` to ``None`` here as
                # the credentials that we saved earlier should be used.
                credentials_file=None,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        # Wrap messages. This must be done after self._grpc_channel exists
        self._prep_wrapped_messages(client_info)

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Return the channel from cache.
        return self._grpc_channel

    @property
    def read_rows(
        self,
    ) -> Callable[[bigtable.ReadRowsRequest], Awaitable[bigtable.ReadRowsResponse]]:
        r"""Return a callable for the read rows method over gRPC.

        Streams back the contents of all requested rows in
        key order, optionally applying the same Reader filter to
        each. Depending on their size, rows and cells may be
        broken up across multiple responses, but atomicity of
        each row will still be preserved. See the
        ReadRowsResponse documentation for details.

        Returns:
            Callable[[~.ReadRowsRequest],
                    Awaitable[~.ReadRowsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "read_rows" not in self._stubs:
            self._stubs["read_rows"] = self.grpc_channel.unary_stream(
                "/google.bigtable.v2.Bigtable/ReadRows",
                request_serializer=bigtable.ReadRowsRequest.serialize,
                response_deserializer=bigtable.ReadRowsResponse.deserialize,
            )
        return self._stubs["read_rows"]

    @property
    def sample_row_keys(
        self,
    ) -> Callable[
        [bigtable.SampleRowKeysRequest], Awaitable[bigtable.SampleRowKeysResponse]
    ]:
        r"""Return a callable for the sample row keys method over gRPC.

        Returns a sample of row keys in the table. The
        returned row keys will delimit contiguous sections of
        the table of approximately equal size, which can be used
        to break up the data for distributed tasks like
        mapreduces.

        Returns:
            Callable[[~.SampleRowKeysRequest],
                    Awaitable[~.SampleRowKeysResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "sample_row_keys" not in self._stubs:
            self._stubs["sample_row_keys"] = self.grpc_channel.unary_stream(
                "/google.bigtable.v2.Bigtable/SampleRowKeys",
                request_serializer=bigtable.SampleRowKeysRequest.serialize,
                response_deserializer=bigtable.SampleRowKeysResponse.deserialize,
            )
        return self._stubs["sample_row_keys"]

    @property
    def mutate_row(
        self,
    ) -> Callable[[bigtable.MutateRowRequest], Awaitable[bigtable.MutateRowResponse]]:
        r"""Return a callable for the mutate row method over gRPC.

        Mutates a row atomically. Cells already present in the row are
        left unchanged unless explicitly changed by ``mutation``.

        Returns:
            Callable[[~.MutateRowRequest],
                    Awaitable[~.MutateRowResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "mutate_row" not in self._stubs:
            self._stubs["mutate_row"] = self.grpc_channel.unary_unary(
                "/google.bigtable.v2.Bigtable/MutateRow",
                request_serializer=bigtable.MutateRowRequest.serialize,
                response_deserializer=bigtable.MutateRowResponse.deserialize,
            )
        return self._stubs["mutate_row"]

    @property
    def mutate_rows(
        self,
    ) -> Callable[[bigtable.MutateRowsRequest], Awaitable[bigtable.MutateRowsResponse]]:
        r"""Return a callable for the mutate rows method over gRPC.

        Mutates multiple rows in a batch. Each individual row
        is mutated atomically as in MutateRow, but the entire
        batch is not executed atomically.

        Returns:
            Callable[[~.MutateRowsRequest],
                    Awaitable[~.MutateRowsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "mutate_rows" not in self._stubs:
            self._stubs["mutate_rows"] = self.grpc_channel.unary_stream(
                "/google.bigtable.v2.Bigtable/MutateRows",
                request_serializer=bigtable.MutateRowsRequest.serialize,
                response_deserializer=bigtable.MutateRowsResponse.deserialize,
            )
        return self._stubs["mutate_rows"]

    @property
    def check_and_mutate_row(
        self,
    ) -> Callable[
        [bigtable.CheckAndMutateRowRequest],
        Awaitable[bigtable.CheckAndMutateRowResponse],
    ]:
        r"""Return a callable for the check and mutate row method over gRPC.

        Mutates a row atomically based on the output of a
        predicate Reader filter.

        Returns:
            Callable[[~.CheckAndMutateRowRequest],
                    Awaitable[~.CheckAndMutateRowResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "check_and_mutate_row" not in self._stubs:
            self._stubs["check_and_mutate_row"] = self.grpc_channel.unary_unary(
                "/google.bigtable.v2.Bigtable/CheckAndMutateRow",
                request_serializer=bigtable.CheckAndMutateRowRequest.serialize,
                response_deserializer=bigtable.CheckAndMutateRowResponse.deserialize,
            )
        return self._stubs["check_and_mutate_row"]

    @property
    def ping_and_warm(
        self,
    ) -> Callable[
        [bigtable.PingAndWarmRequest], Awaitable[bigtable.PingAndWarmResponse]
    ]:
        r"""Return a callable for the ping and warm method over gRPC.

        Warm up associated instance metadata for this
        connection. This call is not required but may be useful
        for connection keep-alive.

        Returns:
            Callable[[~.PingAndWarmRequest],
                    Awaitable[~.PingAndWarmResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "ping_and_warm" not in self._stubs:
            self._stubs["ping_and_warm"] = self.grpc_channel.unary_unary(
                "/google.bigtable.v2.Bigtable/PingAndWarm",
                request_serializer=bigtable.PingAndWarmRequest.serialize,
                response_deserializer=bigtable.PingAndWarmResponse.deserialize,
            )
        return self._stubs["ping_and_warm"]

    @property
    def read_modify_write_row(
        self,
    ) -> Callable[
        [bigtable.ReadModifyWriteRowRequest],
        Awaitable[bigtable.ReadModifyWriteRowResponse],
    ]:
        r"""Return a callable for the read modify write row method over gRPC.

        Modifies a row atomically on the server. The method
        reads the latest existing timestamp and value from the
        specified columns and writes a new entry based on
        pre-defined read/modify/write rules. The new value for
        the timestamp is the greater of the existing timestamp
        or the current server time. The method returns the new
        contents of all modified cells.

        Returns:
            Callable[[~.ReadModifyWriteRowRequest],
                    Awaitable[~.ReadModifyWriteRowResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "read_modify_write_row" not in self._stubs:
            self._stubs["read_modify_write_row"] = self.grpc_channel.unary_unary(
                "/google.bigtable.v2.Bigtable/ReadModifyWriteRow",
                request_serializer=bigtable.ReadModifyWriteRowRequest.serialize,
                response_deserializer=bigtable.ReadModifyWriteRowResponse.deserialize,
            )
        return self._stubs["read_modify_write_row"]

    def close(self):
        return self.grpc_channel.close()


__all__ = ("BigtableGrpcAsyncIOTransport",)
