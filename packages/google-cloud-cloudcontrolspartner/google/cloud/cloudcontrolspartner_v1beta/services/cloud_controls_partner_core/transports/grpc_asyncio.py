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
import inspect
import json
import logging as std_logging
import pickle
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, grpc_helpers_async
from google.api_core import retry_async as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf.json_format import MessageToJson
import google.protobuf.message
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore
import proto  # type: ignore

from google.cloud.cloudcontrolspartner_v1beta.types import (
    access_approval_requests,
    customer_workloads,
    customers,
    ekm_connections,
    partner_permissions,
    partners,
)

from .base import DEFAULT_CLIENT_INFO, CloudControlsPartnerCoreTransport
from .grpc import CloudControlsPartnerCoreGrpcTransport

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = std_logging.getLogger(__name__)


class _LoggingClientAIOInterceptor(
    grpc.aio.UnaryUnaryClientInterceptor
):  # pragma: NO COVER
    async def intercept_unary_unary(self, continuation, client_call_details, request):
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
                    "serviceName": "google.cloud.cloudcontrolspartner.v1beta.CloudControlsPartnerCore",
                    "rpcName": str(client_call_details.method),
                    "request": grpc_request,
                    "metadata": grpc_request["metadata"],
                },
            )
        response = await continuation(client_call_details, request)
        if logging_enabled:  # pragma: NO COVER
            response_metadata = await response.trailing_metadata()
            # Convert gRPC metadata `<class 'grpc.aio._metadata.Metadata'>` to list of tuples
            metadata = (
                dict([(k, str(v)) for k, v in response_metadata])
                if response_metadata
                else None
            )
            result = await response
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
                f"Received response to rpc {client_call_details.method}.",
                extra={
                    "serviceName": "google.cloud.cloudcontrolspartner.v1beta.CloudControlsPartnerCore",
                    "rpcName": str(client_call_details.method),
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


class CloudControlsPartnerCoreGrpcAsyncIOTransport(CloudControlsPartnerCoreTransport):
    """gRPC AsyncIO backend transport for CloudControlsPartnerCore.

    Service describing handlers for resources

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
        host: str = "cloudcontrolspartner.googleapis.com",
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
        host: str = "cloudcontrolspartner.googleapis.com",
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
                 The hostname to connect to (default: 'cloudcontrolspartner.googleapis.com').
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

        self._interceptor = _LoggingClientAIOInterceptor()
        self._grpc_channel._unary_unary_interceptors.append(self._interceptor)
        self._logged_channel = self._grpc_channel
        self._wrap_with_kind = (
            "kind" in inspect.signature(gapic_v1.method_async.wrap_method).parameters
        )
        # Wrap messages. This must be done after self._logged_channel exists
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
    def get_workload(
        self,
    ) -> Callable[
        [customer_workloads.GetWorkloadRequest], Awaitable[customer_workloads.Workload]
    ]:
        r"""Return a callable for the get workload method over gRPC.

        Gets details of a single workload

        Returns:
            Callable[[~.GetWorkloadRequest],
                    Awaitable[~.Workload]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_workload" not in self._stubs:
            self._stubs["get_workload"] = self._logged_channel.unary_unary(
                "/google.cloud.cloudcontrolspartner.v1beta.CloudControlsPartnerCore/GetWorkload",
                request_serializer=customer_workloads.GetWorkloadRequest.serialize,
                response_deserializer=customer_workloads.Workload.deserialize,
            )
        return self._stubs["get_workload"]

    @property
    def list_workloads(
        self,
    ) -> Callable[
        [customer_workloads.ListWorkloadsRequest],
        Awaitable[customer_workloads.ListWorkloadsResponse],
    ]:
        r"""Return a callable for the list workloads method over gRPC.

        Lists customer workloads for a given customer org id

        Returns:
            Callable[[~.ListWorkloadsRequest],
                    Awaitable[~.ListWorkloadsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_workloads" not in self._stubs:
            self._stubs["list_workloads"] = self._logged_channel.unary_unary(
                "/google.cloud.cloudcontrolspartner.v1beta.CloudControlsPartnerCore/ListWorkloads",
                request_serializer=customer_workloads.ListWorkloadsRequest.serialize,
                response_deserializer=customer_workloads.ListWorkloadsResponse.deserialize,
            )
        return self._stubs["list_workloads"]

    @property
    def get_customer(
        self,
    ) -> Callable[[customers.GetCustomerRequest], Awaitable[customers.Customer]]:
        r"""Return a callable for the get customer method over gRPC.

        Gets details of a single customer

        Returns:
            Callable[[~.GetCustomerRequest],
                    Awaitable[~.Customer]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_customer" not in self._stubs:
            self._stubs["get_customer"] = self._logged_channel.unary_unary(
                "/google.cloud.cloudcontrolspartner.v1beta.CloudControlsPartnerCore/GetCustomer",
                request_serializer=customers.GetCustomerRequest.serialize,
                response_deserializer=customers.Customer.deserialize,
            )
        return self._stubs["get_customer"]

    @property
    def list_customers(
        self,
    ) -> Callable[
        [customers.ListCustomersRequest], Awaitable[customers.ListCustomersResponse]
    ]:
        r"""Return a callable for the list customers method over gRPC.

        Lists customers of a partner identified by its Google
        Cloud organization ID

        Returns:
            Callable[[~.ListCustomersRequest],
                    Awaitable[~.ListCustomersResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_customers" not in self._stubs:
            self._stubs["list_customers"] = self._logged_channel.unary_unary(
                "/google.cloud.cloudcontrolspartner.v1beta.CloudControlsPartnerCore/ListCustomers",
                request_serializer=customers.ListCustomersRequest.serialize,
                response_deserializer=customers.ListCustomersResponse.deserialize,
            )
        return self._stubs["list_customers"]

    @property
    def get_ekm_connections(
        self,
    ) -> Callable[
        [ekm_connections.GetEkmConnectionsRequest],
        Awaitable[ekm_connections.EkmConnections],
    ]:
        r"""Return a callable for the get ekm connections method over gRPC.

        Gets the EKM connections associated with a workload

        Returns:
            Callable[[~.GetEkmConnectionsRequest],
                    Awaitable[~.EkmConnections]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_ekm_connections" not in self._stubs:
            self._stubs["get_ekm_connections"] = self._logged_channel.unary_unary(
                "/google.cloud.cloudcontrolspartner.v1beta.CloudControlsPartnerCore/GetEkmConnections",
                request_serializer=ekm_connections.GetEkmConnectionsRequest.serialize,
                response_deserializer=ekm_connections.EkmConnections.deserialize,
            )
        return self._stubs["get_ekm_connections"]

    @property
    def get_partner_permissions(
        self,
    ) -> Callable[
        [partner_permissions.GetPartnerPermissionsRequest],
        Awaitable[partner_permissions.PartnerPermissions],
    ]:
        r"""Return a callable for the get partner permissions method over gRPC.

        Gets the partner permissions granted for a workload

        Returns:
            Callable[[~.GetPartnerPermissionsRequest],
                    Awaitable[~.PartnerPermissions]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_partner_permissions" not in self._stubs:
            self._stubs["get_partner_permissions"] = self._logged_channel.unary_unary(
                "/google.cloud.cloudcontrolspartner.v1beta.CloudControlsPartnerCore/GetPartnerPermissions",
                request_serializer=partner_permissions.GetPartnerPermissionsRequest.serialize,
                response_deserializer=partner_permissions.PartnerPermissions.deserialize,
            )
        return self._stubs["get_partner_permissions"]

    @property
    def list_access_approval_requests(
        self,
    ) -> Callable[
        [access_approval_requests.ListAccessApprovalRequestsRequest],
        Awaitable[access_approval_requests.ListAccessApprovalRequestsResponse],
    ]:
        r"""Return a callable for the list access approval requests method over gRPC.

        Deprecated: Only returns access approval requests
        directly associated with an assured workload folder.

        Returns:
            Callable[[~.ListAccessApprovalRequestsRequest],
                    Awaitable[~.ListAccessApprovalRequestsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_access_approval_requests" not in self._stubs:
            self._stubs[
                "list_access_approval_requests"
            ] = self._logged_channel.unary_unary(
                "/google.cloud.cloudcontrolspartner.v1beta.CloudControlsPartnerCore/ListAccessApprovalRequests",
                request_serializer=access_approval_requests.ListAccessApprovalRequestsRequest.serialize,
                response_deserializer=access_approval_requests.ListAccessApprovalRequestsResponse.deserialize,
            )
        return self._stubs["list_access_approval_requests"]

    @property
    def get_partner(
        self,
    ) -> Callable[[partners.GetPartnerRequest], Awaitable[partners.Partner]]:
        r"""Return a callable for the get partner method over gRPC.

        Get details of a Partner.

        Returns:
            Callable[[~.GetPartnerRequest],
                    Awaitable[~.Partner]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_partner" not in self._stubs:
            self._stubs["get_partner"] = self._logged_channel.unary_unary(
                "/google.cloud.cloudcontrolspartner.v1beta.CloudControlsPartnerCore/GetPartner",
                request_serializer=partners.GetPartnerRequest.serialize,
                response_deserializer=partners.Partner.deserialize,
            )
        return self._stubs["get_partner"]

    @property
    def create_customer(
        self,
    ) -> Callable[[customers.CreateCustomerRequest], Awaitable[customers.Customer]]:
        r"""Return a callable for the create customer method over gRPC.

        Creates a new customer.

        Returns:
            Callable[[~.CreateCustomerRequest],
                    Awaitable[~.Customer]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_customer" not in self._stubs:
            self._stubs["create_customer"] = self._logged_channel.unary_unary(
                "/google.cloud.cloudcontrolspartner.v1beta.CloudControlsPartnerCore/CreateCustomer",
                request_serializer=customers.CreateCustomerRequest.serialize,
                response_deserializer=customers.Customer.deserialize,
            )
        return self._stubs["create_customer"]

    @property
    def update_customer(
        self,
    ) -> Callable[[customers.UpdateCustomerRequest], Awaitable[customers.Customer]]:
        r"""Return a callable for the update customer method over gRPC.

        Update details of a single customer

        Returns:
            Callable[[~.UpdateCustomerRequest],
                    Awaitable[~.Customer]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_customer" not in self._stubs:
            self._stubs["update_customer"] = self._logged_channel.unary_unary(
                "/google.cloud.cloudcontrolspartner.v1beta.CloudControlsPartnerCore/UpdateCustomer",
                request_serializer=customers.UpdateCustomerRequest.serialize,
                response_deserializer=customers.Customer.deserialize,
            )
        return self._stubs["update_customer"]

    @property
    def delete_customer(
        self,
    ) -> Callable[[customers.DeleteCustomerRequest], Awaitable[empty_pb2.Empty]]:
        r"""Return a callable for the delete customer method over gRPC.

        Delete details of a single customer

        Returns:
            Callable[[~.DeleteCustomerRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_customer" not in self._stubs:
            self._stubs["delete_customer"] = self._logged_channel.unary_unary(
                "/google.cloud.cloudcontrolspartner.v1beta.CloudControlsPartnerCore/DeleteCustomer",
                request_serializer=customers.DeleteCustomerRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_customer"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.get_workload: self._wrap_method(
                self.get_workload,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_workloads: self._wrap_method(
                self.list_workloads,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_customer: self._wrap_method(
                self.get_customer,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_customers: self._wrap_method(
                self.list_customers,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_ekm_connections: self._wrap_method(
                self.get_ekm_connections,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_partner_permissions: self._wrap_method(
                self.get_partner_permissions,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_access_approval_requests: self._wrap_method(
                self.list_access_approval_requests,
                default_retry=retries.AsyncRetry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_partner: self._wrap_method(
                self.get_partner,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_customer: self._wrap_method(
                self.create_customer,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_customer: self._wrap_method(
                self.update_customer,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_customer: self._wrap_method(
                self.delete_customer,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    def _wrap_method(self, func, *args, **kwargs):
        if self._wrap_with_kind:  # pragma: NO COVER
            kwargs["kind"] = self.kind
        return gapic_v1.method_async.wrap_method(func, *args, **kwargs)

    def close(self):
        return self._logged_channel.close()

    @property
    def kind(self) -> str:
        return "grpc_asyncio"


__all__ = ("CloudControlsPartnerCoreGrpcAsyncIOTransport",)
