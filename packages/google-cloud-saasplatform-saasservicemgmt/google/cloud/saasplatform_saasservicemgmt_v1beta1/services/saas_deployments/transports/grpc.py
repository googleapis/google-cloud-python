# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
import json
import logging as std_logging
import pickle
from typing import Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, grpc_helpers
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf.json_format import MessageToJson
import google.protobuf.message
import grpc  # type: ignore
import proto  # type: ignore

from google.cloud.saasplatform_saasservicemgmt_v1beta1.types import (
    deployments_resources,
    deployments_service,
)

from .base import DEFAULT_CLIENT_INFO, SaasDeploymentsTransport

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = std_logging.getLogger(__name__)


class _LoggingClientInterceptor(grpc.UnaryUnaryClientInterceptor):  # pragma: NO COVER
    def intercept_unary_unary(self, continuation, client_call_details, request):
        logging_enabled = CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
            std_logging.DEBUG
        )
        if logging_enabled:  # pragma: NO COVER
            request_metadata = client_call_details.metadata
            if isinstance(request, proto.Message):
                request_payload = type(request).to_json(request)
            elif isinstance(request, google.protobuf.message.Message):
                request_payload = MessageToJson(request)
            else:
                request_payload = f"{type(request).__name__}: {pickle.dumps(request)}"

            request_metadata = {
                key: value.decode("utf-8") if isinstance(value, bytes) else value
                for key, value in request_metadata
            }
            grpc_request = {
                "payload": request_payload,
                "requestMethod": "grpc",
                "metadata": dict(request_metadata),
            }
            _LOGGER.debug(
                f"Sending request for {client_call_details.method}",
                extra={
                    "serviceName": "google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments",
                    "rpcName": str(client_call_details.method),
                    "request": grpc_request,
                    "metadata": grpc_request["metadata"],
                },
            )
        response = continuation(client_call_details, request)
        if logging_enabled:  # pragma: NO COVER
            response_metadata = response.trailing_metadata()
            # Convert gRPC metadata `<class 'grpc.aio._metadata.Metadata'>` to list of tuples
            metadata = (
                dict([(k, str(v)) for k, v in response_metadata])
                if response_metadata
                else None
            )
            result = response.result()
            if isinstance(result, proto.Message):
                response_payload = type(result).to_json(result)
            elif isinstance(result, google.protobuf.message.Message):
                response_payload = MessageToJson(result)
            else:
                response_payload = f"{type(result).__name__}: {pickle.dumps(result)}"
            grpc_response = {
                "payload": response_payload,
                "metadata": metadata,
                "status": "OK",
            }
            _LOGGER.debug(
                f"Received response for {client_call_details.method}.",
                extra={
                    "serviceName": "google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments",
                    "rpcName": client_call_details.method,
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


class SaasDeploymentsGrpcTransport(SaasDeploymentsTransport):
    """gRPC backend transport for SaasDeployments.

    Manages the deployment of SaaS services.

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
        host: str = "saasservicemgmt.googleapis.com",
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
                 The hostname to connect to (default: 'saasservicemgmt.googleapis.com').
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

        self._interceptor = _LoggingClientInterceptor()
        self._logged_channel = grpc.intercept_channel(
            self._grpc_channel, self._interceptor
        )

        # Wrap messages. This must be done after self._logged_channel exists
        self._prep_wrapped_messages(client_info)

    @classmethod
    def create_channel(
        cls,
        host: str = "saasservicemgmt.googleapis.com",
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
    def list_saas(
        self,
    ) -> Callable[
        [deployments_service.ListSaasRequest], deployments_service.ListSaasResponse
    ]:
        r"""Return a callable for the list saas method over gRPC.

        Retrieve a collection of saas.

        Returns:
            Callable[[~.ListSaasRequest],
                    ~.ListSaasResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_saas" not in self._stubs:
            self._stubs["list_saas"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/ListSaas",
                request_serializer=deployments_service.ListSaasRequest.serialize,
                response_deserializer=deployments_service.ListSaasResponse.deserialize,
            )
        return self._stubs["list_saas"]

    @property
    def get_saas(
        self,
    ) -> Callable[[deployments_service.GetSaasRequest], deployments_resources.Saas]:
        r"""Return a callable for the get saas method over gRPC.

        Retrieve a single saas.

        Returns:
            Callable[[~.GetSaasRequest],
                    ~.Saas]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_saas" not in self._stubs:
            self._stubs["get_saas"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/GetSaas",
                request_serializer=deployments_service.GetSaasRequest.serialize,
                response_deserializer=deployments_resources.Saas.deserialize,
            )
        return self._stubs["get_saas"]

    @property
    def create_saas(
        self,
    ) -> Callable[[deployments_service.CreateSaasRequest], deployments_resources.Saas]:
        r"""Return a callable for the create saas method over gRPC.

        Create a new saas.

        Returns:
            Callable[[~.CreateSaasRequest],
                    ~.Saas]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_saas" not in self._stubs:
            self._stubs["create_saas"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/CreateSaas",
                request_serializer=deployments_service.CreateSaasRequest.serialize,
                response_deserializer=deployments_resources.Saas.deserialize,
            )
        return self._stubs["create_saas"]

    @property
    def update_saas(
        self,
    ) -> Callable[[deployments_service.UpdateSaasRequest], deployments_resources.Saas]:
        r"""Return a callable for the update saas method over gRPC.

        Update a single saas.

        Returns:
            Callable[[~.UpdateSaasRequest],
                    ~.Saas]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_saas" not in self._stubs:
            self._stubs["update_saas"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/UpdateSaas",
                request_serializer=deployments_service.UpdateSaasRequest.serialize,
                response_deserializer=deployments_resources.Saas.deserialize,
            )
        return self._stubs["update_saas"]

    @property
    def delete_saas(
        self,
    ) -> Callable[[deployments_service.DeleteSaasRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete saas method over gRPC.

        Delete a single saas.

        Returns:
            Callable[[~.DeleteSaasRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_saas" not in self._stubs:
            self._stubs["delete_saas"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/DeleteSaas",
                request_serializer=deployments_service.DeleteSaasRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_saas"]

    @property
    def list_tenants(
        self,
    ) -> Callable[
        [deployments_service.ListTenantsRequest],
        deployments_service.ListTenantsResponse,
    ]:
        r"""Return a callable for the list tenants method over gRPC.

        Retrieve a collection of tenants.

        Returns:
            Callable[[~.ListTenantsRequest],
                    ~.ListTenantsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_tenants" not in self._stubs:
            self._stubs["list_tenants"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/ListTenants",
                request_serializer=deployments_service.ListTenantsRequest.serialize,
                response_deserializer=deployments_service.ListTenantsResponse.deserialize,
            )
        return self._stubs["list_tenants"]

    @property
    def get_tenant(
        self,
    ) -> Callable[[deployments_service.GetTenantRequest], deployments_resources.Tenant]:
        r"""Return a callable for the get tenant method over gRPC.

        Retrieve a single tenant.

        Returns:
            Callable[[~.GetTenantRequest],
                    ~.Tenant]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_tenant" not in self._stubs:
            self._stubs["get_tenant"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/GetTenant",
                request_serializer=deployments_service.GetTenantRequest.serialize,
                response_deserializer=deployments_resources.Tenant.deserialize,
            )
        return self._stubs["get_tenant"]

    @property
    def create_tenant(
        self,
    ) -> Callable[
        [deployments_service.CreateTenantRequest], deployments_resources.Tenant
    ]:
        r"""Return a callable for the create tenant method over gRPC.

        Create a new tenant.

        Returns:
            Callable[[~.CreateTenantRequest],
                    ~.Tenant]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_tenant" not in self._stubs:
            self._stubs["create_tenant"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/CreateTenant",
                request_serializer=deployments_service.CreateTenantRequest.serialize,
                response_deserializer=deployments_resources.Tenant.deserialize,
            )
        return self._stubs["create_tenant"]

    @property
    def update_tenant(
        self,
    ) -> Callable[
        [deployments_service.UpdateTenantRequest], deployments_resources.Tenant
    ]:
        r"""Return a callable for the update tenant method over gRPC.

        Update a single tenant.

        Returns:
            Callable[[~.UpdateTenantRequest],
                    ~.Tenant]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_tenant" not in self._stubs:
            self._stubs["update_tenant"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/UpdateTenant",
                request_serializer=deployments_service.UpdateTenantRequest.serialize,
                response_deserializer=deployments_resources.Tenant.deserialize,
            )
        return self._stubs["update_tenant"]

    @property
    def delete_tenant(
        self,
    ) -> Callable[[deployments_service.DeleteTenantRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete tenant method over gRPC.

        Delete a single tenant.

        Returns:
            Callable[[~.DeleteTenantRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_tenant" not in self._stubs:
            self._stubs["delete_tenant"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/DeleteTenant",
                request_serializer=deployments_service.DeleteTenantRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_tenant"]

    @property
    def list_unit_kinds(
        self,
    ) -> Callable[
        [deployments_service.ListUnitKindsRequest],
        deployments_service.ListUnitKindsResponse,
    ]:
        r"""Return a callable for the list unit kinds method over gRPC.

        Retrieve a collection of unit kinds.

        Returns:
            Callable[[~.ListUnitKindsRequest],
                    ~.ListUnitKindsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_unit_kinds" not in self._stubs:
            self._stubs["list_unit_kinds"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/ListUnitKinds",
                request_serializer=deployments_service.ListUnitKindsRequest.serialize,
                response_deserializer=deployments_service.ListUnitKindsResponse.deserialize,
            )
        return self._stubs["list_unit_kinds"]

    @property
    def get_unit_kind(
        self,
    ) -> Callable[
        [deployments_service.GetUnitKindRequest], deployments_resources.UnitKind
    ]:
        r"""Return a callable for the get unit kind method over gRPC.

        Retrieve a single unit kind.

        Returns:
            Callable[[~.GetUnitKindRequest],
                    ~.UnitKind]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_unit_kind" not in self._stubs:
            self._stubs["get_unit_kind"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/GetUnitKind",
                request_serializer=deployments_service.GetUnitKindRequest.serialize,
                response_deserializer=deployments_resources.UnitKind.deserialize,
            )
        return self._stubs["get_unit_kind"]

    @property
    def create_unit_kind(
        self,
    ) -> Callable[
        [deployments_service.CreateUnitKindRequest], deployments_resources.UnitKind
    ]:
        r"""Return a callable for the create unit kind method over gRPC.

        Create a new unit kind.

        Returns:
            Callable[[~.CreateUnitKindRequest],
                    ~.UnitKind]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_unit_kind" not in self._stubs:
            self._stubs["create_unit_kind"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/CreateUnitKind",
                request_serializer=deployments_service.CreateUnitKindRequest.serialize,
                response_deserializer=deployments_resources.UnitKind.deserialize,
            )
        return self._stubs["create_unit_kind"]

    @property
    def update_unit_kind(
        self,
    ) -> Callable[
        [deployments_service.UpdateUnitKindRequest], deployments_resources.UnitKind
    ]:
        r"""Return a callable for the update unit kind method over gRPC.

        Update a single unit kind.

        Returns:
            Callable[[~.UpdateUnitKindRequest],
                    ~.UnitKind]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_unit_kind" not in self._stubs:
            self._stubs["update_unit_kind"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/UpdateUnitKind",
                request_serializer=deployments_service.UpdateUnitKindRequest.serialize,
                response_deserializer=deployments_resources.UnitKind.deserialize,
            )
        return self._stubs["update_unit_kind"]

    @property
    def delete_unit_kind(
        self,
    ) -> Callable[[deployments_service.DeleteUnitKindRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete unit kind method over gRPC.

        Delete a single unit kind.

        Returns:
            Callable[[~.DeleteUnitKindRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_unit_kind" not in self._stubs:
            self._stubs["delete_unit_kind"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/DeleteUnitKind",
                request_serializer=deployments_service.DeleteUnitKindRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_unit_kind"]

    @property
    def list_units(
        self,
    ) -> Callable[
        [deployments_service.ListUnitsRequest], deployments_service.ListUnitsResponse
    ]:
        r"""Return a callable for the list units method over gRPC.

        Retrieve a collection of units.

        Returns:
            Callable[[~.ListUnitsRequest],
                    ~.ListUnitsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_units" not in self._stubs:
            self._stubs["list_units"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/ListUnits",
                request_serializer=deployments_service.ListUnitsRequest.serialize,
                response_deserializer=deployments_service.ListUnitsResponse.deserialize,
            )
        return self._stubs["list_units"]

    @property
    def get_unit(
        self,
    ) -> Callable[[deployments_service.GetUnitRequest], deployments_resources.Unit]:
        r"""Return a callable for the get unit method over gRPC.

        Retrieve a single unit.

        Returns:
            Callable[[~.GetUnitRequest],
                    ~.Unit]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_unit" not in self._stubs:
            self._stubs["get_unit"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/GetUnit",
                request_serializer=deployments_service.GetUnitRequest.serialize,
                response_deserializer=deployments_resources.Unit.deserialize,
            )
        return self._stubs["get_unit"]

    @property
    def create_unit(
        self,
    ) -> Callable[[deployments_service.CreateUnitRequest], deployments_resources.Unit]:
        r"""Return a callable for the create unit method over gRPC.

        Create a new unit.

        Returns:
            Callable[[~.CreateUnitRequest],
                    ~.Unit]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_unit" not in self._stubs:
            self._stubs["create_unit"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/CreateUnit",
                request_serializer=deployments_service.CreateUnitRequest.serialize,
                response_deserializer=deployments_resources.Unit.deserialize,
            )
        return self._stubs["create_unit"]

    @property
    def update_unit(
        self,
    ) -> Callable[[deployments_service.UpdateUnitRequest], deployments_resources.Unit]:
        r"""Return a callable for the update unit method over gRPC.

        Update a single unit.

        Returns:
            Callable[[~.UpdateUnitRequest],
                    ~.Unit]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_unit" not in self._stubs:
            self._stubs["update_unit"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/UpdateUnit",
                request_serializer=deployments_service.UpdateUnitRequest.serialize,
                response_deserializer=deployments_resources.Unit.deserialize,
            )
        return self._stubs["update_unit"]

    @property
    def delete_unit(
        self,
    ) -> Callable[[deployments_service.DeleteUnitRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete unit method over gRPC.

        Delete a single unit.

        Returns:
            Callable[[~.DeleteUnitRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_unit" not in self._stubs:
            self._stubs["delete_unit"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/DeleteUnit",
                request_serializer=deployments_service.DeleteUnitRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_unit"]

    @property
    def list_unit_operations(
        self,
    ) -> Callable[
        [deployments_service.ListUnitOperationsRequest],
        deployments_service.ListUnitOperationsResponse,
    ]:
        r"""Return a callable for the list unit operations method over gRPC.

        Retrieve a collection of unit operations.

        Returns:
            Callable[[~.ListUnitOperationsRequest],
                    ~.ListUnitOperationsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_unit_operations" not in self._stubs:
            self._stubs["list_unit_operations"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/ListUnitOperations",
                request_serializer=deployments_service.ListUnitOperationsRequest.serialize,
                response_deserializer=deployments_service.ListUnitOperationsResponse.deserialize,
            )
        return self._stubs["list_unit_operations"]

    @property
    def get_unit_operation(
        self,
    ) -> Callable[
        [deployments_service.GetUnitOperationRequest],
        deployments_resources.UnitOperation,
    ]:
        r"""Return a callable for the get unit operation method over gRPC.

        Retrieve a single unit operation.

        Returns:
            Callable[[~.GetUnitOperationRequest],
                    ~.UnitOperation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_unit_operation" not in self._stubs:
            self._stubs["get_unit_operation"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/GetUnitOperation",
                request_serializer=deployments_service.GetUnitOperationRequest.serialize,
                response_deserializer=deployments_resources.UnitOperation.deserialize,
            )
        return self._stubs["get_unit_operation"]

    @property
    def create_unit_operation(
        self,
    ) -> Callable[
        [deployments_service.CreateUnitOperationRequest],
        deployments_resources.UnitOperation,
    ]:
        r"""Return a callable for the create unit operation method over gRPC.

        Create a new unit operation.

        Returns:
            Callable[[~.CreateUnitOperationRequest],
                    ~.UnitOperation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_unit_operation" not in self._stubs:
            self._stubs["create_unit_operation"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/CreateUnitOperation",
                request_serializer=deployments_service.CreateUnitOperationRequest.serialize,
                response_deserializer=deployments_resources.UnitOperation.deserialize,
            )
        return self._stubs["create_unit_operation"]

    @property
    def update_unit_operation(
        self,
    ) -> Callable[
        [deployments_service.UpdateUnitOperationRequest],
        deployments_resources.UnitOperation,
    ]:
        r"""Return a callable for the update unit operation method over gRPC.

        Update a single unit operation.

        Returns:
            Callable[[~.UpdateUnitOperationRequest],
                    ~.UnitOperation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_unit_operation" not in self._stubs:
            self._stubs["update_unit_operation"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/UpdateUnitOperation",
                request_serializer=deployments_service.UpdateUnitOperationRequest.serialize,
                response_deserializer=deployments_resources.UnitOperation.deserialize,
            )
        return self._stubs["update_unit_operation"]

    @property
    def delete_unit_operation(
        self,
    ) -> Callable[[deployments_service.DeleteUnitOperationRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete unit operation method over gRPC.

        Delete a single unit operation.

        Returns:
            Callable[[~.DeleteUnitOperationRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_unit_operation" not in self._stubs:
            self._stubs["delete_unit_operation"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/DeleteUnitOperation",
                request_serializer=deployments_service.DeleteUnitOperationRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_unit_operation"]

    @property
    def list_releases(
        self,
    ) -> Callable[
        [deployments_service.ListReleasesRequest],
        deployments_service.ListReleasesResponse,
    ]:
        r"""Return a callable for the list releases method over gRPC.

        Retrieve a collection of releases.

        Returns:
            Callable[[~.ListReleasesRequest],
                    ~.ListReleasesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_releases" not in self._stubs:
            self._stubs["list_releases"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/ListReleases",
                request_serializer=deployments_service.ListReleasesRequest.serialize,
                response_deserializer=deployments_service.ListReleasesResponse.deserialize,
            )
        return self._stubs["list_releases"]

    @property
    def get_release(
        self,
    ) -> Callable[
        [deployments_service.GetReleaseRequest], deployments_resources.Release
    ]:
        r"""Return a callable for the get release method over gRPC.

        Retrieve a single release.

        Returns:
            Callable[[~.GetReleaseRequest],
                    ~.Release]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_release" not in self._stubs:
            self._stubs["get_release"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/GetRelease",
                request_serializer=deployments_service.GetReleaseRequest.serialize,
                response_deserializer=deployments_resources.Release.deserialize,
            )
        return self._stubs["get_release"]

    @property
    def create_release(
        self,
    ) -> Callable[
        [deployments_service.CreateReleaseRequest], deployments_resources.Release
    ]:
        r"""Return a callable for the create release method over gRPC.

        Create a new release.

        Returns:
            Callable[[~.CreateReleaseRequest],
                    ~.Release]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_release" not in self._stubs:
            self._stubs["create_release"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/CreateRelease",
                request_serializer=deployments_service.CreateReleaseRequest.serialize,
                response_deserializer=deployments_resources.Release.deserialize,
            )
        return self._stubs["create_release"]

    @property
    def update_release(
        self,
    ) -> Callable[
        [deployments_service.UpdateReleaseRequest], deployments_resources.Release
    ]:
        r"""Return a callable for the update release method over gRPC.

        Update a single release.

        Returns:
            Callable[[~.UpdateReleaseRequest],
                    ~.Release]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_release" not in self._stubs:
            self._stubs["update_release"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/UpdateRelease",
                request_serializer=deployments_service.UpdateReleaseRequest.serialize,
                response_deserializer=deployments_resources.Release.deserialize,
            )
        return self._stubs["update_release"]

    @property
    def delete_release(
        self,
    ) -> Callable[[deployments_service.DeleteReleaseRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete release method over gRPC.

        Delete a single release.

        Returns:
            Callable[[~.DeleteReleaseRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_release" not in self._stubs:
            self._stubs["delete_release"] = self._logged_channel.unary_unary(
                "/google.cloud.saasplatform.saasservicemgmt.v1beta1.SaasDeployments/DeleteRelease",
                request_serializer=deployments_service.DeleteReleaseRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_release"]

    def close(self):
        self._logged_channel.close()

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
            self._stubs["list_locations"] = self._logged_channel.unary_unary(
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
            self._stubs["get_location"] = self._logged_channel.unary_unary(
                "/google.cloud.location.Locations/GetLocation",
                request_serializer=locations_pb2.GetLocationRequest.SerializeToString,
                response_deserializer=locations_pb2.Location.FromString,
            )
        return self._stubs["get_location"]

    @property
    def kind(self) -> str:
        return "grpc"


__all__ = ("SaasDeploymentsGrpcTransport",)
