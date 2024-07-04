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
import abc
from typing import Awaitable, Callable, Dict, Optional, Sequence, Union

import google.api_core
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, operations_v1
from google.api_core import retry as retries
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.network_services_v1 import gapic_version as package_version
from google.cloud.network_services_v1.types import (
    endpoint_policy as gcn_endpoint_policy,
)
from google.cloud.network_services_v1.types import (
    service_binding as gcn_service_binding,
)
from google.cloud.network_services_v1.types import endpoint_policy
from google.cloud.network_services_v1.types import gateway
from google.cloud.network_services_v1.types import gateway as gcn_gateway
from google.cloud.network_services_v1.types import grpc_route
from google.cloud.network_services_v1.types import grpc_route as gcn_grpc_route
from google.cloud.network_services_v1.types import http_route
from google.cloud.network_services_v1.types import http_route as gcn_http_route
from google.cloud.network_services_v1.types import mesh
from google.cloud.network_services_v1.types import mesh as gcn_mesh
from google.cloud.network_services_v1.types import service_binding
from google.cloud.network_services_v1.types import tcp_route
from google.cloud.network_services_v1.types import tcp_route as gcn_tcp_route
from google.cloud.network_services_v1.types import tls_route
from google.cloud.network_services_v1.types import tls_route as gcn_tls_route

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


