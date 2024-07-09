# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, grpc_helpers_async, operations_v1
from google.api_core import retry_async as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.storage_control_v2.types import storage_control

from .base import DEFAULT_CLIENT_INFO, StorageControlTransport
from .grpc import StorageControlGrpcTransport


class StorageControlGrpcAsyncIOTransport(StorageControlTransport):
    """gRPC AsyncIO backend transport for StorageControl.

    StorageControl service includes selected control plane
    operations.

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
        host: str = "storage.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
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
        host: str = "storage.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[Union[aio.Channel, Callable[..., aio.Channel]]] = None,
        api_mtls_endpoint: Optional[str] = None,
        client_cert_source: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        ssl_channel_credentials: Optional[grpc.ChannelCredentials] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'storage.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if a ``channel`` instance is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if a ``channel`` instance is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[Union[aio.Channel, Callable[..., aio.Channel]]]):
                A ``Channel`` instance through which to make calls, or a Callable
                that constructs and returns one. If set to None, ``self.create_channel``
                is used to create the channel. If a Callable is given, it will be called
                with the same arguments as used in ``self.create_channel``.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if a ``channel`` instance is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if a ``channel`` instance or ``ssl_channel_credentials`` is provided.
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
        self._operations_client: Optional[operations_v1.OperationsAsyncClient] = None

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if isinstance(channel, aio.Channel):
            # Ignore credentials if a channel was passed.
            credentials = None
            self._ignore_credentials = True
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
            api_audience=api_audience,
        )

        if not self._grpc_channel:
            # initialize with the provided callable or the default channel
            channel_init = channel or type(self).create_channel
            self._grpc_channel = channel_init(
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
    def operations_client(self) -> operations_v1.OperationsAsyncClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Quick check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsAsyncClient(
                self.grpc_channel
            )

        # Return the client from cache.
        return self._operations_client

    @property
    def create_folder(
        self,
    ) -> Callable[
        [storage_control.CreateFolderRequest], Awaitable[storage_control.Folder]
    ]:
        r"""Return a callable for the create folder method over gRPC.

        Creates a new folder. This operation is only
        applicable to a hierarchical namespace enabled bucket.

        Returns:
            Callable[[~.CreateFolderRequest],
                    Awaitable[~.Folder]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_folder" not in self._stubs:
            self._stubs["create_folder"] = self.grpc_channel.unary_unary(
                "/google.storage.control.v2.StorageControl/CreateFolder",
                request_serializer=storage_control.CreateFolderRequest.serialize,
                response_deserializer=storage_control.Folder.deserialize,
            )
        return self._stubs["create_folder"]

    @property
    def delete_folder(
        self,
    ) -> Callable[[storage_control.DeleteFolderRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete folder method over gRPC.

        Permanently deletes an empty folder. This operation
        is only applicable to a hierarchical namespace enabled
        bucket.

        Returns:
            Callable[[~.DeleteFolderRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_folder" not in self._stubs:
            self._stubs["delete_folder"] = self.grpc_channel.unary_unary(
                "/google.storage.control.v2.StorageControl/DeleteFolder",
                request_serializer=storage_control.DeleteFolderRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_folder"]

    @property
    def get_folder(
        self,
    ) -> Callable[
        [storage_control.GetFolderRequest], Awaitable[storage_control.Folder]
    ]:
        r"""Return a callable for the get folder method over gRPC.

        Returns metadata for the specified folder. This
        operation is only applicable to a hierarchical namespace
        enabled bucket.

        Returns:
            Callable[[~.GetFolderRequest],
                    Awaitable[~.Folder]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_folder" not in self._stubs:
            self._stubs["get_folder"] = self.grpc_channel.unary_unary(
                "/google.storage.control.v2.StorageControl/GetFolder",
                request_serializer=storage_control.GetFolderRequest.serialize,
                response_deserializer=storage_control.Folder.deserialize,
            )
        return self._stubs["get_folder"]

    @property
    def list_folders(
        self,
    ) -> Callable[
        [storage_control.ListFoldersRequest],
        Awaitable[storage_control.ListFoldersResponse],
    ]:
        r"""Return a callable for the list folders method over gRPC.

        Retrieves a list of folders. This operation is only
        applicable to a hierarchical namespace enabled bucket.

        Returns:
            Callable[[~.ListFoldersRequest],
                    Awaitable[~.ListFoldersResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_folders" not in self._stubs:
            self._stubs["list_folders"] = self.grpc_channel.unary_unary(
                "/google.storage.control.v2.StorageControl/ListFolders",
                request_serializer=storage_control.ListFoldersRequest.serialize,
                response_deserializer=storage_control.ListFoldersResponse.deserialize,
            )
        return self._stubs["list_folders"]

    @property
    def rename_folder(
        self,
    ) -> Callable[
        [storage_control.RenameFolderRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the rename folder method over gRPC.

        Renames a source folder to a destination folder. This
        operation is only applicable to a hierarchical namespace
        enabled bucket. During a rename, the source and
        destination folders are locked until the long running
        operation completes.

        Returns:
            Callable[[~.RenameFolderRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "rename_folder" not in self._stubs:
            self._stubs["rename_folder"] = self.grpc_channel.unary_unary(
                "/google.storage.control.v2.StorageControl/RenameFolder",
                request_serializer=storage_control.RenameFolderRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["rename_folder"]

    @property
    def get_storage_layout(
        self,
    ) -> Callable[
        [storage_control.GetStorageLayoutRequest],
        Awaitable[storage_control.StorageLayout],
    ]:
        r"""Return a callable for the get storage layout method over gRPC.

        Returns the storage layout configuration for a given
        bucket.

        Returns:
            Callable[[~.GetStorageLayoutRequest],
                    Awaitable[~.StorageLayout]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_storage_layout" not in self._stubs:
            self._stubs["get_storage_layout"] = self.grpc_channel.unary_unary(
                "/google.storage.control.v2.StorageControl/GetStorageLayout",
                request_serializer=storage_control.GetStorageLayoutRequest.serialize,
                response_deserializer=storage_control.StorageLayout.deserialize,
            )
        return self._stubs["get_storage_layout"]

    @property
    def create_managed_folder(
        self,
    ) -> Callable[
        [storage_control.CreateManagedFolderRequest],
        Awaitable[storage_control.ManagedFolder],
    ]:
        r"""Return a callable for the create managed folder method over gRPC.

        Creates a new managed folder.

        Returns:
            Callable[[~.CreateManagedFolderRequest],
                    Awaitable[~.ManagedFolder]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_managed_folder" not in self._stubs:
            self._stubs["create_managed_folder"] = self.grpc_channel.unary_unary(
                "/google.storage.control.v2.StorageControl/CreateManagedFolder",
                request_serializer=storage_control.CreateManagedFolderRequest.serialize,
                response_deserializer=storage_control.ManagedFolder.deserialize,
            )
        return self._stubs["create_managed_folder"]

    @property
    def delete_managed_folder(
        self,
    ) -> Callable[
        [storage_control.DeleteManagedFolderRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the delete managed folder method over gRPC.

        Permanently deletes an empty managed folder.

        Returns:
            Callable[[~.DeleteManagedFolderRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_managed_folder" not in self._stubs:
            self._stubs["delete_managed_folder"] = self.grpc_channel.unary_unary(
                "/google.storage.control.v2.StorageControl/DeleteManagedFolder",
                request_serializer=storage_control.DeleteManagedFolderRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_managed_folder"]

    @property
    def get_managed_folder(
        self,
    ) -> Callable[
        [storage_control.GetManagedFolderRequest],
        Awaitable[storage_control.ManagedFolder],
    ]:
        r"""Return a callable for the get managed folder method over gRPC.

        Returns metadata for the specified managed folder.

        Returns:
            Callable[[~.GetManagedFolderRequest],
                    Awaitable[~.ManagedFolder]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_managed_folder" not in self._stubs:
            self._stubs["get_managed_folder"] = self.grpc_channel.unary_unary(
                "/google.storage.control.v2.StorageControl/GetManagedFolder",
                request_serializer=storage_control.GetManagedFolderRequest.serialize,
                response_deserializer=storage_control.ManagedFolder.deserialize,
            )
        return self._stubs["get_managed_folder"]

    @property
    def list_managed_folders(
        self,
    ) -> Callable[
        [storage_control.ListManagedFoldersRequest],
        Awaitable[storage_control.ListManagedFoldersResponse],
    ]:
        r"""Return a callable for the list managed folders method over gRPC.

        Retrieves a list of managed folders for a given
        bucket.

        Returns:
            Callable[[~.ListManagedFoldersRequest],
                    Awaitable[~.ListManagedFoldersResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_managed_folders" not in self._stubs:
            self._stubs["list_managed_folders"] = self.grpc_channel.unary_unary(
                "/google.storage.control.v2.StorageControl/ListManagedFolders",
                request_serializer=storage_control.ListManagedFoldersRequest.serialize,
                response_deserializer=storage_control.ListManagedFoldersResponse.deserialize,
            )
        return self._stubs["list_managed_folders"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.create_folder: gapic_v1.method_async.wrap_method(
                self.create_folder,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_folder: gapic_v1.method_async.wrap_method(
                self.delete_folder,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_folder: gapic_v1.method_async.wrap_method(
                self.get_folder,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=2,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.InternalServerError,
                        core_exceptions.ResourceExhausted,
                        core_exceptions.ServiceUnavailable,
                        core_exceptions.Unknown,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_folders: gapic_v1.method_async.wrap_method(
                self.list_folders,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=2,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.InternalServerError,
                        core_exceptions.ResourceExhausted,
                        core_exceptions.ServiceUnavailable,
                        core_exceptions.Unknown,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.rename_folder: gapic_v1.method_async.wrap_method(
                self.rename_folder,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=2,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.InternalServerError,
                        core_exceptions.ResourceExhausted,
                        core_exceptions.ServiceUnavailable,
                        core_exceptions.Unknown,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_storage_layout: gapic_v1.method_async.wrap_method(
                self.get_storage_layout,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=2,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.InternalServerError,
                        core_exceptions.ResourceExhausted,
                        core_exceptions.ServiceUnavailable,
                        core_exceptions.Unknown,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_managed_folder: gapic_v1.method_async.wrap_method(
                self.create_managed_folder,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_managed_folder: gapic_v1.method_async.wrap_method(
                self.delete_managed_folder,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_managed_folder: gapic_v1.method_async.wrap_method(
                self.get_managed_folder,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=2,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.InternalServerError,
                        core_exceptions.ResourceExhausted,
                        core_exceptions.ServiceUnavailable,
                        core_exceptions.Unknown,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_managed_folders: gapic_v1.method_async.wrap_method(
                self.list_managed_folders,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=60.0,
                    multiplier=2,
                    predicate=retries.if_exception_type(
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.InternalServerError,
                        core_exceptions.ResourceExhausted,
                        core_exceptions.ServiceUnavailable,
                        core_exceptions.Unknown,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
        }

    def close(self):
        return self.grpc_channel.close()


__all__ = ("StorageControlGrpcAsyncIOTransport",)
