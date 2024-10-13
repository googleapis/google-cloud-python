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
import inspect
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, grpc_helpers_async
from google.api_core import retry_async as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.servicedirectory_v1beta1.types import endpoint as gcs_endpoint
from google.cloud.servicedirectory_v1beta1.types import namespace as gcs_namespace
from google.cloud.servicedirectory_v1beta1.types import endpoint
from google.cloud.servicedirectory_v1beta1.types import namespace
from google.cloud.servicedirectory_v1beta1.types import registration_service
from google.cloud.servicedirectory_v1beta1.types import service
from google.cloud.servicedirectory_v1beta1.types import service as gcs_service

from .base import DEFAULT_CLIENT_INFO, RegistrationServiceTransport
from .grpc import RegistrationServiceGrpcTransport


class RegistrationServiceGrpcAsyncIOTransport(RegistrationServiceTransport):
    """gRPC AsyncIO backend transport for RegistrationService.

    Service Directory API for registering services. It defines the
    following resource model:

    -  The API has a collection of
       [Namespace][google.cloud.servicedirectory.v1beta1.Namespace]
       resources, named ``projects/*/locations/*/namespaces/*``.

    -  Each Namespace has a collection of
       [Service][google.cloud.servicedirectory.v1beta1.Service]
       resources, named
       ``projects/*/locations/*/namespaces/*/services/*``.

    -  Each Service has a collection of
       [Endpoint][google.cloud.servicedirectory.v1beta1.Endpoint]
       resources, named
       ``projects/*/locations/*/namespaces/*/services/*/endpoints/*``.

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
        host: str = "servicedirectory.googleapis.com",
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
        host: str = "servicedirectory.googleapis.com",
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
                 The hostname to connect to (default: 'servicedirectory.googleapis.com').
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
        self._wrap_with_kind = (
            "kind" in inspect.signature(gapic_v1.method_async.wrap_method).parameters
        )
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
    def create_namespace(
        self,
    ) -> Callable[
        [registration_service.CreateNamespaceRequest],
        Awaitable[gcs_namespace.Namespace],
    ]:
        r"""Return a callable for the create namespace method over gRPC.

        Creates a namespace, and returns the new namespace.

        Returns:
            Callable[[~.CreateNamespaceRequest],
                    Awaitable[~.Namespace]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_namespace" not in self._stubs:
            self._stubs["create_namespace"] = self.grpc_channel.unary_unary(
                "/google.cloud.servicedirectory.v1beta1.RegistrationService/CreateNamespace",
                request_serializer=registration_service.CreateNamespaceRequest.serialize,
                response_deserializer=gcs_namespace.Namespace.deserialize,
            )
        return self._stubs["create_namespace"]

    @property
    def list_namespaces(
        self,
    ) -> Callable[
        [registration_service.ListNamespacesRequest],
        Awaitable[registration_service.ListNamespacesResponse],
    ]:
        r"""Return a callable for the list namespaces method over gRPC.

        Lists all namespaces.

        Returns:
            Callable[[~.ListNamespacesRequest],
                    Awaitable[~.ListNamespacesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_namespaces" not in self._stubs:
            self._stubs["list_namespaces"] = self.grpc_channel.unary_unary(
                "/google.cloud.servicedirectory.v1beta1.RegistrationService/ListNamespaces",
                request_serializer=registration_service.ListNamespacesRequest.serialize,
                response_deserializer=registration_service.ListNamespacesResponse.deserialize,
            )
        return self._stubs["list_namespaces"]

    @property
    def get_namespace(
        self,
    ) -> Callable[
        [registration_service.GetNamespaceRequest], Awaitable[namespace.Namespace]
    ]:
        r"""Return a callable for the get namespace method over gRPC.

        Gets a namespace.

        Returns:
            Callable[[~.GetNamespaceRequest],
                    Awaitable[~.Namespace]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_namespace" not in self._stubs:
            self._stubs["get_namespace"] = self.grpc_channel.unary_unary(
                "/google.cloud.servicedirectory.v1beta1.RegistrationService/GetNamespace",
                request_serializer=registration_service.GetNamespaceRequest.serialize,
                response_deserializer=namespace.Namespace.deserialize,
            )
        return self._stubs["get_namespace"]

    @property
    def update_namespace(
        self,
    ) -> Callable[
        [registration_service.UpdateNamespaceRequest],
        Awaitable[gcs_namespace.Namespace],
    ]:
        r"""Return a callable for the update namespace method over gRPC.

        Updates a namespace.

        Returns:
            Callable[[~.UpdateNamespaceRequest],
                    Awaitable[~.Namespace]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_namespace" not in self._stubs:
            self._stubs["update_namespace"] = self.grpc_channel.unary_unary(
                "/google.cloud.servicedirectory.v1beta1.RegistrationService/UpdateNamespace",
                request_serializer=registration_service.UpdateNamespaceRequest.serialize,
                response_deserializer=gcs_namespace.Namespace.deserialize,
            )
        return self._stubs["update_namespace"]

    @property
    def delete_namespace(
        self,
    ) -> Callable[
        [registration_service.DeleteNamespaceRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the delete namespace method over gRPC.

        Deletes a namespace. This also deletes all services
        and endpoints in the namespace.

        Returns:
            Callable[[~.DeleteNamespaceRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_namespace" not in self._stubs:
            self._stubs["delete_namespace"] = self.grpc_channel.unary_unary(
                "/google.cloud.servicedirectory.v1beta1.RegistrationService/DeleteNamespace",
                request_serializer=registration_service.DeleteNamespaceRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_namespace"]

    @property
    def create_service(
        self,
    ) -> Callable[
        [registration_service.CreateServiceRequest], Awaitable[gcs_service.Service]
    ]:
        r"""Return a callable for the create service method over gRPC.

        Creates a service, and returns the new service.

        Returns:
            Callable[[~.CreateServiceRequest],
                    Awaitable[~.Service]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_service" not in self._stubs:
            self._stubs["create_service"] = self.grpc_channel.unary_unary(
                "/google.cloud.servicedirectory.v1beta1.RegistrationService/CreateService",
                request_serializer=registration_service.CreateServiceRequest.serialize,
                response_deserializer=gcs_service.Service.deserialize,
            )
        return self._stubs["create_service"]

    @property
    def list_services(
        self,
    ) -> Callable[
        [registration_service.ListServicesRequest],
        Awaitable[registration_service.ListServicesResponse],
    ]:
        r"""Return a callable for the list services method over gRPC.

        Lists all services belonging to a namespace.

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
                "/google.cloud.servicedirectory.v1beta1.RegistrationService/ListServices",
                request_serializer=registration_service.ListServicesRequest.serialize,
                response_deserializer=registration_service.ListServicesResponse.deserialize,
            )
        return self._stubs["list_services"]

    @property
    def get_service(
        self,
    ) -> Callable[[registration_service.GetServiceRequest], Awaitable[service.Service]]:
        r"""Return a callable for the get service method over gRPC.

        Gets a service.

        Returns:
            Callable[[~.GetServiceRequest],
                    Awaitable[~.Service]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_service" not in self._stubs:
            self._stubs["get_service"] = self.grpc_channel.unary_unary(
                "/google.cloud.servicedirectory.v1beta1.RegistrationService/GetService",
                request_serializer=registration_service.GetServiceRequest.serialize,
                response_deserializer=service.Service.deserialize,
            )
        return self._stubs["get_service"]

    @property
    def update_service(
        self,
    ) -> Callable[
        [registration_service.UpdateServiceRequest], Awaitable[gcs_service.Service]
    ]:
        r"""Return a callable for the update service method over gRPC.

        Updates a service.

        Returns:
            Callable[[~.UpdateServiceRequest],
                    Awaitable[~.Service]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_service" not in self._stubs:
            self._stubs["update_service"] = self.grpc_channel.unary_unary(
                "/google.cloud.servicedirectory.v1beta1.RegistrationService/UpdateService",
                request_serializer=registration_service.UpdateServiceRequest.serialize,
                response_deserializer=gcs_service.Service.deserialize,
            )
        return self._stubs["update_service"]

    @property
    def delete_service(
        self,
    ) -> Callable[
        [registration_service.DeleteServiceRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the delete service method over gRPC.

        Deletes a service. This also deletes all endpoints
        associated with the service.

        Returns:
            Callable[[~.DeleteServiceRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_service" not in self._stubs:
            self._stubs["delete_service"] = self.grpc_channel.unary_unary(
                "/google.cloud.servicedirectory.v1beta1.RegistrationService/DeleteService",
                request_serializer=registration_service.DeleteServiceRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_service"]

    @property
    def create_endpoint(
        self,
    ) -> Callable[
        [registration_service.CreateEndpointRequest], Awaitable[gcs_endpoint.Endpoint]
    ]:
        r"""Return a callable for the create endpoint method over gRPC.

        Creates an endpoint, and returns the new endpoint.

        Returns:
            Callable[[~.CreateEndpointRequest],
                    Awaitable[~.Endpoint]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_endpoint" not in self._stubs:
            self._stubs["create_endpoint"] = self.grpc_channel.unary_unary(
                "/google.cloud.servicedirectory.v1beta1.RegistrationService/CreateEndpoint",
                request_serializer=registration_service.CreateEndpointRequest.serialize,
                response_deserializer=gcs_endpoint.Endpoint.deserialize,
            )
        return self._stubs["create_endpoint"]

    @property
    def list_endpoints(
        self,
    ) -> Callable[
        [registration_service.ListEndpointsRequest],
        Awaitable[registration_service.ListEndpointsResponse],
    ]:
        r"""Return a callable for the list endpoints method over gRPC.

        Lists all endpoints.

        Returns:
            Callable[[~.ListEndpointsRequest],
                    Awaitable[~.ListEndpointsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_endpoints" not in self._stubs:
            self._stubs["list_endpoints"] = self.grpc_channel.unary_unary(
                "/google.cloud.servicedirectory.v1beta1.RegistrationService/ListEndpoints",
                request_serializer=registration_service.ListEndpointsRequest.serialize,
                response_deserializer=registration_service.ListEndpointsResponse.deserialize,
            )
        return self._stubs["list_endpoints"]

    @property
    def get_endpoint(
        self,
    ) -> Callable[
        [registration_service.GetEndpointRequest], Awaitable[endpoint.Endpoint]
    ]:
        r"""Return a callable for the get endpoint method over gRPC.

        Gets an endpoint.

        Returns:
            Callable[[~.GetEndpointRequest],
                    Awaitable[~.Endpoint]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_endpoint" not in self._stubs:
            self._stubs["get_endpoint"] = self.grpc_channel.unary_unary(
                "/google.cloud.servicedirectory.v1beta1.RegistrationService/GetEndpoint",
                request_serializer=registration_service.GetEndpointRequest.serialize,
                response_deserializer=endpoint.Endpoint.deserialize,
            )
        return self._stubs["get_endpoint"]

    @property
    def update_endpoint(
        self,
    ) -> Callable[
        [registration_service.UpdateEndpointRequest], Awaitable[gcs_endpoint.Endpoint]
    ]:
        r"""Return a callable for the update endpoint method over gRPC.

        Updates an endpoint.

        Returns:
            Callable[[~.UpdateEndpointRequest],
                    Awaitable[~.Endpoint]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_endpoint" not in self._stubs:
            self._stubs["update_endpoint"] = self.grpc_channel.unary_unary(
                "/google.cloud.servicedirectory.v1beta1.RegistrationService/UpdateEndpoint",
                request_serializer=registration_service.UpdateEndpointRequest.serialize,
                response_deserializer=gcs_endpoint.Endpoint.deserialize,
            )
        return self._stubs["update_endpoint"]

    @property
    def delete_endpoint(
        self,
    ) -> Callable[
        [registration_service.DeleteEndpointRequest], Awaitable[empty_pb2.Empty]
    ]:
        r"""Return a callable for the delete endpoint method over gRPC.

        Deletes an endpoint.

        Returns:
            Callable[[~.DeleteEndpointRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_endpoint" not in self._stubs:
            self._stubs["delete_endpoint"] = self.grpc_channel.unary_unary(
                "/google.cloud.servicedirectory.v1beta1.RegistrationService/DeleteEndpoint",
                request_serializer=registration_service.DeleteEndpointRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_endpoint"]

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.GetIamPolicyRequest], Awaitable[policy_pb2.Policy]]:
        r"""Return a callable for the get iam policy method over gRPC.

        Gets the IAM Policy for a resource

        Returns:
            Callable[[~.GetIamPolicyRequest],
                    Awaitable[~.Policy]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_iam_policy" not in self._stubs:
            self._stubs["get_iam_policy"] = self.grpc_channel.unary_unary(
                "/google.cloud.servicedirectory.v1beta1.RegistrationService/GetIamPolicy",
                request_serializer=iam_policy_pb2.GetIamPolicyRequest.SerializeToString,
                response_deserializer=policy_pb2.Policy.FromString,
            )
        return self._stubs["get_iam_policy"]

    @property
    def set_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.SetIamPolicyRequest], Awaitable[policy_pb2.Policy]]:
        r"""Return a callable for the set iam policy method over gRPC.

        Sets the IAM Policy for a resource

        Returns:
            Callable[[~.SetIamPolicyRequest],
                    Awaitable[~.Policy]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_iam_policy" not in self._stubs:
            self._stubs["set_iam_policy"] = self.grpc_channel.unary_unary(
                "/google.cloud.servicedirectory.v1beta1.RegistrationService/SetIamPolicy",
                request_serializer=iam_policy_pb2.SetIamPolicyRequest.SerializeToString,
                response_deserializer=policy_pb2.Policy.FromString,
            )
        return self._stubs["set_iam_policy"]

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [iam_policy_pb2.TestIamPermissionsRequest],
        Awaitable[iam_policy_pb2.TestIamPermissionsResponse],
    ]:
        r"""Return a callable for the test iam permissions method over gRPC.

        Tests IAM permissions for a resource (namespace,
        service  or service workload only).

        Returns:
            Callable[[~.TestIamPermissionsRequest],
                    Awaitable[~.TestIamPermissionsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "test_iam_permissions" not in self._stubs:
            self._stubs["test_iam_permissions"] = self.grpc_channel.unary_unary(
                "/google.cloud.servicedirectory.v1beta1.RegistrationService/TestIamPermissions",
                request_serializer=iam_policy_pb2.TestIamPermissionsRequest.SerializeToString,
                response_deserializer=iam_policy_pb2.TestIamPermissionsResponse.FromString,
            )
        return self._stubs["test_iam_permissions"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.create_namespace: self._wrap_method(
                self.create_namespace,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_namespaces: self._wrap_method(
                self.list_namespaces,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_namespace: self._wrap_method(
                self.get_namespace,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_namespace: self._wrap_method(
                self.update_namespace,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_namespace: self._wrap_method(
                self.delete_namespace,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_service: self._wrap_method(
                self.create_service,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_services: self._wrap_method(
                self.list_services,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_service: self._wrap_method(
                self.get_service,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_service: self._wrap_method(
                self.update_service,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_service: self._wrap_method(
                self.delete_service,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_endpoint: self._wrap_method(
                self.create_endpoint,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_endpoints: self._wrap_method(
                self.list_endpoints,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_endpoint: self._wrap_method(
                self.get_endpoint,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_endpoint: self._wrap_method(
                self.update_endpoint,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_endpoint: self._wrap_method(
                self.delete_endpoint,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_iam_policy: self._wrap_method(
                self.get_iam_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.set_iam_policy: self._wrap_method(
                self.set_iam_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.test_iam_permissions: self._wrap_method(
                self.test_iam_permissions,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_location: self._wrap_method(
                self.get_location,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_locations: self._wrap_method(
                self.list_locations,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    def _wrap_method(self, func, *args, **kwargs):
        if self._wrap_with_kind:  # pragma: NO COVER
            kwargs["kind"] = self.kind
        return gapic_v1.method_async.wrap_method(func, *args, **kwargs)

    def close(self):
        return self.grpc_channel.close()

    @property
    def kind(self) -> str:
        return "grpc_asyncio"

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


__all__ = ("RegistrationServiceGrpcAsyncIOTransport",)
