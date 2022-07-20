# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from typing import Dict, Mapping, Optional, Sequence, Tuple, Type, Union

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.api_core.client_options import ClientOptions
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore
import pkg_resources

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore

from google.analytics.admin_v1beta.services.analytics_admin_service import pagers
from google.analytics.admin_v1beta.types import analytics_admin, resources

from .client import AnalyticsAdminServiceClient
from .transports.base import DEFAULT_CLIENT_INFO, AnalyticsAdminServiceTransport
from .transports.grpc_asyncio import AnalyticsAdminServiceGrpcAsyncIOTransport


class AnalyticsAdminServiceAsyncClient:
    """Service Interface for the Analytics Admin API (GA4)."""

    _client: AnalyticsAdminServiceClient

    DEFAULT_ENDPOINT = AnalyticsAdminServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = AnalyticsAdminServiceClient.DEFAULT_MTLS_ENDPOINT

    account_path = staticmethod(AnalyticsAdminServiceClient.account_path)
    parse_account_path = staticmethod(AnalyticsAdminServiceClient.parse_account_path)
    account_summary_path = staticmethod(
        AnalyticsAdminServiceClient.account_summary_path
    )
    parse_account_summary_path = staticmethod(
        AnalyticsAdminServiceClient.parse_account_summary_path
    )
    conversion_event_path = staticmethod(
        AnalyticsAdminServiceClient.conversion_event_path
    )
    parse_conversion_event_path = staticmethod(
        AnalyticsAdminServiceClient.parse_conversion_event_path
    )
    custom_dimension_path = staticmethod(
        AnalyticsAdminServiceClient.custom_dimension_path
    )
    parse_custom_dimension_path = staticmethod(
        AnalyticsAdminServiceClient.parse_custom_dimension_path
    )
    custom_metric_path = staticmethod(AnalyticsAdminServiceClient.custom_metric_path)
    parse_custom_metric_path = staticmethod(
        AnalyticsAdminServiceClient.parse_custom_metric_path
    )
    data_retention_settings_path = staticmethod(
        AnalyticsAdminServiceClient.data_retention_settings_path
    )
    parse_data_retention_settings_path = staticmethod(
        AnalyticsAdminServiceClient.parse_data_retention_settings_path
    )
    data_sharing_settings_path = staticmethod(
        AnalyticsAdminServiceClient.data_sharing_settings_path
    )
    parse_data_sharing_settings_path = staticmethod(
        AnalyticsAdminServiceClient.parse_data_sharing_settings_path
    )
    data_stream_path = staticmethod(AnalyticsAdminServiceClient.data_stream_path)
    parse_data_stream_path = staticmethod(
        AnalyticsAdminServiceClient.parse_data_stream_path
    )
    firebase_link_path = staticmethod(AnalyticsAdminServiceClient.firebase_link_path)
    parse_firebase_link_path = staticmethod(
        AnalyticsAdminServiceClient.parse_firebase_link_path
    )
    google_ads_link_path = staticmethod(
        AnalyticsAdminServiceClient.google_ads_link_path
    )
    parse_google_ads_link_path = staticmethod(
        AnalyticsAdminServiceClient.parse_google_ads_link_path
    )
    measurement_protocol_secret_path = staticmethod(
        AnalyticsAdminServiceClient.measurement_protocol_secret_path
    )
    parse_measurement_protocol_secret_path = staticmethod(
        AnalyticsAdminServiceClient.parse_measurement_protocol_secret_path
    )
    property_path = staticmethod(AnalyticsAdminServiceClient.property_path)
    parse_property_path = staticmethod(AnalyticsAdminServiceClient.parse_property_path)
    common_billing_account_path = staticmethod(
        AnalyticsAdminServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        AnalyticsAdminServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(AnalyticsAdminServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        AnalyticsAdminServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        AnalyticsAdminServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        AnalyticsAdminServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(AnalyticsAdminServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        AnalyticsAdminServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(
        AnalyticsAdminServiceClient.common_location_path
    )
    parse_common_location_path = staticmethod(
        AnalyticsAdminServiceClient.parse_common_location_path
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
            AnalyticsAdminServiceAsyncClient: The constructed client.
        """
        return AnalyticsAdminServiceClient.from_service_account_info.__func__(AnalyticsAdminServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            AnalyticsAdminServiceAsyncClient: The constructed client.
        """
        return AnalyticsAdminServiceClient.from_service_account_file.__func__(AnalyticsAdminServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[ClientOptions] = None
    ):
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variabel is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """
        return AnalyticsAdminServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> AnalyticsAdminServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            AnalyticsAdminServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(AnalyticsAdminServiceClient).get_transport_class,
        type(AnalyticsAdminServiceClient),
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, AnalyticsAdminServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the analytics admin service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.AnalyticsAdminServiceTransport]): The
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
        self._client = AnalyticsAdminServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def get_account(
        self,
        request: Union[analytics_admin.GetAccountRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Account:
        r"""Lookup for a single Account.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_get_account():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.GetAccountRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_account(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.GetAccountRequest, dict]):
                The request object. Request message for GetAccount RPC.
            name (:class:`str`):
                Required. The name of the account to
                lookup. Format: accounts/{account}
                Example: "accounts/100"

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.types.Account:
                A resource message representing a
                Google Analytics account.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.GetAccountRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_account,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_accounts(
        self,
        request: Union[analytics_admin.ListAccountsRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAccountsAsyncPager:
        r"""Returns all accounts accessible by the caller.
        Note that these accounts might not currently have GA4
        properties. Soft-deleted (ie: "trashed") accounts are
        excluded by default. Returns an empty list if no
        relevant accounts are found.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_list_accounts():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.ListAccountsRequest(
                )

                # Make the request
                page_result = client.list_accounts(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.ListAccountsRequest, dict]):
                The request object. Request message for ListAccounts
                RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.services.analytics_admin_service.pagers.ListAccountsAsyncPager:
                Request message for ListAccounts RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        request = analytics_admin.ListAccountsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_accounts,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListAccountsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_account(
        self,
        request: Union[analytics_admin.DeleteAccountRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Marks target Account as soft-deleted (ie: "trashed")
        and returns it.
        This API does not have a method to restore soft-deleted
        accounts. However, they can be restored using the Trash
        Can UI.
        If the accounts are not restored before the expiration
        time, the account and all child resources (eg:
        Properties, GoogleAdsLinks, Streams, UserLinks) will be
        permanently purged.
        https://support.google.com/analytics/answer/6154772
        Returns an error if the target is not found.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_delete_account():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.DeleteAccountRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_account(request=request)

        Args:
            request (Union[google.analytics.admin_v1beta.types.DeleteAccountRequest, dict]):
                The request object. Request message for DeleteAccount
                RPC.
            name (:class:`str`):
                Required. The name of the Account to
                soft-delete. Format: accounts/{account}
                Example: "accounts/100"

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.DeleteAccountRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_account,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def update_account(
        self,
        request: Union[analytics_admin.UpdateAccountRequest, dict] = None,
        *,
        account: resources.Account = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Account:
        r"""Updates an account.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_update_account():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                account = admin_v1beta.Account()
                account.display_name = "display_name_value"

                request = admin_v1beta.UpdateAccountRequest(
                    account=account,
                )

                # Make the request
                response = await client.update_account(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.UpdateAccountRequest, dict]):
                The request object. Request message for UpdateAccount
                RPC.
            account (:class:`google.analytics.admin_v1beta.types.Account`):
                Required. The account to update. The account's ``name``
                field is used to identify the account.

                This corresponds to the ``account`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The list of fields to be updated. Field names
                must be in snake case (e.g., "field_to_update"). Omitted
                fields will not be updated. To replace the entire
                entity, use one path with the string "*" to match all
                fields.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.types.Account:
                A resource message representing a
                Google Analytics account.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([account, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.UpdateAccountRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if account is not None:
            request.account = account
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_account,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("account.name", request.account.name),)
            ),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def provision_account_ticket(
        self,
        request: Union[analytics_admin.ProvisionAccountTicketRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_admin.ProvisionAccountTicketResponse:
        r"""Requests a ticket for creating an account.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_provision_account_ticket():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.ProvisionAccountTicketRequest(
                )

                # Make the request
                response = await client.provision_account_ticket(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.ProvisionAccountTicketRequest, dict]):
                The request object. Request message for
                ProvisionAccountTicket RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.types.ProvisionAccountTicketResponse:
                Response message for
                ProvisionAccountTicket RPC.

        """
        # Create or coerce a protobuf request object.
        request = analytics_admin.ProvisionAccountTicketRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.provision_account_ticket,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_account_summaries(
        self,
        request: Union[analytics_admin.ListAccountSummariesRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAccountSummariesAsyncPager:
        r"""Returns summaries of all accounts accessible by the
        caller.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_list_account_summaries():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.ListAccountSummariesRequest(
                )

                # Make the request
                page_result = client.list_account_summaries(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.ListAccountSummariesRequest, dict]):
                The request object. Request message for
                ListAccountSummaries RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.services.analytics_admin_service.pagers.ListAccountSummariesAsyncPager:
                Response message for
                ListAccountSummaries RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        request = analytics_admin.ListAccountSummariesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_account_summaries,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListAccountSummariesAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_property(
        self,
        request: Union[analytics_admin.GetPropertyRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Property:
        r"""Lookup for a single "GA4" Property.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_get_property():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.GetPropertyRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_property(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.GetPropertyRequest, dict]):
                The request object. Request message for GetProperty RPC.
            name (:class:`str`):
                Required. The name of the property to lookup. Format:
                properties/{property_id} Example: "properties/1000"

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.types.Property:
                A resource message representing a
                Google Analytics GA4 property.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.GetPropertyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_property,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_properties(
        self,
        request: Union[analytics_admin.ListPropertiesRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListPropertiesAsyncPager:
        r"""Returns child Properties under the specified parent
        Account.
        Only "GA4" properties will be returned.
        Properties will be excluded if the caller does not have
        access. Soft-deleted (ie: "trashed") properties are
        excluded by default. Returns an empty list if no
        relevant properties are found.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_list_properties():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.ListPropertiesRequest(
                    filter="filter_value",
                )

                # Make the request
                page_result = client.list_properties(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.ListPropertiesRequest, dict]):
                The request object. Request message for ListProperties
                RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.services.analytics_admin_service.pagers.ListPropertiesAsyncPager:
                Response message for ListProperties
                RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        request = analytics_admin.ListPropertiesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_properties,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListPropertiesAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_property(
        self,
        request: Union[analytics_admin.CreatePropertyRequest, dict] = None,
        *,
        property: resources.Property = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Property:
        r"""Creates an "GA4" property with the specified location
        and attributes.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_create_property():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                property = admin_v1beta.Property()
                property.display_name = "display_name_value"
                property.time_zone = "time_zone_value"

                request = admin_v1beta.CreatePropertyRequest(
                    property=property,
                )

                # Make the request
                response = await client.create_property(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.CreatePropertyRequest, dict]):
                The request object. Request message for CreateProperty
                RPC.
            property (:class:`google.analytics.admin_v1beta.types.Property`):
                Required. The property to create.
                Note: the supplied property must specify
                its parent.

                This corresponds to the ``property`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.types.Property:
                A resource message representing a
                Google Analytics GA4 property.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([property])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.CreatePropertyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if property is not None:
            request.property = property

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_property,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_property(
        self,
        request: Union[analytics_admin.DeletePropertyRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Property:
        r"""Marks target Property as soft-deleted (ie: "trashed")
        and returns it.
        This API does not have a method to restore soft-deleted
        properties. However, they can be restored using the
        Trash Can UI.
        If the properties are not restored before the expiration
        time, the Property and all child resources (eg:
        GoogleAdsLinks, Streams, UserLinks) will be permanently
        purged.
        https://support.google.com/analytics/answer/6154772
        Returns an error if the target is not found, or is not
        an GA4 Property.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_delete_property():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.DeletePropertyRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.delete_property(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.DeletePropertyRequest, dict]):
                The request object. Request message for DeleteProperty
                RPC.
            name (:class:`str`):
                Required. The name of the Property to soft-delete.
                Format: properties/{property_id} Example:
                "properties/1000"

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.types.Property:
                A resource message representing a
                Google Analytics GA4 property.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.DeletePropertyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_property,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_property(
        self,
        request: Union[analytics_admin.UpdatePropertyRequest, dict] = None,
        *,
        property: resources.Property = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Property:
        r"""Updates a property.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_update_property():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                property = admin_v1beta.Property()
                property.display_name = "display_name_value"
                property.time_zone = "time_zone_value"

                request = admin_v1beta.UpdatePropertyRequest(
                    property=property,
                )

                # Make the request
                response = await client.update_property(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.UpdatePropertyRequest, dict]):
                The request object. Request message for UpdateProperty
                RPC.
            property (:class:`google.analytics.admin_v1beta.types.Property`):
                Required. The property to update. The property's
                ``name`` field is used to identify the property to be
                updated.

                This corresponds to the ``property`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The list of fields to be updated. Field names
                must be in snake case (e.g., "field_to_update"). Omitted
                fields will not be updated. To replace the entire
                entity, use one path with the string "*" to match all
                fields.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.types.Property:
                A resource message representing a
                Google Analytics GA4 property.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([property, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.UpdatePropertyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if property is not None:
            request.property = property
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_property,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("property.name", request.property.name),)
            ),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_firebase_link(
        self,
        request: Union[analytics_admin.CreateFirebaseLinkRequest, dict] = None,
        *,
        parent: str = None,
        firebase_link: resources.FirebaseLink = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.FirebaseLink:
        r"""Creates a FirebaseLink.
        Properties can have at most one FirebaseLink.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_create_firebase_link():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.CreateFirebaseLinkRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.create_firebase_link(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.CreateFirebaseLinkRequest, dict]):
                The request object. Request message for
                CreateFirebaseLink RPC
            parent (:class:`str`):
                Required. Format: properties/{property_id} Example:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            firebase_link (:class:`google.analytics.admin_v1beta.types.FirebaseLink`):
                Required. The Firebase link to
                create.

                This corresponds to the ``firebase_link`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.types.FirebaseLink:
                A link between a GA4 property and a
                Firebase project.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, firebase_link])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.CreateFirebaseLinkRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if firebase_link is not None:
            request.firebase_link = firebase_link

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_firebase_link,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_firebase_link(
        self,
        request: Union[analytics_admin.DeleteFirebaseLinkRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a FirebaseLink on a property

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_delete_firebase_link():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.DeleteFirebaseLinkRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_firebase_link(request=request)

        Args:
            request (Union[google.analytics.admin_v1beta.types.DeleteFirebaseLinkRequest, dict]):
                The request object. Request message for
                DeleteFirebaseLink RPC
            name (:class:`str`):
                Required. Format:
                properties/{property_id}/firebaseLinks/{firebase_link_id}
                Example: properties/1234/firebaseLinks/5678

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.DeleteFirebaseLinkRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_firebase_link,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def list_firebase_links(
        self,
        request: Union[analytics_admin.ListFirebaseLinksRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListFirebaseLinksAsyncPager:
        r"""Lists FirebaseLinks on a property.
        Properties can have at most one FirebaseLink.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_list_firebase_links():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.ListFirebaseLinksRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_firebase_links(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.ListFirebaseLinksRequest, dict]):
                The request object. Request message for
                ListFirebaseLinks RPC
            parent (:class:`str`):
                Required. Format: properties/{property_id} Example:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.services.analytics_admin_service.pagers.ListFirebaseLinksAsyncPager:
                Response message for
                ListFirebaseLinks RPC
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.ListFirebaseLinksRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_firebase_links,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListFirebaseLinksAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_google_ads_link(
        self,
        request: Union[analytics_admin.CreateGoogleAdsLinkRequest, dict] = None,
        *,
        parent: str = None,
        google_ads_link: resources.GoogleAdsLink = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.GoogleAdsLink:
        r"""Creates a GoogleAdsLink.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_create_google_ads_link():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.CreateGoogleAdsLinkRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.create_google_ads_link(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.CreateGoogleAdsLinkRequest, dict]):
                The request object. Request message for
                CreateGoogleAdsLink RPC
            parent (:class:`str`):
                Required. Example format:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            google_ads_link (:class:`google.analytics.admin_v1beta.types.GoogleAdsLink`):
                Required. The GoogleAdsLink to
                create.

                This corresponds to the ``google_ads_link`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.types.GoogleAdsLink:
                A link between a GA4 property and a
                Google Ads account.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, google_ads_link])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.CreateGoogleAdsLinkRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if google_ads_link is not None:
            request.google_ads_link = google_ads_link

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_google_ads_link,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_google_ads_link(
        self,
        request: Union[analytics_admin.UpdateGoogleAdsLinkRequest, dict] = None,
        *,
        google_ads_link: resources.GoogleAdsLink = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.GoogleAdsLink:
        r"""Updates a GoogleAdsLink on a property

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_update_google_ads_link():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.UpdateGoogleAdsLinkRequest(
                )

                # Make the request
                response = await client.update_google_ads_link(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.UpdateGoogleAdsLinkRequest, dict]):
                The request object. Request message for
                UpdateGoogleAdsLink RPC
            google_ads_link (:class:`google.analytics.admin_v1beta.types.GoogleAdsLink`):
                The GoogleAdsLink to update
                This corresponds to the ``google_ads_link`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The list of fields to be updated. Field names
                must be in snake case (e.g., "field_to_update"). Omitted
                fields will not be updated. To replace the entire
                entity, use one path with the string "*" to match all
                fields.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.types.GoogleAdsLink:
                A link between a GA4 property and a
                Google Ads account.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([google_ads_link, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.UpdateGoogleAdsLinkRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if google_ads_link is not None:
            request.google_ads_link = google_ads_link
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_google_ads_link,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("google_ads_link.name", request.google_ads_link.name),)
            ),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_google_ads_link(
        self,
        request: Union[analytics_admin.DeleteGoogleAdsLinkRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a GoogleAdsLink on a property

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_delete_google_ads_link():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.DeleteGoogleAdsLinkRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_google_ads_link(request=request)

        Args:
            request (Union[google.analytics.admin_v1beta.types.DeleteGoogleAdsLinkRequest, dict]):
                The request object. Request message for
                DeleteGoogleAdsLink RPC.
            name (:class:`str`):
                Required. Example format:
                properties/1234/googleAdsLinks/5678

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.DeleteGoogleAdsLinkRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_google_ads_link,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def list_google_ads_links(
        self,
        request: Union[analytics_admin.ListGoogleAdsLinksRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListGoogleAdsLinksAsyncPager:
        r"""Lists GoogleAdsLinks on a property.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_list_google_ads_links():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.ListGoogleAdsLinksRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_google_ads_links(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.ListGoogleAdsLinksRequest, dict]):
                The request object. Request message for
                ListGoogleAdsLinks RPC.
            parent (:class:`str`):
                Required. Example format:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.services.analytics_admin_service.pagers.ListGoogleAdsLinksAsyncPager:
                Response message for
                ListGoogleAdsLinks RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.ListGoogleAdsLinksRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_google_ads_links,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListGoogleAdsLinksAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_data_sharing_settings(
        self,
        request: Union[analytics_admin.GetDataSharingSettingsRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.DataSharingSettings:
        r"""Get data sharing settings on an account.
        Data sharing settings are singletons.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_get_data_sharing_settings():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.GetDataSharingSettingsRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_data_sharing_settings(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.GetDataSharingSettingsRequest, dict]):
                The request object. Request message for
                GetDataSharingSettings RPC.
            name (:class:`str`):
                Required. The name of the settings to
                lookup. Format:
                accounts/{account}/dataSharingSettings
                Example:
                "accounts/1000/dataSharingSettings"

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.types.DataSharingSettings:
                A resource message representing data
                sharing settings of a Google Analytics
                account.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.GetDataSharingSettingsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_data_sharing_settings,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_measurement_protocol_secret(
        self,
        request: Union[
            analytics_admin.GetMeasurementProtocolSecretRequest, dict
        ] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.MeasurementProtocolSecret:
        r"""Lookup for a single "GA4" MeasurementProtocolSecret.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_get_measurement_protocol_secret():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.GetMeasurementProtocolSecretRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_measurement_protocol_secret(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.GetMeasurementProtocolSecretRequest, dict]):
                The request object. Request message for
                GetMeasurementProtocolSecret RPC.
            name (:class:`str`):
                Required. The name of the measurement
                protocol secret to lookup. Format:
                properties/{property}/dataStreams/{dataStream}/measurementProtocolSecrets/{measurementProtocolSecret}

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.types.MeasurementProtocolSecret:
                A secret value used for sending hits
                to Measurement Protocol.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.GetMeasurementProtocolSecretRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_measurement_protocol_secret,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_measurement_protocol_secrets(
        self,
        request: Union[
            analytics_admin.ListMeasurementProtocolSecretsRequest, dict
        ] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListMeasurementProtocolSecretsAsyncPager:
        r"""Returns child MeasurementProtocolSecrets under the
        specified parent Property.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_list_measurement_protocol_secrets():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.ListMeasurementProtocolSecretsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_measurement_protocol_secrets(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.ListMeasurementProtocolSecretsRequest, dict]):
                The request object. Request message for
                ListMeasurementProtocolSecret RPC
            parent (:class:`str`):
                Required. The resource name of the
                parent stream. Format:
                properties/{property}/dataStreams/{dataStream}/measurementProtocolSecrets

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.services.analytics_admin_service.pagers.ListMeasurementProtocolSecretsAsyncPager:
                Response message for
                ListMeasurementProtocolSecret RPC
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.ListMeasurementProtocolSecretsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_measurement_protocol_secrets,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListMeasurementProtocolSecretsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_measurement_protocol_secret(
        self,
        request: Union[
            analytics_admin.CreateMeasurementProtocolSecretRequest, dict
        ] = None,
        *,
        parent: str = None,
        measurement_protocol_secret: resources.MeasurementProtocolSecret = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.MeasurementProtocolSecret:
        r"""Creates a measurement protocol secret.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_create_measurement_protocol_secret():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                measurement_protocol_secret = admin_v1beta.MeasurementProtocolSecret()
                measurement_protocol_secret.display_name = "display_name_value"

                request = admin_v1beta.CreateMeasurementProtocolSecretRequest(
                    parent="parent_value",
                    measurement_protocol_secret=measurement_protocol_secret,
                )

                # Make the request
                response = await client.create_measurement_protocol_secret(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.CreateMeasurementProtocolSecretRequest, dict]):
                The request object. Request message for
                CreateMeasurementProtocolSecret RPC
            parent (:class:`str`):
                Required. The parent resource where
                this secret will be created. Format:
                properties/{property}/dataStreams/{dataStream}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            measurement_protocol_secret (:class:`google.analytics.admin_v1beta.types.MeasurementProtocolSecret`):
                Required. The measurement protocol
                secret to create.

                This corresponds to the ``measurement_protocol_secret`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.types.MeasurementProtocolSecret:
                A secret value used for sending hits
                to Measurement Protocol.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, measurement_protocol_secret])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.CreateMeasurementProtocolSecretRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if measurement_protocol_secret is not None:
            request.measurement_protocol_secret = measurement_protocol_secret

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_measurement_protocol_secret,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_measurement_protocol_secret(
        self,
        request: Union[
            analytics_admin.DeleteMeasurementProtocolSecretRequest, dict
        ] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes target MeasurementProtocolSecret.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_delete_measurement_protocol_secret():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.DeleteMeasurementProtocolSecretRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_measurement_protocol_secret(request=request)

        Args:
            request (Union[google.analytics.admin_v1beta.types.DeleteMeasurementProtocolSecretRequest, dict]):
                The request object. Request message for
                DeleteMeasurementProtocolSecret RPC
            name (:class:`str`):
                Required. The name of the
                MeasurementProtocolSecret to delete.
                Format:
                properties/{property}/dataStreams/{dataStream}/measurementProtocolSecrets/{measurementProtocolSecret}

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.DeleteMeasurementProtocolSecretRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_measurement_protocol_secret,
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
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def update_measurement_protocol_secret(
        self,
        request: Union[
            analytics_admin.UpdateMeasurementProtocolSecretRequest, dict
        ] = None,
        *,
        measurement_protocol_secret: resources.MeasurementProtocolSecret = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.MeasurementProtocolSecret:
        r"""Updates a measurement protocol secret.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_update_measurement_protocol_secret():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                measurement_protocol_secret = admin_v1beta.MeasurementProtocolSecret()
                measurement_protocol_secret.display_name = "display_name_value"

                request = admin_v1beta.UpdateMeasurementProtocolSecretRequest(
                    measurement_protocol_secret=measurement_protocol_secret,
                )

                # Make the request
                response = await client.update_measurement_protocol_secret(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.UpdateMeasurementProtocolSecretRequest, dict]):
                The request object. Request message for
                UpdateMeasurementProtocolSecret RPC
            measurement_protocol_secret (:class:`google.analytics.admin_v1beta.types.MeasurementProtocolSecret`):
                Required. The measurement protocol
                secret to update.

                This corresponds to the ``measurement_protocol_secret`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                The list of fields to be updated.
                Omitted fields will not be updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.types.MeasurementProtocolSecret:
                A secret value used for sending hits
                to Measurement Protocol.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([measurement_protocol_secret, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.UpdateMeasurementProtocolSecretRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if measurement_protocol_secret is not None:
            request.measurement_protocol_secret = measurement_protocol_secret
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_measurement_protocol_secret,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    (
                        "measurement_protocol_secret.name",
                        request.measurement_protocol_secret.name,
                    ),
                )
            ),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def acknowledge_user_data_collection(
        self,
        request: Union[
            analytics_admin.AcknowledgeUserDataCollectionRequest, dict
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_admin.AcknowledgeUserDataCollectionResponse:
        r"""Acknowledges the terms of user data collection for
        the specified property.
        This acknowledgement must be completed (either in the
        Google Analytics UI or via this API) before
        MeasurementProtocolSecret resources may be created.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_acknowledge_user_data_collection():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.AcknowledgeUserDataCollectionRequest(
                    property="property_value",
                    acknowledgement="acknowledgement_value",
                )

                # Make the request
                response = await client.acknowledge_user_data_collection(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.AcknowledgeUserDataCollectionRequest, dict]):
                The request object. Request message for
                AcknowledgeUserDataCollection RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.types.AcknowledgeUserDataCollectionResponse:
                Response message for
                AcknowledgeUserDataCollection RPC.

        """
        # Create or coerce a protobuf request object.
        request = analytics_admin.AcknowledgeUserDataCollectionRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.acknowledge_user_data_collection,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("property", request.property),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def search_change_history_events(
        self,
        request: Union[analytics_admin.SearchChangeHistoryEventsRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.SearchChangeHistoryEventsAsyncPager:
        r"""Searches through all changes to an account or its
        children given the specified set of filters.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_search_change_history_events():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.SearchChangeHistoryEventsRequest(
                    account="account_value",
                )

                # Make the request
                page_result = client.search_change_history_events(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.SearchChangeHistoryEventsRequest, dict]):
                The request object. Request message for
                SearchChangeHistoryEvents RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.services.analytics_admin_service.pagers.SearchChangeHistoryEventsAsyncPager:
                Response message for SearchAccounts
                RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        request = analytics_admin.SearchChangeHistoryEventsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.search_change_history_events,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("account", request.account),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.SearchChangeHistoryEventsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_conversion_event(
        self,
        request: Union[analytics_admin.CreateConversionEventRequest, dict] = None,
        *,
        parent: str = None,
        conversion_event: resources.ConversionEvent = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.ConversionEvent:
        r"""Creates a conversion event with the specified
        attributes.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_create_conversion_event():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.CreateConversionEventRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.create_conversion_event(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.CreateConversionEventRequest, dict]):
                The request object. Request message for
                CreateConversionEvent RPC
            parent (:class:`str`):
                Required. The resource name of the
                parent property where this conversion
                event will be created. Format:
                properties/123

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            conversion_event (:class:`google.analytics.admin_v1beta.types.ConversionEvent`):
                Required. The conversion event to
                create.

                This corresponds to the ``conversion_event`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.types.ConversionEvent:
                A conversion event in a Google
                Analytics property.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, conversion_event])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.CreateConversionEventRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if conversion_event is not None:
            request.conversion_event = conversion_event

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_conversion_event,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_conversion_event(
        self,
        request: Union[analytics_admin.GetConversionEventRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.ConversionEvent:
        r"""Retrieve a single conversion event.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_get_conversion_event():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.GetConversionEventRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_conversion_event(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.GetConversionEventRequest, dict]):
                The request object. Request message for
                GetConversionEvent RPC
            name (:class:`str`):
                Required. The resource name of the conversion event to
                retrieve. Format:
                properties/{property}/conversionEvents/{conversion_event}
                Example: "properties/123/conversionEvents/456"

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.types.ConversionEvent:
                A conversion event in a Google
                Analytics property.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.GetConversionEventRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_conversion_event,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_conversion_event(
        self,
        request: Union[analytics_admin.DeleteConversionEventRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a conversion event in a property.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_delete_conversion_event():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.DeleteConversionEventRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_conversion_event(request=request)

        Args:
            request (Union[google.analytics.admin_v1beta.types.DeleteConversionEventRequest, dict]):
                The request object. Request message for
                DeleteConversionEvent RPC
            name (:class:`str`):
                Required. The resource name of the conversion event to
                delete. Format:
                properties/{property}/conversionEvents/{conversion_event}
                Example: "properties/123/conversionEvents/456"

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.DeleteConversionEventRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_conversion_event,
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
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def list_conversion_events(
        self,
        request: Union[analytics_admin.ListConversionEventsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListConversionEventsAsyncPager:
        r"""Returns a list of conversion events in the specified
        parent property.
        Returns an empty list if no conversion events are found.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_list_conversion_events():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.ListConversionEventsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_conversion_events(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.ListConversionEventsRequest, dict]):
                The request object. Request message for
                ListConversionEvents RPC
            parent (:class:`str`):
                Required. The resource name of the
                parent property. Example:
                'properties/123'

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.services.analytics_admin_service.pagers.ListConversionEventsAsyncPager:
                Response message for
                ListConversionEvents RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.ListConversionEventsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_conversion_events,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListConversionEventsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_custom_dimension(
        self,
        request: Union[analytics_admin.CreateCustomDimensionRequest, dict] = None,
        *,
        parent: str = None,
        custom_dimension: resources.CustomDimension = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.CustomDimension:
        r"""Creates a CustomDimension.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_create_custom_dimension():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                custom_dimension = admin_v1beta.CustomDimension()
                custom_dimension.parameter_name = "parameter_name_value"
                custom_dimension.display_name = "display_name_value"
                custom_dimension.scope = "USER"

                request = admin_v1beta.CreateCustomDimensionRequest(
                    parent="parent_value",
                    custom_dimension=custom_dimension,
                )

                # Make the request
                response = await client.create_custom_dimension(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.CreateCustomDimensionRequest, dict]):
                The request object. Request message for
                CreateCustomDimension RPC.
            parent (:class:`str`):
                Required. Example format:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            custom_dimension (:class:`google.analytics.admin_v1beta.types.CustomDimension`):
                Required. The CustomDimension to
                create.

                This corresponds to the ``custom_dimension`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.types.CustomDimension:
                A definition for a CustomDimension.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, custom_dimension])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.CreateCustomDimensionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if custom_dimension is not None:
            request.custom_dimension = custom_dimension

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_custom_dimension,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_custom_dimension(
        self,
        request: Union[analytics_admin.UpdateCustomDimensionRequest, dict] = None,
        *,
        custom_dimension: resources.CustomDimension = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.CustomDimension:
        r"""Updates a CustomDimension on a property.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_update_custom_dimension():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.UpdateCustomDimensionRequest(
                )

                # Make the request
                response = await client.update_custom_dimension(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.UpdateCustomDimensionRequest, dict]):
                The request object. Request message for
                UpdateCustomDimension RPC.
            custom_dimension (:class:`google.analytics.admin_v1beta.types.CustomDimension`):
                The CustomDimension to update
                This corresponds to the ``custom_dimension`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The list of fields to be updated. Omitted
                fields will not be updated. To replace the entire
                entity, use one path with the string "*" to match all
                fields.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.types.CustomDimension:
                A definition for a CustomDimension.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([custom_dimension, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.UpdateCustomDimensionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if custom_dimension is not None:
            request.custom_dimension = custom_dimension
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_custom_dimension,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("custom_dimension.name", request.custom_dimension.name),)
            ),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_custom_dimensions(
        self,
        request: Union[analytics_admin.ListCustomDimensionsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCustomDimensionsAsyncPager:
        r"""Lists CustomDimensions on a property.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_list_custom_dimensions():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.ListCustomDimensionsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_custom_dimensions(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.ListCustomDimensionsRequest, dict]):
                The request object. Request message for
                ListCustomDimensions RPC.
            parent (:class:`str`):
                Required. Example format:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.services.analytics_admin_service.pagers.ListCustomDimensionsAsyncPager:
                Response message for
                ListCustomDimensions RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.ListCustomDimensionsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_custom_dimensions,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListCustomDimensionsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def archive_custom_dimension(
        self,
        request: Union[analytics_admin.ArchiveCustomDimensionRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Archives a CustomDimension on a property.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_archive_custom_dimension():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.ArchiveCustomDimensionRequest(
                    name="name_value",
                )

                # Make the request
                await client.archive_custom_dimension(request=request)

        Args:
            request (Union[google.analytics.admin_v1beta.types.ArchiveCustomDimensionRequest, dict]):
                The request object. Request message for
                ArchiveCustomDimension RPC.
            name (:class:`str`):
                Required. The name of the
                CustomDimension to archive. Example
                format:
                properties/1234/customDimensions/5678

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.ArchiveCustomDimensionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.archive_custom_dimension,
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
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def get_custom_dimension(
        self,
        request: Union[analytics_admin.GetCustomDimensionRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.CustomDimension:
        r"""Lookup for a single CustomDimension.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_get_custom_dimension():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.GetCustomDimensionRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_custom_dimension(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.GetCustomDimensionRequest, dict]):
                The request object. Request message for
                GetCustomDimension RPC.
            name (:class:`str`):
                Required. The name of the
                CustomDimension to get. Example format:
                properties/1234/customDimensions/5678

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.types.CustomDimension:
                A definition for a CustomDimension.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.GetCustomDimensionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_custom_dimension,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_custom_metric(
        self,
        request: Union[analytics_admin.CreateCustomMetricRequest, dict] = None,
        *,
        parent: str = None,
        custom_metric: resources.CustomMetric = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.CustomMetric:
        r"""Creates a CustomMetric.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_create_custom_metric():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                custom_metric = admin_v1beta.CustomMetric()
                custom_metric.parameter_name = "parameter_name_value"
                custom_metric.display_name = "display_name_value"
                custom_metric.measurement_unit = "HOURS"
                custom_metric.scope = "EVENT"

                request = admin_v1beta.CreateCustomMetricRequest(
                    parent="parent_value",
                    custom_metric=custom_metric,
                )

                # Make the request
                response = await client.create_custom_metric(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.CreateCustomMetricRequest, dict]):
                The request object. Request message for
                CreateCustomMetric RPC.
            parent (:class:`str`):
                Required. Example format:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            custom_metric (:class:`google.analytics.admin_v1beta.types.CustomMetric`):
                Required. The CustomMetric to create.
                This corresponds to the ``custom_metric`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.types.CustomMetric:
                A definition for a custom metric.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, custom_metric])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.CreateCustomMetricRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if custom_metric is not None:
            request.custom_metric = custom_metric

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_custom_metric,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_custom_metric(
        self,
        request: Union[analytics_admin.UpdateCustomMetricRequest, dict] = None,
        *,
        custom_metric: resources.CustomMetric = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.CustomMetric:
        r"""Updates a CustomMetric on a property.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_update_custom_metric():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.UpdateCustomMetricRequest(
                )

                # Make the request
                response = await client.update_custom_metric(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.UpdateCustomMetricRequest, dict]):
                The request object. Request message for
                UpdateCustomMetric RPC.
            custom_metric (:class:`google.analytics.admin_v1beta.types.CustomMetric`):
                The CustomMetric to update
                This corresponds to the ``custom_metric`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The list of fields to be updated. Omitted
                fields will not be updated. To replace the entire
                entity, use one path with the string "*" to match all
                fields.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.types.CustomMetric:
                A definition for a custom metric.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([custom_metric, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.UpdateCustomMetricRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if custom_metric is not None:
            request.custom_metric = custom_metric
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_custom_metric,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("custom_metric.name", request.custom_metric.name),)
            ),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_custom_metrics(
        self,
        request: Union[analytics_admin.ListCustomMetricsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCustomMetricsAsyncPager:
        r"""Lists CustomMetrics on a property.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_list_custom_metrics():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.ListCustomMetricsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_custom_metrics(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.ListCustomMetricsRequest, dict]):
                The request object. Request message for
                ListCustomMetrics RPC.
            parent (:class:`str`):
                Required. Example format:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.services.analytics_admin_service.pagers.ListCustomMetricsAsyncPager:
                Response message for
                ListCustomMetrics RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.ListCustomMetricsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_custom_metrics,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListCustomMetricsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def archive_custom_metric(
        self,
        request: Union[analytics_admin.ArchiveCustomMetricRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Archives a CustomMetric on a property.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_archive_custom_metric():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.ArchiveCustomMetricRequest(
                    name="name_value",
                )

                # Make the request
                await client.archive_custom_metric(request=request)

        Args:
            request (Union[google.analytics.admin_v1beta.types.ArchiveCustomMetricRequest, dict]):
                The request object. Request message for
                ArchiveCustomMetric RPC.
            name (:class:`str`):
                Required. The name of the
                CustomMetric to archive. Example format:
                properties/1234/customMetrics/5678

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.ArchiveCustomMetricRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.archive_custom_metric,
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
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def get_custom_metric(
        self,
        request: Union[analytics_admin.GetCustomMetricRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.CustomMetric:
        r"""Lookup for a single CustomMetric.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_get_custom_metric():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.GetCustomMetricRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_custom_metric(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.GetCustomMetricRequest, dict]):
                The request object. Request message for GetCustomMetric
                RPC.
            name (:class:`str`):
                Required. The name of the
                CustomMetric to get. Example format:
                properties/1234/customMetrics/5678

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.types.CustomMetric:
                A definition for a custom metric.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.GetCustomMetricRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_custom_metric,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_data_retention_settings(
        self,
        request: Union[analytics_admin.GetDataRetentionSettingsRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.DataRetentionSettings:
        r"""Returns the singleton data retention settings for
        this property.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_get_data_retention_settings():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.GetDataRetentionSettingsRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_data_retention_settings(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.GetDataRetentionSettingsRequest, dict]):
                The request object. Request message for
                GetDataRetentionSettings RPC.
            name (:class:`str`):
                Required. The name of the settings to
                lookup. Format:
                properties/{property}/dataRetentionSettings
                Example:
                "properties/1000/dataRetentionSettings"

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.types.DataRetentionSettings:
                Settings values for data retention.
                This is a singleton resource.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.GetDataRetentionSettingsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_data_retention_settings,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_data_retention_settings(
        self,
        request: Union[analytics_admin.UpdateDataRetentionSettingsRequest, dict] = None,
        *,
        data_retention_settings: resources.DataRetentionSettings = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.DataRetentionSettings:
        r"""Updates the singleton data retention settings for
        this property.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_update_data_retention_settings():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.UpdateDataRetentionSettingsRequest(
                )

                # Make the request
                response = await client.update_data_retention_settings(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.UpdateDataRetentionSettingsRequest, dict]):
                The request object. Request message for
                UpdateDataRetentionSettings RPC.
            data_retention_settings (:class:`google.analytics.admin_v1beta.types.DataRetentionSettings`):
                Required. The settings to update. The ``name`` field is
                used to identify the settings to be updated.

                This corresponds to the ``data_retention_settings`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The list of fields to be updated. Field names
                must be in snake case (e.g., "field_to_update"). Omitted
                fields will not be updated. To replace the entire
                entity, use one path with the string "*" to match all
                fields.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.types.DataRetentionSettings:
                Settings values for data retention.
                This is a singleton resource.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([data_retention_settings, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.UpdateDataRetentionSettingsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if data_retention_settings is not None:
            request.data_retention_settings = data_retention_settings
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_data_retention_settings,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    (
                        "data_retention_settings.name",
                        request.data_retention_settings.name,
                    ),
                )
            ),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_data_stream(
        self,
        request: Union[analytics_admin.CreateDataStreamRequest, dict] = None,
        *,
        parent: str = None,
        data_stream: resources.DataStream = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.DataStream:
        r"""Creates a DataStream.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_create_data_stream():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                data_stream = admin_v1beta.DataStream()
                data_stream.type_ = "IOS_APP_DATA_STREAM"

                request = admin_v1beta.CreateDataStreamRequest(
                    parent="parent_value",
                    data_stream=data_stream,
                )

                # Make the request
                response = await client.create_data_stream(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.CreateDataStreamRequest, dict]):
                The request object. Request message for CreateDataStream
                RPC.
            parent (:class:`str`):
                Required. Example format:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            data_stream (:class:`google.analytics.admin_v1beta.types.DataStream`):
                Required. The DataStream to create.
                This corresponds to the ``data_stream`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.types.DataStream:
                A resource message representing a
                data stream.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, data_stream])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.CreateDataStreamRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if data_stream is not None:
            request.data_stream = data_stream

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_data_stream,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_data_stream(
        self,
        request: Union[analytics_admin.DeleteDataStreamRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a DataStream on a property.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_delete_data_stream():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.DeleteDataStreamRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_data_stream(request=request)

        Args:
            request (Union[google.analytics.admin_v1beta.types.DeleteDataStreamRequest, dict]):
                The request object. Request message for DeleteDataStream
                RPC.
            name (:class:`str`):
                Required. The name of the DataStream
                to delete. Example format:
                properties/1234/dataStreams/5678

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.DeleteDataStreamRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_data_stream,
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
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def update_data_stream(
        self,
        request: Union[analytics_admin.UpdateDataStreamRequest, dict] = None,
        *,
        data_stream: resources.DataStream = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.DataStream:
        r"""Updates a DataStream on a property.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_update_data_stream():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.UpdateDataStreamRequest(
                )

                # Make the request
                response = await client.update_data_stream(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.UpdateDataStreamRequest, dict]):
                The request object. Request message for UpdateDataStream
                RPC.
            data_stream (:class:`google.analytics.admin_v1beta.types.DataStream`):
                The DataStream to update
                This corresponds to the ``data_stream`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The list of fields to be updated. Omitted
                fields will not be updated. To replace the entire
                entity, use one path with the string "*" to match all
                fields.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.types.DataStream:
                A resource message representing a
                data stream.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([data_stream, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.UpdateDataStreamRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if data_stream is not None:
            request.data_stream = data_stream
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_data_stream,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("data_stream.name", request.data_stream.name),)
            ),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_data_streams(
        self,
        request: Union[analytics_admin.ListDataStreamsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDataStreamsAsyncPager:
        r"""Lists DataStreams on a property.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_list_data_streams():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.ListDataStreamsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_data_streams(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.ListDataStreamsRequest, dict]):
                The request object. Request message for ListDataStreams
                RPC.
            parent (:class:`str`):
                Required. Example format:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.services.analytics_admin_service.pagers.ListDataStreamsAsyncPager:
                Response message for ListDataStreams
                RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.ListDataStreamsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_data_streams,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListDataStreamsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_data_stream(
        self,
        request: Union[analytics_admin.GetDataStreamRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.DataStream:
        r"""Lookup for a single DataStream.

        .. code-block:: python

            from google.analytics import admin_v1beta

            async def sample_get_data_stream():
                # Create a client
                client = admin_v1beta.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1beta.GetDataStreamRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_data_stream(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.analytics.admin_v1beta.types.GetDataStreamRequest, dict]):
                The request object. Request message for GetDataStream
                RPC.
            name (:class:`str`):
                Required. The name of the DataStream
                to get. Example format:
                properties/1234/dataStreams/5678

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1beta.types.DataStream:
                A resource message representing a
                data stream.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.GetDataStreamRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_data_stream,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-analytics-admin",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("AnalyticsAdminServiceAsyncClient",)