class NetworkServicesTransport(abc.ABC):
    """Abstract transport class for NetworkServices."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    DEFAULT_HOST: str = "networkservices.googleapis.com"

    def __init__(
        self,
        *,
        host: str = DEFAULT_HOST,
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        api_audience: Optional[str] = None,
        **kwargs,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'networkservices.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
        """

        scopes_kwargs = {"scopes": scopes, "default_scopes": self.AUTH_SCOPES}

        # Save the scopes.
        self._scopes = scopes
        if not hasattr(self, "_ignore_credentials"):
            self._ignore_credentials: bool = False

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise core_exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = google.auth.load_credentials_from_file(
                credentials_file, **scopes_kwargs, quota_project_id=quota_project_id
            )
        elif credentials is None and not self._ignore_credentials:
            credentials, _ = google.auth.default(
                **scopes_kwargs, quota_project_id=quota_project_id
            )
            # Don't apply audience if the credentials file passed from user.
            if hasattr(credentials, "with_gdch_audience"):
                credentials = credentials.with_gdch_audience(
                    api_audience if api_audience else host
                )

        # If the credentials are service account credentials, then always try to use self signed JWT.
        if (
            always_use_jwt_access
            and isinstance(credentials, service_account.Credentials)
            and hasattr(service_account.Credentials, "with_always_use_jwt_access")
        ):
            credentials = credentials.with_always_use_jwt_access(True)

        # Save the credentials.
        self._credentials = credentials

        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

    @property
    def host(self):
        return self._host

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.list_endpoint_policies: gapic_v1.method.wrap_method(
                self.list_endpoint_policies,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_endpoint_policy: gapic_v1.method.wrap_method(
                self.get_endpoint_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_endpoint_policy: gapic_v1.method.wrap_method(
                self.create_endpoint_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_endpoint_policy: gapic_v1.method.wrap_method(
                self.update_endpoint_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_endpoint_policy: gapic_v1.method.wrap_method(
                self.delete_endpoint_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_gateways: gapic_v1.method.wrap_method(
                self.list_gateways,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_gateway: gapic_v1.method.wrap_method(
                self.get_gateway,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_gateway: gapic_v1.method.wrap_method(
                self.create_gateway,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_gateway: gapic_v1.method.wrap_method(
                self.update_gateway,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_gateway: gapic_v1.method.wrap_method(
                self.delete_gateway,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_grpc_routes: gapic_v1.method.wrap_method(
                self.list_grpc_routes,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_grpc_route: gapic_v1.method.wrap_method(
                self.get_grpc_route,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_grpc_route: gapic_v1.method.wrap_method(
                self.create_grpc_route,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_grpc_route: gapic_v1.method.wrap_method(
                self.update_grpc_route,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_grpc_route: gapic_v1.method.wrap_method(
                self.delete_grpc_route,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_http_routes: gapic_v1.method.wrap_method(
                self.list_http_routes,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_http_route: gapic_v1.method.wrap_method(
                self.get_http_route,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_http_route: gapic_v1.method.wrap_method(
                self.create_http_route,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_http_route: gapic_v1.method.wrap_method(
                self.update_http_route,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_http_route: gapic_v1.method.wrap_method(
                self.delete_http_route,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_tcp_routes: gapic_v1.method.wrap_method(
                self.list_tcp_routes,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_tcp_route: gapic_v1.method.wrap_method(
                self.get_tcp_route,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_tcp_route: gapic_v1.method.wrap_method(
                self.create_tcp_route,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_tcp_route: gapic_v1.method.wrap_method(
                self.update_tcp_route,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_tcp_route: gapic_v1.method.wrap_method(
                self.delete_tcp_route,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_tls_routes: gapic_v1.method.wrap_method(
                self.list_tls_routes,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_tls_route: gapic_v1.method.wrap_method(
                self.get_tls_route,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_tls_route: gapic_v1.method.wrap_method(
                self.create_tls_route,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_tls_route: gapic_v1.method.wrap_method(
                self.update_tls_route,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_tls_route: gapic_v1.method.wrap_method(
                self.delete_tls_route,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_service_bindings: gapic_v1.method.wrap_method(
                self.list_service_bindings,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_service_binding: gapic_v1.method.wrap_method(
                self.get_service_binding,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_service_binding: gapic_v1.method.wrap_method(
                self.create_service_binding,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_service_binding: gapic_v1.method.wrap_method(
                self.delete_service_binding,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_meshes: gapic_v1.method.wrap_method(
                self.list_meshes,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_mesh: gapic_v1.method.wrap_method(
                self.get_mesh,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_mesh: gapic_v1.method.wrap_method(
                self.create_mesh,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_mesh: gapic_v1.method.wrap_method(
                self.update_mesh,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_mesh: gapic_v1.method.wrap_method(
                self.delete_mesh,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    def close(self):
        """Closes resources associated with the transport.

        .. warning::
             Only call this method if the transport is NOT shared
             with other clients - this may cause errors in other clients!
        """
        raise NotImplementedError()

    @property
    def operations_client(self):
        """Return the client designed to process long-running operations."""
        raise NotImplementedError()

    @property
    def list_endpoint_policies(
        self,
    ) -> Callable[
        [endpoint_policy.ListEndpointPoliciesRequest],
        Union[
            endpoint_policy.ListEndpointPoliciesResponse,
            Awaitable[endpoint_policy.ListEndpointPoliciesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_endpoint_policy(
        self,
    ) -> Callable[
        [endpoint_policy.GetEndpointPolicyRequest],
        Union[
            endpoint_policy.EndpointPolicy, Awaitable[endpoint_policy.EndpointPolicy]
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_endpoint_policy(
        self,
    ) -> Callable[
        [gcn_endpoint_policy.CreateEndpointPolicyRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_endpoint_policy(
        self,
    ) -> Callable[
        [gcn_endpoint_policy.UpdateEndpointPolicyRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_endpoint_policy(
        self,
    ) -> Callable[
        [endpoint_policy.DeleteEndpointPolicyRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_gateways(
        self,
    ) -> Callable[
        [gateway.ListGatewaysRequest],
        Union[gateway.ListGatewaysResponse, Awaitable[gateway.ListGatewaysResponse]],
    ]:
        raise NotImplementedError()

    @property
    def get_gateway(
        self,
    ) -> Callable[
        [gateway.GetGatewayRequest], Union[gateway.Gateway, Awaitable[gateway.Gateway]]
    ]:
        raise NotImplementedError()

    @property
    def create_gateway(
        self,
    ) -> Callable[
        [gcn_gateway.CreateGatewayRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_gateway(
        self,
    ) -> Callable[
        [gcn_gateway.UpdateGatewayRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_gateway(
        self,
    ) -> Callable[
        [gateway.DeleteGatewayRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_grpc_routes(
        self,
    ) -> Callable[
        [grpc_route.ListGrpcRoutesRequest],
        Union[
            grpc_route.ListGrpcRoutesResponse,
            Awaitable[grpc_route.ListGrpcRoutesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_grpc_route(
        self,
    ) -> Callable[
        [grpc_route.GetGrpcRouteRequest],
        Union[grpc_route.GrpcRoute, Awaitable[grpc_route.GrpcRoute]],
    ]:
        raise NotImplementedError()

    @property
    def create_grpc_route(
        self,
    ) -> Callable[
        [gcn_grpc_route.CreateGrpcRouteRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_grpc_route(
        self,
    ) -> Callable[
        [gcn_grpc_route.UpdateGrpcRouteRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_grpc_route(
        self,
    ) -> Callable[
        [grpc_route.DeleteGrpcRouteRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_http_routes(
        self,
    ) -> Callable[
        [http_route.ListHttpRoutesRequest],
        Union[
            http_route.ListHttpRoutesResponse,
            Awaitable[http_route.ListHttpRoutesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_http_route(
        self,
    ) -> Callable[
        [http_route.GetHttpRouteRequest],
        Union[http_route.HttpRoute, Awaitable[http_route.HttpRoute]],
    ]:
        raise NotImplementedError()

    @property
    def create_http_route(
        self,
    ) -> Callable[
        [gcn_http_route.CreateHttpRouteRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_http_route(
        self,
    ) -> Callable[
        [gcn_http_route.UpdateHttpRouteRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_http_route(
        self,
    ) -> Callable[
        [http_route.DeleteHttpRouteRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_tcp_routes(
        self,
    ) -> Callable[
        [tcp_route.ListTcpRoutesRequest],
        Union[
            tcp_route.ListTcpRoutesResponse, Awaitable[tcp_route.ListTcpRoutesResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_tcp_route(
        self,
    ) -> Callable[
        [tcp_route.GetTcpRouteRequest],
        Union[tcp_route.TcpRoute, Awaitable[tcp_route.TcpRoute]],
    ]:
        raise NotImplementedError()

    @property
    def create_tcp_route(
        self,
    ) -> Callable[
        [gcn_tcp_route.CreateTcpRouteRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_tcp_route(
        self,
    ) -> Callable[
        [gcn_tcp_route.UpdateTcpRouteRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_tcp_route(
        self,
    ) -> Callable[
        [tcp_route.DeleteTcpRouteRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_tls_routes(
        self,
    ) -> Callable[
        [tls_route.ListTlsRoutesRequest],
        Union[
            tls_route.ListTlsRoutesResponse, Awaitable[tls_route.ListTlsRoutesResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_tls_route(
        self,
    ) -> Callable[
        [tls_route.GetTlsRouteRequest],
        Union[tls_route.TlsRoute, Awaitable[tls_route.TlsRoute]],
    ]:
        raise NotImplementedError()

    @property
    def create_tls_route(
        self,
    ) -> Callable[
        [gcn_tls_route.CreateTlsRouteRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_tls_route(
        self,
    ) -> Callable[
        [gcn_tls_route.UpdateTlsRouteRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_tls_route(
        self,
    ) -> Callable[
        [tls_route.DeleteTlsRouteRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_service_bindings(
        self,
    ) -> Callable[
        [service_binding.ListServiceBindingsRequest],
        Union[
            service_binding.ListServiceBindingsResponse,
            Awaitable[service_binding.ListServiceBindingsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_service_binding(
        self,
    ) -> Callable[
        [service_binding.GetServiceBindingRequest],
        Union[
            service_binding.ServiceBinding, Awaitable[service_binding.ServiceBinding]
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_service_binding(
        self,
    ) -> Callable[
        [gcn_service_binding.CreateServiceBindingRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_service_binding(
        self,
    ) -> Callable[
        [service_binding.DeleteServiceBindingRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_meshes(
        self,
    ) -> Callable[
        [mesh.ListMeshesRequest],
        Union[mesh.ListMeshesResponse, Awaitable[mesh.ListMeshesResponse]],
    ]:
        raise NotImplementedError()

    @property
    def get_mesh(
        self,
    ) -> Callable[[mesh.GetMeshRequest], Union[mesh.Mesh, Awaitable[mesh.Mesh]]]:
        raise NotImplementedError()

    @property
    def create_mesh(
        self,
    ) -> Callable[
        [gcn_mesh.CreateMeshRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_mesh(
        self,
    ) -> Callable[
        [gcn_mesh.UpdateMeshRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_mesh(
        self,
    ) -> Callable[
        [mesh.DeleteMeshRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_operations(
        self,
    ) -> Callable[
        [operations_pb2.ListOperationsRequest],
        Union[
            operations_pb2.ListOperationsResponse,
            Awaitable[operations_pb2.ListOperationsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_operation(
        self,
    ) -> Callable[
        [operations_pb2.GetOperationRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def cancel_operation(
        self,
    ) -> Callable[[operations_pb2.CancelOperationRequest], None,]:
        raise NotImplementedError()

    @property
    def delete_operation(
        self,
    ) -> Callable[[operations_pb2.DeleteOperationRequest], None,]:
        raise NotImplementedError()

    @property
    def set_iam_policy(
        self,
    ) -> Callable[
        [iam_policy_pb2.SetIamPolicyRequest],
        Union[policy_pb2.Policy, Awaitable[policy_pb2.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def get_iam_policy(
        self,
    ) -> Callable[
        [iam_policy_pb2.GetIamPolicyRequest],
        Union[policy_pb2.Policy, Awaitable[policy_pb2.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [iam_policy_pb2.TestIamPermissionsRequest],
        Union[
            iam_policy_pb2.TestIamPermissionsResponse,
            Awaitable[iam_policy_pb2.TestIamPermissionsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_location(
        self,
    ) -> Callable[
        [locations_pb2.GetLocationRequest],
        Union[locations_pb2.Location, Awaitable[locations_pb2.Location]],
    ]:
        raise NotImplementedError()

    @property
    def list_locations(
        self,
    ) -> Callable[
        [locations_pb2.ListLocationsRequest],
        Union[
            locations_pb2.ListLocationsResponse,
            Awaitable[locations_pb2.ListLocationsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def kind(self) -> str:
        raise NotImplementedError()


__all__ = ("NetworkServicesTransport",)
