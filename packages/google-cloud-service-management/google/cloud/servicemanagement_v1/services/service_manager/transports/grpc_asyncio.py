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

from google.api import service_pb2  # type: ignore
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, grpc_helpers_async, operations_v1
from google.api_core import retry_async as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.servicemanagement_v1.types import resources, servicemanager

from .base import DEFAULT_CLIENT_INFO, ServiceManagerTransport
from .grpc import ServiceManagerGrpcTransport


class ServiceManagerGrpcAsyncIOTransport(ServiceManagerTransport):
    """gRPC AsyncIO backend transport for ServiceManager.

    `Google Service Management
    API <https://cloud.google.com/service-infrastructure/docs/overview>`__

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
        host: str = "servicemanagement.googleapis.com",
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
        host: str = "servicemanagement.googleapis.com",
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
                 The hostname to connect to (default: 'servicemanagement.googleapis.com').
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
    def list_services(
        self,
    ) -> Callable[
        [servicemanager.ListServicesRequest],
        Awaitable[servicemanager.ListServicesResponse],
    ]:
        r"""Return a callable for the list services method over gRPC.

        Lists managed services.

        Returns all public services. For authenticated users,
        also returns all services the calling user has
        "servicemanagement.services.get" permission for.

        Returns:
            Callable[[~.ListServicesRequest],
                    Awaitable[~.ListServicesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_services" not in self._stubs:
            self._stubs["list_services"] = self.grpc_channel.unary_unary(
                "/google.api.servicemanagement.v1.ServiceManager/ListServices",
                request_serializer=servicemanager.ListServicesRequest.serialize,
                response_deserializer=servicemanager.ListServicesResponse.deserialize,
            )
        return self._stubs["list_services"]

    @property
    def get_service(
        self,
    ) -> Callable[
        [servicemanager.GetServiceRequest], Awaitable[resources.ManagedService]
    ]:
        r"""Return a callable for the get service method over gRPC.

        Gets a managed service. Authentication is required
        unless the service is public.

        Returns:
            Callable[[~.GetServiceRequest],
                    Awaitable[~.ManagedService]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_service" not in self._stubs:
            self._stubs["get_service"] = self.grpc_channel.unary_unary(
                "/google.api.servicemanagement.v1.ServiceManager/GetService",
                request_serializer=servicemanager.GetServiceRequest.serialize,
                response_deserializer=resources.ManagedService.deserialize,
            )
        return self._stubs["get_service"]

    @property
    def create_service(
        self,
    ) -> Callable[
        [servicemanager.CreateServiceRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create service method over gRPC.

        Creates a new managed service.

        A managed service is immutable, and is subject to
        mandatory 30-day data retention. You cannot move a
        service or recreate it within 30 days after deletion.

        One producer project can own no more than 500 services.
        For security and reliability purposes, a production
        service should be hosted in a dedicated producer
        project.

        Operation<response: ManagedService>

        Returns:
            Callable[[~.CreateServiceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_service" not in self._stubs:
            self._stubs["create_service"] = self.grpc_channel.unary_unary(
                "/google.api.servicemanagement.v1.ServiceManager/CreateService",
                request_serializer=servicemanager.CreateServiceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_service"]

    @property
    def delete_service(
        self,
    ) -> Callable[
        [servicemanager.DeleteServiceRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete service method over gRPC.

        Deletes a managed service. This method will change the service
        to the ``Soft-Delete`` state for 30 days. Within this period,
        service producers may call
        [UndeleteService][google.api.servicemanagement.v1.ServiceManager.UndeleteService]
        to restore the service. After 30 days, the service will be
        permanently deleted.

        Operation<response: google.protobuf.Empty>

        Returns:
            Callable[[~.DeleteServiceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_service" not in self._stubs:
            self._stubs["delete_service"] = self.grpc_channel.unary_unary(
                "/google.api.servicemanagement.v1.ServiceManager/DeleteService",
                request_serializer=servicemanager.DeleteServiceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_service"]

    @property
    def undelete_service(
        self,
    ) -> Callable[
        [servicemanager.UndeleteServiceRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the undelete service method over gRPC.

        Revives a previously deleted managed service. The
        method restores the service using the configuration at
        the time the service was deleted. The target service
        must exist and must have been deleted within the last 30
        days.

        Operation<response: UndeleteServiceResponse>

        Returns:
            Callable[[~.UndeleteServiceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "undelete_service" not in self._stubs:
            self._stubs["undelete_service"] = self.grpc_channel.unary_unary(
                "/google.api.servicemanagement.v1.ServiceManager/UndeleteService",
                request_serializer=servicemanager.UndeleteServiceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["undelete_service"]

    @property
    def list_service_configs(
        self,
    ) -> Callable[
        [servicemanager.ListServiceConfigsRequest],
        Awaitable[servicemanager.ListServiceConfigsResponse],
    ]:
        r"""Return a callable for the list service configs method over gRPC.

        Lists the history of the service configuration for a
        managed service, from the newest to the oldest.

        Returns:
            Callable[[~.ListServiceConfigsRequest],
                    Awaitable[~.ListServiceConfigsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_service_configs" not in self._stubs:
            self._stubs["list_service_configs"] = self.grpc_channel.unary_unary(
                "/google.api.servicemanagement.v1.ServiceManager/ListServiceConfigs",
                request_serializer=servicemanager.ListServiceConfigsRequest.serialize,
                response_deserializer=servicemanager.ListServiceConfigsResponse.deserialize,
            )
        return self._stubs["list_service_configs"]

    @property
    def get_service_config(
        self,
    ) -> Callable[
        [servicemanager.GetServiceConfigRequest], Awaitable[service_pb2.Service]
    ]:
        r"""Return a callable for the get service config method over gRPC.

        Gets a service configuration (version) for a managed
        service.

        Returns:
            Callable[[~.GetServiceConfigRequest],
                    Awaitable[~.Service]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_service_config" not in self._stubs:
            self._stubs["get_service_config"] = self.grpc_channel.unary_unary(
                "/google.api.servicemanagement.v1.ServiceManager/GetServiceConfig",
                request_serializer=servicemanager.GetServiceConfigRequest.serialize,
                response_deserializer=service_pb2.Service.FromString,
            )
        return self._stubs["get_service_config"]

    @property
    def create_service_config(
        self,
    ) -> Callable[
        [servicemanager.CreateServiceConfigRequest], Awaitable[service_pb2.Service]
    ]:
        r"""Return a callable for the create service config method over gRPC.

        Creates a new service configuration (version) for a managed
        service. This method only stores the service configuration. To
        roll out the service configuration to backend systems please
        call
        [CreateServiceRollout][google.api.servicemanagement.v1.ServiceManager.CreateServiceRollout].

        Only the 100 most recent service configurations and ones
        referenced by existing rollouts are kept for each service. The
        rest will be deleted eventually.

        Returns:
            Callable[[~.CreateServiceConfigRequest],
                    Awaitable[~.Service]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_service_config" not in self._stubs:
            self._stubs["create_service_config"] = self.grpc_channel.unary_unary(
                "/google.api.servicemanagement.v1.ServiceManager/CreateServiceConfig",
                request_serializer=servicemanager.CreateServiceConfigRequest.serialize,
                response_deserializer=service_pb2.Service.FromString,
            )
        return self._stubs["create_service_config"]

    @property
    def submit_config_source(
        self,
    ) -> Callable[
        [servicemanager.SubmitConfigSourceRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the submit config source method over gRPC.

        Creates a new service configuration (version) for a managed
        service based on user-supplied configuration source files (for
        example: OpenAPI Specification). This method stores the source
        configurations as well as the generated service configuration.
        To rollout the service configuration to other services, please
        call
        [CreateServiceRollout][google.api.servicemanagement.v1.ServiceManager.CreateServiceRollout].

        Only the 100 most recent configuration sources and ones
        referenced by existing service configurtions are kept for each
        service. The rest will be deleted eventually.

        Operation<response: SubmitConfigSourceResponse>

        Returns:
            Callable[[~.SubmitConfigSourceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "submit_config_source" not in self._stubs:
            self._stubs["submit_config_source"] = self.grpc_channel.unary_unary(
                "/google.api.servicemanagement.v1.ServiceManager/SubmitConfigSource",
                request_serializer=servicemanager.SubmitConfigSourceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["submit_config_source"]

    @property
    def list_service_rollouts(
        self,
    ) -> Callable[
        [servicemanager.ListServiceRolloutsRequest],
        Awaitable[servicemanager.ListServiceRolloutsResponse],
    ]:
        r"""Return a callable for the list service rollouts method over gRPC.

        Lists the history of the service configuration
        rollouts for a managed service, from the newest to the
        oldest.

        Returns:
            Callable[[~.ListServiceRolloutsRequest],
                    Awaitable[~.ListServiceRolloutsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_service_rollouts" not in self._stubs:
            self._stubs["list_service_rollouts"] = self.grpc_channel.unary_unary(
                "/google.api.servicemanagement.v1.ServiceManager/ListServiceRollouts",
                request_serializer=servicemanager.ListServiceRolloutsRequest.serialize,
                response_deserializer=servicemanager.ListServiceRolloutsResponse.deserialize,
            )
        return self._stubs["list_service_rollouts"]

    @property
    def get_service_rollout(
        self,
    ) -> Callable[
        [servicemanager.GetServiceRolloutRequest], Awaitable[resources.Rollout]
    ]:
        r"""Return a callable for the get service rollout method over gRPC.

        Gets a service configuration
        [rollout][google.api.servicemanagement.v1.Rollout].

        Returns:
            Callable[[~.GetServiceRolloutRequest],
                    Awaitable[~.Rollout]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_service_rollout" not in self._stubs:
            self._stubs["get_service_rollout"] = self.grpc_channel.unary_unary(
                "/google.api.servicemanagement.v1.ServiceManager/GetServiceRollout",
                request_serializer=servicemanager.GetServiceRolloutRequest.serialize,
                response_deserializer=resources.Rollout.deserialize,
            )
        return self._stubs["get_service_rollout"]

    @property
    def create_service_rollout(
        self,
    ) -> Callable[
        [servicemanager.CreateServiceRolloutRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the create service rollout method over gRPC.

        Creates a new service configuration rollout. Based on
        rollout, the Google Service Management will roll out the
        service configurations to different backend services.
        For example, the logging configuration will be pushed to
        Google Cloud Logging.

        Please note that any previous pending and running
        Rollouts and associated Operations will be automatically
        cancelled so that the latest Rollout will not be blocked
        by previous Rollouts.

        Only the 100 most recent (in any state) and the last 10
        successful (if not already part of the set of 100 most
        recent) rollouts are kept for each service. The rest
        will be deleted eventually.

        Operation<response: Rollout>

        Returns:
            Callable[[~.CreateServiceRolloutRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_service_rollout" not in self._stubs:
            self._stubs["create_service_rollout"] = self.grpc_channel.unary_unary(
                "/google.api.servicemanagement.v1.ServiceManager/CreateServiceRollout",
                request_serializer=servicemanager.CreateServiceRolloutRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_service_rollout"]

    @property
    def generate_config_report(
        self,
    ) -> Callable[
        [servicemanager.GenerateConfigReportRequest],
        Awaitable[servicemanager.GenerateConfigReportResponse],
    ]:
        r"""Return a callable for the generate config report method over gRPC.

        Generates and returns a report (errors, warnings and changes
        from existing configurations) associated with
        GenerateConfigReportRequest.new_value

        If GenerateConfigReportRequest.old_value is specified,
        GenerateConfigReportRequest will contain a single ChangeReport
        based on the comparison between
        GenerateConfigReportRequest.new_value and
        GenerateConfigReportRequest.old_value. If
        GenerateConfigReportRequest.old_value is not specified, this
        method will compare GenerateConfigReportRequest.new_value with
        the last pushed service configuration.

        Returns:
            Callable[[~.GenerateConfigReportRequest],
                    Awaitable[~.GenerateConfigReportResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "generate_config_report" not in self._stubs:
            self._stubs["generate_config_report"] = self.grpc_channel.unary_unary(
                "/google.api.servicemanagement.v1.ServiceManager/GenerateConfigReport",
                request_serializer=servicemanager.GenerateConfigReportRequest.serialize,
                response_deserializer=servicemanager.GenerateConfigReportResponse.deserialize,
            )
        return self._stubs["generate_config_report"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.list_services: gapic_v1.method_async.wrap_method(
                self.list_services,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_service: gapic_v1.method_async.wrap_method(
                self.get_service,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_service: gapic_v1.method_async.wrap_method(
                self.create_service,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_service: gapic_v1.method_async.wrap_method(
                self.delete_service,
                default_timeout=None,
                client_info=client_info,
            ),
            self.undelete_service: gapic_v1.method_async.wrap_method(
                self.undelete_service,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_service_configs: gapic_v1.method_async.wrap_method(
                self.list_service_configs,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_service_config: gapic_v1.method_async.wrap_method(
                self.get_service_config,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_service_config: gapic_v1.method_async.wrap_method(
                self.create_service_config,
                default_timeout=None,
                client_info=client_info,
            ),
            self.submit_config_source: gapic_v1.method_async.wrap_method(
                self.submit_config_source,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_service_rollouts: gapic_v1.method_async.wrap_method(
                self.list_service_rollouts,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_service_rollout: gapic_v1.method_async.wrap_method(
                self.get_service_rollout,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_service_rollout: gapic_v1.method_async.wrap_method(
                self.create_service_rollout,
                default_timeout=None,
                client_info=client_info,
            ),
            self.generate_config_report: gapic_v1.method_async.wrap_method(
                self.generate_config_report,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    def close(self):
        return self.grpc_channel.close()

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
    def set_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.SetIamPolicyRequest], policy_pb2.Policy]:
        r"""Return a callable for the set iam policy method over gRPC.
        Sets the IAM access control policy on the specified
        function. Replaces any existing policy.
        Returns:
            Callable[[~.SetIamPolicyRequest],
                    ~.Policy]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_iam_policy" not in self._stubs:
            self._stubs["set_iam_policy"] = self.grpc_channel.unary_unary(
                "/google.iam.v1.IAMPolicy/SetIamPolicy",
                request_serializer=iam_policy_pb2.SetIamPolicyRequest.SerializeToString,
                response_deserializer=policy_pb2.Policy.FromString,
            )
        return self._stubs["set_iam_policy"]

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.GetIamPolicyRequest], policy_pb2.Policy]:
        r"""Return a callable for the get iam policy method over gRPC.
        Gets the IAM access control policy for a function.
        Returns an empty policy if the function exists and does
        not have a policy set.
        Returns:
            Callable[[~.GetIamPolicyRequest],
                    ~.Policy]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_iam_policy" not in self._stubs:
            self._stubs["get_iam_policy"] = self.grpc_channel.unary_unary(
                "/google.iam.v1.IAMPolicy/GetIamPolicy",
                request_serializer=iam_policy_pb2.GetIamPolicyRequest.SerializeToString,
                response_deserializer=policy_pb2.Policy.FromString,
            )
        return self._stubs["get_iam_policy"]

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [iam_policy_pb2.TestIamPermissionsRequest],
        iam_policy_pb2.TestIamPermissionsResponse,
    ]:
        r"""Return a callable for the test iam permissions method over gRPC.
        Tests the specified permissions against the IAM access control
        policy for a function. If the function does not exist, this will
        return an empty set of permissions, not a NOT_FOUND error.
        Returns:
            Callable[[~.TestIamPermissionsRequest],
                    ~.TestIamPermissionsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "test_iam_permissions" not in self._stubs:
            self._stubs["test_iam_permissions"] = self.grpc_channel.unary_unary(
                "/google.iam.v1.IAMPolicy/TestIamPermissions",
                request_serializer=iam_policy_pb2.TestIamPermissionsRequest.SerializeToString,
                response_deserializer=iam_policy_pb2.TestIamPermissionsResponse.FromString,
            )
        return self._stubs["test_iam_permissions"]


__all__ = ("ServiceManagerGrpcAsyncIOTransport",)
