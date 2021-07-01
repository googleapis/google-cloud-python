# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
from typing import Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import grpc_helpers  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.api_core import gapic_v1  # type: ignore
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.cloud.channel_v1.types import channel_partner_links
from google.cloud.channel_v1.types import customers
from google.cloud.channel_v1.types import entitlements
from google.cloud.channel_v1.types import offers
from google.cloud.channel_v1.types import service
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from .base import CloudChannelServiceTransport, DEFAULT_CLIENT_INFO


class CloudChannelServiceGrpcTransport(CloudChannelServiceTransport):
    """gRPC backend transport for CloudChannelService.

    CloudChannelService lets Google cloud resellers and distributors
    manage their customers, channel partners, entitlements, and reports.

    Using this service:

    1. Resellers and distributors can manage a customer entity.
    2. Distributors can register an authorized reseller in their channel
       and provide them with delegated admin access.
    3. Resellers and distributors can manage customer entitlements.

    CloudChannelService exposes the following resources:

    -  [Customer][google.cloud.channel.v1.Customer]s: An entity—usually
       an enterprise—managed by a reseller or distributor.

    -  [Entitlement][google.cloud.channel.v1.Entitlement]s: An entity
       that provides a customer with the means to use a service.
       Entitlements are created or updated as a result of a successful
       fulfillment.

    -  [ChannelPartnerLink][google.cloud.channel.v1.ChannelPartnerLink]s:
       An entity that identifies links between distributors and their
       indirect resellers in a channel.

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
        host: str = "cloudchannel.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Sequence[str] = None,
        channel: grpc.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        ssl_channel_credentials: grpc.ChannelCredentials = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
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
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure mutual TLS channel. It is
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
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}
        self._operations_client = None

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
        )

        if not self._grpc_channel:
            self._grpc_channel = type(self).create_channel(
                self._host,
                credentials=self._credentials,
                credentials_file=credentials_file,
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
        host: str = "cloudchannel.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: str = None,
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
        """Return the channel designed to connect to this service.
        """
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Sanity check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsClient(self.grpc_channel)

        # Return the client from cache.
        return self._operations_client

    @property
    def list_customers(
        self,
    ) -> Callable[[service.ListCustomersRequest], service.ListCustomersResponse]:
        r"""Return a callable for the list customers method over gRPC.

        List [Customer][google.cloud.channel.v1.Customer]s.

        Possible error codes:

        -  PERMISSION_DENIED: The reseller account making the request is
           different from the reseller account in the API request.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.

        Return value: List of
        [Customer][google.cloud.channel.v1.Customer]s, or an empty list
        if there are no customers.

        Returns:
            Callable[[~.ListCustomersRequest],
                    ~.ListCustomersResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_customers" not in self._stubs:
            self._stubs["list_customers"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/ListCustomers",
                request_serializer=service.ListCustomersRequest.serialize,
                response_deserializer=service.ListCustomersResponse.deserialize,
            )
        return self._stubs["list_customers"]

    @property
    def get_customer(
        self,
    ) -> Callable[[service.GetCustomerRequest], customers.Customer]:
        r"""Return a callable for the get customer method over gRPC.

        Returns the requested
        [Customer][google.cloud.channel.v1.Customer] resource.

        Possible error codes:

        -  PERMISSION_DENIED: The reseller account making the request is
           different from the reseller account in the API request.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.
        -  NOT_FOUND: The customer resource doesn't exist. Usually the
           result of an invalid name parameter.

        Return value: The [Customer][google.cloud.channel.v1.Customer]
        resource.

        Returns:
            Callable[[~.GetCustomerRequest],
                    ~.Customer]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_customer" not in self._stubs:
            self._stubs["get_customer"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/GetCustomer",
                request_serializer=service.GetCustomerRequest.serialize,
                response_deserializer=customers.Customer.deserialize,
            )
        return self._stubs["get_customer"]

    @property
    def check_cloud_identity_accounts_exist(
        self,
    ) -> Callable[
        [service.CheckCloudIdentityAccountsExistRequest],
        service.CheckCloudIdentityAccountsExistResponse,
    ]:
        r"""Return a callable for the check cloud identity accounts
        exist method over gRPC.

        Confirms the existence of Cloud Identity accounts based on the
        domain and if the Cloud Identity accounts are owned by the
        reseller.

        Possible error codes:

        -  PERMISSION_DENIED: The reseller account making the request is
           different from the reseller account in the API request.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.
        -  INVALID_VALUE: Invalid domain value in the request.

        Return value: A list of
        [CloudIdentityCustomerAccount][google.cloud.channel.v1.CloudIdentityCustomerAccount]
        resources for the domain (may be empty)

        Note: in the v1alpha1 version of the API, a NOT_FOUND error
        returns if no
        [CloudIdentityCustomerAccount][google.cloud.channel.v1.CloudIdentityCustomerAccount]
        resources match the domain.

        Returns:
            Callable[[~.CheckCloudIdentityAccountsExistRequest],
                    ~.CheckCloudIdentityAccountsExistResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "check_cloud_identity_accounts_exist" not in self._stubs:
            self._stubs[
                "check_cloud_identity_accounts_exist"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/CheckCloudIdentityAccountsExist",
                request_serializer=service.CheckCloudIdentityAccountsExistRequest.serialize,
                response_deserializer=service.CheckCloudIdentityAccountsExistResponse.deserialize,
            )
        return self._stubs["check_cloud_identity_accounts_exist"]

    @property
    def create_customer(
        self,
    ) -> Callable[[service.CreateCustomerRequest], customers.Customer]:
        r"""Return a callable for the create customer method over gRPC.

        Creates a new [Customer][google.cloud.channel.v1.Customer]
        resource under the reseller or distributor account.

        Possible error codes:

        -  PERMISSION_DENIED: The reseller account making the request is
           different from the reseller account in the API request.
        -  INVALID_ARGUMENT:

           -  Required request parameters are missing or invalid.
           -  Domain field value doesn't match the primary email domain.

        Return value: The newly created
        [Customer][google.cloud.channel.v1.Customer] resource.

        Returns:
            Callable[[~.CreateCustomerRequest],
                    ~.Customer]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_customer" not in self._stubs:
            self._stubs["create_customer"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/CreateCustomer",
                request_serializer=service.CreateCustomerRequest.serialize,
                response_deserializer=customers.Customer.deserialize,
            )
        return self._stubs["create_customer"]

    @property
    def update_customer(
        self,
    ) -> Callable[[service.UpdateCustomerRequest], customers.Customer]:
        r"""Return a callable for the update customer method over gRPC.

        Updates an existing [Customer][google.cloud.channel.v1.Customer]
        resource for the reseller or distributor.

        Possible error codes:

        -  PERMISSION_DENIED: The reseller account making the request is
           different from the reseller account in the API request.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.
        -  NOT_FOUND: No [Customer][google.cloud.channel.v1.Customer]
           resource found for the name in the request.

        Return value: The updated
        [Customer][google.cloud.channel.v1.Customer] resource.

        Returns:
            Callable[[~.UpdateCustomerRequest],
                    ~.Customer]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_customer" not in self._stubs:
            self._stubs["update_customer"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/UpdateCustomer",
                request_serializer=service.UpdateCustomerRequest.serialize,
                response_deserializer=customers.Customer.deserialize,
            )
        return self._stubs["update_customer"]

    @property
    def delete_customer(
        self,
    ) -> Callable[[service.DeleteCustomerRequest], empty_pb2.Empty]:
        r"""Return a callable for the delete customer method over gRPC.

        Deletes the given [Customer][google.cloud.channel.v1.Customer]
        permanently.

        Possible error codes:

        -  PERMISSION_DENIED: The account making the request does not
           own this customer.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.
        -  FAILED_PRECONDITION: The customer has existing entitlements.
        -  NOT_FOUND: No [Customer][google.cloud.channel.v1.Customer]
           resource found for the name in the request.

        Returns:
            Callable[[~.DeleteCustomerRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_customer" not in self._stubs:
            self._stubs["delete_customer"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/DeleteCustomer",
                request_serializer=service.DeleteCustomerRequest.serialize,
                response_deserializer=empty_pb2.Empty.FromString,
            )
        return self._stubs["delete_customer"]

    @property
    def provision_cloud_identity(
        self,
    ) -> Callable[[service.ProvisionCloudIdentityRequest], operations_pb2.Operation]:
        r"""Return a callable for the provision cloud identity method over gRPC.

        Creates a Cloud Identity for the given customer using the
        customer's information, or the information provided here.

        Possible error codes:

        -  PERMISSION_DENIED: The customer doesn't belong to the
           reseller.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.
        -  NOT_FOUND: The customer was not found.
        -  ALREADY_EXISTS: The customer's primary email already exists.
           Retry after changing the customer's primary contact email.
        -  INTERNAL: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.
        -  UNKNOWN: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.

        Return value: The ID of a long-running operation.

        To get the results of the operation, call the GetOperation
        method of CloudChannelOperationsService. The Operation metadata
        contains an instance of
        [OperationMetadata][google.cloud.channel.v1.OperationMetadata].

        Returns:
            Callable[[~.ProvisionCloudIdentityRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "provision_cloud_identity" not in self._stubs:
            self._stubs["provision_cloud_identity"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/ProvisionCloudIdentity",
                request_serializer=service.ProvisionCloudIdentityRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["provision_cloud_identity"]

    @property
    def list_entitlements(
        self,
    ) -> Callable[[service.ListEntitlementsRequest], service.ListEntitlementsResponse]:
        r"""Return a callable for the list entitlements method over gRPC.

        Lists [Entitlement][google.cloud.channel.v1.Entitlement]s
        belonging to a customer.

        Possible error codes:

        -  PERMISSION_DENIED: The customer doesn't belong to the
           reseller.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.

        Return value: A list of the customer's
        [Entitlement][google.cloud.channel.v1.Entitlement]s.

        Returns:
            Callable[[~.ListEntitlementsRequest],
                    ~.ListEntitlementsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_entitlements" not in self._stubs:
            self._stubs["list_entitlements"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/ListEntitlements",
                request_serializer=service.ListEntitlementsRequest.serialize,
                response_deserializer=service.ListEntitlementsResponse.deserialize,
            )
        return self._stubs["list_entitlements"]

    @property
    def list_transferable_skus(
        self,
    ) -> Callable[
        [service.ListTransferableSkusRequest], service.ListTransferableSkusResponse
    ]:
        r"""Return a callable for the list transferable skus method over gRPC.

        List [TransferableSku][google.cloud.channel.v1.TransferableSku]s
        of a customer based on the Cloud Identity ID or Customer Name in
        the request.

        Use this method to list the entitlements information of an
        unowned customer. You should provide the customer's Cloud
        Identity ID or Customer Name.

        Possible error codes:

        -  PERMISSION_DENIED:

           -  The customer doesn't belong to the reseller and has no
              auth token.
           -  The supplied auth token is invalid.
           -  The reseller account making the request is different from
              the reseller account in the query.

        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.

        Return value: A list of the customer's
        [TransferableSku][google.cloud.channel.v1.TransferableSku].

        Returns:
            Callable[[~.ListTransferableSkusRequest],
                    ~.ListTransferableSkusResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_transferable_skus" not in self._stubs:
            self._stubs["list_transferable_skus"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/ListTransferableSkus",
                request_serializer=service.ListTransferableSkusRequest.serialize,
                response_deserializer=service.ListTransferableSkusResponse.deserialize,
            )
        return self._stubs["list_transferable_skus"]

    @property
    def list_transferable_offers(
        self,
    ) -> Callable[
        [service.ListTransferableOffersRequest], service.ListTransferableOffersResponse
    ]:
        r"""Return a callable for the list transferable offers method over gRPC.

        List
        [TransferableOffer][google.cloud.channel.v1.TransferableOffer]s
        of a customer based on Cloud Identity ID or Customer Name in the
        request.

        Use this method when a reseller gets the entitlement information
        of an unowned customer. The reseller should provide the
        customer's Cloud Identity ID or Customer Name.

        Possible error codes:

        -  PERMISSION_DENIED:

           -  The customer doesn't belong to the reseller and has no
              auth token.
           -  The supplied auth token is invalid.
           -  The reseller account making the request is different from
              the reseller account in the query.

        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.

        Return value: List of
        [TransferableOffer][google.cloud.channel.v1.TransferableOffer]
        for the given customer and SKU.

        Returns:
            Callable[[~.ListTransferableOffersRequest],
                    ~.ListTransferableOffersResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_transferable_offers" not in self._stubs:
            self._stubs["list_transferable_offers"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/ListTransferableOffers",
                request_serializer=service.ListTransferableOffersRequest.serialize,
                response_deserializer=service.ListTransferableOffersResponse.deserialize,
            )
        return self._stubs["list_transferable_offers"]

    @property
    def get_entitlement(
        self,
    ) -> Callable[[service.GetEntitlementRequest], entitlements.Entitlement]:
        r"""Return a callable for the get entitlement method over gRPC.

        Returns the requested
        [Entitlement][google.cloud.channel.v1.Entitlement] resource.

        Possible error codes:

        -  PERMISSION_DENIED: The customer doesn't belong to the
           reseller.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.
        -  NOT_FOUND: The customer entitlement was not found.

        Return value: The requested
        [Entitlement][google.cloud.channel.v1.Entitlement] resource.

        Returns:
            Callable[[~.GetEntitlementRequest],
                    ~.Entitlement]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_entitlement" not in self._stubs:
            self._stubs["get_entitlement"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/GetEntitlement",
                request_serializer=service.GetEntitlementRequest.serialize,
                response_deserializer=entitlements.Entitlement.deserialize,
            )
        return self._stubs["get_entitlement"]

    @property
    def create_entitlement(
        self,
    ) -> Callable[[service.CreateEntitlementRequest], operations_pb2.Operation]:
        r"""Return a callable for the create entitlement method over gRPC.

        Creates an entitlement for a customer.

        Possible error codes:

        -  PERMISSION_DENIED: The customer doesn't belong to the
           reseller.
        -  INVALID_ARGUMENT:

           -  Required request parameters are missing or invalid.
           -  There is already a customer entitlement for a SKU from the
              same product family.

        -  INVALID_VALUE: Make sure the OfferId is valid. If it is,
           contact Google Channel support for further troubleshooting.
        -  NOT_FOUND: The customer or offer resource was not found.
        -  ALREADY_EXISTS:

           -  The SKU was already purchased for the customer.
           -  The customer's primary email already exists. Retry after
              changing the customer's primary contact email.

        -  CONDITION_NOT_MET or FAILED_PRECONDITION:

           -  The domain required for purchasing a SKU has not been
              verified.
           -  A pre-requisite SKU required to purchase an Add-On SKU is
              missing. For example, Google Workspace Business Starter is
              required to purchase Vault or Drive.
           -  (Developer accounts only) Reseller and resold domain must
              meet the following naming requirements:

              -  Domain names must start with goog-test.
              -  Domain names must include the reseller domain.

        -  INTERNAL: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.
        -  UNKNOWN: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.

        Return value: The ID of a long-running operation.

        To get the results of the operation, call the GetOperation
        method of CloudChannelOperationsService. The Operation metadata
        will contain an instance of
        [OperationMetadata][google.cloud.channel.v1.OperationMetadata].

        Returns:
            Callable[[~.CreateEntitlementRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_entitlement" not in self._stubs:
            self._stubs["create_entitlement"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/CreateEntitlement",
                request_serializer=service.CreateEntitlementRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_entitlement"]

    @property
    def change_parameters(
        self,
    ) -> Callable[[service.ChangeParametersRequest], operations_pb2.Operation]:
        r"""Return a callable for the change parameters method over gRPC.

        Change parameters of the entitlement.

        An entitlement update is a long-running operation and it updates
        the entitlement as a result of fulfillment.

        Possible error codes:

        -  PERMISSION_DENIED: The customer doesn't belong to the
           reseller.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid. For example, the number of seats being changed is
           greater than the allowed number of max seats, or decreasing
           seats for a commitment based plan.
        -  NOT_FOUND: Entitlement resource not found.
        -  INTERNAL: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.
        -  UNKNOWN: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.

        Return value: The ID of a long-running operation.

        To get the results of the operation, call the GetOperation
        method of CloudChannelOperationsService. The Operation metadata
        will contain an instance of
        [OperationMetadata][google.cloud.channel.v1.OperationMetadata].

        Returns:
            Callable[[~.ChangeParametersRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "change_parameters" not in self._stubs:
            self._stubs["change_parameters"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/ChangeParameters",
                request_serializer=service.ChangeParametersRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["change_parameters"]

    @property
    def change_renewal_settings(
        self,
    ) -> Callable[[service.ChangeRenewalSettingsRequest], operations_pb2.Operation]:
        r"""Return a callable for the change renewal settings method over gRPC.

        Updates the renewal settings for an existing customer
        entitlement.

        An entitlement update is a long-running operation and it updates
        the entitlement as a result of fulfillment.

        Possible error codes:

        -  PERMISSION_DENIED: The customer doesn't belong to the
           reseller.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.
        -  NOT_FOUND: Entitlement resource not found.
        -  NOT_COMMITMENT_PLAN: Renewal Settings are only applicable for
           a commitment plan. Can't enable or disable renewals for
           non-commitment plans.
        -  INTERNAL: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.
        -  UNKNOWN: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.

        Return value: The ID of a long-running operation.

        To get the results of the operation, call the GetOperation
        method of CloudChannelOperationsService. The Operation metadata
        will contain an instance of
        [OperationMetadata][google.cloud.channel.v1.OperationMetadata].

        Returns:
            Callable[[~.ChangeRenewalSettingsRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "change_renewal_settings" not in self._stubs:
            self._stubs["change_renewal_settings"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/ChangeRenewalSettings",
                request_serializer=service.ChangeRenewalSettingsRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["change_renewal_settings"]

    @property
    def change_offer(
        self,
    ) -> Callable[[service.ChangeOfferRequest], operations_pb2.Operation]:
        r"""Return a callable for the change offer method over gRPC.

        Updates the Offer for an existing customer entitlement.

        An entitlement update is a long-running operation and it updates
        the entitlement as a result of fulfillment.

        Possible error codes:

        -  PERMISSION_DENIED: The customer doesn't belong to the
           reseller.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.
        -  NOT_FOUND: Offer or Entitlement resource not found.
        -  INTERNAL: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.
        -  UNKNOWN: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.

        Return value: The ID of a long-running operation.

        To get the results of the operation, call the GetOperation
        method of CloudChannelOperationsService. The Operation metadata
        will contain an instance of
        [OperationMetadata][google.cloud.channel.v1.OperationMetadata].

        Returns:
            Callable[[~.ChangeOfferRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "change_offer" not in self._stubs:
            self._stubs["change_offer"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/ChangeOffer",
                request_serializer=service.ChangeOfferRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["change_offer"]

    @property
    def start_paid_service(
        self,
    ) -> Callable[[service.StartPaidServiceRequest], operations_pb2.Operation]:
        r"""Return a callable for the start paid service method over gRPC.

        Starts paid service for a trial entitlement.

        Starts paid service for a trial entitlement immediately. This
        method is only applicable if a plan is set up for a trial
        entitlement but has some trial days remaining.

        Possible error codes:

        -  PERMISSION_DENIED: The customer doesn't belong to the
           reseller.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.
        -  NOT_FOUND: Entitlement resource not found.
        -  FAILED_PRECONDITION/NOT_IN_TRIAL: This method only works for
           entitlement on trial plans.
        -  INTERNAL: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.
        -  UNKNOWN: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.

        Return value: The ID of a long-running operation.

        To get the results of the operation, call the GetOperation
        method of CloudChannelOperationsService. The Operation metadata
        will contain an instance of
        [OperationMetadata][google.cloud.channel.v1.OperationMetadata].

        Returns:
            Callable[[~.StartPaidServiceRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "start_paid_service" not in self._stubs:
            self._stubs["start_paid_service"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/StartPaidService",
                request_serializer=service.StartPaidServiceRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["start_paid_service"]

    @property
    def suspend_entitlement(
        self,
    ) -> Callable[[service.SuspendEntitlementRequest], operations_pb2.Operation]:
        r"""Return a callable for the suspend entitlement method over gRPC.

        Suspends a previously fulfilled entitlement.

        An entitlement suspension is a long-running operation.

        Possible error codes:

        -  PERMISSION_DENIED: The customer doesn't belong to the
           reseller.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.
        -  NOT_FOUND: Entitlement resource not found.
        -  NOT_ACTIVE: Entitlement is not active.
        -  INTERNAL: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.
        -  UNKNOWN: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.

        Return value: The ID of a long-running operation.

        To get the results of the operation, call the GetOperation
        method of CloudChannelOperationsService. The Operation metadata
        will contain an instance of
        [OperationMetadata][google.cloud.channel.v1.OperationMetadata].

        Returns:
            Callable[[~.SuspendEntitlementRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "suspend_entitlement" not in self._stubs:
            self._stubs["suspend_entitlement"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/SuspendEntitlement",
                request_serializer=service.SuspendEntitlementRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["suspend_entitlement"]

    @property
    def cancel_entitlement(
        self,
    ) -> Callable[[service.CancelEntitlementRequest], operations_pb2.Operation]:
        r"""Return a callable for the cancel entitlement method over gRPC.

        Cancels a previously fulfilled entitlement.

        An entitlement cancellation is a long-running operation.

        Possible error codes:

        -  PERMISSION_DENIED: The reseller account making the request is
           different from the reseller account in the API request.
        -  FAILED_PRECONDITION: There are Google Cloud projects linked
           to the Google Cloud entitlement's Cloud Billing subaccount.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.
        -  NOT_FOUND: Entitlement resource not found.
        -  DELETION_TYPE_NOT_ALLOWED: Cancel is only allowed for Google
           Workspace add-ons, or entitlements for Google Cloud's
           development platform.
        -  INTERNAL: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.
        -  UNKNOWN: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.

        Return value: The ID of a long-running operation.

        To get the results of the operation, call the GetOperation
        method of CloudChannelOperationsService. The response will
        contain google.protobuf.Empty on success. The Operation metadata
        will contain an instance of
        [OperationMetadata][google.cloud.channel.v1.OperationMetadata].

        Returns:
            Callable[[~.CancelEntitlementRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "cancel_entitlement" not in self._stubs:
            self._stubs["cancel_entitlement"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/CancelEntitlement",
                request_serializer=service.CancelEntitlementRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["cancel_entitlement"]

    @property
    def activate_entitlement(
        self,
    ) -> Callable[[service.ActivateEntitlementRequest], operations_pb2.Operation]:
        r"""Return a callable for the activate entitlement method over gRPC.

        Activates a previously suspended entitlement. Entitlements
        suspended for pending ToS acceptance can't be activated using
        this method.

        An entitlement activation is a long-running operation and it
        updates the state of the customer entitlement.

        Possible error codes:

        -  PERMISSION_DENIED: The reseller account making the request is
           different from the reseller account in the API request.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.
        -  NOT_FOUND: Entitlement resource not found.
        -  SUSPENSION_NOT_RESELLER_INITIATED: Can only activate
           reseller-initiated suspensions and entitlements that have
           accepted the TOS.
        -  NOT_SUSPENDED: Can only activate suspended entitlements not
           in an ACTIVE state.
        -  INTERNAL: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.
        -  UNKNOWN: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.

        Return value: The ID of a long-running operation.

        To get the results of the operation, call the GetOperation
        method of CloudChannelOperationsService. The Operation metadata
        will contain an instance of
        [OperationMetadata][google.cloud.channel.v1.OperationMetadata].

        Returns:
            Callable[[~.ActivateEntitlementRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "activate_entitlement" not in self._stubs:
            self._stubs["activate_entitlement"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/ActivateEntitlement",
                request_serializer=service.ActivateEntitlementRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["activate_entitlement"]

    @property
    def transfer_entitlements(
        self,
    ) -> Callable[[service.TransferEntitlementsRequest], operations_pb2.Operation]:
        r"""Return a callable for the transfer entitlements method over gRPC.

        Transfers customer entitlements to new reseller.

        Possible error codes:

        -  PERMISSION_DENIED: The customer doesn't belong to the
           reseller.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.
        -  NOT_FOUND: The customer or offer resource was not found.
        -  ALREADY_EXISTS: The SKU was already transferred for the
           customer.
        -  CONDITION_NOT_MET or FAILED_PRECONDITION:

           -  The SKU requires domain verification to transfer, but the
              domain is not verified.
           -  An Add-On SKU (example, Vault or Drive) is missing the
              pre-requisite SKU (example, G Suite Basic).
           -  (Developer accounts only) Reseller and resold domain must
              meet the following naming requirements:

              -  Domain names must start with goog-test.
              -  Domain names must include the reseller domain.

           -  Specify all transferring entitlements.

        -  INTERNAL: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.
        -  UNKNOWN: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.

        Return value: The ID of a long-running operation.

        To get the results of the operation, call the GetOperation
        method of CloudChannelOperationsService. The Operation metadata
        will contain an instance of
        [OperationMetadata][google.cloud.channel.v1.OperationMetadata].

        Returns:
            Callable[[~.TransferEntitlementsRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "transfer_entitlements" not in self._stubs:
            self._stubs["transfer_entitlements"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/TransferEntitlements",
                request_serializer=service.TransferEntitlementsRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["transfer_entitlements"]

    @property
    def transfer_entitlements_to_google(
        self,
    ) -> Callable[
        [service.TransferEntitlementsToGoogleRequest], operations_pb2.Operation
    ]:
        r"""Return a callable for the transfer entitlements to
        google method over gRPC.

        Transfers customer entitlements from their current reseller to
        Google.

        Possible error codes:

        -  PERMISSION_DENIED: The customer doesn't belong to the
           reseller.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.
        -  NOT_FOUND: The customer or offer resource was not found.
        -  ALREADY_EXISTS: The SKU was already transferred for the
           customer.
        -  CONDITION_NOT_MET or FAILED_PRECONDITION:

           -  The SKU requires domain verification to transfer, but the
              domain is not verified.
           -  An Add-On SKU (example, Vault or Drive) is missing the
              pre-requisite SKU (example, G Suite Basic).
           -  (Developer accounts only) Reseller and resold domain must
              meet the following naming requirements:

              -  Domain names must start with goog-test.
              -  Domain names must include the reseller domain.

        -  INTERNAL: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.
        -  UNKNOWN: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.

        Return value: The ID of a long-running operation.

        To get the results of the operation, call the GetOperation
        method of CloudChannelOperationsService. The response will
        contain google.protobuf.Empty on success. The Operation metadata
        will contain an instance of
        [OperationMetadata][google.cloud.channel.v1.OperationMetadata].

        Returns:
            Callable[[~.TransferEntitlementsToGoogleRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "transfer_entitlements_to_google" not in self._stubs:
            self._stubs[
                "transfer_entitlements_to_google"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/TransferEntitlementsToGoogle",
                request_serializer=service.TransferEntitlementsToGoogleRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["transfer_entitlements_to_google"]

    @property
    def list_channel_partner_links(
        self,
    ) -> Callable[
        [service.ListChannelPartnerLinksRequest],
        service.ListChannelPartnerLinksResponse,
    ]:
        r"""Return a callable for the list channel partner links method over gRPC.

        List
        [ChannelPartnerLink][google.cloud.channel.v1.ChannelPartnerLink]s
        belonging to a distributor. You must be a distributor to call
        this method.

        Possible error codes:

        -  PERMISSION_DENIED: The reseller account making the request is
           different from the reseller account in the API request.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.

        Return value: The list of the distributor account's
        [ChannelPartnerLink][google.cloud.channel.v1.ChannelPartnerLink]
        resources.

        Returns:
            Callable[[~.ListChannelPartnerLinksRequest],
                    ~.ListChannelPartnerLinksResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_channel_partner_links" not in self._stubs:
            self._stubs["list_channel_partner_links"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/ListChannelPartnerLinks",
                request_serializer=service.ListChannelPartnerLinksRequest.serialize,
                response_deserializer=service.ListChannelPartnerLinksResponse.deserialize,
            )
        return self._stubs["list_channel_partner_links"]

    @property
    def get_channel_partner_link(
        self,
    ) -> Callable[
        [service.GetChannelPartnerLinkRequest], channel_partner_links.ChannelPartnerLink
    ]:
        r"""Return a callable for the get channel partner link method over gRPC.

        Returns the requested
        [ChannelPartnerLink][google.cloud.channel.v1.ChannelPartnerLink]
        resource. You must be a distributor to call this method.

        Possible error codes:

        -  PERMISSION_DENIED: The reseller account making the request is
           different from the reseller account in the API request.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.
        -  NOT_FOUND: ChannelPartnerLink resource not found because of
           an invalid channel partner link name.

        Return value: The
        [ChannelPartnerLink][google.cloud.channel.v1.ChannelPartnerLink]
        resource.

        Returns:
            Callable[[~.GetChannelPartnerLinkRequest],
                    ~.ChannelPartnerLink]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_channel_partner_link" not in self._stubs:
            self._stubs["get_channel_partner_link"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/GetChannelPartnerLink",
                request_serializer=service.GetChannelPartnerLinkRequest.serialize,
                response_deserializer=channel_partner_links.ChannelPartnerLink.deserialize,
            )
        return self._stubs["get_channel_partner_link"]

    @property
    def create_channel_partner_link(
        self,
    ) -> Callable[
        [service.CreateChannelPartnerLinkRequest],
        channel_partner_links.ChannelPartnerLink,
    ]:
        r"""Return a callable for the create channel partner link method over gRPC.

        Initiates a channel partner link between a distributor and a
        reseller, or between resellers in an n-tier reseller channel.
        Invited partners need to follow the invite_link_uri provided in
        the response to accept. After accepting the invitation, a link
        is set up between the two parties. You must be a distributor to
        call this method.

        Possible error codes:

        -  PERMISSION_DENIED: The reseller account making the request is
           different from the reseller account in the API request.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.
        -  ALREADY_EXISTS: The ChannelPartnerLink sent in the request
           already exists.
        -  NOT_FOUND: No Cloud Identity customer exists for provided
           domain.
        -  INTERNAL: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.
        -  UNKNOWN: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.

        Return value: The new
        [ChannelPartnerLink][google.cloud.channel.v1.ChannelPartnerLink]
        resource.

        Returns:
            Callable[[~.CreateChannelPartnerLinkRequest],
                    ~.ChannelPartnerLink]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_channel_partner_link" not in self._stubs:
            self._stubs["create_channel_partner_link"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/CreateChannelPartnerLink",
                request_serializer=service.CreateChannelPartnerLinkRequest.serialize,
                response_deserializer=channel_partner_links.ChannelPartnerLink.deserialize,
            )
        return self._stubs["create_channel_partner_link"]

    @property
    def update_channel_partner_link(
        self,
    ) -> Callable[
        [service.UpdateChannelPartnerLinkRequest],
        channel_partner_links.ChannelPartnerLink,
    ]:
        r"""Return a callable for the update channel partner link method over gRPC.

        Updates a channel partner link. Distributors call this method to
        change a link's status. For example, to suspend a partner link.
        You must be a distributor to call this method.

        Possible error codes:

        -  PERMISSION_DENIED: The reseller account making the request is
           different from the reseller account in the API request.
        -  INVALID_ARGUMENT:

           -  Required request parameters are missing or invalid.
           -  Link state cannot change from invited to active or
              suspended.
           -  Cannot send reseller_cloud_identity_id, invite_url, or
              name in update mask.

        -  NOT_FOUND: ChannelPartnerLink resource not found.
        -  INTERNAL: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.
        -  UNKNOWN: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.

        Return value: The updated
        [ChannelPartnerLink][google.cloud.channel.v1.ChannelPartnerLink]
        resource.

        Returns:
            Callable[[~.UpdateChannelPartnerLinkRequest],
                    ~.ChannelPartnerLink]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_channel_partner_link" not in self._stubs:
            self._stubs["update_channel_partner_link"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/UpdateChannelPartnerLink",
                request_serializer=service.UpdateChannelPartnerLinkRequest.serialize,
                response_deserializer=channel_partner_links.ChannelPartnerLink.deserialize,
            )
        return self._stubs["update_channel_partner_link"]

    @property
    def lookup_offer(self) -> Callable[[service.LookupOfferRequest], offers.Offer]:
        r"""Return a callable for the lookup offer method over gRPC.

        Returns the requested [Offer][google.cloud.channel.v1.Offer]
        resource.

        Possible error codes:

        -  PERMISSION_DENIED: The entitlement doesn't belong to the
           reseller.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.
        -  NOT_FOUND: Entitlement or offer was not found.

        Return value: The [Offer][google.cloud.channel.v1.Offer]
        resource.

        Returns:
            Callable[[~.LookupOfferRequest],
                    ~.Offer]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "lookup_offer" not in self._stubs:
            self._stubs["lookup_offer"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/LookupOffer",
                request_serializer=service.LookupOfferRequest.serialize,
                response_deserializer=offers.Offer.deserialize,
            )
        return self._stubs["lookup_offer"]

    @property
    def list_products(
        self,
    ) -> Callable[[service.ListProductsRequest], service.ListProductsResponse]:
        r"""Return a callable for the list products method over gRPC.

        Lists the Products the reseller is authorized to sell.

        Possible error codes:

        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.

        Returns:
            Callable[[~.ListProductsRequest],
                    ~.ListProductsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_products" not in self._stubs:
            self._stubs["list_products"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/ListProducts",
                request_serializer=service.ListProductsRequest.serialize,
                response_deserializer=service.ListProductsResponse.deserialize,
            )
        return self._stubs["list_products"]

    @property
    def list_skus(
        self,
    ) -> Callable[[service.ListSkusRequest], service.ListSkusResponse]:
        r"""Return a callable for the list skus method over gRPC.

        Lists the SKUs for a product the reseller is authorized to sell.

        Possible error codes:

        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.

        Returns:
            Callable[[~.ListSkusRequest],
                    ~.ListSkusResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_skus" not in self._stubs:
            self._stubs["list_skus"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/ListSkus",
                request_serializer=service.ListSkusRequest.serialize,
                response_deserializer=service.ListSkusResponse.deserialize,
            )
        return self._stubs["list_skus"]

    @property
    def list_offers(
        self,
    ) -> Callable[[service.ListOffersRequest], service.ListOffersResponse]:
        r"""Return a callable for the list offers method over gRPC.

        Lists the Offers the reseller can sell.

        Possible error codes:

        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.

        Returns:
            Callable[[~.ListOffersRequest],
                    ~.ListOffersResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_offers" not in self._stubs:
            self._stubs["list_offers"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/ListOffers",
                request_serializer=service.ListOffersRequest.serialize,
                response_deserializer=service.ListOffersResponse.deserialize,
            )
        return self._stubs["list_offers"]

    @property
    def list_purchasable_skus(
        self,
    ) -> Callable[
        [service.ListPurchasableSkusRequest], service.ListPurchasableSkusResponse
    ]:
        r"""Return a callable for the list purchasable skus method over gRPC.

        Lists the following:

        -  SKUs that you can purchase for a customer
        -  SKUs that you can upgrade or downgrade for an entitlement.

        Possible error codes:

        -  PERMISSION_DENIED: The customer doesn't belong to the
           reseller.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.

        Returns:
            Callable[[~.ListPurchasableSkusRequest],
                    ~.ListPurchasableSkusResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_purchasable_skus" not in self._stubs:
            self._stubs["list_purchasable_skus"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/ListPurchasableSkus",
                request_serializer=service.ListPurchasableSkusRequest.serialize,
                response_deserializer=service.ListPurchasableSkusResponse.deserialize,
            )
        return self._stubs["list_purchasable_skus"]

    @property
    def list_purchasable_offers(
        self,
    ) -> Callable[
        [service.ListPurchasableOffersRequest], service.ListPurchasableOffersResponse
    ]:
        r"""Return a callable for the list purchasable offers method over gRPC.

        Lists the following:

        -  Offers that you can purchase for a customer.
        -  Offers that you can change for an entitlement.

        Possible error codes:

        -  PERMISSION_DENIED: The customer doesn't belong to the
           reseller
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.

        Returns:
            Callable[[~.ListPurchasableOffersRequest],
                    ~.ListPurchasableOffersResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_purchasable_offers" not in self._stubs:
            self._stubs["list_purchasable_offers"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/ListPurchasableOffers",
                request_serializer=service.ListPurchasableOffersRequest.serialize,
                response_deserializer=service.ListPurchasableOffersResponse.deserialize,
            )
        return self._stubs["list_purchasable_offers"]

    @property
    def register_subscriber(
        self,
    ) -> Callable[
        [service.RegisterSubscriberRequest], service.RegisterSubscriberResponse
    ]:
        r"""Return a callable for the register subscriber method over gRPC.

        Registers a service account with subscriber privileges on the
        Cloud Pub/Sub topic for this Channel Services account. After you
        create a subscriber, you get the events through
        [SubscriberEvent][google.cloud.channel.v1.SubscriberEvent]

        Possible error codes:

        -  PERMISSION_DENIED: The reseller account making the request
           and the provided reseller account are different, or the
           impersonated user is not a super admin.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.
        -  INTERNAL: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.
        -  UNKNOWN: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.

        Return value: The topic name with the registered service email
        address.

        Returns:
            Callable[[~.RegisterSubscriberRequest],
                    ~.RegisterSubscriberResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "register_subscriber" not in self._stubs:
            self._stubs["register_subscriber"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/RegisterSubscriber",
                request_serializer=service.RegisterSubscriberRequest.serialize,
                response_deserializer=service.RegisterSubscriberResponse.deserialize,
            )
        return self._stubs["register_subscriber"]

    @property
    def unregister_subscriber(
        self,
    ) -> Callable[
        [service.UnregisterSubscriberRequest], service.UnregisterSubscriberResponse
    ]:
        r"""Return a callable for the unregister subscriber method over gRPC.

        Unregisters a service account with subscriber privileges on the
        Cloud Pub/Sub topic created for this Channel Services account.
        If there are no service accounts left with subscriber
        privileges, this deletes the topic. You can call ListSubscribers
        to check for these accounts.

        Possible error codes:

        -  PERMISSION_DENIED: The reseller account making the request
           and the provided reseller account are different, or the
           impersonated user is not a super admin.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.
        -  NOT_FOUND: The topic resource doesn't exist.
        -  INTERNAL: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.
        -  UNKNOWN: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.

        Return value: The topic name that unregistered the service email
        address. Returns a success response if the service email address
        wasn't registered with the topic.

        Returns:
            Callable[[~.UnregisterSubscriberRequest],
                    ~.UnregisterSubscriberResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "unregister_subscriber" not in self._stubs:
            self._stubs["unregister_subscriber"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/UnregisterSubscriber",
                request_serializer=service.UnregisterSubscriberRequest.serialize,
                response_deserializer=service.UnregisterSubscriberResponse.deserialize,
            )
        return self._stubs["unregister_subscriber"]

    @property
    def list_subscribers(
        self,
    ) -> Callable[[service.ListSubscribersRequest], service.ListSubscribersResponse]:
        r"""Return a callable for the list subscribers method over gRPC.

        Lists service accounts with subscriber privileges on the Cloud
        Pub/Sub topic created for this Channel Services account.

        Possible error codes:

        -  PERMISSION_DENIED: The reseller account making the request
           and the provided reseller account are different, or the
           impersonated user is not a super admin.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.
        -  NOT_FOUND: The topic resource doesn't exist.
        -  INTERNAL: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.
        -  UNKNOWN: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support.

        Return value: A list of service email addresses.

        Returns:
            Callable[[~.ListSubscribersRequest],
                    ~.ListSubscribersResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_subscribers" not in self._stubs:
            self._stubs["list_subscribers"] = self.grpc_channel.unary_unary(
                "/google.cloud.channel.v1.CloudChannelService/ListSubscribers",
                request_serializer=service.ListSubscribersRequest.serialize,
                response_deserializer=service.ListSubscribersResponse.deserialize,
            )
        return self._stubs["list_subscribers"]


__all__ = ("CloudChannelServiceGrpcTransport",)
