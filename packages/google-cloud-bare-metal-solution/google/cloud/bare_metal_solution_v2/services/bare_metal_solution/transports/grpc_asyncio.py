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
from google.api_core import operations_v1
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.bare_metal_solution_v2.types import instance
from google.cloud.bare_metal_solution_v2.types import instance as gcb_instance
from google.cloud.bare_metal_solution_v2.types import lun
from google.cloud.bare_metal_solution_v2.types import network
from google.cloud.bare_metal_solution_v2.types import network as gcb_network
from google.cloud.bare_metal_solution_v2.types import nfs_share
from google.cloud.bare_metal_solution_v2.types import nfs_share as gcb_nfs_share
from google.cloud.bare_metal_solution_v2.types import volume
from google.cloud.bare_metal_solution_v2.types import volume as gcb_volume
from google.longrunning import operations_pb2  # type: ignore
from .base import BareMetalSolutionTransport, DEFAULT_CLIENT_INFO
from .grpc import BareMetalSolutionGrpcTransport


class BareMetalSolutionGrpcAsyncIOTransport(BareMetalSolutionTransport):
    """gRPC AsyncIO backend transport for BareMetalSolution.

    Performs management operations on Bare Metal Solution servers.

    The ``baremetalsolution.googleapis.com`` service provides management
    capabilities for Bare Metal Solution servers. To access the API
    methods, you must assign Bare Metal Solution IAM roles containing
    the desired permissions to your staff in your Google Cloud project.
    You must also enable the Bare Metal Solution API. Once enabled, the
    methods act upon specific servers in your Bare Metal Solution
    environment.

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
        host: str = "baremetalsolution.googleapis.com",
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
        host: str = "baremetalsolution.googleapis.com",
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
        api_audience: Optional[str] = None,
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
        self._operations_client: Optional[operations_v1.OperationsAsyncClient] = None

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
            api_audience=api_audience,
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
    def list_instances(
        self,
    ) -> Callable[
        [instance.ListInstancesRequest], Awaitable[instance.ListInstancesResponse]
    ]:
        r"""Return a callable for the list instances method over gRPC.

        List servers in a given project and location.

        Returns:
            Callable[[~.ListInstancesRequest],
                    Awaitable[~.ListInstancesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_instances" not in self._stubs:
            self._stubs["list_instances"] = self.grpc_channel.unary_unary(
                "/google.cloud.baremetalsolution.v2.BareMetalSolution/ListInstances",
                request_serializer=instance.ListInstancesRequest.serialize,
                response_deserializer=instance.ListInstancesResponse.deserialize,
            )
        return self._stubs["list_instances"]

    @property
    def get_instance(
        self,
    ) -> Callable[[instance.GetInstanceRequest], Awaitable[instance.Instance]]:
        r"""Return a callable for the get instance method over gRPC.

        Get details about a single server.

        Returns:
            Callable[[~.GetInstanceRequest],
                    Awaitable[~.Instance]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_instance" not in self._stubs:
            self._stubs["get_instance"] = self.grpc_channel.unary_unary(
                "/google.cloud.baremetalsolution.v2.BareMetalSolution/GetInstance",
                request_serializer=instance.GetInstanceRequest.serialize,
                response_deserializer=instance.Instance.deserialize,
            )
        return self._stubs["get_instance"]

    @property
    def update_instance(
        self,
    ) -> Callable[
        [gcb_instance.UpdateInstanceRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update instance method over gRPC.

        Update details of a single server.

        Returns:
            Callable[[~.UpdateInstanceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_instance" not in self._stubs:
            self._stubs["update_instance"] = self.grpc_channel.unary_unary(
                "/google.cloud.baremetalsolution.v2.BareMetalSolution/UpdateInstance",
                request_serializer=gcb_instance.UpdateInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_instance"]

    @property
    def reset_instance(
        self,
    ) -> Callable[[instance.ResetInstanceRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the reset instance method over gRPC.

        Perform an ungraceful, hard reset on a server.
        Equivalent to shutting the power off and then turning it
        back on.

        Returns:
            Callable[[~.ResetInstanceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "reset_instance" not in self._stubs:
            self._stubs["reset_instance"] = self.grpc_channel.unary_unary(
                "/google.cloud.baremetalsolution.v2.BareMetalSolution/ResetInstance",
                request_serializer=instance.ResetInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["reset_instance"]

    @property
    def start_instance(
        self,
    ) -> Callable[[instance.StartInstanceRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the start instance method over gRPC.

        Starts a server that was shutdown.

        Returns:
            Callable[[~.StartInstanceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "start_instance" not in self._stubs:
            self._stubs["start_instance"] = self.grpc_channel.unary_unary(
                "/google.cloud.baremetalsolution.v2.BareMetalSolution/StartInstance",
                request_serializer=instance.StartInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["start_instance"]

    @property
    def stop_instance(
        self,
    ) -> Callable[[instance.StopInstanceRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the stop instance method over gRPC.

        Stop a running server.

        Returns:
            Callable[[~.StopInstanceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "stop_instance" not in self._stubs:
            self._stubs["stop_instance"] = self.grpc_channel.unary_unary(
                "/google.cloud.baremetalsolution.v2.BareMetalSolution/StopInstance",
                request_serializer=instance.StopInstanceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["stop_instance"]

    @property
    def detach_lun(
        self,
    ) -> Callable[[gcb_instance.DetachLunRequest], Awaitable[operations_pb2.Operation]]:
        r"""Return a callable for the detach lun method over gRPC.

        Detach LUN from Instance.

        Returns:
            Callable[[~.DetachLunRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "detach_lun" not in self._stubs:
            self._stubs["detach_lun"] = self.grpc_channel.unary_unary(
                "/google.cloud.baremetalsolution.v2.BareMetalSolution/DetachLun",
                request_serializer=gcb_instance.DetachLunRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["detach_lun"]

    @property
    def list_volumes(
        self,
    ) -> Callable[[volume.ListVolumesRequest], Awaitable[volume.ListVolumesResponse]]:
        r"""Return a callable for the list volumes method over gRPC.

        List storage volumes in a given project and location.

        Returns:
            Callable[[~.ListVolumesRequest],
                    Awaitable[~.ListVolumesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_volumes" not in self._stubs:
            self._stubs["list_volumes"] = self.grpc_channel.unary_unary(
                "/google.cloud.baremetalsolution.v2.BareMetalSolution/ListVolumes",
                request_serializer=volume.ListVolumesRequest.serialize,
                response_deserializer=volume.ListVolumesResponse.deserialize,
            )
        return self._stubs["list_volumes"]

    @property
    def get_volume(
        self,
    ) -> Callable[[volume.GetVolumeRequest], Awaitable[volume.Volume]]:
        r"""Return a callable for the get volume method over gRPC.

        Get details of a single storage volume.

        Returns:
            Callable[[~.GetVolumeRequest],
                    Awaitable[~.Volume]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_volume" not in self._stubs:
            self._stubs["get_volume"] = self.grpc_channel.unary_unary(
                "/google.cloud.baremetalsolution.v2.BareMetalSolution/GetVolume",
                request_serializer=volume.GetVolumeRequest.serialize,
                response_deserializer=volume.Volume.deserialize,
            )
        return self._stubs["get_volume"]

    @property
    def update_volume(
        self,
    ) -> Callable[
        [gcb_volume.UpdateVolumeRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update volume method over gRPC.

        Update details of a single storage volume.

        Returns:
            Callable[[~.UpdateVolumeRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_volume" not in self._stubs:
            self._stubs["update_volume"] = self.grpc_channel.unary_unary(
                "/google.cloud.baremetalsolution.v2.BareMetalSolution/UpdateVolume",
                request_serializer=gcb_volume.UpdateVolumeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_volume"]

    @property
    def resize_volume(
        self,
    ) -> Callable[
        [gcb_volume.ResizeVolumeRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the resize volume method over gRPC.

        Emergency Volume resize.

        Returns:
            Callable[[~.ResizeVolumeRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "resize_volume" not in self._stubs:
            self._stubs["resize_volume"] = self.grpc_channel.unary_unary(
                "/google.cloud.baremetalsolution.v2.BareMetalSolution/ResizeVolume",
                request_serializer=gcb_volume.ResizeVolumeRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["resize_volume"]

    @property
    def list_networks(
        self,
    ) -> Callable[
        [network.ListNetworksRequest], Awaitable[network.ListNetworksResponse]
    ]:
        r"""Return a callable for the list networks method over gRPC.

        List network in a given project and location.

        Returns:
            Callable[[~.ListNetworksRequest],
                    Awaitable[~.ListNetworksResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_networks" not in self._stubs:
            self._stubs["list_networks"] = self.grpc_channel.unary_unary(
                "/google.cloud.baremetalsolution.v2.BareMetalSolution/ListNetworks",
                request_serializer=network.ListNetworksRequest.serialize,
                response_deserializer=network.ListNetworksResponse.deserialize,
            )
        return self._stubs["list_networks"]

    @property
    def list_network_usage(
        self,
    ) -> Callable[
        [network.ListNetworkUsageRequest], Awaitable[network.ListNetworkUsageResponse]
    ]:
        r"""Return a callable for the list network usage method over gRPC.

        List all Networks (and used IPs for each Network) in
        the vendor account associated with the specified
        project.

        Returns:
            Callable[[~.ListNetworkUsageRequest],
                    Awaitable[~.ListNetworkUsageResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_network_usage" not in self._stubs:
            self._stubs["list_network_usage"] = self.grpc_channel.unary_unary(
                "/google.cloud.baremetalsolution.v2.BareMetalSolution/ListNetworkUsage",
                request_serializer=network.ListNetworkUsageRequest.serialize,
                response_deserializer=network.ListNetworkUsageResponse.deserialize,
            )
        return self._stubs["list_network_usage"]

    @property
    def get_network(
        self,
    ) -> Callable[[network.GetNetworkRequest], Awaitable[network.Network]]:
        r"""Return a callable for the get network method over gRPC.

        Get details of a single network.

        Returns:
            Callable[[~.GetNetworkRequest],
                    Awaitable[~.Network]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_network" not in self._stubs:
            self._stubs["get_network"] = self.grpc_channel.unary_unary(
                "/google.cloud.baremetalsolution.v2.BareMetalSolution/GetNetwork",
                request_serializer=network.GetNetworkRequest.serialize,
                response_deserializer=network.Network.deserialize,
            )
        return self._stubs["get_network"]

    @property
    def update_network(
        self,
    ) -> Callable[
        [gcb_network.UpdateNetworkRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update network method over gRPC.

        Update details of a single network.

        Returns:
            Callable[[~.UpdateNetworkRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_network" not in self._stubs:
            self._stubs["update_network"] = self.grpc_channel.unary_unary(
                "/google.cloud.baremetalsolution.v2.BareMetalSolution/UpdateNetwork",
                request_serializer=gcb_network.UpdateNetworkRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_network"]

    @property
    def get_lun(self) -> Callable[[lun.GetLunRequest], Awaitable[lun.Lun]]:
        r"""Return a callable for the get lun method over gRPC.

        Get details of a single storage logical unit
        number(LUN).

        Returns:
            Callable[[~.GetLunRequest],
                    Awaitable[~.Lun]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_lun" not in self._stubs:
            self._stubs["get_lun"] = self.grpc_channel.unary_unary(
                "/google.cloud.baremetalsolution.v2.BareMetalSolution/GetLun",
                request_serializer=lun.GetLunRequest.serialize,
                response_deserializer=lun.Lun.deserialize,
            )
        return self._stubs["get_lun"]

    @property
    def list_luns(
        self,
    ) -> Callable[[lun.ListLunsRequest], Awaitable[lun.ListLunsResponse]]:
        r"""Return a callable for the list luns method over gRPC.

        List storage volume luns for given storage volume.

        Returns:
            Callable[[~.ListLunsRequest],
                    Awaitable[~.ListLunsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_luns" not in self._stubs:
            self._stubs["list_luns"] = self.grpc_channel.unary_unary(
                "/google.cloud.baremetalsolution.v2.BareMetalSolution/ListLuns",
                request_serializer=lun.ListLunsRequest.serialize,
                response_deserializer=lun.ListLunsResponse.deserialize,
            )
        return self._stubs["list_luns"]

    @property
    def get_nfs_share(
        self,
    ) -> Callable[[nfs_share.GetNfsShareRequest], Awaitable[nfs_share.NfsShare]]:
        r"""Return a callable for the get nfs share method over gRPC.

        Get details of a single NFS share.

        Returns:
            Callable[[~.GetNfsShareRequest],
                    Awaitable[~.NfsShare]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_nfs_share" not in self._stubs:
            self._stubs["get_nfs_share"] = self.grpc_channel.unary_unary(
                "/google.cloud.baremetalsolution.v2.BareMetalSolution/GetNfsShare",
                request_serializer=nfs_share.GetNfsShareRequest.serialize,
                response_deserializer=nfs_share.NfsShare.deserialize,
            )
        return self._stubs["get_nfs_share"]

    @property
    def list_nfs_shares(
        self,
    ) -> Callable[
        [nfs_share.ListNfsSharesRequest], Awaitable[nfs_share.ListNfsSharesResponse]
    ]:
        r"""Return a callable for the list nfs shares method over gRPC.

        List NFS shares.

        Returns:
            Callable[[~.ListNfsSharesRequest],
                    Awaitable[~.ListNfsSharesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_nfs_shares" not in self._stubs:
            self._stubs["list_nfs_shares"] = self.grpc_channel.unary_unary(
                "/google.cloud.baremetalsolution.v2.BareMetalSolution/ListNfsShares",
                request_serializer=nfs_share.ListNfsSharesRequest.serialize,
                response_deserializer=nfs_share.ListNfsSharesResponse.deserialize,
            )
        return self._stubs["list_nfs_shares"]

    @property
    def update_nfs_share(
        self,
    ) -> Callable[
        [gcb_nfs_share.UpdateNfsShareRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the update nfs share method over gRPC.

        Update details of a single NFS share.

        Returns:
            Callable[[~.UpdateNfsShareRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_nfs_share" not in self._stubs:
            self._stubs["update_nfs_share"] = self.grpc_channel.unary_unary(
                "/google.cloud.baremetalsolution.v2.BareMetalSolution/UpdateNfsShare",
                request_serializer=gcb_nfs_share.UpdateNfsShareRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["update_nfs_share"]

    def close(self):
        return self.grpc_channel.close()


__all__ = ("BareMetalSolutionGrpcAsyncIOTransport",)
