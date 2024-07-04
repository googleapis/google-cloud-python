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
from typing import Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, grpc_helpers, operations_v1
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
import grpc  # type: ignore

from google.cloud.dataplex_v1.types import catalog

from .base import DEFAULT_CLIENT_INFO, CatalogServiceTransport


class CatalogServiceGrpcTransport(CatalogServiceTransport):
    """gRPC backend transport for CatalogService.

    The primary resources offered by this service are
    EntryGroups, EntryTypes, AspectTypes, Entry and Aspect which
    collectively allow a data administrator to organize, manage,
    secure and catalog data across their organization located across
    cloud projects in a variety of storage systems including Cloud
    Storage and BigQuery.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _stubs: Dict[str, Callable]

    def __init__(
        self,
        *,
        host: str = "dataplex.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[Union[grpc.Channel, Callable[..., grpc.Channel]]] = None,
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
                 The hostname to connect to (default: 'dataplex.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if a ``channel`` instance is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if a ``channel`` instance is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if a ``channel`` instance is provided.
            channel (Optional[Union[grpc.Channel, Callable[..., grpc.Channel]]]):
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
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}
        self._operations_client: Optional[operations_v1.OperationsClient] = None

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if isinstance(channel, grpc.Channel):
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

    @classmethod
    def create_channel(
        cls,
        host: str = "dataplex.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.

        Raises:
            google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """

        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Return the channel designed to connect to this service."""
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Quick check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsClient(self.grpc_channel)

        # Return the client from cache.
        return self._operations_client

    @property
    def create_entry_type(
        self,
    ) -> Callable[[catalog.CreateEntryTypeRequest], operations_pb2.Operation]:
        r"""Return a callable for the create entry type method over gRPC.

        Creates an EntryType

        Returns:
            Callable[[~.CreateEntryTypeRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_entry_type" not in self._stubs:
            self._stubs["create_entry_type"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataplex.v1.CatalogService/CreateEntryType",
                request_serializer=catalog.CreateEntryTypeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_entry_type"]

    @property
    def update_entry_type(
        self,
    ) -> Callable[[catalog.UpdateEntryTypeRequest], operations_pb2.Operation]:
        r"""Return a callable for the update entry type method over gRPC.

        Updates a EntryType resource.

        Returns:
            Callable[[~.UpdateEntryTypeRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_entry_type" not in self._stubs:
            self._stubs["update_entry_type"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataplex.v1.CatalogService/UpdateEntryType",
                request_serializer=catalog.UpdateEntryTypeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_entry_type"]

    @property
    def delete_entry_type(
        self,
    ) -> Callable[[catalog.DeleteEntryTypeRequest], operations_pb2.Operation]:
        r"""Return a callable for the delete entry type method over gRPC.

        Deletes a EntryType resource.

        Returns:
            Callable[[~.DeleteEntryTypeRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_entry_type" not in self._stubs:
            self._stubs["delete_entry_type"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataplex.v1.CatalogService/DeleteEntryType",
                request_serializer=catalog.DeleteEntryTypeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_entry_type"]

    @property
    def list_entry_types(
        self,
    ) -> Callable[[catalog.ListEntryTypesRequest], catalog.ListEntryTypesResponse]:
        r"""Return a callable for the list entry types method over gRPC.

        Lists EntryType resources in a project and location.

        Returns:
            Callable[[~.ListEntryTypesRequest],
                    ~.ListEntryTypesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_entry_types" not in self._stubs:
            self._stubs["list_entry_types"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataplex.v1.CatalogService/ListEntryTypes",
                request_serializer=catalog.ListEntryTypesRequest.serialize,
                response_deserializer=catalog.ListEntryTypesResponse.deserialize,
            )
        return self._stubs["list_entry_types"]

    @property
    def get_entry_type(
        self,
    ) -> Callable[[catalog.GetEntryTypeRequest], catalog.EntryType]:
        r"""Return a callable for the get entry type method over gRPC.

        Retrieves a EntryType resource.

        Returns:
            Callable[[~.GetEntryTypeRequest],
                    ~.EntryType]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_entry_type" not in self._stubs:
            self._stubs["get_entry_type"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataplex.v1.CatalogService/GetEntryType",
                request_serializer=catalog.GetEntryTypeRequest.serialize,
                response_deserializer=catalog.EntryType.deserialize,
            )
        return self._stubs["get_entry_type"]

    @property
    def create_aspect_type(
        self,
    ) -> Callable[[catalog.CreateAspectTypeRequest], operations_pb2.Operation]:
        r"""Return a callable for the create aspect type method over gRPC.

        Creates an AspectType

        Returns:
            Callable[[~.CreateAspectTypeRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_aspect_type" not in self._stubs:
            self._stubs["create_aspect_type"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataplex.v1.CatalogService/CreateAspectType",
                request_serializer=catalog.CreateAspectTypeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_aspect_type"]

    @property
    def update_aspect_type(
        self,
    ) -> Callable[[catalog.UpdateAspectTypeRequest], operations_pb2.Operation]:
        r"""Return a callable for the update aspect type method over gRPC.

        Updates a AspectType resource.

        Returns:
            Callable[[~.UpdateAspectTypeRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_aspect_type" not in self._stubs:
            self._stubs["update_aspect_type"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataplex.v1.CatalogService/UpdateAspectType",
                request_serializer=catalog.UpdateAspectTypeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_aspect_type"]

    @property
    def delete_aspect_type(
        self,
    ) -> Callable[[catalog.DeleteAspectTypeRequest], operations_pb2.Operation]:
        r"""Return a callable for the delete aspect type method over gRPC.

        Deletes a AspectType resource.

        Returns:
            Callable[[~.DeleteAspectTypeRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_aspect_type" not in self._stubs:
            self._stubs["delete_aspect_type"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataplex.v1.CatalogService/DeleteAspectType",
                request_serializer=catalog.DeleteAspectTypeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_aspect_type"]

    @property
    def list_aspect_types(
        self,
    ) -> Callable[[catalog.ListAspectTypesRequest], catalog.ListAspectTypesResponse]:
        r"""Return a callable for the list aspect types method over gRPC.

        Lists AspectType resources in a project and location.

        Returns:
            Callable[[~.ListAspectTypesRequest],
                    ~.ListAspectTypesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_aspect_types" not in self._stubs:
            self._stubs["list_aspect_types"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataplex.v1.CatalogService/ListAspectTypes",
                request_serializer=catalog.ListAspectTypesRequest.serialize,
                response_deserializer=catalog.ListAspectTypesResponse.deserialize,
            )
        return self._stubs["list_aspect_types"]

    @property
    def get_aspect_type(
        self,
    ) -> Callable[[catalog.GetAspectTypeRequest], catalog.AspectType]:
        r"""Return a callable for the get aspect type method over gRPC.

        Retrieves a AspectType resource.

        Returns:
            Callable[[~.GetAspectTypeRequest],
                    ~.AspectType]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_aspect_type" not in self._stubs:
            self._stubs["get_aspect_type"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataplex.v1.CatalogService/GetAspectType",
                request_serializer=catalog.GetAspectTypeRequest.serialize,
                response_deserializer=catalog.AspectType.deserialize,
            )
        return self._stubs["get_aspect_type"]

    @property
    def create_entry_group(
        self,
    ) -> Callable[[catalog.CreateEntryGroupRequest], operations_pb2.Operation]:
        r"""Return a callable for the create entry group method over gRPC.

        Creates an EntryGroup

        Returns:
            Callable[[~.CreateEntryGroupRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_entry_group" not in self._stubs:
            self._stubs["create_entry_group"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataplex.v1.CatalogService/CreateEntryGroup",
                request_serializer=catalog.CreateEntryGroupRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_entry_group"]

    @property
    def update_entry_group(
        self,
    ) -> Callable[[catalog.UpdateEntryGroupRequest], operations_pb2.Operation]:
        r"""Return a callable for the update entry group method over gRPC.

        Updates a EntryGroup resource.

        Returns:
            Callable[[~.UpdateEntryGroupRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_entry_group" not in self._stubs:
            self._stubs["update_entry_group"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataplex.v1.CatalogService/UpdateEntryGroup",
                request_serializer=catalog.UpdateEntryGroupRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_entry_group"]

    @property
    def delete_entry_group(
        self,
    ) -> Callable[[catalog.DeleteEntryGroupRequest], operations_pb2.Operation]:
        r"""Return a callable for the delete entry group method over gRPC.

        Deletes a EntryGroup resource.

        Returns:
            Callable[[~.DeleteEntryGroupRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_entry_group" not in self._stubs:
            self._stubs["delete_entry_group"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataplex.v1.CatalogService/DeleteEntryGroup",
                request_serializer=catalog.DeleteEntryGroupRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_entry_group"]

    @property
    def list_entry_groups(
        self,
    ) -> Callable[[catalog.ListEntryGroupsRequest], catalog.ListEntryGroupsResponse]:
        r"""Return a callable for the list entry groups method over gRPC.

        Lists EntryGroup resources in a project and location.

        Returns:
            Callable[[~.ListEntryGroupsRequest],
                    ~.ListEntryGroupsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_entry_groups" not in self._stubs:
            self._stubs["list_entry_groups"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataplex.v1.CatalogService/ListEntryGroups",
                request_serializer=catalog.ListEntryGroupsRequest.serialize,
                response_deserializer=catalog.ListEntryGroupsResponse.deserialize,
            )
        return self._stubs["list_entry_groups"]

    @property
    def get_entry_group(
        self,
    ) -> Callable[[catalog.GetEntryGroupRequest], catalog.EntryGroup]:
        r"""Return a callable for the get entry group method over gRPC.

        Retrieves a EntryGroup resource.

        Returns:
            Callable[[~.GetEntryGroupRequest],
                    ~.EntryGroup]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_entry_group" not in self._stubs:
            self._stubs["get_entry_group"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataplex.v1.CatalogService/GetEntryGroup",
                request_serializer=catalog.GetEntryGroupRequest.serialize,
                response_deserializer=catalog.EntryGroup.deserialize,
            )
        return self._stubs["get_entry_group"]

    @property
    def create_entry(self) -> Callable[[catalog.CreateEntryRequest], catalog.Entry]:
        r"""Return a callable for the create entry method over gRPC.

        Creates an Entry.

        Returns:
            Callable[[~.CreateEntryRequest],
                    ~.Entry]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_entry" not in self._stubs:
            self._stubs["create_entry"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataplex.v1.CatalogService/CreateEntry",
                request_serializer=catalog.CreateEntryRequest.serialize,
                response_deserializer=catalog.Entry.deserialize,
            )
        return self._stubs["create_entry"]

    @property
    def update_entry(self) -> Callable[[catalog.UpdateEntryRequest], catalog.Entry]:
        r"""Return a callable for the update entry method over gRPC.

        Updates an Entry.

        Returns:
            Callable[[~.UpdateEntryRequest],
                    ~.Entry]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_entry" not in self._stubs:
            self._stubs["update_entry"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataplex.v1.CatalogService/UpdateEntry",
                request_serializer=catalog.UpdateEntryRequest.serialize,
                response_deserializer=catalog.Entry.deserialize,
            )
        return self._stubs["update_entry"]

    @property
    def delete_entry(self) -> Callable[[catalog.DeleteEntryRequest], catalog.Entry]:
        r"""Return a callable for the delete entry method over gRPC.

        Deletes an Entry.

        Returns:
            Callable[[~.DeleteEntryRequest],
                    ~.Entry]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_entry" not in self._stubs:
            self._stubs["delete_entry"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataplex.v1.CatalogService/DeleteEntry",
                request_serializer=catalog.DeleteEntryRequest.serialize,
                response_deserializer=catalog.Entry.deserialize,
            )
        return self._stubs["delete_entry"]

    @property
    def list_entries(
        self,
    ) -> Callable[[catalog.ListEntriesRequest], catalog.ListEntriesResponse]:
        r"""Return a callable for the list entries method over gRPC.

        Lists entries within an entry group.

        Returns:
            Callable[[~.ListEntriesRequest],
                    ~.ListEntriesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_entries" not in self._stubs:
            self._stubs["list_entries"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataplex.v1.CatalogService/ListEntries",
                request_serializer=catalog.ListEntriesRequest.serialize,
                response_deserializer=catalog.ListEntriesResponse.deserialize,
            )
        return self._stubs["list_entries"]

    @property
    def get_entry(self) -> Callable[[catalog.GetEntryRequest], catalog.Entry]:
        r"""Return a callable for the get entry method over gRPC.

        Gets a single entry.

        Returns:
            Callable[[~.GetEntryRequest],
                    ~.Entry]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_entry" not in self._stubs:
            self._stubs["get_entry"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataplex.v1.CatalogService/GetEntry",
                request_serializer=catalog.GetEntryRequest.serialize,
                response_deserializer=catalog.Entry.deserialize,
            )
        return self._stubs["get_entry"]

    @property
    def lookup_entry(self) -> Callable[[catalog.LookupEntryRequest], catalog.Entry]:
        r"""Return a callable for the lookup entry method over gRPC.

        Looks up a single entry.

        Returns:
            Callable[[~.LookupEntryRequest],
                    ~.Entry]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "lookup_entry" not in self._stubs:
            self._stubs["lookup_entry"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataplex.v1.CatalogService/LookupEntry",
                request_serializer=catalog.LookupEntryRequest.serialize,
                response_deserializer=catalog.Entry.deserialize,
            )
        return self._stubs["lookup_entry"]

    @property
    def search_entries(
        self,
    ) -> Callable[[catalog.SearchEntriesRequest], catalog.SearchEntriesResponse]:
        r"""Return a callable for the search entries method over gRPC.

        Searches for entries matching given query and scope.

        Returns:
            Callable[[~.SearchEntriesRequest],
                    ~.SearchEntriesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "search_entries" not in self._stubs:
            self._stubs["search_entries"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataplex.v1.CatalogService/SearchEntries",
                request_serializer=catalog.SearchEntriesRequest.serialize,
                response_deserializer=catalog.SearchEntriesResponse.deserialize,
            )
        return self._stubs["search_entries"]

    def close(self):
        self.grpc_channel.close()

    @property
    def delete_operation(
        self,
    ) -> Callable[[operations_pb2.DeleteOperationRequest], None]:
        r"""Return a callable for the delete_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_operation" not in self._stubs:
            self._stubs["delete_operation"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/DeleteOperation",
                request_serializer=operations_pb2.DeleteOperationRequest.SerializeToString,
                response_deserializer=None,
            )
        return self._stubs["delete_operation"]

    @property
    def cancel_operation(
        self,
    ) -> Callable[[operations_pb2.CancelOperationRequest], None]:
        r"""Return a callable for the cancel_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "cancel_operation" not in self._stubs:
            self._stubs["cancel_operation"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/CancelOperation",
                request_serializer=operations_pb2.CancelOperationRequest.SerializeToString,
                response_deserializer=None,
            )
        return self._stubs["cancel_operation"]

    @property
    def get_operation(
        self,
    ) -> Callable[[operations_pb2.GetOperationRequest], operations_pb2.Operation]:
        r"""Return a callable for the get_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_operation" not in self._stubs:
            self._stubs["get_operation"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/GetOperation",
                request_serializer=operations_pb2.GetOperationRequest.SerializeToString,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["get_operation"]

    @property
    def list_operations(
        self,
    ) -> Callable[
        [operations_pb2.ListOperationsRequest], operations_pb2.ListOperationsResponse
    ]:
        r"""Return a callable for the list_operations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_operations" not in self._stubs:
            self._stubs["list_operations"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/ListOperations",
                request_serializer=operations_pb2.ListOperationsRequest.SerializeToString,
                response_deserializer=operations_pb2.ListOperationsResponse.FromString,
            )
        return self._stubs["list_operations"]

    @property
    def list_locations(
        self,
    ) -> Callable[
        [locations_pb2.ListLocationsRequest], locations_pb2.ListLocationsResponse
    ]:
        r"""Return a callable for the list locations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_locations" not in self._stubs:
            self._stubs["list_locations"] = self.grpc_channel.unary_unary(
                "/google.cloud.location.Locations/ListLocations",
                request_serializer=locations_pb2.ListLocationsRequest.SerializeToString,
                response_deserializer=locations_pb2.ListLocationsResponse.FromString,
            )
        return self._stubs["list_locations"]

    @property
    def get_location(
        self,
    ) -> Callable[[locations_pb2.GetLocationRequest], locations_pb2.Location]:
        r"""Return a callable for the list locations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_location" not in self._stubs:
            self._stubs["get_location"] = self.grpc_channel.unary_unary(
                "/google.cloud.location.Locations/GetLocation",
                request_serializer=locations_pb2.GetLocationRequest.SerializeToString,
                response_deserializer=locations_pb2.Location.FromString,
            )
        return self._stubs["get_location"]

    @property
    def kind(self) -> str:
        return "grpc"


__all__ = ("CatalogServiceGrpcTransport",)
