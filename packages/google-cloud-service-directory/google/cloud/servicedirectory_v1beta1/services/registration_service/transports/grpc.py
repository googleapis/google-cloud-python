# -*- coding: utf-8 -*-

# Copyright (C) 2019  Google LLC
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

from typing import Callable, Dict

from google.api_core import grpc_helpers  # type: ignore
from google.auth import credentials  # type: ignore

import grpc  # type: ignore

from google.cloud.servicedirectory_v1beta1.types import endpoint
from google.cloud.servicedirectory_v1beta1.types import endpoint as gcs_endpoint
from google.cloud.servicedirectory_v1beta1.types import namespace
from google.cloud.servicedirectory_v1beta1.types import namespace as gcs_namespace
from google.cloud.servicedirectory_v1beta1.types import registration_service
from google.cloud.servicedirectory_v1beta1.types import service
from google.cloud.servicedirectory_v1beta1.types import service as gcs_service
from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore

from .base import RegistrationServiceTransport


class RegistrationServiceGrpcTransport(RegistrationServiceTransport):
    """gRPC backend transport for RegistrationService.

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

    def __init__(
        self,
        *,
        host: str = "servicedirectory.googleapis.com",
        credentials: credentials.Credentials = None,
        channel: grpc.Channel = None
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
        """
        # Sanity check: Ensure that channel and credentials are not both
        # provided.
        if channel:
            credentials = False

        # Run the base constructor.
        super().__init__(host=host, credentials=credentials)
        self._stubs = {}  # type: Dict[str, Callable]

        # If a channel was explicitly provided, set it.
        if channel:
            self._grpc_channel = channel

    @classmethod
    def create_channel(
        cls,
        host: str = "servicedirectory.googleapis.com",
        credentials: credentials.Credentials = None,
        **kwargs
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            address (Optionsl[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return grpc_helpers.create_channel(
            host, credentials=credentials, scopes=cls.AUTH_SCOPES, **kwargs
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Sanity check: Only create a new channel if we do not already
        # have one.
        if not hasattr(self, "_grpc_channel"):
            self._grpc_channel = self.create_channel(
                self._host, credentials=self._credentials
            )

        # Return the channel from cache.
        return self._grpc_channel

    @property
    def create_namespace(
        self
    ) -> Callable[
        [registration_service.CreateNamespaceRequest], gcs_namespace.Namespace
    ]:
        r"""Return a callable for the create namespace method over gRPC.

        Creates a namespace, and returns the new Namespace.

        Returns:
            Callable[[~.CreateNamespaceRequest],
                    ~.Namespace]:
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
        self
    ) -> Callable[
        [registration_service.ListNamespacesRequest],
        registration_service.ListNamespacesResponse,
    ]:
        r"""Return a callable for the list namespaces method over gRPC.

        Lists all namespaces.

        Returns:
            Callable[[~.ListNamespacesRequest],
                    ~.ListNamespacesResponse]:
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
        self
    ) -> Callable[[registration_service.GetNamespaceRequest], namespace.Namespace]:
        r"""Return a callable for the get namespace method over gRPC.

        Gets a namespace.

        Returns:
            Callable[[~.GetNamespaceRequest],
                    ~.Namespace]:
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
        self
    ) -> Callable[
        [registration_service.UpdateNamespaceRequest], gcs_namespace.Namespace
    ]:
        r"""Return a callable for the update namespace method over gRPC.

        Updates a namespace.

        Returns:
            Callable[[~.UpdateNamespaceRequest],
                    ~.Namespace]:
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
        self
    ) -> Callable[[registration_service.DeleteNamespaceRequest], empty.Empty]:
        r"""Return a callable for the delete namespace method over gRPC.

        Deletes a namespace. This also deletes all services
        and endpoints in the namespace.

        Returns:
            Callable[[~.DeleteNamespaceRequest],
                    ~.Empty]:
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
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["delete_namespace"]

    @property
    def create_service(
        self
    ) -> Callable[[registration_service.CreateServiceRequest], gcs_service.Service]:
        r"""Return a callable for the create service method over gRPC.

        Creates a service, and returns the new Service.

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
                "/google.cloud.servicedirectory.v1beta1.RegistrationService/CreateService",
                request_serializer=registration_service.CreateServiceRequest.serialize,
                response_deserializer=gcs_service.Service.deserialize,
            )
        return self._stubs["create_service"]

    @property
    def list_services(
        self
    ) -> Callable[
        [registration_service.ListServicesRequest],
        registration_service.ListServicesResponse,
    ]:
        r"""Return a callable for the list services method over gRPC.

        Lists all services belonging to a namespace.

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
                "/google.cloud.servicedirectory.v1beta1.RegistrationService/ListServices",
                request_serializer=registration_service.ListServicesRequest.serialize,
                response_deserializer=registration_service.ListServicesResponse.deserialize,
            )
        return self._stubs["list_services"]

    @property
    def get_service(
        self
    ) -> Callable[[registration_service.GetServiceRequest], service.Service]:
        r"""Return a callable for the get service method over gRPC.

        Gets a service.

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
                "/google.cloud.servicedirectory.v1beta1.RegistrationService/GetService",
                request_serializer=registration_service.GetServiceRequest.serialize,
                response_deserializer=service.Service.deserialize,
            )
        return self._stubs["get_service"]

    @property
    def update_service(
        self
    ) -> Callable[[registration_service.UpdateServiceRequest], gcs_service.Service]:
        r"""Return a callable for the update service method over gRPC.

        Updates a service.

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
                "/google.cloud.servicedirectory.v1beta1.RegistrationService/UpdateService",
                request_serializer=registration_service.UpdateServiceRequest.serialize,
                response_deserializer=gcs_service.Service.deserialize,
            )
        return self._stubs["update_service"]

    @property
    def delete_service(
        self
    ) -> Callable[[registration_service.DeleteServiceRequest], empty.Empty]:
        r"""Return a callable for the delete service method over gRPC.

        Deletes a service. This also deletes all endpoints
        associated with the service.

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
                "/google.cloud.servicedirectory.v1beta1.RegistrationService/DeleteService",
                request_serializer=registration_service.DeleteServiceRequest.serialize,
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["delete_service"]

    @property
    def create_endpoint(
        self
    ) -> Callable[[registration_service.CreateEndpointRequest], gcs_endpoint.Endpoint]:
        r"""Return a callable for the create endpoint method over gRPC.

        Creates a endpoint, and returns the new Endpoint.

        Returns:
            Callable[[~.CreateEndpointRequest],
                    ~.Endpoint]:
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
        self
    ) -> Callable[
        [registration_service.ListEndpointsRequest],
        registration_service.ListEndpointsResponse,
    ]:
        r"""Return a callable for the list endpoints method over gRPC.

        Lists all endpoints.

        Returns:
            Callable[[~.ListEndpointsRequest],
                    ~.ListEndpointsResponse]:
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
        self
    ) -> Callable[[registration_service.GetEndpointRequest], endpoint.Endpoint]:
        r"""Return a callable for the get endpoint method over gRPC.

        Gets a endpoint.

        Returns:
            Callable[[~.GetEndpointRequest],
                    ~.Endpoint]:
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
        self
    ) -> Callable[[registration_service.UpdateEndpointRequest], gcs_endpoint.Endpoint]:
        r"""Return a callable for the update endpoint method over gRPC.

        Updates a endpoint.

        Returns:
            Callable[[~.UpdateEndpointRequest],
                    ~.Endpoint]:
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
        self
    ) -> Callable[[registration_service.DeleteEndpointRequest], empty.Empty]:
        r"""Return a callable for the delete endpoint method over gRPC.

        Deletes a endpoint.

        Returns:
            Callable[[~.DeleteEndpointRequest],
                    ~.Empty]:
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
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["delete_endpoint"]

    @property
    def get_iam_policy(
        self
    ) -> Callable[[iam_policy.GetIamPolicyRequest], policy.Policy]:
        r"""Return a callable for the get iam policy method over gRPC.

        Gets the IAM Policy for a resource (namespace or
        service only).

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
                "/google.cloud.servicedirectory.v1beta1.RegistrationService/GetIamPolicy",
                request_serializer=iam_policy.GetIamPolicyRequest.SerializeToString,
                response_deserializer=policy.Policy.FromString,
            )
        return self._stubs["get_iam_policy"]

    @property
    def set_iam_policy(
        self
    ) -> Callable[[iam_policy.SetIamPolicyRequest], policy.Policy]:
        r"""Return a callable for the set iam policy method over gRPC.

        Sets the IAM Policy for a resource (namespace or
        service only).

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
                "/google.cloud.servicedirectory.v1beta1.RegistrationService/SetIamPolicy",
                request_serializer=iam_policy.SetIamPolicyRequest.SerializeToString,
                response_deserializer=policy.Policy.FromString,
            )
        return self._stubs["set_iam_policy"]

    @property
    def test_iam_permissions(
        self
    ) -> Callable[
        [iam_policy.TestIamPermissionsRequest], iam_policy.TestIamPermissionsResponse
    ]:
        r"""Return a callable for the test iam permissions method over gRPC.

        Tests IAM permissions for a resource (namespace or
        service only).

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
                "/google.cloud.servicedirectory.v1beta1.RegistrationService/TestIamPermissions",
                request_serializer=iam_policy.TestIamPermissionsRequest.SerializeToString,
                response_deserializer=iam_policy.TestIamPermissionsResponse.FromString,
            )
        return self._stubs["test_iam_permissions"]


__all__ = ("RegistrationServiceGrpcTransport",)
