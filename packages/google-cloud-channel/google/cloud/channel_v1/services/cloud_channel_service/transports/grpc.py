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
from typing import Callable, Dict, Optional, Sequence, Tuple

from google.api_core import grpc_helpers  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google import auth  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.cloud.channel_v1.types import channel_partner_links
from google.cloud.channel_v1.types import customers
from google.cloud.channel_v1.types import entitlements
from google.cloud.channel_v1.types import service
from google.longrunning import operations_pb2 as operations  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore

from .base import CloudChannelServiceTransport, DEFAULT_CLIENT_INFO


class CloudChannelServiceGrpcTransport(CloudChannelServiceTransport):
    """gRPC backend transport for CloudChannelService.

    CloudChannelService enables Google cloud resellers and distributors
    to manage their customers, channel partners, entitlements and
    reports.

    Using this service:

    1. Resellers or distributors can manage a customer entity.
    2. Distributors can register an authorized reseller in their channel
       and then enable delegated admin access for the reseller.
    3. Resellers or distributors can manage entitlements for their
       customers.

    The service primarily exposes the following resources:

    -  [Customer][google.cloud.channel.v1.Customer]s: A Customer
       represents an entity managed by a reseller or distributor. A
       customer typically represents an enterprise. In an n-tier resale
       channel hierarchy, customers are generally represented as leaf
       nodes. Customers primarily have an Entitlement sub-resource
       discussed below.

    -  [Entitlement][google.cloud.channel.v1.Entitlement]s: An
       Entitlement represents an entity which provides a customer means
       to start using a service. Entitlements are created or updated as
       a result of a successful fulfillment.

    -  [ChannelPartnerLink][google.cloud.channel.v1.ChannelPartnerLink]s:
       A ChannelPartnerLink is an entity that identifies links between
       distributors and their indirect resellers in a channel.

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
        credentials: credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Sequence[str] = None,
        channel: grpc.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        ssl_channel_credentials: grpc.ChannelCredentials = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
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
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._ssl_channel_credentials = ssl_channel_credentials

        if channel:
            # Sanity check: Ensure that channel and credentials are not both
            # provided.
            credentials = False

            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None
        elif api_mtls_endpoint:
            warnings.warn(
                "api_mtls_endpoint and client_cert_source are deprecated",
                DeprecationWarning,
            )

            host = (
                api_mtls_endpoint
                if ":" in api_mtls_endpoint
                else api_mtls_endpoint + ":443"
            )

            if credentials is None:
                credentials, _ = auth.default(
                    scopes=self.AUTH_SCOPES, quota_project_id=quota_project_id
                )

            # Create SSL credentials with client_cert_source or application
            # default SSL credentials.
            if client_cert_source:
                cert, key = client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
            else:
                ssl_credentials = SslCredentials().ssl_credentials

            # create a new channel. The provided one is ignored.
            self._grpc_channel = type(self).create_channel(
                host,
                credentials=credentials,
                credentials_file=credentials_file,
                ssl_credentials=ssl_credentials,
                scopes=scopes or self.AUTH_SCOPES,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            self._ssl_channel_credentials = ssl_credentials
        else:
            host = host if ":" in host else host + ":443"

            if credentials is None:
                credentials, _ = auth.default(
                    scopes=self.AUTH_SCOPES, quota_project_id=quota_project_id
                )

            # create a new channel. The provided one is ignored.
            self._grpc_channel = type(self).create_channel(
                host,
                credentials=credentials,
                credentials_file=credentials_file,
                ssl_credentials=ssl_channel_credentials,
                scopes=scopes or self.AUTH_SCOPES,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        self._stubs = {}  # type: Dict[str, Callable]
        self._operations_client = None

        # Run the base constructor.
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes or self.AUTH_SCOPES,
            quota_project_id=quota_project_id,
            client_info=client_info,
        )

    @classmethod
    def create_channel(
        cls,
        host: str = "cloudchannel.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            address (Optional[str]): The host for the channel to use.
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
        scopes = scopes or cls.AUTH_SCOPES
        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
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

        List downstream [Customer][google.cloud.channel.v1.Customer]s.

        Possible Error Codes:

        -  PERMISSION_DENIED: If the reseller account making the request
           and the reseller account being queried for are different.
        -  INVALID_ARGUMENT: Missing or invalid required parameters in
           the request.

        Return Value: List of
        [Customer][google.cloud.channel.v1.Customer]s pertaining to the
        reseller or empty list if there are none.

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

        Returns a requested [Customer][google.cloud.channel.v1.Customer]
        resource.

        Possible Error Codes:

        -  PERMISSION_DENIED: If the reseller account making the request
           and the reseller account being queried for are different.
        -  INVALID_ARGUMENT: Missing or invalid required parameters in
           the request.
        -  NOT_FOUND: If the customer resource doesn't exist. Usually
           the result of an invalid name parameter.

        Return Value: [Customer][google.cloud.channel.v1.Customer]
        resource if found, error otherwise.

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

        Confirms the existence of Cloud Identity accounts, based on the
        domain and whether the Cloud Identity accounts are owned by the
        reseller.

        Possible Error Codes:

        -  PERMISSION_DENIED: If the reseller account making the request
           and the reseller account being queried for are different.
        -  INVALID_ARGUMENT: Missing or invalid required parameters in
           the request.
        -  INVALID_VALUE: Invalid domain value in the request.
        -  NOT_FOUND: If there is no
           [CloudIdentityCustomerAccount][google.cloud.channel.v1.CloudIdentityCustomerAccount]
           customer for the domain specified in the request.

        Return Value: List of
        [CloudIdentityCustomerAccount][google.cloud.channel.v1.CloudIdentityCustomerAccount]
        resources if any exist for the domain, otherwise an error is
        returned.

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

        Possible Error Codes:

        .. raw:: html

            <ul>
            <li>PERMISSION_DENIED: If the reseller account making the request and the
            reseller account being queried for are different.</li>
            <li> INVALID_ARGUMENT:
            <ul>
             <li> Missing or invalid required parameters in the request. </li>
             <li> Domain field value doesn't match the domain specified in primary
             email.</li>
            </ul>
            </li>
            </ul>

        Return Value: If successful, the newly created
        [Customer][google.cloud.channel.v1.Customer] resource, otherwise
        returns an error.

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
        resource belonging to the reseller or distributor.

        Possible Error Codes:

        -  PERMISSION_DENIED: If the reseller account making the request
           and the reseller account being queried for are different.
        -  INVALID_ARGUMENT: Missing or invalid required parameters in
           the request.
        -  NOT_FOUND: No [Customer][google.cloud.channel.v1.Customer]
           resource found for the name specified in the request.

        Return Value: If successful, the updated
        [Customer][google.cloud.channel.v1.Customer] resource, otherwise
        returns an error.

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
    def delete_customer(self) -> Callable[[service.DeleteCustomerRequest], empty.Empty]:
        r"""Return a callable for the delete customer method over gRPC.

        Deletes the given [Customer][google.cloud.channel.v1.Customer]
        permanently and irreversibly.

        Possible Error Codes:

        -  PERMISSION_DENIED: If the account making the request does not
           own this customer.
        -  INVALID_ARGUMENT: Missing or invalid required parameters in
           the request.
        -  FAILED_PRECONDITION: If the customer has existing
           entitlements.
        -  NOT_FOUND: No [Customer][google.cloud.channel.v1.Customer]
           resource found for the name specified in the request.

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
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["delete_customer"]

    @property
    def provision_cloud_identity(
        self,
    ) -> Callable[[service.ProvisionCloudIdentityRequest], operations.Operation]:
        r"""Return a callable for the provision cloud identity method over gRPC.

        Creates a Cloud Identity for the given customer using the
        customer's information or the information provided here, if
        present.

        Possible Error Codes:

        -  PERMISSION_DENIED: If the customer doesn't belong to the
           reseller.
        -  INVALID_ARGUMENT: Missing or invalid required parameters in
           the request.
        -  NOT_FOUND: If the customer is not found for the reseller.
        -  ALREADY_EXISTS: If the customer's primary email already
           exists. In this case, retry after changing the customer's
           primary contact email.
        -  INTERNAL: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support in this case.
        -  UNKNOWN: Any non-user error related to a technical issue in
           the backend. Contact Cloud Channel support in this case.

        Return Value: Long Running Operation ID.

        To get the results of the operation, call the GetOperation
        method of CloudChannelOperationsService. The Operation metadata
        will contain an instance of
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
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["provision_cloud_identity"]

    @property
    def list_entitlements(
        self,
    ) -> Callable[[service.ListEntitlementsRequest], service.ListEntitlementsResponse]:
        r"""Return a callable for the list entitlements method over gRPC.

        List [Entitlement][google.cloud.channel.v1.Entitlement]s
        belonging to a customer.

        Possible Error Codes:

        -  PERMISSION_DENIED: If the customer doesn't belong to the
           reseller.
        -  INVALID_ARGUMENT: Missing or invalid required parameters in
           the request.

        Return Value: List of
        [Entitlement][google.cloud.channel.v1.Entitlement]s belonging to
        the customer, or empty list if there are none.

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
        of a customer based on Cloud Identity ID or Customer Name in the
        request.

        This method is used when a reseller lists the entitlements
        information of a customer that is not owned. The reseller should
        provide the customer's Cloud Identity ID or Customer Name.

        Possible Error Codes:

        .. raw:: html

            <ul>
            <li>PERMISSION_DENIED, due to one of the following reasons:
            <ul>
               <li> If the customer doesn't belong to the reseller and no auth token,
               or an invalid auth token is supplied. </li> <li> If the reseller account
               making the request and the reseller account being queried for are
               different. </li>
            </ul>
            </li>
            <li> INVALID_ARGUMENT: Missing or invalid required parameters in the
            request.</li>
            </ul>

        Return Value: List of
        [TransferableSku][google.cloud.channel.v1.TransferableSku] for
        the given customer.

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

        This method is used when a reseller gets the entitlement
        information of a customer that is not owned. The reseller should
        provide the customer's Cloud Identity ID or Customer Name.

        Possible Error Codes:

        -  PERMISSION_DENIED, due to one of the following reasons: (a)
           If the customer doesn't belong to the reseller and no auth
           token or invalid auth token is supplied. (b) If the reseller
           account making the request and the reseller account being
           queried for are different.
        -  INVALID_ARGUMENT: Missing or invalid required parameters in
           the request.

        Return Value: List of
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

        Returns a requested
        [Entitlement][google.cloud.channel.v1.Entitlement] resource.

        Possible Error Codes:

        -  PERMISSION_DENIED: If the customer doesn't belong to the
           reseller.
        -  INVALID_ARGUMENT: Missing or invalid required parameters in
           the request.
        -  NOT_FOUND: If the entitlement is not found for the customer.

        Return Value: If found, the requested
        [Entitlement][google.cloud.channel.v1.Entitlement] resource,
        otherwise returns an error.

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
    ) -> Callable[[service.CreateEntitlementRequest], operations.Operation]:
        r"""Return a callable for the create entitlement method over gRPC.

        Creates an entitlement for a customer.

        Possible Error Codes:

        .. raw:: html

            <ul>
            <li> PERMISSION_DENIED: If the customer doesn't belong to the reseller.
            </li> <li> INVALID_ARGUMENT: <ul>
              <li> Missing or invalid required parameters in the request. </li>
              <li> Cannot purchase an entitlement if there is already an
               entitlement for customer, for a SKU from the same product family. </li>
              <li> INVALID_VALUE: Offer passed in isn't valid. Make sure OfferId is
            valid. If it is valid, then contact Google Channel support for further
            troubleshooting. </li>
            </ul>
            </li>
            <li> NOT_FOUND: If the customer or offer resource is not found for the
            reseller. </li>
            <li> ALREADY_EXISTS: This failure can happen in the following cases:
              <ul>
                <li>If the SKU has been already purchased for the customer.</li>
                <li>If the customer's primary email already exists. In this case retry
                    after changing the customer's primary contact email.
                </li>
              </ul>
            </li>
            <li> CONDITION_NOT_MET or FAILED_PRECONDITION: This
            failure can happen in the following cases:
            <ul>
               <li> Purchasing a SKU that requires domain verification and the
               domain has not been verified. </li>
               <li> Purchasing an Add-On SKU like Vault or Drive without purchasing
               the pre-requisite SKU, such as Google Workspace Business Starter. </li>
               <li> Applicable only for developer accounts: reseller and resold
               domain. Must meet the following domain naming requirements:
                <ul>
                  <li> Domain names must start with goog-test. </li>
                  <li> Resold domain names must include the reseller domain. </li>
                </ul>
               </li>
            </ul>
            </li>
            <li> INTERNAL: Any non-user error related to a technical issue in the
            backend. Contact Cloud Channel Support in this case. </li>
            <li> UNKNOWN: Any non-user error related to a technical issue in the
            backend. Contact Cloud Channel Support in this case. </li>
            </ul>

        Return Value: Long Running Operation ID.

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
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["create_entitlement"]

    @property
    def change_parameters(
        self,
    ) -> Callable[[service.ChangeParametersRequest], operations.Operation]:
        r"""Return a callable for the change parameters method over gRPC.

        Change parameters of the entitlement

        An entitlement parameters update is a long-running operation and
        results in updates to the entitlement as a result of
        fulfillment.

        Possible Error Codes:

        -  PERMISSION_DENIED: If the customer doesn't belong to the
           reseller.
        -  INVALID_ARGUMENT: Missing or invalid required parameters in
           the request. For example, if the number of seats being
           changed to is greater than the allowed number of max seats
           for the resource. Or decreasing seats for a commitment based
           plan.
        -  NOT_FOUND: Entitlement resource not found.
        -  INTERNAL: Any non-user error related to a technical issue in
           the backend. In this case, contact Cloud Channel support.
        -  UNKNOWN: Any non-user error related to a technical issue in
           the backend. In this case, contact Cloud Channel support.

        Return Value: Long Running Operation ID.

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
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["change_parameters"]

    @property
    def change_renewal_settings(
        self,
    ) -> Callable[[service.ChangeRenewalSettingsRequest], operations.Operation]:
        r"""Return a callable for the change renewal settings method over gRPC.

        Updates the renewal settings for an existing customer
        entitlement.

        An entitlement update is a long-running operation and results in
        updates to the entitlement as a result of fulfillment.

        Possible Error Codes:

        -  PERMISSION_DENIED: If the customer doesn't belong to the
           reseller.
        -  INVALID_ARGUMENT: Missing or invalid required parameters in
           the request.
        -  NOT_FOUND: Entitlement resource not found.
        -  NOT_COMMITMENT_PLAN: Renewal Settings are only applicable for
           a commitment plan. Can't enable or disable renewal for
           non-commitment plans.
        -  INTERNAL: Any non user error related to a technical issue in
           the backend. In this case, contact Cloud Channel support.
        -  UNKNOWN: Any non user error related to a technical issue in
           the backend. In this case, contact Cloud Channel support.

        Return Value: Long Running Operation ID.

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
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["change_renewal_settings"]

    @property
    def change_offer(
        self,
    ) -> Callable[[service.ChangeOfferRequest], operations.Operation]:
        r"""Return a callable for the change offer method over gRPC.

        Updates the Offer for an existing customer entitlement.

        An entitlement update is a long-running operation and results in
        updates to the entitlement as a result of fulfillment.

        Possible Error Codes:

        -  PERMISSION_DENIED: If the customer doesn't belong to the
           reseller.
        -  INVALID_ARGUMENT: Missing or invalid required parameters in
           the request.
        -  NOT_FOUND: Offer or Entitlement resource not found.
        -  INTERNAL: Any non-user error related to a technical issue in
           the backend. In this case, contact Cloud Channel support.
        -  UNKNOWN: Any non-user error related to a technical issue in
           the backend. In this case, contact Cloud Channel support.

        Return Value: Long Running Operation ID.

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
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["change_offer"]

    @property
    def start_paid_service(
        self,
    ) -> Callable[[service.StartPaidServiceRequest], operations.Operation]:
        r"""Return a callable for the start paid service method over gRPC.

        Starts paid service for a trial entitlement.

        Starts paid service for a trial entitlement immediately. This
        method is only applicable if a plan has already been set up for
        a trial entitlement but has some trial days remaining.

        Possible Error Codes:

        -  PERMISSION_DENIED: If the customer doesn't belong to the
           reseller.
        -  INVALID_ARGUMENT: Missing or invalid required parameters in
           the request.
        -  NOT_FOUND: Entitlement resource not found.
        -  FAILED_PRECONDITION/NOT_IN_TRIAL: This method only works for
           entitlement on trial plans.
        -  INTERNAL: Any non-user error related to a technical issue in
           the backend. In this case, contact Cloud Channel support.
        -  UNKNOWN: Any non-user error related to a technical issue in
           the backend. In this case, contact Cloud Channel support.

        Return Value: Long Running Operation ID.

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
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["start_paid_service"]

    @property
    def suspend_entitlement(
        self,
    ) -> Callable[[service.SuspendEntitlementRequest], operations.Operation]:
        r"""Return a callable for the suspend entitlement method over gRPC.

        Suspends a previously fulfilled entitlement. An entitlement
        suspension is a long-running operation.

        Possible Error Codes:

        -  PERMISSION_DENIED: If the customer doesn't belong to the
           reseller.
        -  INVALID_ARGUMENT: Missing or invalid required parameters in
           the request.
        -  NOT_FOUND: Entitlement resource not found.
        -  NOT_ACTIVE: Entitlement is not active.
        -  INTERNAL: Any non-user error related to a technical issue in
           the backend. In this case, contact Cloud Channel support.
        -  UNKNOWN: Any non-user error related to a technical issue in
           the backend. In this case, contact Cloud Channel support.

        Return Value: Long Running Operation ID.

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
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["suspend_entitlement"]

    @property
    def cancel_entitlement(
        self,
    ) -> Callable[[service.CancelEntitlementRequest], operations.Operation]:
        r"""Return a callable for the cancel entitlement method over gRPC.

        Cancels a previously fulfilled entitlement. An entitlement
        cancellation is a long-running operation.

        Possible Error Codes:

        -  PERMISSION_DENIED: If the customer doesn't belong to the
           reseller or if the reseller account making the request and
           reseller account being queried for are different.
        -  FAILED_PRECONDITION: If there are any Google Cloud projects
           linked to the Google Cloud entitlement's Cloud Billing
           subaccount.
        -  INVALID_ARGUMENT: Missing or invalid required parameters in
           the request.
        -  NOT_FOUND: Entitlement resource not found.
        -  DELETION_TYPE_NOT_ALLOWED: Cancel is only allowed for Google
           Workspace add-ons or entitlements for Google Cloud's
           development platform.
        -  INTERNAL: Any non-user error related to a technical issue in
           the backend. In this case, contact Cloud Channel support.
        -  UNKNOWN: Any non-user error related to a technical issue in
           the backend. In this case, contact Cloud Channel support.

        Return Value: Long Running Operation ID.

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
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["cancel_entitlement"]

    @property
    def activate_entitlement(
        self,
    ) -> Callable[[service.ActivateEntitlementRequest], operations.Operation]:
        r"""Return a callable for the activate entitlement method over gRPC.

        Activates a previously suspended entitlement. The entitlement
        must be in a suspended state for it to be activated.
        Entitlements suspended for pending ToS acceptance can't be
        activated using this method. An entitlement activation is a
        long-running operation and can result in updates to the state of
        the customer entitlement.

        Possible Error Codes:

        -  PERMISSION_DENIED: If the customer doesn't belong to the
           reseller or if the reseller account making the request and
           reseller account being queried for are different.
        -  INVALID_ARGUMENT: Missing or invalid required parameters in
           the request.
        -  NOT_FOUND: Entitlement resource not found.
        -  SUSPENSION_NOT_RESELLER_INITIATED: Can't activate an
           entitlement that is pending TOS acceptance. Only reseller
           initiated suspensions can be activated.
        -  NOT_SUSPENDED: Can't activate entitlements that are already
           in ACTIVE state. Can only activate suspended entitlements.
        -  INTERNAL: Any non-user error related to a technical issue in
           the backend. In this case, contact Cloud Channel support.
        -  UNKNOWN: Any non-user error related to a technical issue in
           the backend. In this case, contact Cloud Channel support.

        Return Value: Long Running Operation ID.

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
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["activate_entitlement"]

    @property
    def transfer_entitlements(
        self,
    ) -> Callable[[service.TransferEntitlementsRequest], operations.Operation]:
        r"""Return a callable for the transfer entitlements method over gRPC.

        Transfers customer entitlements to new reseller.

        Possible Error Codes:

        .. raw:: html

            <ul>
            <li> PERMISSION_DENIED: If the customer doesn't belong to the
            reseller.</li> <li> INVALID_ARGUMENT: Missing or invalid required
            parameters in the request. </li> <li> NOT_FOUND: If the customer or offer
            resource is not found for the reseller. </li> <li> ALREADY_EXISTS: If the
            SKU has been already transferred for the customer. </li> <li>
            CONDITION_NOT_MET or FAILED_PRECONDITION: This failure can happen in the
            following cases: <ul>
               <li> Transferring a SKU that requires domain verification and the
            domain has not been verified. </li>
               <li> Transferring an Add-On SKU like Vault or Drive without transferring
            the pre-requisite SKU, such as G Suite Basic </li> <li> Applicable only for
            developer accounts: reseller and resold domain must follow the domain
            naming convention as follows:
                 <ul>
                    <li> Domain names must start with goog-test. </li>
                    <li> Resold domain names must include the reseller domain. </li>
                 </ul>
              </li>
              <li> All transferring entitlements must be specified. </li>
            </ul>
            </li>
            <li> INTERNAL: Any non-user error related to a technical issue in the
            backend. Please contact Cloud Channel Support in this case. </li>
            <li> UNKNOWN: Any non-user error related to a technical issue in the
            backend. Please contact Cloud Channel Support in this case. </li>
            </ul>

        Return Value: Long Running Operation ID.

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
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["transfer_entitlements"]

    @property
    def transfer_entitlements_to_google(
        self,
    ) -> Callable[[service.TransferEntitlementsToGoogleRequest], operations.Operation]:
        r"""Return a callable for the transfer entitlements to
        google method over gRPC.

        Transfers customer entitlements from current reseller to Google.

        Possible Error Codes:

        .. raw:: html

            <ul>
            <li> PERMISSION_DENIED: If the customer doesn't belong to the reseller.
            </li> <li> INVALID_ARGUMENT: Missing or invalid required parameters in the
            request. </li>
            <li> NOT_FOUND: If the customer or offer resource is not found
            for the reseller. </li>
            <li> ALREADY_EXISTS: If the SKU has been already
            transferred for the customer. </li>
            <li> CONDITION_NOT_MET or FAILED_PRECONDITION: This failure can happen in
            the following cases:
            <ul>
               <li> Transferring a SKU that requires domain verification and the
            domain has not been verified. </li>
               <li> Transferring an Add-On SKU like Vault or Drive without purchasing
            the pre-requisite SKU, such as G Suite Basic </li> <li> Applicable only for
            developer accounts: reseller and resold domain must follow the domain
            naming convention as follows:
                 <ul>
                    <li> Domain names must start with goog-test. </li>
                    <li> Resold domain names must include the reseller domain. </li>
                 </ul>
               </li>
            </ul>
            </li>
            <li> INTERNAL: Any non-user error related to a technical issue in the
            backend. Please contact Cloud Channel Support in this case. </li>
            <li> UNKNOWN: Any non-user error related to a technical issue in the
            backend. Please contact Cloud Channel Support in this case.</li>
            </ul>

        Return Value: Long Running Operation ID.

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
                response_deserializer=operations.Operation.FromString,
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
        belonging to a distributor. To call this method, you must be a
        distributor.

        Possible Error Codes:

        -  PERMISSION_DENIED: If the reseller account making the request
           and the reseller account being queried for are different.
        -  INVALID_ARGUMENT: Missing or invalid required parameters in
           the request.

        Return Value: If successful, returns the list of
        [ChannelPartnerLink][google.cloud.channel.v1.ChannelPartnerLink]
        resources for the distributor account, otherwise returns an
        error.

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

        Returns a requested
        [ChannelPartnerLink][google.cloud.channel.v1.ChannelPartnerLink]
        resource. To call this method, you must be a distributor.

        Possible Error Codes:

        -  PERMISSION_DENIED: If the reseller account making the request
           and the reseller account being queried for are different.
        -  INVALID_ARGUMENT: Missing or invalid required parameters in
           the request.
        -  NOT_FOUND: ChannelPartnerLink resource not found. Results due
           invalid channel partner link name.

        Return Value:
        [ChannelPartnerLink][google.cloud.channel.v1.ChannelPartnerLink]
        resource if found, otherwise returns an error.

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
        reseller or between resellers in an n-tier reseller channel. To
        accept the invite, the invited partner should follow the
        invite_link_uri provided in the response. If the link creation
        is accepted, a valid link is set up between the two involved
        parties. To call this method, you must be a distributor.

        Possible Error Codes:

        -  PERMISSION_DENIED: If the reseller account making the request
           and the reseller account being queried for are different.
        -  INVALID_ARGUMENT: Missing or invalid required parameters in
           the request.
        -  ALREADY_EXISTS: If the ChannelPartnerLink sent in the request
           already exists.
        -  NOT_FOUND: If no Cloud Identity customer exists for domain
           provided.
        -  INTERNAL: Any non-user error related to a technical issue in
           the backend. In this case, contact Cloud Channel support.
        -  UNKNOWN: Any non-user error related to a technical issue in
           the backend. In this case, contact Cloud Channel support.

        Return Value: Newly created
        [ChannelPartnerLink][google.cloud.channel.v1.ChannelPartnerLink]
        resource if successful, otherwise error is returned.

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

        Updates a channel partner link. A distributor calls this method
        to change a link's status. For example, suspend a partner link.
        To call this method, you must be a distributor.

        Possible Error Codes:

        .. raw:: html

            <ul>
            <li> PERMISSION_DENIED: If the reseller account making the request and the
            reseller account being queried for are different. </li>
            <li> INVALID_ARGUMENT:
            <ul>
              <li> Missing or invalid required parameters in the request. </li>
              <li> Updating link state from invited to active or suspended. </li>
              <li> Sending reseller_cloud_identity_id, invite_url or name in update
              mask. </li>
            </ul>
            </li>
            <li> NOT_FOUND: ChannelPartnerLink resource not found.</li>
            <li> INTERNAL: Any non-user error related to a technical issue in the
            backend. In this case, contact Cloud Channel support. </li>
            <li> UNKNOWN: Any non-user error related to a technical issue in the
            backend. In this case, contact Cloud Channel support.</li>
            </ul>

        Return Value: If successful, the updated
        [ChannelPartnerLink][google.cloud.channel.v1.ChannelPartnerLink]
        resource, otherwise returns an error.

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
    def list_products(
        self,
    ) -> Callable[[service.ListProductsRequest], service.ListProductsResponse]:
        r"""Return a callable for the list products method over gRPC.

        Lists the Products the reseller is authorized to sell.

        Possible Error Codes:

        -  INVALID_ARGUMENT: Missing or invalid required parameters in
           the request.

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

        Possible Error Codes:

        -  INVALID_ARGUMENT: Missing or invalid required parameters in
           the request.

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

        Possible Error Codes:

        -  INVALID_ARGUMENT: Missing or invalid required parameters in
           the request.

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

        Lists the Purchasable SKUs for following cases:

        -  SKUs that can be newly purchased for a customer
        -  SKUs that can be upgraded/downgraded to, for an entitlement.

        Possible Error Codes:

        -  PERMISSION_DENIED: If the customer doesn't belong to the
           reseller
        -  INVALID_ARGUMENT: Missing or invalid required parameters in
           the request.

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

        Lists the Purchasable Offers for the following cases:

        -  Offers that can be newly purchased for a customer
        -  Offers that can be changed to, for an entitlement.

        Possible Error Codes:

        -  PERMISSION_DENIED: If the customer doesn't belong to the
           reseller
        -  INVALID_ARGUMENT: Missing or invalid required parameters in
           the request.

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


__all__ = ("CloudChannelServiceGrpcTransport",)
