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

from google.api_core import gapic_v1, grpc_helpers
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
import grpc  # type: ignore

from google.cloud.monitoring_v3.types import service
from google.cloud.monitoring_v3.types import service as gm_service
from google.cloud.monitoring_v3.types import service_service

from .base import DEFAULT_CLIENT_INFO, ServiceMonitoringServiceTransport


class ServiceMonitoringServiceGrpcTransport(ServiceMonitoringServiceTransport):
    """gRPC backend transport for ServiceMonitoringService.

    The Cloud Monitoring Service-Oriented Monitoring API has endpoints
    for managing and querying aspects of a Metrics Scope's services.
    These include the ``Service``'s monitored resources, its
    Service-Level Objectives, and a taxonomy of categorized Health
    Metrics.

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
        host: str = "monitoring.googleapis.com",
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
                 The hostname to connect to (default: 'monitoring.googleapis.com').
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
        host: str = "monitoring.googleapis.com",
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
    def create_service(
        self,
    ) -> Callable[[service_service.CreateServiceRequest], gm_service.Service]:
        r"""Return a callable for the create service method over gRPC.

        Create a ``Service``.

        Returns:
            Callable[[~.CreateServiceRequest],
                    ~.Service]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_service" not in self._stubs:
            self._stubs["create_service"] = self.grpc_channel.unary_unary(
                "/google.monitoring.v3.ServiceMonitoringService/CreateService",
                request_serializer=service_service.CreateServiceRequest.serialize,
                response_deserializer=gm_service.Service.deserialize,
            )
        return self._stubs["create_service"]

    @property
    def get_service(
        self,
    ) -> Callable[[service_service.GetServiceRequest], service.Service]:
        r"""Return a callable for the get service method over gRPC.

        Get the named ``Service``.

        Returns:
            Callable[[~.GetServiceRequest],
                    ~.Service]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_service" not in self._stubs:
            self._stubs["get_service"] = self.grpc_channel.unary_unary(
                "/google.monitoring.v3.ServiceMonitoringService/GetService",
                request_serializer=service_service.GetServiceRequest.serialize,
                response_deserializer=service.Service.deserialize,
            )
        return self._stubs["get_service"]

    @property
    def list_services(
        self,
    ) -> Callable[
        [service_service.ListServicesRequest], service_service.ListServicesResponse
    ]:
        r"""Return a callable for the list services method over gRPC.

        List ``Service``\ s for this Metrics Scope.

        Returns:
            Callable[[~.ListServicesRequest],
                    ~.ListServicesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_services" not in self._stubs:
            self._stubs["list_services"] = self.grpc_channel.unary_unary(
                "/google.monitoring.v3.ServiceMonitoringService/ListServices",
                request_serializer=service_service.ListServicesRequest.serialize,
                response_deserializer=service_service.ListServicesResponse.deserialize,
            )
        return self._stubs["list_services"]

    @property
    def update_service(
        self,
    ) -> Callable[[service_service.UpdateServiceRequest], gm_service.Service]:
        r"""Return a callable for the update service method over gRPC.

        Update this ``Service``.

        Returns:
            Callable[[~.UpdateServiceRequest],
                    ~.Service]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_service" not in self._stubs:
            self._stubs["update_service"] = self.grpc_channel.unary_unary(
                "/google.monitoring.v3.ServiceMonitoringService/UpdateService",
                request_serializer=service_service.UpdateServiceRequest.serialize,
                response_deserializer=gm_service.Service.deserialize,
            )
        return self._stubs["update_service"]

    @property
    def delete_service(
        self,
    ) -> Callable[[service_service.DeleteServiceRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete service method over gRPC.

        Soft delete this ``Service``.

        Returns:
            Callable[[~.DeleteServiceRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_service" not in self._stubs:
            self._stubs["delete_service"] = self.grpc_channel.unary_unary(
                "/google.monitoring.v3.ServiceMonitoringService/DeleteService",
                request_serializer=service_service.DeleteServiceRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_service"]

    @property
    def create_service_level_objective(
        self,
    ) -> Callable[
        [service_service.CreateServiceLevelObjectiveRequest],
        service.ServiceLevelObjective,
    ]:
        r"""Return a callable for the create service level objective method over gRPC.

        Create a ``ServiceLevelObjective`` for the given ``Service``.

        Returns:
            Callable[[~.CreateServiceLevelObjectiveRequest],
                    ~.ServiceLevelObjective]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_service_level_objective" not in self._stubs:
            self._stubs[
                "create_service_level_objective"
            ] = self.grpc_channel.unary_unary(
                "/google.monitoring.v3.ServiceMonitoringService/CreateServiceLevelObjective",
                request_serializer=service_service.CreateServiceLevelObjectiveRequest.serialize,
                response_deserializer=service.ServiceLevelObjective.deserialize,
            )
        return self._stubs["create_service_level_objective"]

    @property
    def get_service_level_objective(
        self,
    ) -> Callable[
        [service_service.GetServiceLevelObjectiveRequest], service.ServiceLevelObjective
    ]:
        r"""Return a callable for the get service level objective method over gRPC.

        Get a ``ServiceLevelObjective`` by name.

        Returns:
            Callable[[~.GetServiceLevelObjectiveRequest],
                    ~.ServiceLevelObjective]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_service_level_objective" not in self._stubs:
            self._stubs["get_service_level_objective"] = self.grpc_channel.unary_unary(
                "/google.monitoring.v3.ServiceMonitoringService/GetServiceLevelObjective",
                request_serializer=service_service.GetServiceLevelObjectiveRequest.serialize,
                response_deserializer=service.ServiceLevelObjective.deserialize,
            )
        return self._stubs["get_service_level_objective"]

    @property
    def list_service_level_objectives(
        self,
    ) -> Callable[
        [service_service.ListServiceLevelObjectivesRequest],
        service_service.ListServiceLevelObjectivesResponse,
    ]:
        r"""Return a callable for the list service level objectives method over gRPC.

        List the ``ServiceLevelObjective``\ s for the given ``Service``.

        Returns:
            Callable[[~.ListServiceLevelObjectivesRequest],
                    ~.ListServiceLevelObjectivesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_service_level_objectives" not in self._stubs:
            self._stubs[
                "list_service_level_objectives"
            ] = self.grpc_channel.unary_unary(
                "/google.monitoring.v3.ServiceMonitoringService/ListServiceLevelObjectives",
                request_serializer=service_service.ListServiceLevelObjectivesRequest.serialize,
                response_deserializer=service_service.ListServiceLevelObjectivesResponse.deserialize,
            )
        return self._stubs["list_service_level_objectives"]

    @property
    def update_service_level_objective(
        self,
    ) -> Callable[
        [service_service.UpdateServiceLevelObjectiveRequest],
        service.ServiceLevelObjective,
    ]:
        r"""Return a callable for the update service level objective method over gRPC.

        Update the given ``ServiceLevelObjective``.

        Returns:
            Callable[[~.UpdateServiceLevelObjectiveRequest],
                    ~.ServiceLevelObjective]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_service_level_objective" not in self._stubs:
            self._stubs[
                "update_service_level_objective"
            ] = self.grpc_channel.unary_unary(
                "/google.monitoring.v3.ServiceMonitoringService/UpdateServiceLevelObjective",
                request_serializer=service_service.UpdateServiceLevelObjectiveRequest.serialize,
                response_deserializer=service.ServiceLevelObjective.deserialize,
            )
        return self._stubs["update_service_level_objective"]

    @property
    def delete_service_level_objective(
        self,
    ) -> Callable[
        [service_service.DeleteServiceLevelObjectiveRequest], empty_pb2.Empty
    ]:
        r"""Return a callable for the delete service level objective method over gRPC.

        Delete the given ``ServiceLevelObjective``.

        Returns:
            Callable[[~.DeleteServiceLevelObjectiveRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_service_level_objective" not in self._stubs:
            self._stubs[
                "delete_service_level_objective"
            ] = self.grpc_channel.unary_unary(
                "/google.monitoring.v3.ServiceMonitoringService/DeleteServiceLevelObjective",
                request_serializer=service_service.DeleteServiceLevelObjectiveRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_service_level_objective"]

    def close(self):
        self.grpc_channel.close()

    @property
    def kind(self) -> str:
        return "grpc"


__all__ = ("ServiceMonitoringServiceGrpcTransport",)
