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
from collections import OrderedDict
import functools
import re
from typing import Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.channel_v1.services.cloud_channel_service import pagers
from google.cloud.channel_v1.types import channel_partner_links
from google.cloud.channel_v1.types import common
from google.cloud.channel_v1.types import customers
from google.cloud.channel_v1.types import entitlements
from google.cloud.channel_v1.types import offers
from google.cloud.channel_v1.types import operations
from google.cloud.channel_v1.types import products
from google.cloud.channel_v1.types import service
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.type import postal_address_pb2  # type: ignore
from .transports.base import CloudChannelServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import CloudChannelServiceGrpcAsyncIOTransport
from .client import CloudChannelServiceClient


class CloudChannelServiceAsyncClient:
    """CloudChannelService lets Google cloud resellers and distributors
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
    """

    _client: CloudChannelServiceClient

    DEFAULT_ENDPOINT = CloudChannelServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = CloudChannelServiceClient.DEFAULT_MTLS_ENDPOINT

    customer_path = staticmethod(CloudChannelServiceClient.customer_path)
    parse_customer_path = staticmethod(CloudChannelServiceClient.parse_customer_path)
    entitlement_path = staticmethod(CloudChannelServiceClient.entitlement_path)
    parse_entitlement_path = staticmethod(
        CloudChannelServiceClient.parse_entitlement_path
    )
    offer_path = staticmethod(CloudChannelServiceClient.offer_path)
    parse_offer_path = staticmethod(CloudChannelServiceClient.parse_offer_path)
    product_path = staticmethod(CloudChannelServiceClient.product_path)
    parse_product_path = staticmethod(CloudChannelServiceClient.parse_product_path)
    sku_path = staticmethod(CloudChannelServiceClient.sku_path)
    parse_sku_path = staticmethod(CloudChannelServiceClient.parse_sku_path)
    common_billing_account_path = staticmethod(
        CloudChannelServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        CloudChannelServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(CloudChannelServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        CloudChannelServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        CloudChannelServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        CloudChannelServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(CloudChannelServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        CloudChannelServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(CloudChannelServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        CloudChannelServiceClient.parse_common_location_path
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            CloudChannelServiceAsyncClient: The constructed client.
        """
        return CloudChannelServiceClient.from_service_account_info.__func__(CloudChannelServiceAsyncClient, info, *args, **kwargs)  # type: ignore

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            CloudChannelServiceAsyncClient: The constructed client.
        """
        return CloudChannelServiceClient.from_service_account_file.__func__(CloudChannelServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> CloudChannelServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            CloudChannelServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(CloudChannelServiceClient).get_transport_class,
        type(CloudChannelServiceClient),
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, CloudChannelServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the cloud channel service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.CloudChannelServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = CloudChannelServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_customers(
        self,
        request: service.ListCustomersRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCustomersAsyncPager:
        r"""List [Customer][google.cloud.channel.v1.Customer]s.

        Possible error codes:

        -  PERMISSION_DENIED: The reseller account making the request is
           different from the reseller account in the API request.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.

        Return value: List of
        [Customer][google.cloud.channel.v1.Customer]s, or an empty list
        if there are no customers.

        Args:
            request (:class:`google.cloud.channel_v1.types.ListCustomersRequest`):
                The request object. Request message for
                [CloudChannelService.ListCustomers][google.cloud.channel.v1.CloudChannelService.ListCustomers]
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.channel_v1.services.cloud_channel_service.pagers.ListCustomersAsyncPager:
                Response message for
                [CloudChannelService.ListCustomers][google.cloud.channel.v1.CloudChannelService.ListCustomers].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        request = service.ListCustomersRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_customers,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListCustomersAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_customer(
        self,
        request: service.GetCustomerRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> customers.Customer:
        r"""Returns the requested
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

        Args:
            request (:class:`google.cloud.channel_v1.types.GetCustomerRequest`):
                The request object. Request message for
                [CloudChannelService.GetCustomer][google.cloud.channel.v1.CloudChannelService.GetCustomer].
            name (:class:`str`):
                Required. The resource name of the customer to retrieve.
                Name uses the format:
                accounts/{account_id}/customers/{customer_id}

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.channel_v1.types.Customer:
                Entity representing a customer of a
                reseller or distributor.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.GetCustomerRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_customer,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def check_cloud_identity_accounts_exist(
        self,
        request: service.CheckCloudIdentityAccountsExistRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> service.CheckCloudIdentityAccountsExistResponse:
        r"""Confirms the existence of Cloud Identity accounts based on the
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

        Args:
            request (:class:`google.cloud.channel_v1.types.CheckCloudIdentityAccountsExistRequest`):
                The request object. Request message for
                [CloudChannelService.CheckCloudIdentityAccountsExist][google.cloud.channel.v1.CloudChannelService.CheckCloudIdentityAccountsExist].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.channel_v1.types.CheckCloudIdentityAccountsExistResponse:
                Response message for
                   [CloudChannelService.CheckCloudIdentityAccountsExist][google.cloud.channel.v1.CloudChannelService.CheckCloudIdentityAccountsExist].

        """
        # Create or coerce a protobuf request object.
        request = service.CheckCloudIdentityAccountsExistRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.check_cloud_identity_accounts_exist,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def create_customer(
        self,
        request: service.CreateCustomerRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> customers.Customer:
        r"""Creates a new [Customer][google.cloud.channel.v1.Customer]
        resource under the reseller or distributor account.

        Possible error codes:

        -  PERMISSION_DENIED: The reseller account making the request is
           different from the reseller account in the API request.
        -  INVALID_ARGUMENT:

           -  Required request parameters are missing or invalid.
           -  Domain field value doesn't match the primary email domain.

        Return value: The newly created
        [Customer][google.cloud.channel.v1.Customer] resource.

        Args:
            request (:class:`google.cloud.channel_v1.types.CreateCustomerRequest`):
                The request object. Request message for
                [CloudChannelService.CreateCustomer][google.cloud.channel.v1.CloudChannelService.CreateCustomer]
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.channel_v1.types.Customer:
                Entity representing a customer of a
                reseller or distributor.

        """
        # Create or coerce a protobuf request object.
        request = service.CreateCustomerRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_customer,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def update_customer(
        self,
        request: service.UpdateCustomerRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> customers.Customer:
        r"""Updates an existing [Customer][google.cloud.channel.v1.Customer]
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

        Args:
            request (:class:`google.cloud.channel_v1.types.UpdateCustomerRequest`):
                The request object. Request message for
                [CloudChannelService.UpdateCustomer][google.cloud.channel.v1.CloudChannelService.UpdateCustomer].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.channel_v1.types.Customer:
                Entity representing a customer of a
                reseller or distributor.

        """
        # Create or coerce a protobuf request object.
        request = service.UpdateCustomerRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_customer,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("customer.name", request.customer.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_customer(
        self,
        request: service.DeleteCustomerRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the given [Customer][google.cloud.channel.v1.Customer]
        permanently.

        Possible error codes:

        -  PERMISSION_DENIED: The account making the request does not
           own this customer.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.
        -  FAILED_PRECONDITION: The customer has existing entitlements.
        -  NOT_FOUND: No [Customer][google.cloud.channel.v1.Customer]
           resource found for the name in the request.

        Args:
            request (:class:`google.cloud.channel_v1.types.DeleteCustomerRequest`):
                The request object. Request message for
                [CloudChannelService.DeleteCustomer][google.cloud.channel.v1.CloudChannelService.DeleteCustomer].
            name (:class:`str`):
                Required. The resource name of the
                customer to delete.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service.DeleteCustomerRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_customer,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    async def provision_cloud_identity(
        self,
        request: service.ProvisionCloudIdentityRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a Cloud Identity for the given customer using the
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

        Args:
            request (:class:`google.cloud.channel_v1.types.ProvisionCloudIdentityRequest`):
                The request object. Request message for
                [CloudChannelService.ProvisionCloudIdentity][google.cloud.channel.v1.CloudChannelService.ProvisionCloudIdentity]
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.channel_v1.types.Customer` Entity
                representing a customer of a reseller or distributor.

        """
        # Create or coerce a protobuf request object.
        request = service.ProvisionCloudIdentityRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.provision_cloud_identity,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("customer", request.customer),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            customers.Customer,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_entitlements(
        self,
        request: service.ListEntitlementsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListEntitlementsAsyncPager:
        r"""Lists [Entitlement][google.cloud.channel.v1.Entitlement]s
        belonging to a customer.

        Possible error codes:

        -  PERMISSION_DENIED: The customer doesn't belong to the
           reseller.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.

        Return value: A list of the customer's
        [Entitlement][google.cloud.channel.v1.Entitlement]s.

        Args:
            request (:class:`google.cloud.channel_v1.types.ListEntitlementsRequest`):
                The request object. Request message for
                [CloudChannelService.ListEntitlements][google.cloud.channel.v1.CloudChannelService.ListEntitlements]
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.channel_v1.services.cloud_channel_service.pagers.ListEntitlementsAsyncPager:
                Response message for
                [CloudChannelService.ListEntitlements][google.cloud.channel.v1.CloudChannelService.ListEntitlements].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        request = service.ListEntitlementsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_entitlements,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListEntitlementsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_transferable_skus(
        self,
        request: service.ListTransferableSkusRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTransferableSkusAsyncPager:
        r"""List [TransferableSku][google.cloud.channel.v1.TransferableSku]s
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

        Args:
            request (:class:`google.cloud.channel_v1.types.ListTransferableSkusRequest`):
                The request object. Request message for
                [CloudChannelService.ListTransferableSkus][google.cloud.channel.v1.CloudChannelService.ListTransferableSkus]
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.channel_v1.services.cloud_channel_service.pagers.ListTransferableSkusAsyncPager:
                Response message for
                [CloudChannelService.ListTransferableSkus][google.cloud.channel.v1.CloudChannelService.ListTransferableSkus].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        request = service.ListTransferableSkusRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_transferable_skus,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListTransferableSkusAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_transferable_offers(
        self,
        request: service.ListTransferableOffersRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTransferableOffersAsyncPager:
        r"""List
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

        Args:
            request (:class:`google.cloud.channel_v1.types.ListTransferableOffersRequest`):
                The request object. Request message for
                [CloudChannelService.ListTransferableOffers][google.cloud.channel.v1.CloudChannelService.ListTransferableOffers]
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.channel_v1.services.cloud_channel_service.pagers.ListTransferableOffersAsyncPager:
                Response message for
                [CloudChannelService.ListTransferableOffers][google.cloud.channel.v1.CloudChannelService.ListTransferableOffers].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        request = service.ListTransferableOffersRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_transferable_offers,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListTransferableOffersAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_entitlement(
        self,
        request: service.GetEntitlementRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> entitlements.Entitlement:
        r"""Returns the requested
        [Entitlement][google.cloud.channel.v1.Entitlement] resource.

        Possible error codes:

        -  PERMISSION_DENIED: The customer doesn't belong to the
           reseller.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.
        -  NOT_FOUND: The customer entitlement was not found.

        Return value: The requested
        [Entitlement][google.cloud.channel.v1.Entitlement] resource.

        Args:
            request (:class:`google.cloud.channel_v1.types.GetEntitlementRequest`):
                The request object. Request message for
                [CloudChannelService.GetEntitlement][google.cloud.channel.v1.CloudChannelService.GetEntitlement].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.channel_v1.types.Entitlement:
                An entitlement is a representation of
                a customer's ability to use a service.

        """
        # Create or coerce a protobuf request object.
        request = service.GetEntitlementRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_entitlement,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def create_entitlement(
        self,
        request: service.CreateEntitlementRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates an entitlement for a customer.

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

        Args:
            request (:class:`google.cloud.channel_v1.types.CreateEntitlementRequest`):
                The request object. Request message for
                [CloudChannelService.CreateEntitlement][google.cloud.channel.v1.CloudChannelService.CreateEntitlement]
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.channel_v1.types.Entitlement` An
                entitlement is a representation of a customer's ability
                to use a service.

        """
        # Create or coerce a protobuf request object.
        request = service.CreateEntitlementRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_entitlement,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            entitlements.Entitlement,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def change_parameters(
        self,
        request: service.ChangeParametersRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Change parameters of the entitlement.

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

        Args:
            request (:class:`google.cloud.channel_v1.types.ChangeParametersRequest`):
                The request object. Request message for
                [CloudChannelService.ChangeParametersRequest][].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.channel_v1.types.Entitlement` An
                entitlement is a representation of a customer's ability
                to use a service.

        """
        # Create or coerce a protobuf request object.
        request = service.ChangeParametersRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.change_parameters,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            entitlements.Entitlement,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def change_renewal_settings(
        self,
        request: service.ChangeRenewalSettingsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates the renewal settings for an existing customer
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

        Args:
            request (:class:`google.cloud.channel_v1.types.ChangeRenewalSettingsRequest`):
                The request object. Request message for
                [CloudChannelService.ChangeRenewalSettings][google.cloud.channel.v1.CloudChannelService.ChangeRenewalSettings].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.channel_v1.types.Entitlement` An
                entitlement is a representation of a customer's ability
                to use a service.

        """
        # Create or coerce a protobuf request object.
        request = service.ChangeRenewalSettingsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.change_renewal_settings,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            entitlements.Entitlement,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def change_offer(
        self,
        request: service.ChangeOfferRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates the Offer for an existing customer entitlement.

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

        Args:
            request (:class:`google.cloud.channel_v1.types.ChangeOfferRequest`):
                The request object. Request message for
                [CloudChannelService.ChangeOffer][google.cloud.channel.v1.CloudChannelService.ChangeOffer].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.channel_v1.types.Entitlement` An
                entitlement is a representation of a customer's ability
                to use a service.

        """
        # Create or coerce a protobuf request object.
        request = service.ChangeOfferRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.change_offer,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            entitlements.Entitlement,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def start_paid_service(
        self,
        request: service.StartPaidServiceRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Starts paid service for a trial entitlement.

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

        Args:
            request (:class:`google.cloud.channel_v1.types.StartPaidServiceRequest`):
                The request object. Request message for
                [CloudChannelService.StartPaidService][google.cloud.channel.v1.CloudChannelService.StartPaidService].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.channel_v1.types.Entitlement` An
                entitlement is a representation of a customer's ability
                to use a service.

        """
        # Create or coerce a protobuf request object.
        request = service.StartPaidServiceRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.start_paid_service,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            entitlements.Entitlement,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def suspend_entitlement(
        self,
        request: service.SuspendEntitlementRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Suspends a previously fulfilled entitlement.

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

        Args:
            request (:class:`google.cloud.channel_v1.types.SuspendEntitlementRequest`):
                The request object. Request message for
                [CloudChannelService.SuspendEntitlement][google.cloud.channel.v1.CloudChannelService.SuspendEntitlement].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.channel_v1.types.Entitlement` An
                entitlement is a representation of a customer's ability
                to use a service.

        """
        # Create or coerce a protobuf request object.
        request = service.SuspendEntitlementRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.suspend_entitlement,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            entitlements.Entitlement,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def cancel_entitlement(
        self,
        request: service.CancelEntitlementRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Cancels a previously fulfilled entitlement.

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

        Args:
            request (:class:`google.cloud.channel_v1.types.CancelEntitlementRequest`):
                The request object. Request message for
                [CloudChannelService.CancelEntitlement][google.cloud.channel.v1.CloudChannelService.CancelEntitlement].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

        """
        # Create or coerce a protobuf request object.
        request = service.CancelEntitlementRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.cancel_entitlement,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def activate_entitlement(
        self,
        request: service.ActivateEntitlementRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Activates a previously suspended entitlement. Entitlements
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

        Args:
            request (:class:`google.cloud.channel_v1.types.ActivateEntitlementRequest`):
                The request object. Request message for
                [CloudChannelService.ActivateEntitlement][google.cloud.channel.v1.CloudChannelService.ActivateEntitlement].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.channel_v1.types.Entitlement` An
                entitlement is a representation of a customer's ability
                to use a service.

        """
        # Create or coerce a protobuf request object.
        request = service.ActivateEntitlementRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.activate_entitlement,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            entitlements.Entitlement,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def transfer_entitlements(
        self,
        request: service.TransferEntitlementsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Transfers customer entitlements to new reseller.

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

        Args:
            request (:class:`google.cloud.channel_v1.types.TransferEntitlementsRequest`):
                The request object. Request message for
                [CloudChannelService.TransferEntitlements][google.cloud.channel.v1.CloudChannelService.TransferEntitlements].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.channel_v1.types.TransferEntitlementsResponse` Response message for [CloudChannelService.TransferEntitlements][google.cloud.channel.v1.CloudChannelService.TransferEntitlements].
                   This is put in the response field of
                   google.longrunning.Operation.

        """
        # Create or coerce a protobuf request object.
        request = service.TransferEntitlementsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.transfer_entitlements,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            service.TransferEntitlementsResponse,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def transfer_entitlements_to_google(
        self,
        request: service.TransferEntitlementsToGoogleRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Transfers customer entitlements from their current reseller to
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

        Args:
            request (:class:`google.cloud.channel_v1.types.TransferEntitlementsToGoogleRequest`):
                The request object. Request message for
                [CloudChannelService.TransferEntitlementsToGoogle][google.cloud.channel.v1.CloudChannelService.TransferEntitlementsToGoogle].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

        """
        # Create or coerce a protobuf request object.
        request = service.TransferEntitlementsToGoogleRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.transfer_entitlements_to_google,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_channel_partner_links(
        self,
        request: service.ListChannelPartnerLinksRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListChannelPartnerLinksAsyncPager:
        r"""List
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

        Args:
            request (:class:`google.cloud.channel_v1.types.ListChannelPartnerLinksRequest`):
                The request object. Request message for
                [CloudChannelService.ListChannelPartnerLinks][google.cloud.channel.v1.CloudChannelService.ListChannelPartnerLinks]
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.channel_v1.services.cloud_channel_service.pagers.ListChannelPartnerLinksAsyncPager:
                Response message for
                [CloudChannelService.ListChannelPartnerLinks][google.cloud.channel.v1.CloudChannelService.ListChannelPartnerLinks].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        request = service.ListChannelPartnerLinksRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_channel_partner_links,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListChannelPartnerLinksAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_channel_partner_link(
        self,
        request: service.GetChannelPartnerLinkRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> channel_partner_links.ChannelPartnerLink:
        r"""Returns the requested
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

        Args:
            request (:class:`google.cloud.channel_v1.types.GetChannelPartnerLinkRequest`):
                The request object. Request message for
                [CloudChannelService.GetChannelPartnerLink][google.cloud.channel.v1.CloudChannelService.GetChannelPartnerLink].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.channel_v1.types.ChannelPartnerLink:
                Entity representing a link between
                distributors and their indirect
                resellers in an n-tier resale channel.

        """
        # Create or coerce a protobuf request object.
        request = service.GetChannelPartnerLinkRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_channel_partner_link,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def create_channel_partner_link(
        self,
        request: service.CreateChannelPartnerLinkRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> channel_partner_links.ChannelPartnerLink:
        r"""Initiates a channel partner link between a distributor and a
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

        Args:
            request (:class:`google.cloud.channel_v1.types.CreateChannelPartnerLinkRequest`):
                The request object. Request message for
                [CloudChannelService.CreateChannelPartnerLink][google.cloud.channel.v1.CloudChannelService.CreateChannelPartnerLink]
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.channel_v1.types.ChannelPartnerLink:
                Entity representing a link between
                distributors and their indirect
                resellers in an n-tier resale channel.

        """
        # Create or coerce a protobuf request object.
        request = service.CreateChannelPartnerLinkRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_channel_partner_link,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def update_channel_partner_link(
        self,
        request: service.UpdateChannelPartnerLinkRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> channel_partner_links.ChannelPartnerLink:
        r"""Updates a channel partner link. Distributors call this method to
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

        Args:
            request (:class:`google.cloud.channel_v1.types.UpdateChannelPartnerLinkRequest`):
                The request object. Request message for
                [CloudChannelService.UpdateChannelPartnerLink][google.cloud.channel.v1.CloudChannelService.UpdateChannelPartnerLink]
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.channel_v1.types.ChannelPartnerLink:
                Entity representing a link between
                distributors and their indirect
                resellers in an n-tier resale channel.

        """
        # Create or coerce a protobuf request object.
        request = service.UpdateChannelPartnerLinkRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_channel_partner_link,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def lookup_offer(
        self,
        request: service.LookupOfferRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> offers.Offer:
        r"""Returns the requested [Offer][google.cloud.channel.v1.Offer]
        resource.

        Possible error codes:

        -  PERMISSION_DENIED: The entitlement doesn't belong to the
           reseller.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.
        -  NOT_FOUND: Entitlement or offer was not found.

        Return value: The [Offer][google.cloud.channel.v1.Offer]
        resource.

        Args:
            request (:class:`google.cloud.channel_v1.types.LookupOfferRequest`):
                The request object. Request message for LookupOffer.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.channel_v1.types.Offer:
                Represents an offer made to resellers for purchase.
                   An offer is associated with a
                   [Sku][google.cloud.channel.v1.Sku], has a plan for
                   payment, a price, and defines the constraints for
                   buying.

        """
        # Create or coerce a protobuf request object.
        request = service.LookupOfferRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.lookup_offer,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("entitlement", request.entitlement),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_products(
        self,
        request: service.ListProductsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListProductsAsyncPager:
        r"""Lists the Products the reseller is authorized to sell.

        Possible error codes:

        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.

        Args:
            request (:class:`google.cloud.channel_v1.types.ListProductsRequest`):
                The request object. Request message for ListProducts.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.channel_v1.services.cloud_channel_service.pagers.ListProductsAsyncPager:
                Response message for ListProducts.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        request = service.ListProductsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_products,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListProductsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_skus(
        self,
        request: service.ListSkusRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListSkusAsyncPager:
        r"""Lists the SKUs for a product the reseller is authorized to sell.

        Possible error codes:

        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.

        Args:
            request (:class:`google.cloud.channel_v1.types.ListSkusRequest`):
                The request object. Request message for ListSkus.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.channel_v1.services.cloud_channel_service.pagers.ListSkusAsyncPager:
                Response message for ListSkus.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        request = service.ListSkusRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_skus,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListSkusAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_offers(
        self,
        request: service.ListOffersRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListOffersAsyncPager:
        r"""Lists the Offers the reseller can sell.

        Possible error codes:

        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.

        Args:
            request (:class:`google.cloud.channel_v1.types.ListOffersRequest`):
                The request object. Request message for ListOffers.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.channel_v1.services.cloud_channel_service.pagers.ListOffersAsyncPager:
                Response message for ListOffers.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        request = service.ListOffersRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_offers,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListOffersAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_purchasable_skus(
        self,
        request: service.ListPurchasableSkusRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListPurchasableSkusAsyncPager:
        r"""Lists the following:

        -  SKUs that you can purchase for a customer
        -  SKUs that you can upgrade or downgrade for an entitlement.

        Possible error codes:

        -  PERMISSION_DENIED: The customer doesn't belong to the
           reseller.
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.

        Args:
            request (:class:`google.cloud.channel_v1.types.ListPurchasableSkusRequest`):
                The request object. Request message for
                ListPurchasableSkus.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.channel_v1.services.cloud_channel_service.pagers.ListPurchasableSkusAsyncPager:
                Response message for
                ListPurchasableSkus.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        request = service.ListPurchasableSkusRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_purchasable_skus,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("customer", request.customer),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListPurchasableSkusAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_purchasable_offers(
        self,
        request: service.ListPurchasableOffersRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListPurchasableOffersAsyncPager:
        r"""Lists the following:

        -  Offers that you can purchase for a customer.
        -  Offers that you can change for an entitlement.

        Possible error codes:

        -  PERMISSION_DENIED: The customer doesn't belong to the
           reseller
        -  INVALID_ARGUMENT: Required request parameters are missing or
           invalid.

        Args:
            request (:class:`google.cloud.channel_v1.types.ListPurchasableOffersRequest`):
                The request object. Request message for
                ListPurchasableOffers.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.channel_v1.services.cloud_channel_service.pagers.ListPurchasableOffersAsyncPager:
                Response message for
                ListPurchasableOffers.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        request = service.ListPurchasableOffersRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_purchasable_offers,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("customer", request.customer),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListPurchasableOffersAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def register_subscriber(
        self,
        request: service.RegisterSubscriberRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> service.RegisterSubscriberResponse:
        r"""Registers a service account with subscriber privileges on the
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

        Args:
            request (:class:`google.cloud.channel_v1.types.RegisterSubscriberRequest`):
                The request object. Request Message for
                RegisterSubscriber.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.channel_v1.types.RegisterSubscriberResponse:
                Response Message for
                RegisterSubscriber.

        """
        # Create or coerce a protobuf request object.
        request = service.RegisterSubscriberRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.register_subscriber,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("account", request.account),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def unregister_subscriber(
        self,
        request: service.UnregisterSubscriberRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> service.UnregisterSubscriberResponse:
        r"""Unregisters a service account with subscriber privileges on the
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

        Args:
            request (:class:`google.cloud.channel_v1.types.UnregisterSubscriberRequest`):
                The request object. Request Message for
                UnregisterSubscriber.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.channel_v1.types.UnregisterSubscriberResponse:
                Response Message for
                UnregisterSubscriber.

        """
        # Create or coerce a protobuf request object.
        request = service.UnregisterSubscriberRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.unregister_subscriber,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("account", request.account),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_subscribers(
        self,
        request: service.ListSubscribersRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListSubscribersAsyncPager:
        r"""Lists service accounts with subscriber privileges on the Cloud
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

        Args:
            request (:class:`google.cloud.channel_v1.types.ListSubscribersRequest`):
                The request object. Request Message for ListSubscribers.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.channel_v1.services.cloud_channel_service.pagers.ListSubscribersAsyncPager:
                Response Message for ListSubscribers.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        request = service.ListSubscribersRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_subscribers,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("account", request.account),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListSubscribersAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-channel",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("CloudChannelServiceAsyncClient",)
