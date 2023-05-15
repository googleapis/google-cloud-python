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
from typing import (
    Dict,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.api_core.client_options import ClientOptions
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.analytics.admin_v1alpha import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore

from google.analytics.admin_v1alpha.services.analytics_admin_service import pagers
from google.analytics.admin_v1alpha.types import channel_group as gaa_channel_group
from google.analytics.admin_v1alpha.types import (
    expanded_data_set as gaa_expanded_data_set,
)
from google.analytics.admin_v1alpha.types import access_report, analytics_admin
from google.analytics.admin_v1alpha.types import audience
from google.analytics.admin_v1alpha.types import audience as gaa_audience
from google.analytics.admin_v1alpha.types import channel_group
from google.analytics.admin_v1alpha.types import event_create_and_edit
from google.analytics.admin_v1alpha.types import expanded_data_set
from google.analytics.admin_v1alpha.types import resources

from .client import AnalyticsAdminServiceClient
from .transports.base import DEFAULT_CLIENT_INFO, AnalyticsAdminServiceTransport
from .transports.grpc_asyncio import AnalyticsAdminServiceGrpcAsyncIOTransport


class AnalyticsAdminServiceAsyncClient:
    """Service Interface for the Analytics Admin API (GA4)."""

    _client: AnalyticsAdminServiceClient

    DEFAULT_ENDPOINT = AnalyticsAdminServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = AnalyticsAdminServiceClient.DEFAULT_MTLS_ENDPOINT

    access_binding_path = staticmethod(AnalyticsAdminServiceClient.access_binding_path)
    parse_access_binding_path = staticmethod(
        AnalyticsAdminServiceClient.parse_access_binding_path
    )
    account_path = staticmethod(AnalyticsAdminServiceClient.account_path)
    parse_account_path = staticmethod(AnalyticsAdminServiceClient.parse_account_path)
    account_summary_path = staticmethod(
        AnalyticsAdminServiceClient.account_summary_path
    )
    parse_account_summary_path = staticmethod(
        AnalyticsAdminServiceClient.parse_account_summary_path
    )
    ad_sense_link_path = staticmethod(AnalyticsAdminServiceClient.ad_sense_link_path)
    parse_ad_sense_link_path = staticmethod(
        AnalyticsAdminServiceClient.parse_ad_sense_link_path
    )
    attribution_settings_path = staticmethod(
        AnalyticsAdminServiceClient.attribution_settings_path
    )
    parse_attribution_settings_path = staticmethod(
        AnalyticsAdminServiceClient.parse_attribution_settings_path
    )
    audience_path = staticmethod(AnalyticsAdminServiceClient.audience_path)
    parse_audience_path = staticmethod(AnalyticsAdminServiceClient.parse_audience_path)
    big_query_link_path = staticmethod(AnalyticsAdminServiceClient.big_query_link_path)
    parse_big_query_link_path = staticmethod(
        AnalyticsAdminServiceClient.parse_big_query_link_path
    )
    channel_group_path = staticmethod(AnalyticsAdminServiceClient.channel_group_path)
    parse_channel_group_path = staticmethod(
        AnalyticsAdminServiceClient.parse_channel_group_path
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
    display_video360_advertiser_link_path = staticmethod(
        AnalyticsAdminServiceClient.display_video360_advertiser_link_path
    )
    parse_display_video360_advertiser_link_path = staticmethod(
        AnalyticsAdminServiceClient.parse_display_video360_advertiser_link_path
    )
    display_video360_advertiser_link_proposal_path = staticmethod(
        AnalyticsAdminServiceClient.display_video360_advertiser_link_proposal_path
    )
    parse_display_video360_advertiser_link_proposal_path = staticmethod(
        AnalyticsAdminServiceClient.parse_display_video360_advertiser_link_proposal_path
    )
    enhanced_measurement_settings_path = staticmethod(
        AnalyticsAdminServiceClient.enhanced_measurement_settings_path
    )
    parse_enhanced_measurement_settings_path = staticmethod(
        AnalyticsAdminServiceClient.parse_enhanced_measurement_settings_path
    )
    event_create_rule_path = staticmethod(
        AnalyticsAdminServiceClient.event_create_rule_path
    )
    parse_event_create_rule_path = staticmethod(
        AnalyticsAdminServiceClient.parse_event_create_rule_path
    )
    expanded_data_set_path = staticmethod(
        AnalyticsAdminServiceClient.expanded_data_set_path
    )
    parse_expanded_data_set_path = staticmethod(
        AnalyticsAdminServiceClient.parse_expanded_data_set_path
    )
    firebase_link_path = staticmethod(AnalyticsAdminServiceClient.firebase_link_path)
    parse_firebase_link_path = staticmethod(
        AnalyticsAdminServiceClient.parse_firebase_link_path
    )
    global_site_tag_path = staticmethod(
        AnalyticsAdminServiceClient.global_site_tag_path
    )
    parse_global_site_tag_path = staticmethod(
        AnalyticsAdminServiceClient.parse_global_site_tag_path
    )
    google_ads_link_path = staticmethod(
        AnalyticsAdminServiceClient.google_ads_link_path
    )
    parse_google_ads_link_path = staticmethod(
        AnalyticsAdminServiceClient.parse_google_ads_link_path
    )
    google_signals_settings_path = staticmethod(
        AnalyticsAdminServiceClient.google_signals_settings_path
    )
    parse_google_signals_settings_path = staticmethod(
        AnalyticsAdminServiceClient.parse_google_signals_settings_path
    )
    measurement_protocol_secret_path = staticmethod(
        AnalyticsAdminServiceClient.measurement_protocol_secret_path
    )
    parse_measurement_protocol_secret_path = staticmethod(
        AnalyticsAdminServiceClient.parse_measurement_protocol_secret_path
    )
    property_path = staticmethod(AnalyticsAdminServiceClient.property_path)
    parse_property_path = staticmethod(AnalyticsAdminServiceClient.parse_property_path)
    search_ads360_link_path = staticmethod(
        AnalyticsAdminServiceClient.search_ads360_link_path
    )
    parse_search_ads360_link_path = staticmethod(
        AnalyticsAdminServiceClient.parse_search_ads360_link_path
    )
    user_link_path = staticmethod(AnalyticsAdminServiceClient.user_link_path)
    parse_user_link_path = staticmethod(
        AnalyticsAdminServiceClient.parse_user_link_path
    )
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
        default mTLS endpoint; if the environment variable is "never", use the default API
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
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, AnalyticsAdminServiceTransport] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
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
        request: Optional[Union[analytics_admin.GetAccountRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Account:
        r"""Lookup for a single Account.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_get_account():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.GetAccountRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_account(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.GetAccountRequest, dict]]):
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
            google.analytics.admin_v1alpha.types.Account:
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
        request: Optional[Union[analytics_admin.ListAccountsRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAccountsAsyncPager:
        r"""Returns all accounts accessible by the caller.
        Note that these accounts might not currently have GA4
        properties. Soft-deleted (ie: "trashed") accounts are
        excluded by default. Returns an empty list if no
        relevant accounts are found.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_list_accounts():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.ListAccountsRequest(
                )

                # Make the request
                page_result = client.list_accounts(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.ListAccountsRequest, dict]]):
                The request object. Request message for ListAccounts RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListAccountsAsyncPager:
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
        request: Optional[Union[analytics_admin.DeleteAccountRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
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

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_delete_account():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.DeleteAccountRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_account(request=request)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.DeleteAccountRequest, dict]]):
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
        request: Optional[Union[analytics_admin.UpdateAccountRequest, dict]] = None,
        *,
        account: Optional[resources.Account] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Account:
        r"""Updates an account.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_update_account():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                account = admin_v1alpha.Account()
                account.display_name = "display_name_value"

                request = admin_v1alpha.UpdateAccountRequest(
                    account=account,
                )

                # Make the request
                response = await client.update_account(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.UpdateAccountRequest, dict]]):
                The request object. Request message for UpdateAccount
                RPC.
            account (:class:`google.analytics.admin_v1alpha.types.Account`):
                Required. The account to update. The account's ``name``
                field is used to identify the account.

                This corresponds to the ``account`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The list of fields to be updated. Field names
                must be in snake case (for example, "field_to_update").
                Omitted fields will not be updated. To replace the
                entire entity, use one path with the string "*" to match
                all fields.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.Account:
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
        request: Optional[
            Union[analytics_admin.ProvisionAccountTicketRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_admin.ProvisionAccountTicketResponse:
        r"""Requests a ticket for creating an account.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_provision_account_ticket():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.ProvisionAccountTicketRequest(
                )

                # Make the request
                response = await client.provision_account_ticket(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.ProvisionAccountTicketRequest, dict]]):
                The request object. Request message for
                ProvisionAccountTicket RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.ProvisionAccountTicketResponse:
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
        request: Optional[
            Union[analytics_admin.ListAccountSummariesRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAccountSummariesAsyncPager:
        r"""Returns summaries of all accounts accessible by the
        caller.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_list_account_summaries():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.ListAccountSummariesRequest(
                )

                # Make the request
                page_result = client.list_account_summaries(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.ListAccountSummariesRequest, dict]]):
                The request object. Request message for
                ListAccountSummaries RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListAccountSummariesAsyncPager:
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
        request: Optional[Union[analytics_admin.GetPropertyRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Property:
        r"""Lookup for a single "GA4" Property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_get_property():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.GetPropertyRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_property(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.GetPropertyRequest, dict]]):
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
            google.analytics.admin_v1alpha.types.Property:
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
        request: Optional[Union[analytics_admin.ListPropertiesRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
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

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_list_properties():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.ListPropertiesRequest(
                    filter="filter_value",
                )

                # Make the request
                page_result = client.list_properties(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.ListPropertiesRequest, dict]]):
                The request object. Request message for ListProperties
                RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListPropertiesAsyncPager:
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
        request: Optional[Union[analytics_admin.CreatePropertyRequest, dict]] = None,
        *,
        property: Optional[resources.Property] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Property:
        r"""Creates an "GA4" property with the specified location
        and attributes.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_create_property():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                property = admin_v1alpha.Property()
                property.display_name = "display_name_value"
                property.time_zone = "time_zone_value"

                request = admin_v1alpha.CreatePropertyRequest(
                    property=property,
                )

                # Make the request
                response = await client.create_property(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.CreatePropertyRequest, dict]]):
                The request object. Request message for CreateProperty
                RPC.
            property (:class:`google.analytics.admin_v1alpha.types.Property`):
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
            google.analytics.admin_v1alpha.types.Property:
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
        request: Optional[Union[analytics_admin.DeletePropertyRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
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
        Returns an error if the target is not found, or is not a
        GA4 Property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_delete_property():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.DeletePropertyRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.delete_property(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.DeletePropertyRequest, dict]]):
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
            google.analytics.admin_v1alpha.types.Property:
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
        request: Optional[Union[analytics_admin.UpdatePropertyRequest, dict]] = None,
        *,
        property: Optional[resources.Property] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Property:
        r"""Updates a property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_update_property():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                property = admin_v1alpha.Property()
                property.display_name = "display_name_value"
                property.time_zone = "time_zone_value"

                request = admin_v1alpha.UpdatePropertyRequest(
                    property=property,
                )

                # Make the request
                response = await client.update_property(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.UpdatePropertyRequest, dict]]):
                The request object. Request message for UpdateProperty
                RPC.
            property (:class:`google.analytics.admin_v1alpha.types.Property`):
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
            google.analytics.admin_v1alpha.types.Property:
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

    async def get_user_link(
        self,
        request: Optional[Union[analytics_admin.GetUserLinkRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.UserLink:
        r"""Gets information about a user's link to an account or
        property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_get_user_link():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.GetUserLinkRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_user_link(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.GetUserLinkRequest, dict]]):
                The request object. Request message for GetUserLink RPC.
            name (:class:`str`):
                Required. Example format:
                accounts/1234/userLinks/5678

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.UserLink:
                A resource message representing a
                user's permissions on an Account or
                Property resource.

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

        request = analytics_admin.GetUserLinkRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_user_link,
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

    async def batch_get_user_links(
        self,
        request: Optional[Union[analytics_admin.BatchGetUserLinksRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_admin.BatchGetUserLinksResponse:
        r"""Gets information about multiple users' links to an
        account or property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_batch_get_user_links():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.BatchGetUserLinksRequest(
                    parent="parent_value",
                    names=['names_value1', 'names_value2'],
                )

                # Make the request
                response = await client.batch_get_user_links(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.BatchGetUserLinksRequest, dict]]):
                The request object. Request message for BatchGetUserLinks
                RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.BatchGetUserLinksResponse:
                Response message for
                BatchGetUserLinks RPC.

        """
        # Create or coerce a protobuf request object.
        request = analytics_admin.BatchGetUserLinksRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.batch_get_user_links,
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

    async def list_user_links(
        self,
        request: Optional[Union[analytics_admin.ListUserLinksRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListUserLinksAsyncPager:
        r"""Lists all user links on an account or property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_list_user_links():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.ListUserLinksRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_user_links(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.ListUserLinksRequest, dict]]):
                The request object. Request message for ListUserLinks
                RPC.
            parent (:class:`str`):
                Required. Example format:
                accounts/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListUserLinksAsyncPager:
                Response message for ListUserLinks
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

        request = analytics_admin.ListUserLinksRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_user_links,
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
        response = pagers.ListUserLinksAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def audit_user_links(
        self,
        request: Optional[Union[analytics_admin.AuditUserLinksRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.AuditUserLinksAsyncPager:
        r"""Lists all user links on an account or property,
        including implicit ones that come from effective
        permissions granted by groups or organization admin
        roles.

        If a returned user link does not have direct
        permissions, they cannot be removed from the account or
        property directly with the DeleteUserLink command. They
        have to be removed from the group/etc that gives them
        permissions, which is currently only usable/discoverable
        in the GA or GMP UIs.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_audit_user_links():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.AuditUserLinksRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.audit_user_links(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.AuditUserLinksRequest, dict]]):
                The request object. Request message for AuditUserLinks
                RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.AuditUserLinksAsyncPager:
                Response message for AuditUserLinks
                RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        request = analytics_admin.AuditUserLinksRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.audit_user_links,
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
        response = pagers.AuditUserLinksAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_user_link(
        self,
        request: Optional[Union[analytics_admin.CreateUserLinkRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        user_link: Optional[resources.UserLink] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.UserLink:
        r"""Creates a user link on an account or property.
        If the user with the specified email already has
        permissions on the account or property, then the user's
        existing permissions will be unioned with the
        permissions specified in the new UserLink.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_create_user_link():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.CreateUserLinkRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.create_user_link(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.CreateUserLinkRequest, dict]]):
                The request object. Request message for CreateUserLink
                RPC.
                Users can have multiple email addresses
                associated with their Google account,
                and one of these email addresses is the
                "primary" email address. Any of the
                email addresses associated with a Google
                account may be used for a new UserLink,
                but the returned UserLink will always
                contain the "primary" email address. As
                a result, the input and output email
                address for this request may differ.
            parent (:class:`str`):
                Required. Example format:
                accounts/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            user_link (:class:`google.analytics.admin_v1alpha.types.UserLink`):
                Required. The user link to create.
                This corresponds to the ``user_link`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.UserLink:
                A resource message representing a
                user's permissions on an Account or
                Property resource.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, user_link])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.CreateUserLinkRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if user_link is not None:
            request.user_link = user_link

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_user_link,
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

    async def batch_create_user_links(
        self,
        request: Optional[
            Union[analytics_admin.BatchCreateUserLinksRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_admin.BatchCreateUserLinksResponse:
        r"""Creates information about multiple users' links to an
        account or property.
        This method is transactional. If any UserLink cannot be
        created, none of the UserLinks will be created.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_batch_create_user_links():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                requests = admin_v1alpha.CreateUserLinkRequest()
                requests.parent = "parent_value"

                request = admin_v1alpha.BatchCreateUserLinksRequest(
                    parent="parent_value",
                    requests=requests,
                )

                # Make the request
                response = await client.batch_create_user_links(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.BatchCreateUserLinksRequest, dict]]):
                The request object. Request message for
                BatchCreateUserLinks RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.BatchCreateUserLinksResponse:
                Response message for
                BatchCreateUserLinks RPC.

        """
        # Create or coerce a protobuf request object.
        request = analytics_admin.BatchCreateUserLinksRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.batch_create_user_links,
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

    async def update_user_link(
        self,
        request: Optional[Union[analytics_admin.UpdateUserLinkRequest, dict]] = None,
        *,
        user_link: Optional[resources.UserLink] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.UserLink:
        r"""Updates a user link on an account or property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_update_user_link():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.UpdateUserLinkRequest(
                )

                # Make the request
                response = await client.update_user_link(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.UpdateUserLinkRequest, dict]]):
                The request object. Request message for UpdateUserLink
                RPC.
            user_link (:class:`google.analytics.admin_v1alpha.types.UserLink`):
                Required. The user link to update.
                This corresponds to the ``user_link`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.UserLink:
                A resource message representing a
                user's permissions on an Account or
                Property resource.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([user_link])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.UpdateUserLinkRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if user_link is not None:
            request.user_link = user_link

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_user_link,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("user_link.name", request.user_link.name),)
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

    async def batch_update_user_links(
        self,
        request: Optional[
            Union[analytics_admin.BatchUpdateUserLinksRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_admin.BatchUpdateUserLinksResponse:
        r"""Updates information about multiple users' links to an
        account or property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_batch_update_user_links():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.BatchUpdateUserLinksRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.batch_update_user_links(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.BatchUpdateUserLinksRequest, dict]]):
                The request object. Request message for
                BatchUpdateUserLinks RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.BatchUpdateUserLinksResponse:
                Response message for
                BatchUpdateUserLinks RPC.

        """
        # Create or coerce a protobuf request object.
        request = analytics_admin.BatchUpdateUserLinksRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.batch_update_user_links,
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

    async def delete_user_link(
        self,
        request: Optional[Union[analytics_admin.DeleteUserLinkRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a user link on an account or property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_delete_user_link():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.DeleteUserLinkRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_user_link(request=request)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.DeleteUserLinkRequest, dict]]):
                The request object. Request message for DeleteUserLink
                RPC.
            name (:class:`str`):
                Required. Example format:
                accounts/1234/userLinks/5678

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

        request = analytics_admin.DeleteUserLinkRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_user_link,
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

    async def batch_delete_user_links(
        self,
        request: Optional[
            Union[analytics_admin.BatchDeleteUserLinksRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes information about multiple users' links to an
        account or property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_batch_delete_user_links():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                requests = admin_v1alpha.DeleteUserLinkRequest()
                requests.name = "name_value"

                request = admin_v1alpha.BatchDeleteUserLinksRequest(
                    parent="parent_value",
                    requests=requests,
                )

                # Make the request
                await client.batch_delete_user_links(request=request)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.BatchDeleteUserLinksRequest, dict]]):
                The request object. Request message for
                BatchDeleteUserLinks RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        request = analytics_admin.BatchDeleteUserLinksRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.batch_delete_user_links,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def create_firebase_link(
        self,
        request: Optional[
            Union[analytics_admin.CreateFirebaseLinkRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        firebase_link: Optional[resources.FirebaseLink] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.FirebaseLink:
        r"""Creates a FirebaseLink.
        Properties can have at most one FirebaseLink.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_create_firebase_link():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.CreateFirebaseLinkRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.create_firebase_link(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.CreateFirebaseLinkRequest, dict]]):
                The request object. Request message for
                CreateFirebaseLink RPC
            parent (:class:`str`):
                Required. Format: properties/{property_id} Example:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            firebase_link (:class:`google.analytics.admin_v1alpha.types.FirebaseLink`):
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
            google.analytics.admin_v1alpha.types.FirebaseLink:
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
        request: Optional[
            Union[analytics_admin.DeleteFirebaseLinkRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a FirebaseLink on a property

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_delete_firebase_link():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.DeleteFirebaseLinkRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_firebase_link(request=request)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.DeleteFirebaseLinkRequest, dict]]):
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
        request: Optional[Union[analytics_admin.ListFirebaseLinksRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListFirebaseLinksAsyncPager:
        r"""Lists FirebaseLinks on a property.
        Properties can have at most one FirebaseLink.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_list_firebase_links():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.ListFirebaseLinksRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_firebase_links(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.ListFirebaseLinksRequest, dict]]):
                The request object. Request message for ListFirebaseLinks
                RPC
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListFirebaseLinksAsyncPager:
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

    async def get_global_site_tag(
        self,
        request: Optional[Union[analytics_admin.GetGlobalSiteTagRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.GlobalSiteTag:
        r"""Returns the Site Tag for the specified web stream.
        Site Tags are immutable singletons.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_get_global_site_tag():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.GetGlobalSiteTagRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_global_site_tag(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.GetGlobalSiteTagRequest, dict]]):
                The request object. Request message for GetGlobalSiteTag
                RPC.
            name (:class:`str`):
                Required. The name of the site tag to lookup. Note that
                site tags are singletons and do not have unique IDs.
                Format:
                properties/{property_id}/dataStreams/{stream_id}/globalSiteTag
                Example: "properties/123/dataStreams/456/globalSiteTag"

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.GlobalSiteTag:
                Read-only resource with the tag for
                sending data from a website to a
                DataStream. Only present for web
                DataStream resources.

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

        request = analytics_admin.GetGlobalSiteTagRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_global_site_tag,
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

    async def create_google_ads_link(
        self,
        request: Optional[
            Union[analytics_admin.CreateGoogleAdsLinkRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        google_ads_link: Optional[resources.GoogleAdsLink] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.GoogleAdsLink:
        r"""Creates a GoogleAdsLink.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_create_google_ads_link():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.CreateGoogleAdsLinkRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.create_google_ads_link(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.CreateGoogleAdsLinkRequest, dict]]):
                The request object. Request message for
                CreateGoogleAdsLink RPC
            parent (:class:`str`):
                Required. Example format:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            google_ads_link (:class:`google.analytics.admin_v1alpha.types.GoogleAdsLink`):
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
            google.analytics.admin_v1alpha.types.GoogleAdsLink:
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
        request: Optional[
            Union[analytics_admin.UpdateGoogleAdsLinkRequest, dict]
        ] = None,
        *,
        google_ads_link: Optional[resources.GoogleAdsLink] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.GoogleAdsLink:
        r"""Updates a GoogleAdsLink on a property

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_update_google_ads_link():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.UpdateGoogleAdsLinkRequest(
                )

                # Make the request
                response = await client.update_google_ads_link(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.UpdateGoogleAdsLinkRequest, dict]]):
                The request object. Request message for
                UpdateGoogleAdsLink RPC
            google_ads_link (:class:`google.analytics.admin_v1alpha.types.GoogleAdsLink`):
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
            google.analytics.admin_v1alpha.types.GoogleAdsLink:
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
        request: Optional[
            Union[analytics_admin.DeleteGoogleAdsLinkRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a GoogleAdsLink on a property

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_delete_google_ads_link():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.DeleteGoogleAdsLinkRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_google_ads_link(request=request)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.DeleteGoogleAdsLinkRequest, dict]]):
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
        request: Optional[
            Union[analytics_admin.ListGoogleAdsLinksRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListGoogleAdsLinksAsyncPager:
        r"""Lists GoogleAdsLinks on a property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_list_google_ads_links():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.ListGoogleAdsLinksRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_google_ads_links(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.ListGoogleAdsLinksRequest, dict]]):
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListGoogleAdsLinksAsyncPager:
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
        request: Optional[
            Union[analytics_admin.GetDataSharingSettingsRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.DataSharingSettings:
        r"""Get data sharing settings on an account.
        Data sharing settings are singletons.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_get_data_sharing_settings():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.GetDataSharingSettingsRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_data_sharing_settings(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.GetDataSharingSettingsRequest, dict]]):
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
            google.analytics.admin_v1alpha.types.DataSharingSettings:
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
        request: Optional[
            Union[analytics_admin.GetMeasurementProtocolSecretRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.MeasurementProtocolSecret:
        r"""Lookup for a single "GA4" MeasurementProtocolSecret.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_get_measurement_protocol_secret():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.GetMeasurementProtocolSecretRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_measurement_protocol_secret(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.GetMeasurementProtocolSecretRequest, dict]]):
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
            google.analytics.admin_v1alpha.types.MeasurementProtocolSecret:
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
        request: Optional[
            Union[analytics_admin.ListMeasurementProtocolSecretsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListMeasurementProtocolSecretsAsyncPager:
        r"""Returns child MeasurementProtocolSecrets under the
        specified parent Property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_list_measurement_protocol_secrets():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.ListMeasurementProtocolSecretsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_measurement_protocol_secrets(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.ListMeasurementProtocolSecretsRequest, dict]]):
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListMeasurementProtocolSecretsAsyncPager:
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
        request: Optional[
            Union[analytics_admin.CreateMeasurementProtocolSecretRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        measurement_protocol_secret: Optional[
            resources.MeasurementProtocolSecret
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.MeasurementProtocolSecret:
        r"""Creates a measurement protocol secret.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_create_measurement_protocol_secret():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                measurement_protocol_secret = admin_v1alpha.MeasurementProtocolSecret()
                measurement_protocol_secret.display_name = "display_name_value"

                request = admin_v1alpha.CreateMeasurementProtocolSecretRequest(
                    parent="parent_value",
                    measurement_protocol_secret=measurement_protocol_secret,
                )

                # Make the request
                response = await client.create_measurement_protocol_secret(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.CreateMeasurementProtocolSecretRequest, dict]]):
                The request object. Request message for
                CreateMeasurementProtocolSecret RPC
            parent (:class:`str`):
                Required. The parent resource where
                this secret will be created. Format:
                properties/{property}/dataStreams/{dataStream}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            measurement_protocol_secret (:class:`google.analytics.admin_v1alpha.types.MeasurementProtocolSecret`):
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
            google.analytics.admin_v1alpha.types.MeasurementProtocolSecret:
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
        request: Optional[
            Union[analytics_admin.DeleteMeasurementProtocolSecretRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes target MeasurementProtocolSecret.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_delete_measurement_protocol_secret():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.DeleteMeasurementProtocolSecretRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_measurement_protocol_secret(request=request)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.DeleteMeasurementProtocolSecretRequest, dict]]):
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
        request: Optional[
            Union[analytics_admin.UpdateMeasurementProtocolSecretRequest, dict]
        ] = None,
        *,
        measurement_protocol_secret: Optional[
            resources.MeasurementProtocolSecret
        ] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.MeasurementProtocolSecret:
        r"""Updates a measurement protocol secret.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_update_measurement_protocol_secret():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                measurement_protocol_secret = admin_v1alpha.MeasurementProtocolSecret()
                measurement_protocol_secret.display_name = "display_name_value"

                request = admin_v1alpha.UpdateMeasurementProtocolSecretRequest(
                    measurement_protocol_secret=measurement_protocol_secret,
                )

                # Make the request
                response = await client.update_measurement_protocol_secret(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.UpdateMeasurementProtocolSecretRequest, dict]]):
                The request object. Request message for
                UpdateMeasurementProtocolSecret RPC
            measurement_protocol_secret (:class:`google.analytics.admin_v1alpha.types.MeasurementProtocolSecret`):
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
            google.analytics.admin_v1alpha.types.MeasurementProtocolSecret:
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
        request: Optional[
            Union[analytics_admin.AcknowledgeUserDataCollectionRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_admin.AcknowledgeUserDataCollectionResponse:
        r"""Acknowledges the terms of user data collection for
        the specified property.
        This acknowledgement must be completed (either in the
        Google Analytics UI or through this API) before
        MeasurementProtocolSecret resources may be created.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_acknowledge_user_data_collection():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.AcknowledgeUserDataCollectionRequest(
                    property="property_value",
                    acknowledgement="acknowledgement_value",
                )

                # Make the request
                response = await client.acknowledge_user_data_collection(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.AcknowledgeUserDataCollectionRequest, dict]]):
                The request object. Request message for
                AcknowledgeUserDataCollection RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.AcknowledgeUserDataCollectionResponse:
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
        request: Optional[
            Union[analytics_admin.SearchChangeHistoryEventsRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.SearchChangeHistoryEventsAsyncPager:
        r"""Searches through all changes to an account or its
        children given the specified set of filters.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_search_change_history_events():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.SearchChangeHistoryEventsRequest(
                    account="account_value",
                )

                # Make the request
                page_result = client.search_change_history_events(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.SearchChangeHistoryEventsRequest, dict]]):
                The request object. Request message for
                SearchChangeHistoryEvents RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.SearchChangeHistoryEventsAsyncPager:
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

    async def get_google_signals_settings(
        self,
        request: Optional[
            Union[analytics_admin.GetGoogleSignalsSettingsRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.GoogleSignalsSettings:
        r"""Lookup for Google Signals settings for a property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_get_google_signals_settings():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.GetGoogleSignalsSettingsRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_google_signals_settings(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.GetGoogleSignalsSettingsRequest, dict]]):
                The request object. Request message for
                GetGoogleSignalsSettings RPC
            name (:class:`str`):
                Required. The name of the google
                signals settings to retrieve. Format:
                properties/{property}/googleSignalsSettings

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.GoogleSignalsSettings:
                Settings values for Google Signals.
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

        request = analytics_admin.GetGoogleSignalsSettingsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_google_signals_settings,
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

    async def update_google_signals_settings(
        self,
        request: Optional[
            Union[analytics_admin.UpdateGoogleSignalsSettingsRequest, dict]
        ] = None,
        *,
        google_signals_settings: Optional[resources.GoogleSignalsSettings] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.GoogleSignalsSettings:
        r"""Updates Google Signals settings for a property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_update_google_signals_settings():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.UpdateGoogleSignalsSettingsRequest(
                )

                # Make the request
                response = await client.update_google_signals_settings(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.UpdateGoogleSignalsSettingsRequest, dict]]):
                The request object. Request message for
                UpdateGoogleSignalsSettings RPC
            google_signals_settings (:class:`google.analytics.admin_v1alpha.types.GoogleSignalsSettings`):
                Required. The settings to update. The ``name`` field is
                used to identify the settings to be updated.

                This corresponds to the ``google_signals_settings`` field
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
            google.analytics.admin_v1alpha.types.GoogleSignalsSettings:
                Settings values for Google Signals.
                This is a singleton resource.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([google_signals_settings, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.UpdateGoogleSignalsSettingsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if google_signals_settings is not None:
            request.google_signals_settings = google_signals_settings
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_google_signals_settings,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    (
                        "google_signals_settings.name",
                        request.google_signals_settings.name,
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

    async def create_conversion_event(
        self,
        request: Optional[
            Union[analytics_admin.CreateConversionEventRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        conversion_event: Optional[resources.ConversionEvent] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.ConversionEvent:
        r"""Creates a conversion event with the specified
        attributes.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_create_conversion_event():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.CreateConversionEventRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.create_conversion_event(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.CreateConversionEventRequest, dict]]):
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
            conversion_event (:class:`google.analytics.admin_v1alpha.types.ConversionEvent`):
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
            google.analytics.admin_v1alpha.types.ConversionEvent:
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
        request: Optional[
            Union[analytics_admin.GetConversionEventRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.ConversionEvent:
        r"""Retrieve a single conversion event.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_get_conversion_event():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.GetConversionEventRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_conversion_event(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.GetConversionEventRequest, dict]]):
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
            google.analytics.admin_v1alpha.types.ConversionEvent:
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
        request: Optional[
            Union[analytics_admin.DeleteConversionEventRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a conversion event in a property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_delete_conversion_event():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.DeleteConversionEventRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_conversion_event(request=request)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.DeleteConversionEventRequest, dict]]):
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
        request: Optional[
            Union[analytics_admin.ListConversionEventsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListConversionEventsAsyncPager:
        r"""Returns a list of conversion events in the specified
        parent property.
        Returns an empty list if no conversion events are found.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_list_conversion_events():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.ListConversionEventsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_conversion_events(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.ListConversionEventsRequest, dict]]):
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListConversionEventsAsyncPager:
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

    async def get_display_video360_advertiser_link(
        self,
        request: Optional[
            Union[analytics_admin.GetDisplayVideo360AdvertiserLinkRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.DisplayVideo360AdvertiserLink:
        r"""Look up a single DisplayVideo360AdvertiserLink

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_get_display_video360_advertiser_link():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.GetDisplayVideo360AdvertiserLinkRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_display_video360_advertiser_link(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.GetDisplayVideo360AdvertiserLinkRequest, dict]]):
                The request object. Request message for
                GetDisplayVideo360AdvertiserLink RPC.
            name (:class:`str`):
                Required. The name of the
                DisplayVideo360AdvertiserLink to get.
                Example format:
                properties/1234/displayVideo360AdvertiserLink/5678

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.DisplayVideo360AdvertiserLink:
                A link between a GA4 property and a
                Display & Video 360 advertiser.

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

        request = analytics_admin.GetDisplayVideo360AdvertiserLinkRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_display_video360_advertiser_link,
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

    async def list_display_video360_advertiser_links(
        self,
        request: Optional[
            Union[analytics_admin.ListDisplayVideo360AdvertiserLinksRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDisplayVideo360AdvertiserLinksAsyncPager:
        r"""Lists all DisplayVideo360AdvertiserLinks on a
        property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_list_display_video360_advertiser_links():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.ListDisplayVideo360AdvertiserLinksRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_display_video360_advertiser_links(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.ListDisplayVideo360AdvertiserLinksRequest, dict]]):
                The request object. Request message for
                ListDisplayVideo360AdvertiserLinks RPC.
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListDisplayVideo360AdvertiserLinksAsyncPager:
                Response message for
                ListDisplayVideo360AdvertiserLinks RPC.
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

        request = analytics_admin.ListDisplayVideo360AdvertiserLinksRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_display_video360_advertiser_links,
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
        response = pagers.ListDisplayVideo360AdvertiserLinksAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_display_video360_advertiser_link(
        self,
        request: Optional[
            Union[analytics_admin.CreateDisplayVideo360AdvertiserLinkRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        display_video_360_advertiser_link: Optional[
            resources.DisplayVideo360AdvertiserLink
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.DisplayVideo360AdvertiserLink:
        r"""Creates a DisplayVideo360AdvertiserLink.
        This can only be utilized by users who have proper
        authorization both on the Google Analytics property and
        on the Display & Video 360 advertiser. Users who do not
        have access to the Display & Video 360 advertiser should
        instead seek to create a DisplayVideo360LinkProposal.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_create_display_video360_advertiser_link():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.CreateDisplayVideo360AdvertiserLinkRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.create_display_video360_advertiser_link(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.CreateDisplayVideo360AdvertiserLinkRequest, dict]]):
                The request object. Request message for
                CreateDisplayVideo360AdvertiserLink RPC.
            parent (:class:`str`):
                Required. Example format:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            display_video_360_advertiser_link (:class:`google.analytics.admin_v1alpha.types.DisplayVideo360AdvertiserLink`):
                Required. The
                DisplayVideo360AdvertiserLink to create.

                This corresponds to the ``display_video_360_advertiser_link`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.DisplayVideo360AdvertiserLink:
                A link between a GA4 property and a
                Display & Video 360 advertiser.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, display_video_360_advertiser_link])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.CreateDisplayVideo360AdvertiserLinkRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if display_video_360_advertiser_link is not None:
            request.display_video_360_advertiser_link = (
                display_video_360_advertiser_link
            )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_display_video360_advertiser_link,
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

    async def delete_display_video360_advertiser_link(
        self,
        request: Optional[
            Union[analytics_admin.DeleteDisplayVideo360AdvertiserLinkRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a DisplayVideo360AdvertiserLink on a
        property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_delete_display_video360_advertiser_link():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.DeleteDisplayVideo360AdvertiserLinkRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_display_video360_advertiser_link(request=request)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.DeleteDisplayVideo360AdvertiserLinkRequest, dict]]):
                The request object. Request message for
                DeleteDisplayVideo360AdvertiserLink RPC.
            name (:class:`str`):
                Required. The name of the
                DisplayVideo360AdvertiserLink to delete.
                Example format:
                properties/1234/displayVideo360AdvertiserLinks/5678

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

        request = analytics_admin.DeleteDisplayVideo360AdvertiserLinkRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_display_video360_advertiser_link,
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

    async def update_display_video360_advertiser_link(
        self,
        request: Optional[
            Union[analytics_admin.UpdateDisplayVideo360AdvertiserLinkRequest, dict]
        ] = None,
        *,
        display_video_360_advertiser_link: Optional[
            resources.DisplayVideo360AdvertiserLink
        ] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.DisplayVideo360AdvertiserLink:
        r"""Updates a DisplayVideo360AdvertiserLink on a
        property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_update_display_video360_advertiser_link():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.UpdateDisplayVideo360AdvertiserLinkRequest(
                )

                # Make the request
                response = await client.update_display_video360_advertiser_link(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.UpdateDisplayVideo360AdvertiserLinkRequest, dict]]):
                The request object. Request message for
                UpdateDisplayVideo360AdvertiserLink RPC.
            display_video_360_advertiser_link (:class:`google.analytics.admin_v1alpha.types.DisplayVideo360AdvertiserLink`):
                The DisplayVideo360AdvertiserLink to
                update

                This corresponds to the ``display_video_360_advertiser_link`` field
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
            google.analytics.admin_v1alpha.types.DisplayVideo360AdvertiserLink:
                A link between a GA4 property and a
                Display & Video 360 advertiser.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([display_video_360_advertiser_link, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.UpdateDisplayVideo360AdvertiserLinkRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if display_video_360_advertiser_link is not None:
            request.display_video_360_advertiser_link = (
                display_video_360_advertiser_link
            )
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_display_video360_advertiser_link,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    (
                        "display_video_360_advertiser_link.name",
                        request.display_video_360_advertiser_link.name,
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

    async def get_display_video360_advertiser_link_proposal(
        self,
        request: Optional[
            Union[analytics_admin.GetDisplayVideo360AdvertiserLinkProposalRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.DisplayVideo360AdvertiserLinkProposal:
        r"""Lookup for a single
        DisplayVideo360AdvertiserLinkProposal.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_get_display_video360_advertiser_link_proposal():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.GetDisplayVideo360AdvertiserLinkProposalRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_display_video360_advertiser_link_proposal(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.GetDisplayVideo360AdvertiserLinkProposalRequest, dict]]):
                The request object. Request message for
                GetDisplayVideo360AdvertiserLinkProposal
                RPC.
            name (:class:`str`):
                Required. The name of the
                DisplayVideo360AdvertiserLinkProposal to
                get. Example format:
                properties/1234/displayVideo360AdvertiserLinkProposals/5678

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.DisplayVideo360AdvertiserLinkProposal:
                A proposal for a link between a GA4
                property and a Display & Video 360
                advertiser.
                A proposal is converted to a
                DisplayVideo360AdvertiserLink once
                approved. Google Analytics admins
                approve inbound proposals while Display
                & Video 360 admins approve outbound
                proposals.

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

        request = analytics_admin.GetDisplayVideo360AdvertiserLinkProposalRequest(
            request
        )

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_display_video360_advertiser_link_proposal,
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

    async def list_display_video360_advertiser_link_proposals(
        self,
        request: Optional[
            Union[
                analytics_admin.ListDisplayVideo360AdvertiserLinkProposalsRequest, dict
            ]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDisplayVideo360AdvertiserLinkProposalsAsyncPager:
        r"""Lists DisplayVideo360AdvertiserLinkProposals on a
        property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_list_display_video360_advertiser_link_proposals():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.ListDisplayVideo360AdvertiserLinkProposalsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_display_video360_advertiser_link_proposals(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.ListDisplayVideo360AdvertiserLinkProposalsRequest, dict]]):
                The request object. Request message for
                ListDisplayVideo360AdvertiserLinkProposals
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListDisplayVideo360AdvertiserLinkProposalsAsyncPager:
                Response message for
                ListDisplayVideo360AdvertiserLinkProposals
                RPC.  Iterating over this object will
                yield results and resolve additional
                pages automatically.

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

        request = analytics_admin.ListDisplayVideo360AdvertiserLinkProposalsRequest(
            request
        )

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_display_video360_advertiser_link_proposals,
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
        response = pagers.ListDisplayVideo360AdvertiserLinkProposalsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_display_video360_advertiser_link_proposal(
        self,
        request: Optional[
            Union[
                analytics_admin.CreateDisplayVideo360AdvertiserLinkProposalRequest, dict
            ]
        ] = None,
        *,
        parent: Optional[str] = None,
        display_video_360_advertiser_link_proposal: Optional[
            resources.DisplayVideo360AdvertiserLinkProposal
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.DisplayVideo360AdvertiserLinkProposal:
        r"""Creates a DisplayVideo360AdvertiserLinkProposal.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_create_display_video360_advertiser_link_proposal():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.CreateDisplayVideo360AdvertiserLinkProposalRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.create_display_video360_advertiser_link_proposal(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.CreateDisplayVideo360AdvertiserLinkProposalRequest, dict]]):
                The request object. Request message for
                CreateDisplayVideo360AdvertiserLinkProposal
                RPC.
            parent (:class:`str`):
                Required. Example format:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            display_video_360_advertiser_link_proposal (:class:`google.analytics.admin_v1alpha.types.DisplayVideo360AdvertiserLinkProposal`):
                Required. The
                DisplayVideo360AdvertiserLinkProposal to
                create.

                This corresponds to the ``display_video_360_advertiser_link_proposal`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.DisplayVideo360AdvertiserLinkProposal:
                A proposal for a link between a GA4
                property and a Display & Video 360
                advertiser.
                A proposal is converted to a
                DisplayVideo360AdvertiserLink once
                approved. Google Analytics admins
                approve inbound proposals while Display
                & Video 360 admins approve outbound
                proposals.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, display_video_360_advertiser_link_proposal])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.CreateDisplayVideo360AdvertiserLinkProposalRequest(
            request
        )

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if display_video_360_advertiser_link_proposal is not None:
            request.display_video_360_advertiser_link_proposal = (
                display_video_360_advertiser_link_proposal
            )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_display_video360_advertiser_link_proposal,
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

    async def delete_display_video360_advertiser_link_proposal(
        self,
        request: Optional[
            Union[
                analytics_admin.DeleteDisplayVideo360AdvertiserLinkProposalRequest, dict
            ]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a DisplayVideo360AdvertiserLinkProposal on a
        property. This can only be used on cancelled proposals.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_delete_display_video360_advertiser_link_proposal():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.DeleteDisplayVideo360AdvertiserLinkProposalRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_display_video360_advertiser_link_proposal(request=request)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.DeleteDisplayVideo360AdvertiserLinkProposalRequest, dict]]):
                The request object. Request message for
                DeleteDisplayVideo360AdvertiserLinkProposal
                RPC.
            name (:class:`str`):
                Required. The name of the
                DisplayVideo360AdvertiserLinkProposal to
                delete. Example format:
                properties/1234/displayVideo360AdvertiserLinkProposals/5678

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

        request = analytics_admin.DeleteDisplayVideo360AdvertiserLinkProposalRequest(
            request
        )

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_display_video360_advertiser_link_proposal,
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

    async def approve_display_video360_advertiser_link_proposal(
        self,
        request: Optional[
            Union[
                analytics_admin.ApproveDisplayVideo360AdvertiserLinkProposalRequest,
                dict,
            ]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_admin.ApproveDisplayVideo360AdvertiserLinkProposalResponse:
        r"""Approves a DisplayVideo360AdvertiserLinkProposal.
        The DisplayVideo360AdvertiserLinkProposal will be
        deleted and a new DisplayVideo360AdvertiserLink will be
        created.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_approve_display_video360_advertiser_link_proposal():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.ApproveDisplayVideo360AdvertiserLinkProposalRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.approve_display_video360_advertiser_link_proposal(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.ApproveDisplayVideo360AdvertiserLinkProposalRequest, dict]]):
                The request object. Request message for
                ApproveDisplayVideo360AdvertiserLinkProposal
                RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.ApproveDisplayVideo360AdvertiserLinkProposalResponse:
                Response message for
                ApproveDisplayVideo360AdvertiserLinkProposal
                RPC.

        """
        # Create or coerce a protobuf request object.
        request = analytics_admin.ApproveDisplayVideo360AdvertiserLinkProposalRequest(
            request
        )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.approve_display_video360_advertiser_link_proposal,
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

    async def cancel_display_video360_advertiser_link_proposal(
        self,
        request: Optional[
            Union[
                analytics_admin.CancelDisplayVideo360AdvertiserLinkProposalRequest, dict
            ]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.DisplayVideo360AdvertiserLinkProposal:
        r"""Cancels a DisplayVideo360AdvertiserLinkProposal.
        Cancelling can mean either:
        - Declining a proposal initiated from Display & Video
        360 - Withdrawing a proposal initiated from Google
        Analytics After being cancelled, a proposal will
        eventually be deleted automatically.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_cancel_display_video360_advertiser_link_proposal():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.CancelDisplayVideo360AdvertiserLinkProposalRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.cancel_display_video360_advertiser_link_proposal(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.CancelDisplayVideo360AdvertiserLinkProposalRequest, dict]]):
                The request object. Request message for
                CancelDisplayVideo360AdvertiserLinkProposal
                RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.DisplayVideo360AdvertiserLinkProposal:
                A proposal for a link between a GA4
                property and a Display & Video 360
                advertiser.
                A proposal is converted to a
                DisplayVideo360AdvertiserLink once
                approved. Google Analytics admins
                approve inbound proposals while Display
                & Video 360 admins approve outbound
                proposals.

        """
        # Create or coerce a protobuf request object.
        request = analytics_admin.CancelDisplayVideo360AdvertiserLinkProposalRequest(
            request
        )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.cancel_display_video360_advertiser_link_proposal,
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

    async def create_custom_dimension(
        self,
        request: Optional[
            Union[analytics_admin.CreateCustomDimensionRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        custom_dimension: Optional[resources.CustomDimension] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.CustomDimension:
        r"""Creates a CustomDimension.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_create_custom_dimension():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                custom_dimension = admin_v1alpha.CustomDimension()
                custom_dimension.parameter_name = "parameter_name_value"
                custom_dimension.display_name = "display_name_value"
                custom_dimension.scope = "ITEM"

                request = admin_v1alpha.CreateCustomDimensionRequest(
                    parent="parent_value",
                    custom_dimension=custom_dimension,
                )

                # Make the request
                response = await client.create_custom_dimension(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.CreateCustomDimensionRequest, dict]]):
                The request object. Request message for
                CreateCustomDimension RPC.
            parent (:class:`str`):
                Required. Example format:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            custom_dimension (:class:`google.analytics.admin_v1alpha.types.CustomDimension`):
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
            google.analytics.admin_v1alpha.types.CustomDimension:
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
        request: Optional[
            Union[analytics_admin.UpdateCustomDimensionRequest, dict]
        ] = None,
        *,
        custom_dimension: Optional[resources.CustomDimension] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.CustomDimension:
        r"""Updates a CustomDimension on a property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_update_custom_dimension():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.UpdateCustomDimensionRequest(
                )

                # Make the request
                response = await client.update_custom_dimension(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.UpdateCustomDimensionRequest, dict]]):
                The request object. Request message for
                UpdateCustomDimension RPC.
            custom_dimension (:class:`google.analytics.admin_v1alpha.types.CustomDimension`):
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
            google.analytics.admin_v1alpha.types.CustomDimension:
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
        request: Optional[
            Union[analytics_admin.ListCustomDimensionsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCustomDimensionsAsyncPager:
        r"""Lists CustomDimensions on a property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_list_custom_dimensions():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.ListCustomDimensionsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_custom_dimensions(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.ListCustomDimensionsRequest, dict]]):
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListCustomDimensionsAsyncPager:
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
        request: Optional[
            Union[analytics_admin.ArchiveCustomDimensionRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Archives a CustomDimension on a property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_archive_custom_dimension():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.ArchiveCustomDimensionRequest(
                    name="name_value",
                )

                # Make the request
                await client.archive_custom_dimension(request=request)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.ArchiveCustomDimensionRequest, dict]]):
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
        request: Optional[
            Union[analytics_admin.GetCustomDimensionRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.CustomDimension:
        r"""Lookup for a single CustomDimension.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_get_custom_dimension():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.GetCustomDimensionRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_custom_dimension(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.GetCustomDimensionRequest, dict]]):
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
            google.analytics.admin_v1alpha.types.CustomDimension:
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
        request: Optional[
            Union[analytics_admin.CreateCustomMetricRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        custom_metric: Optional[resources.CustomMetric] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.CustomMetric:
        r"""Creates a CustomMetric.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_create_custom_metric():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                custom_metric = admin_v1alpha.CustomMetric()
                custom_metric.parameter_name = "parameter_name_value"
                custom_metric.display_name = "display_name_value"
                custom_metric.measurement_unit = "HOURS"
                custom_metric.scope = "EVENT"

                request = admin_v1alpha.CreateCustomMetricRequest(
                    parent="parent_value",
                    custom_metric=custom_metric,
                )

                # Make the request
                response = await client.create_custom_metric(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.CreateCustomMetricRequest, dict]]):
                The request object. Request message for
                CreateCustomMetric RPC.
            parent (:class:`str`):
                Required. Example format:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            custom_metric (:class:`google.analytics.admin_v1alpha.types.CustomMetric`):
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
            google.analytics.admin_v1alpha.types.CustomMetric:
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
        request: Optional[
            Union[analytics_admin.UpdateCustomMetricRequest, dict]
        ] = None,
        *,
        custom_metric: Optional[resources.CustomMetric] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.CustomMetric:
        r"""Updates a CustomMetric on a property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_update_custom_metric():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.UpdateCustomMetricRequest(
                )

                # Make the request
                response = await client.update_custom_metric(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.UpdateCustomMetricRequest, dict]]):
                The request object. Request message for
                UpdateCustomMetric RPC.
            custom_metric (:class:`google.analytics.admin_v1alpha.types.CustomMetric`):
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
            google.analytics.admin_v1alpha.types.CustomMetric:
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
        request: Optional[Union[analytics_admin.ListCustomMetricsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCustomMetricsAsyncPager:
        r"""Lists CustomMetrics on a property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_list_custom_metrics():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.ListCustomMetricsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_custom_metrics(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.ListCustomMetricsRequest, dict]]):
                The request object. Request message for ListCustomMetrics
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListCustomMetricsAsyncPager:
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
        request: Optional[
            Union[analytics_admin.ArchiveCustomMetricRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Archives a CustomMetric on a property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_archive_custom_metric():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.ArchiveCustomMetricRequest(
                    name="name_value",
                )

                # Make the request
                await client.archive_custom_metric(request=request)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.ArchiveCustomMetricRequest, dict]]):
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
        request: Optional[Union[analytics_admin.GetCustomMetricRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.CustomMetric:
        r"""Lookup for a single CustomMetric.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_get_custom_metric():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.GetCustomMetricRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_custom_metric(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.GetCustomMetricRequest, dict]]):
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
            google.analytics.admin_v1alpha.types.CustomMetric:
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
        request: Optional[
            Union[analytics_admin.GetDataRetentionSettingsRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.DataRetentionSettings:
        r"""Returns the singleton data retention settings for
        this property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_get_data_retention_settings():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.GetDataRetentionSettingsRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_data_retention_settings(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.GetDataRetentionSettingsRequest, dict]]):
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
            google.analytics.admin_v1alpha.types.DataRetentionSettings:
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
        request: Optional[
            Union[analytics_admin.UpdateDataRetentionSettingsRequest, dict]
        ] = None,
        *,
        data_retention_settings: Optional[resources.DataRetentionSettings] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.DataRetentionSettings:
        r"""Updates the singleton data retention settings for
        this property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_update_data_retention_settings():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.UpdateDataRetentionSettingsRequest(
                )

                # Make the request
                response = await client.update_data_retention_settings(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.UpdateDataRetentionSettingsRequest, dict]]):
                The request object. Request message for
                UpdateDataRetentionSettings RPC.
            data_retention_settings (:class:`google.analytics.admin_v1alpha.types.DataRetentionSettings`):
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
            google.analytics.admin_v1alpha.types.DataRetentionSettings:
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
        request: Optional[Union[analytics_admin.CreateDataStreamRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        data_stream: Optional[resources.DataStream] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.DataStream:
        r"""Creates a DataStream.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_create_data_stream():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                data_stream = admin_v1alpha.DataStream()
                data_stream.type_ = "IOS_APP_DATA_STREAM"

                request = admin_v1alpha.CreateDataStreamRequest(
                    parent="parent_value",
                    data_stream=data_stream,
                )

                # Make the request
                response = await client.create_data_stream(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.CreateDataStreamRequest, dict]]):
                The request object. Request message for CreateDataStream
                RPC.
            parent (:class:`str`):
                Required. Example format:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            data_stream (:class:`google.analytics.admin_v1alpha.types.DataStream`):
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
            google.analytics.admin_v1alpha.types.DataStream:
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
        request: Optional[Union[analytics_admin.DeleteDataStreamRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a DataStream on a property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_delete_data_stream():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.DeleteDataStreamRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_data_stream(request=request)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.DeleteDataStreamRequest, dict]]):
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
        request: Optional[Union[analytics_admin.UpdateDataStreamRequest, dict]] = None,
        *,
        data_stream: Optional[resources.DataStream] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.DataStream:
        r"""Updates a DataStream on a property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_update_data_stream():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.UpdateDataStreamRequest(
                )

                # Make the request
                response = await client.update_data_stream(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.UpdateDataStreamRequest, dict]]):
                The request object. Request message for UpdateDataStream
                RPC.
            data_stream (:class:`google.analytics.admin_v1alpha.types.DataStream`):
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
            google.analytics.admin_v1alpha.types.DataStream:
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
        request: Optional[Union[analytics_admin.ListDataStreamsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDataStreamsAsyncPager:
        r"""Lists DataStreams on a property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_list_data_streams():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.ListDataStreamsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_data_streams(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.ListDataStreamsRequest, dict]]):
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListDataStreamsAsyncPager:
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
        request: Optional[Union[analytics_admin.GetDataStreamRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.DataStream:
        r"""Lookup for a single DataStream.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_get_data_stream():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.GetDataStreamRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_data_stream(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.GetDataStreamRequest, dict]]):
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
            google.analytics.admin_v1alpha.types.DataStream:
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

    async def get_audience(
        self,
        request: Optional[Union[analytics_admin.GetAudienceRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> audience.Audience:
        r"""Lookup for a single Audience.
        Audiences created before 2020 may not be supported.
        Default audiences will not show filter definitions.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_get_audience():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.GetAudienceRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_audience(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.GetAudienceRequest, dict]]):
                The request object. Request message for GetAudience RPC.
            name (:class:`str`):
                Required. The name of the Audience to
                get. Example format:
                properties/1234/audiences/5678

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.Audience:
                A resource message representing a GA4
                Audience.

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

        request = analytics_admin.GetAudienceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_audience,
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

    async def list_audiences(
        self,
        request: Optional[Union[analytics_admin.ListAudiencesRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAudiencesAsyncPager:
        r"""Lists Audiences on a property.
        Audiences created before 2020 may not be supported.
        Default audiences will not show filter definitions.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_list_audiences():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.ListAudiencesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_audiences(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.ListAudiencesRequest, dict]]):
                The request object. Request message for ListAudiences
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListAudiencesAsyncPager:
                Response message for ListAudiences
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

        request = analytics_admin.ListAudiencesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_audiences,
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
        response = pagers.ListAudiencesAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_audience(
        self,
        request: Optional[Union[analytics_admin.CreateAudienceRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        audience: Optional[gaa_audience.Audience] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gaa_audience.Audience:
        r"""Creates an Audience.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_create_audience():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                audience = admin_v1alpha.Audience()
                audience.display_name = "display_name_value"
                audience.description = "description_value"
                audience.membership_duration_days = 2561
                audience.filter_clauses.simple_filter.scope = "AUDIENCE_FILTER_SCOPE_ACROSS_ALL_SESSIONS"
                audience.filter_clauses.clause_type = "EXCLUDE"

                request = admin_v1alpha.CreateAudienceRequest(
                    parent="parent_value",
                    audience=audience,
                )

                # Make the request
                response = await client.create_audience(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.CreateAudienceRequest, dict]]):
                The request object. Request message for CreateAudience
                RPC.
            parent (:class:`str`):
                Required. Example format:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            audience (:class:`google.analytics.admin_v1alpha.types.Audience`):
                Required. The audience to create.
                This corresponds to the ``audience`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.Audience:
                A resource message representing a GA4
                Audience.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, audience])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.CreateAudienceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if audience is not None:
            request.audience = audience

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_audience,
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

    async def update_audience(
        self,
        request: Optional[Union[analytics_admin.UpdateAudienceRequest, dict]] = None,
        *,
        audience: Optional[gaa_audience.Audience] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gaa_audience.Audience:
        r"""Updates an Audience on a property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_update_audience():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                audience = admin_v1alpha.Audience()
                audience.display_name = "display_name_value"
                audience.description = "description_value"
                audience.membership_duration_days = 2561
                audience.filter_clauses.simple_filter.scope = "AUDIENCE_FILTER_SCOPE_ACROSS_ALL_SESSIONS"
                audience.filter_clauses.clause_type = "EXCLUDE"

                request = admin_v1alpha.UpdateAudienceRequest(
                    audience=audience,
                )

                # Make the request
                response = await client.update_audience(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.UpdateAudienceRequest, dict]]):
                The request object. Request message for UpdateAudience
                RPC.
            audience (:class:`google.analytics.admin_v1alpha.types.Audience`):
                Required. The audience to update. The audience's
                ``name`` field is used to identify the audience to be
                updated.

                This corresponds to the ``audience`` field
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
            google.analytics.admin_v1alpha.types.Audience:
                A resource message representing a GA4
                Audience.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([audience, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.UpdateAudienceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if audience is not None:
            request.audience = audience
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_audience,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("audience.name", request.audience.name),)
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

    async def archive_audience(
        self,
        request: Optional[Union[analytics_admin.ArchiveAudienceRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Archives an Audience on a property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_archive_audience():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.ArchiveAudienceRequest(
                    name="name_value",
                )

                # Make the request
                await client.archive_audience(request=request)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.ArchiveAudienceRequest, dict]]):
                The request object. Request message for ArchiveAudience
                RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        request = analytics_admin.ArchiveAudienceRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.archive_audience,
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

    async def get_search_ads360_link(
        self,
        request: Optional[
            Union[analytics_admin.GetSearchAds360LinkRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.SearchAds360Link:
        r"""Look up a single SearchAds360Link

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_get_search_ads360_link():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.GetSearchAds360LinkRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_search_ads360_link(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.GetSearchAds360LinkRequest, dict]]):
                The request object. Request message for
                GetSearchAds360Link RPC.
            name (:class:`str`):
                Required. The name of the
                SearchAds360Link to get. Example format:
                properties/1234/SearchAds360Link/5678

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.SearchAds360Link:
                A link between a GA4 property and a
                Search Ads 360 entity.

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

        request = analytics_admin.GetSearchAds360LinkRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_search_ads360_link,
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

    async def list_search_ads360_links(
        self,
        request: Optional[
            Union[analytics_admin.ListSearchAds360LinksRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListSearchAds360LinksAsyncPager:
        r"""Lists all SearchAds360Links on a property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_list_search_ads360_links():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.ListSearchAds360LinksRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_search_ads360_links(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.ListSearchAds360LinksRequest, dict]]):
                The request object. Request message for
                ListSearchAds360Links RPC.
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListSearchAds360LinksAsyncPager:
                Response message for
                ListSearchAds360Links RPC.
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

        request = analytics_admin.ListSearchAds360LinksRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_search_ads360_links,
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
        response = pagers.ListSearchAds360LinksAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_search_ads360_link(
        self,
        request: Optional[
            Union[analytics_admin.CreateSearchAds360LinkRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        search_ads_360_link: Optional[resources.SearchAds360Link] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.SearchAds360Link:
        r"""Creates a SearchAds360Link.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_create_search_ads360_link():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.CreateSearchAds360LinkRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.create_search_ads360_link(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.CreateSearchAds360LinkRequest, dict]]):
                The request object. Request message for
                CreateSearchAds360Link RPC.
            parent (:class:`str`):
                Required. Example format:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            search_ads_360_link (:class:`google.analytics.admin_v1alpha.types.SearchAds360Link`):
                Required. The SearchAds360Link to
                create.

                This corresponds to the ``search_ads_360_link`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.SearchAds360Link:
                A link between a GA4 property and a
                Search Ads 360 entity.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, search_ads_360_link])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.CreateSearchAds360LinkRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if search_ads_360_link is not None:
            request.search_ads_360_link = search_ads_360_link

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_search_ads360_link,
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

    async def delete_search_ads360_link(
        self,
        request: Optional[
            Union[analytics_admin.DeleteSearchAds360LinkRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a SearchAds360Link on a property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_delete_search_ads360_link():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.DeleteSearchAds360LinkRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_search_ads360_link(request=request)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.DeleteSearchAds360LinkRequest, dict]]):
                The request object. Request message for
                DeleteSearchAds360Link RPC.
            name (:class:`str`):
                Required. The name of the
                SearchAds360Link to delete. Example
                format:
                properties/1234/SearchAds360Links/5678

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

        request = analytics_admin.DeleteSearchAds360LinkRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_search_ads360_link,
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

    async def update_search_ads360_link(
        self,
        request: Optional[
            Union[analytics_admin.UpdateSearchAds360LinkRequest, dict]
        ] = None,
        *,
        search_ads_360_link: Optional[resources.SearchAds360Link] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.SearchAds360Link:
        r"""Updates a SearchAds360Link on a property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_update_search_ads360_link():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.UpdateSearchAds360LinkRequest(
                )

                # Make the request
                response = await client.update_search_ads360_link(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.UpdateSearchAds360LinkRequest, dict]]):
                The request object. Request message for
                UpdateSearchAds360Link RPC.
            search_ads_360_link (:class:`google.analytics.admin_v1alpha.types.SearchAds360Link`):
                The SearchAds360Link to update
                This corresponds to the ``search_ads_360_link`` field
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
            google.analytics.admin_v1alpha.types.SearchAds360Link:
                A link between a GA4 property and a
                Search Ads 360 entity.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([search_ads_360_link, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.UpdateSearchAds360LinkRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if search_ads_360_link is not None:
            request.search_ads_360_link = search_ads_360_link
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_search_ads360_link,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("search_ads_360_link.name", request.search_ads_360_link.name),)
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

    async def get_attribution_settings(
        self,
        request: Optional[
            Union[analytics_admin.GetAttributionSettingsRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.AttributionSettings:
        r"""Lookup for a AttributionSettings singleton.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_get_attribution_settings():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.GetAttributionSettingsRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_attribution_settings(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.GetAttributionSettingsRequest, dict]]):
                The request object. Request message for
                GetAttributionSettings RPC.
            name (:class:`str`):
                Required. The name of the attribution
                settings to retrieve. Format:
                properties/{property}/attributionSettings

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.AttributionSettings:
                The attribution settings used for a
                given property. This is a singleton
                resource.

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

        request = analytics_admin.GetAttributionSettingsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_attribution_settings,
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

    async def update_attribution_settings(
        self,
        request: Optional[
            Union[analytics_admin.UpdateAttributionSettingsRequest, dict]
        ] = None,
        *,
        attribution_settings: Optional[resources.AttributionSettings] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.AttributionSettings:
        r"""Updates attribution settings on a property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_update_attribution_settings():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                attribution_settings = admin_v1alpha.AttributionSettings()
                attribution_settings.acquisition_conversion_event_lookback_window = "ACQUISITION_CONVERSION_EVENT_LOOKBACK_WINDOW_30_DAYS"
                attribution_settings.other_conversion_event_lookback_window = "OTHER_CONVERSION_EVENT_LOOKBACK_WINDOW_90_DAYS"
                attribution_settings.reporting_attribution_model = "ADS_PREFERRED_LAST_CLICK"

                request = admin_v1alpha.UpdateAttributionSettingsRequest(
                    attribution_settings=attribution_settings,
                )

                # Make the request
                response = await client.update_attribution_settings(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.UpdateAttributionSettingsRequest, dict]]):
                The request object. Request message for
                UpdateAttributionSettings RPC
            attribution_settings (:class:`google.analytics.admin_v1alpha.types.AttributionSettings`):
                Required. The attribution settings to update. The
                ``name`` field is used to identify the settings to be
                updated.

                This corresponds to the ``attribution_settings`` field
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
            google.analytics.admin_v1alpha.types.AttributionSettings:
                The attribution settings used for a
                given property. This is a singleton
                resource.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([attribution_settings, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.UpdateAttributionSettingsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if attribution_settings is not None:
            request.attribution_settings = attribution_settings
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_attribution_settings,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("attribution_settings.name", request.attribution_settings.name),)
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

    async def run_access_report(
        self,
        request: Optional[Union[analytics_admin.RunAccessReportRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_admin.RunAccessReportResponse:
        r"""Returns a customized report of data access records. The report
        provides records of each time a user reads Google Analytics
        reporting data. Access records are retained for up to 2 years.

        Data Access Reports can be requested for a property. The
        property must be in Google Analytics 360. This method is only
        available to Administrators.

        These data access records include GA4 UI Reporting, GA4 UI
        Explorations, GA4 Data API, and other products like Firebase &
        Admob that can retrieve data from Google Analytics through a
        linkage. These records don't include property configuration
        changes like adding a stream or changing a property's time zone.
        For configuration change history, see
        `searchChangeHistoryEvents <https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/accounts/searchChangeHistoryEvents>`__.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_run_access_report():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.RunAccessReportRequest(
                )

                # Make the request
                response = await client.run_access_report(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.RunAccessReportRequest, dict]]):
                The request object. The request for a Data Access Record
                Report.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.RunAccessReportResponse:
                The customized Data Access Record
                Report response.

        """
        # Create or coerce a protobuf request object.
        request = analytics_admin.RunAccessReportRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.run_access_report,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("entity", request.entity),)),
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

    async def create_access_binding(
        self,
        request: Optional[
            Union[analytics_admin.CreateAccessBindingRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        access_binding: Optional[resources.AccessBinding] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.AccessBinding:
        r"""Creates an access binding on an account or property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_create_access_binding():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                access_binding = admin_v1alpha.AccessBinding()
                access_binding.user = "user_value"

                request = admin_v1alpha.CreateAccessBindingRequest(
                    parent="parent_value",
                    access_binding=access_binding,
                )

                # Make the request
                response = await client.create_access_binding(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.CreateAccessBindingRequest, dict]]):
                The request object. Request message for
                CreateAccessBinding RPC.
            parent (:class:`str`):
                Required. Formats:
                - accounts/{account}
                - properties/{property}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            access_binding (:class:`google.analytics.admin_v1alpha.types.AccessBinding`):
                Required. The access binding to
                create.

                This corresponds to the ``access_binding`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.AccessBinding:
                A binding of a user to a set of
                roles.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, access_binding])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.CreateAccessBindingRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if access_binding is not None:
            request.access_binding = access_binding

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_access_binding,
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

    async def get_access_binding(
        self,
        request: Optional[Union[analytics_admin.GetAccessBindingRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.AccessBinding:
        r"""Gets information about an access binding.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_get_access_binding():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.GetAccessBindingRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_access_binding(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.GetAccessBindingRequest, dict]]):
                The request object. Request message for GetAccessBinding
                RPC.
            name (:class:`str`):
                Required. The name of the access
                binding to retrieve. Formats:
                -
                accounts/{account}/accessBindings/{accessBinding}
                -
                properties/{property}/accessBindings/{accessBinding}

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.AccessBinding:
                A binding of a user to a set of
                roles.

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

        request = analytics_admin.GetAccessBindingRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_access_binding,
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

    async def update_access_binding(
        self,
        request: Optional[
            Union[analytics_admin.UpdateAccessBindingRequest, dict]
        ] = None,
        *,
        access_binding: Optional[resources.AccessBinding] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.AccessBinding:
        r"""Updates an access binding on an account or property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_update_access_binding():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                access_binding = admin_v1alpha.AccessBinding()
                access_binding.user = "user_value"

                request = admin_v1alpha.UpdateAccessBindingRequest(
                    access_binding=access_binding,
                )

                # Make the request
                response = await client.update_access_binding(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.UpdateAccessBindingRequest, dict]]):
                The request object. Request message for
                UpdateAccessBinding RPC.
            access_binding (:class:`google.analytics.admin_v1alpha.types.AccessBinding`):
                Required. The access binding to
                update.

                This corresponds to the ``access_binding`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.AccessBinding:
                A binding of a user to a set of
                roles.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([access_binding])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.UpdateAccessBindingRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if access_binding is not None:
            request.access_binding = access_binding

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_access_binding,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("access_binding.name", request.access_binding.name),)
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

    async def delete_access_binding(
        self,
        request: Optional[
            Union[analytics_admin.DeleteAccessBindingRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an access binding on an account or property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_delete_access_binding():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.DeleteAccessBindingRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_access_binding(request=request)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.DeleteAccessBindingRequest, dict]]):
                The request object. Request message for
                DeleteAccessBinding RPC.
            name (:class:`str`):
                Required. Formats:
                -
                accounts/{account}/accessBindings/{accessBinding}
                -
                properties/{property}/accessBindings/{accessBinding}

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

        request = analytics_admin.DeleteAccessBindingRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_access_binding,
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

    async def list_access_bindings(
        self,
        request: Optional[
            Union[analytics_admin.ListAccessBindingsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAccessBindingsAsyncPager:
        r"""Lists all access bindings on an account or property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_list_access_bindings():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.ListAccessBindingsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_access_bindings(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.ListAccessBindingsRequest, dict]]):
                The request object. Request message for
                ListAccessBindings RPC.
            parent (:class:`str`):
                Required. Formats:
                - accounts/{account}
                - properties/{property}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListAccessBindingsAsyncPager:
                Response message for
                ListAccessBindings RPC.
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

        request = analytics_admin.ListAccessBindingsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_access_bindings,
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
        response = pagers.ListAccessBindingsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def batch_create_access_bindings(
        self,
        request: Optional[
            Union[analytics_admin.BatchCreateAccessBindingsRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_admin.BatchCreateAccessBindingsResponse:
        r"""Creates information about multiple access bindings to
        an account or property.

        This method is transactional. If any AccessBinding
        cannot be created, none of the AccessBindings will be
        created.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_batch_create_access_bindings():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                requests = admin_v1alpha.CreateAccessBindingRequest()
                requests.parent = "parent_value"
                requests.access_binding.user = "user_value"

                request = admin_v1alpha.BatchCreateAccessBindingsRequest(
                    parent="parent_value",
                    requests=requests,
                )

                # Make the request
                response = await client.batch_create_access_bindings(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.BatchCreateAccessBindingsRequest, dict]]):
                The request object. Request message for
                BatchCreateAccessBindings RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.BatchCreateAccessBindingsResponse:
                Response message for
                BatchCreateAccessBindings RPC.

        """
        # Create or coerce a protobuf request object.
        request = analytics_admin.BatchCreateAccessBindingsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.batch_create_access_bindings,
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

    async def batch_get_access_bindings(
        self,
        request: Optional[
            Union[analytics_admin.BatchGetAccessBindingsRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_admin.BatchGetAccessBindingsResponse:
        r"""Gets information about multiple access bindings to an
        account or property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_batch_get_access_bindings():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.BatchGetAccessBindingsRequest(
                    parent="parent_value",
                    names=['names_value1', 'names_value2'],
                )

                # Make the request
                response = await client.batch_get_access_bindings(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.BatchGetAccessBindingsRequest, dict]]):
                The request object. Request message for
                BatchGetAccessBindings RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.BatchGetAccessBindingsResponse:
                Response message for
                BatchGetAccessBindings RPC.

        """
        # Create or coerce a protobuf request object.
        request = analytics_admin.BatchGetAccessBindingsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.batch_get_access_bindings,
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

    async def batch_update_access_bindings(
        self,
        request: Optional[
            Union[analytics_admin.BatchUpdateAccessBindingsRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_admin.BatchUpdateAccessBindingsResponse:
        r"""Updates information about multiple access bindings to
        an account or property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_batch_update_access_bindings():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                requests = admin_v1alpha.UpdateAccessBindingRequest()
                requests.access_binding.user = "user_value"

                request = admin_v1alpha.BatchUpdateAccessBindingsRequest(
                    parent="parent_value",
                    requests=requests,
                )

                # Make the request
                response = await client.batch_update_access_bindings(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.BatchUpdateAccessBindingsRequest, dict]]):
                The request object. Request message for
                BatchUpdateAccessBindings RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.BatchUpdateAccessBindingsResponse:
                Response message for
                BatchUpdateAccessBindings RPC.

        """
        # Create or coerce a protobuf request object.
        request = analytics_admin.BatchUpdateAccessBindingsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.batch_update_access_bindings,
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

    async def batch_delete_access_bindings(
        self,
        request: Optional[
            Union[analytics_admin.BatchDeleteAccessBindingsRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes information about multiple users' links to an
        account or property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_batch_delete_access_bindings():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                requests = admin_v1alpha.DeleteAccessBindingRequest()
                requests.name = "name_value"

                request = admin_v1alpha.BatchDeleteAccessBindingsRequest(
                    parent="parent_value",
                    requests=requests,
                )

                # Make the request
                await client.batch_delete_access_bindings(request=request)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.BatchDeleteAccessBindingsRequest, dict]]):
                The request object. Request message for
                BatchDeleteAccessBindings RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        request = analytics_admin.BatchDeleteAccessBindingsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.batch_delete_access_bindings,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def get_expanded_data_set(
        self,
        request: Optional[
            Union[analytics_admin.GetExpandedDataSetRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> expanded_data_set.ExpandedDataSet:
        r"""Lookup for a single ExpandedDataSet.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_get_expanded_data_set():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.GetExpandedDataSetRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_expanded_data_set(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.GetExpandedDataSetRequest, dict]]):
                The request object. Request message for
                GetExpandedDataSet RPC.
            name (:class:`str`):
                Required. The name of the
                ExpandedDataSet to get. Example format:
                properties/1234/expandedDataSets/5678

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.ExpandedDataSet:
                A resource message representing a GA4
                ExpandedDataSet.

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

        request = analytics_admin.GetExpandedDataSetRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_expanded_data_set,
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

    async def list_expanded_data_sets(
        self,
        request: Optional[
            Union[analytics_admin.ListExpandedDataSetsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListExpandedDataSetsAsyncPager:
        r"""Lists ExpandedDataSets on a property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_list_expanded_data_sets():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.ListExpandedDataSetsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_expanded_data_sets(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.ListExpandedDataSetsRequest, dict]]):
                The request object. Request message for
                ListExpandedDataSets RPC.
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListExpandedDataSetsAsyncPager:
                Response message for
                ListExpandedDataSets RPC.
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

        request = analytics_admin.ListExpandedDataSetsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_expanded_data_sets,
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
        response = pagers.ListExpandedDataSetsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_expanded_data_set(
        self,
        request: Optional[
            Union[analytics_admin.CreateExpandedDataSetRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        expanded_data_set: Optional[gaa_expanded_data_set.ExpandedDataSet] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gaa_expanded_data_set.ExpandedDataSet:
        r"""Creates a ExpandedDataSet.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_create_expanded_data_set():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                expanded_data_set = admin_v1alpha.ExpandedDataSet()
                expanded_data_set.display_name = "display_name_value"

                request = admin_v1alpha.CreateExpandedDataSetRequest(
                    parent="parent_value",
                    expanded_data_set=expanded_data_set,
                )

                # Make the request
                response = await client.create_expanded_data_set(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.CreateExpandedDataSetRequest, dict]]):
                The request object. Request message for
                CreateExpandedDataSet RPC.
            parent (:class:`str`):
                Required. Example format:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            expanded_data_set (:class:`google.analytics.admin_v1alpha.types.ExpandedDataSet`):
                Required. The ExpandedDataSet to
                create.

                This corresponds to the ``expanded_data_set`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.ExpandedDataSet:
                A resource message representing a GA4
                ExpandedDataSet.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, expanded_data_set])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.CreateExpandedDataSetRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if expanded_data_set is not None:
            request.expanded_data_set = expanded_data_set

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_expanded_data_set,
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

    async def update_expanded_data_set(
        self,
        request: Optional[
            Union[analytics_admin.UpdateExpandedDataSetRequest, dict]
        ] = None,
        *,
        expanded_data_set: Optional[gaa_expanded_data_set.ExpandedDataSet] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gaa_expanded_data_set.ExpandedDataSet:
        r"""Updates a ExpandedDataSet on a property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_update_expanded_data_set():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                expanded_data_set = admin_v1alpha.ExpandedDataSet()
                expanded_data_set.display_name = "display_name_value"

                request = admin_v1alpha.UpdateExpandedDataSetRequest(
                    expanded_data_set=expanded_data_set,
                )

                # Make the request
                response = await client.update_expanded_data_set(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.UpdateExpandedDataSetRequest, dict]]):
                The request object. Request message for
                UpdateExpandedDataSet RPC.
            expanded_data_set (:class:`google.analytics.admin_v1alpha.types.ExpandedDataSet`):
                Required. The ExpandedDataSet to update. The resource's
                ``name`` field is used to identify the ExpandedDataSet
                to be updated.

                This corresponds to the ``expanded_data_set`` field
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
            google.analytics.admin_v1alpha.types.ExpandedDataSet:
                A resource message representing a GA4
                ExpandedDataSet.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([expanded_data_set, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.UpdateExpandedDataSetRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if expanded_data_set is not None:
            request.expanded_data_set = expanded_data_set
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_expanded_data_set,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("expanded_data_set.name", request.expanded_data_set.name),)
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

    async def delete_expanded_data_set(
        self,
        request: Optional[
            Union[analytics_admin.DeleteExpandedDataSetRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a ExpandedDataSet on a property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_delete_expanded_data_set():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.DeleteExpandedDataSetRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_expanded_data_set(request=request)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.DeleteExpandedDataSetRequest, dict]]):
                The request object. Request message for
                DeleteExpandedDataSet RPC.
            name (:class:`str`):
                Required. Example format:
                properties/1234/expandedDataSets/5678

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

        request = analytics_admin.DeleteExpandedDataSetRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_expanded_data_set,
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

    async def get_channel_group(
        self,
        request: Optional[Union[analytics_admin.GetChannelGroupRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> channel_group.ChannelGroup:
        r"""Lookup for a single ChannelGroup.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_get_channel_group():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.GetChannelGroupRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_channel_group(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.GetChannelGroupRequest, dict]]):
                The request object. Request message for GetChannelGroup
                RPC.
            name (:class:`str`):
                Required. The ChannelGroup to get.
                Example format:
                properties/1234/channelGroups/5678

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.ChannelGroup:
                A resource message representing a
                Channel Group.

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

        request = analytics_admin.GetChannelGroupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_channel_group,
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

    async def list_channel_groups(
        self,
        request: Optional[Union[analytics_admin.ListChannelGroupsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListChannelGroupsAsyncPager:
        r"""Lists ChannelGroups on a property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_list_channel_groups():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.ListChannelGroupsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_channel_groups(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.ListChannelGroupsRequest, dict]]):
                The request object. Request message for ListChannelGroups
                RPC.
            parent (:class:`str`):
                Required. The property for which to
                list ChannelGroups. Example format:
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListChannelGroupsAsyncPager:
                Response message for
                ListChannelGroups RPC.
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

        request = analytics_admin.ListChannelGroupsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_channel_groups,
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
        response = pagers.ListChannelGroupsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_channel_group(
        self,
        request: Optional[
            Union[analytics_admin.CreateChannelGroupRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        channel_group: Optional[gaa_channel_group.ChannelGroup] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gaa_channel_group.ChannelGroup:
        r"""Creates a ChannelGroup.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_create_channel_group():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                channel_group = admin_v1alpha.ChannelGroup()
                channel_group.display_name = "display_name_value"
                channel_group.grouping_rule.display_name = "display_name_value"

                request = admin_v1alpha.CreateChannelGroupRequest(
                    parent="parent_value",
                    channel_group=channel_group,
                )

                # Make the request
                response = await client.create_channel_group(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.CreateChannelGroupRequest, dict]]):
                The request object. Request message for
                CreateChannelGroup RPC.
            parent (:class:`str`):
                Required. The property for which to
                create a ChannelGroup. Example format:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            channel_group (:class:`google.analytics.admin_v1alpha.types.ChannelGroup`):
                Required. The ChannelGroup to create.
                This corresponds to the ``channel_group`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.ChannelGroup:
                A resource message representing a
                Channel Group.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, channel_group])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.CreateChannelGroupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if channel_group is not None:
            request.channel_group = channel_group

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_channel_group,
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

    async def update_channel_group(
        self,
        request: Optional[
            Union[analytics_admin.UpdateChannelGroupRequest, dict]
        ] = None,
        *,
        channel_group: Optional[gaa_channel_group.ChannelGroup] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gaa_channel_group.ChannelGroup:
        r"""Updates a ChannelGroup.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_update_channel_group():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                channel_group = admin_v1alpha.ChannelGroup()
                channel_group.display_name = "display_name_value"
                channel_group.grouping_rule.display_name = "display_name_value"

                request = admin_v1alpha.UpdateChannelGroupRequest(
                    channel_group=channel_group,
                )

                # Make the request
                response = await client.update_channel_group(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.UpdateChannelGroupRequest, dict]]):
                The request object. Request message for
                UpdateChannelGroup RPC.
            channel_group (:class:`google.analytics.admin_v1alpha.types.ChannelGroup`):
                Required. The ChannelGroup to update. The resource's
                ``name`` field is used to identify the ChannelGroup to
                be updated.

                This corresponds to the ``channel_group`` field
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
            google.analytics.admin_v1alpha.types.ChannelGroup:
                A resource message representing a
                Channel Group.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([channel_group, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.UpdateChannelGroupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if channel_group is not None:
            request.channel_group = channel_group
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_channel_group,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("channel_group.name", request.channel_group.name),)
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

    async def delete_channel_group(
        self,
        request: Optional[
            Union[analytics_admin.DeleteChannelGroupRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a ChannelGroup on a property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_delete_channel_group():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.DeleteChannelGroupRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_channel_group(request=request)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.DeleteChannelGroupRequest, dict]]):
                The request object. Request message for
                DeleteChannelGroup RPC.
            name (:class:`str`):
                Required. The ChannelGroup to delete.
                Example format:
                properties/1234/channelGroups/5678

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

        request = analytics_admin.DeleteChannelGroupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_channel_group,
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

    async def set_automated_ga4_configuration_opt_out(
        self,
        request: Optional[
            Union[analytics_admin.SetAutomatedGa4ConfigurationOptOutRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_admin.SetAutomatedGa4ConfigurationOptOutResponse:
        r"""Sets the opt out status for the automated GA4 setup
        process for a UA property.
        Note: this has no effect on GA4 property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_set_automated_ga4_configuration_opt_out():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.SetAutomatedGa4ConfigurationOptOutRequest(
                    property="property_value",
                )

                # Make the request
                response = await client.set_automated_ga4_configuration_opt_out(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.SetAutomatedGa4ConfigurationOptOutRequest, dict]]):
                The request object. Request for setting the opt out
                status for the automated GA4 setup
                process.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.SetAutomatedGa4ConfigurationOptOutResponse:
                Response message for setting the opt
                out status for the automated GA4 setup
                process.

        """
        # Create or coerce a protobuf request object.
        request = analytics_admin.SetAutomatedGa4ConfigurationOptOutRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.set_automated_ga4_configuration_opt_out,
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

        # Done; return the response.
        return response

    async def fetch_automated_ga4_configuration_opt_out(
        self,
        request: Optional[
            Union[analytics_admin.FetchAutomatedGa4ConfigurationOptOutRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_admin.FetchAutomatedGa4ConfigurationOptOutResponse:
        r"""Fetches the opt out status for the automated GA4
        setup process for a UA property.
        Note: this has no effect on GA4 property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_fetch_automated_ga4_configuration_opt_out():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.FetchAutomatedGa4ConfigurationOptOutRequest(
                    property="property_value",
                )

                # Make the request
                response = await client.fetch_automated_ga4_configuration_opt_out(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.FetchAutomatedGa4ConfigurationOptOutRequest, dict]]):
                The request object. Request for fetching the opt out
                status for the automated GA4 setup
                process.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.FetchAutomatedGa4ConfigurationOptOutResponse:
                Response message for fetching the opt
                out status for the automated GA4 setup
                process.

        """
        # Create or coerce a protobuf request object.
        request = analytics_admin.FetchAutomatedGa4ConfigurationOptOutRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.fetch_automated_ga4_configuration_opt_out,
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

        # Done; return the response.
        return response

    async def get_big_query_link(
        self,
        request: Optional[Union[analytics_admin.GetBigQueryLinkRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.BigQueryLink:
        r"""Lookup for a single BigQuery Link.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_get_big_query_link():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.GetBigQueryLinkRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_big_query_link(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.GetBigQueryLinkRequest, dict]]):
                The request object. Request message for GetBigQueryLink
                RPC.
            name (:class:`str`):
                Required. The name of the BigQuery link to lookup.
                Format:
                properties/{property_id}/bigQueryLinks/{bigquery_link_id}
                Example: properties/123/bigQueryLinks/456

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.BigQueryLink:
                A link between a GA4 Property and
                BigQuery project.

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

        request = analytics_admin.GetBigQueryLinkRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_big_query_link,
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

    async def list_big_query_links(
        self,
        request: Optional[Union[analytics_admin.ListBigQueryLinksRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListBigQueryLinksAsyncPager:
        r"""Lists BigQuery Links on a property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_list_big_query_links():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.ListBigQueryLinksRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_big_query_links(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.ListBigQueryLinksRequest, dict]]):
                The request object. Request message for ListBigQueryLinks
                RPC.
            parent (:class:`str`):
                Required. The name of the property to list BigQuery
                links under. Format: properties/{property_id} Example:
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListBigQueryLinksAsyncPager:
                Response message for
                ListBigQueryLinks RPC
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

        request = analytics_admin.ListBigQueryLinksRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_big_query_links,
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
        response = pagers.ListBigQueryLinksAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_enhanced_measurement_settings(
        self,
        request: Optional[
            Union[analytics_admin.GetEnhancedMeasurementSettingsRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.EnhancedMeasurementSettings:
        r"""Returns the enhanced measurement settings for this
        data stream. Note that the stream must enable enhanced
        measurement for these settings to take effect.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_get_enhanced_measurement_settings():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.GetEnhancedMeasurementSettingsRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_enhanced_measurement_settings(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.GetEnhancedMeasurementSettingsRequest, dict]]):
                The request object. Request message for
                GetEnhancedMeasurementSettings RPC.
            name (:class:`str`):
                Required. The name of the settings to lookup. Format:
                properties/{property}/dataStreams/{data_stream}/enhancedMeasurementSettings
                Example:
                "properties/1000/dataStreams/2000/enhancedMeasurementSettings"

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.EnhancedMeasurementSettings:
                Singleton resource under a
                WebDataStream, configuring measurement
                of additional site interactions and
                content.

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

        request = analytics_admin.GetEnhancedMeasurementSettingsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_enhanced_measurement_settings,
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

    async def update_enhanced_measurement_settings(
        self,
        request: Optional[
            Union[analytics_admin.UpdateEnhancedMeasurementSettingsRequest, dict]
        ] = None,
        *,
        enhanced_measurement_settings: Optional[
            resources.EnhancedMeasurementSettings
        ] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.EnhancedMeasurementSettings:
        r"""Updates the enhanced measurement settings for this
        data stream. Note that the stream must enable enhanced
        measurement for these settings to take effect.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_update_enhanced_measurement_settings():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                enhanced_measurement_settings = admin_v1alpha.EnhancedMeasurementSettings()
                enhanced_measurement_settings.search_query_parameter = "search_query_parameter_value"

                request = admin_v1alpha.UpdateEnhancedMeasurementSettingsRequest(
                    enhanced_measurement_settings=enhanced_measurement_settings,
                )

                # Make the request
                response = await client.update_enhanced_measurement_settings(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.UpdateEnhancedMeasurementSettingsRequest, dict]]):
                The request object. Request message for
                UpdateEnhancedMeasurementSettings RPC.
            enhanced_measurement_settings (:class:`google.analytics.admin_v1alpha.types.EnhancedMeasurementSettings`):
                Required. The settings to update. The ``name`` field is
                used to identify the settings to be updated.

                This corresponds to the ``enhanced_measurement_settings`` field
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
            google.analytics.admin_v1alpha.types.EnhancedMeasurementSettings:
                Singleton resource under a
                WebDataStream, configuring measurement
                of additional site interactions and
                content.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([enhanced_measurement_settings, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.UpdateEnhancedMeasurementSettingsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if enhanced_measurement_settings is not None:
            request.enhanced_measurement_settings = enhanced_measurement_settings
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_enhanced_measurement_settings,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    (
                        "enhanced_measurement_settings.name",
                        request.enhanced_measurement_settings.name,
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

    async def create_connected_site_tag(
        self,
        request: Optional[
            Union[analytics_admin.CreateConnectedSiteTagRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_admin.CreateConnectedSiteTagResponse:
        r"""Creates a connected site tag for a Universal
        Analytics property. You can create a maximum of 20
        connected site tags per property. Note: This API cannot
        be used on GA4 properties.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_create_connected_site_tag():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                connected_site_tag = admin_v1alpha.ConnectedSiteTag()
                connected_site_tag.display_name = "display_name_value"
                connected_site_tag.tag_id = "tag_id_value"

                request = admin_v1alpha.CreateConnectedSiteTagRequest(
                    connected_site_tag=connected_site_tag,
                )

                # Make the request
                response = await client.create_connected_site_tag(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.CreateConnectedSiteTagRequest, dict]]):
                The request object. Request message for
                CreateConnectedSiteTag RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.CreateConnectedSiteTagResponse:
                Response message for
                CreateConnectedSiteTag RPC.

        """
        # Create or coerce a protobuf request object.
        request = analytics_admin.CreateConnectedSiteTagRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_connected_site_tag,
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

        # Done; return the response.
        return response

    async def delete_connected_site_tag(
        self,
        request: Optional[
            Union[analytics_admin.DeleteConnectedSiteTagRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a connected site tag for a Universal
        Analytics property. Note: this has no effect on GA4
        properties.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_delete_connected_site_tag():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.DeleteConnectedSiteTagRequest(
                )

                # Make the request
                await client.delete_connected_site_tag(request=request)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.DeleteConnectedSiteTagRequest, dict]]):
                The request object. Request message for
                DeleteConnectedSiteTag RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        request = analytics_admin.DeleteConnectedSiteTagRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_connected_site_tag,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def list_connected_site_tags(
        self,
        request: Optional[
            Union[analytics_admin.ListConnectedSiteTagsRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_admin.ListConnectedSiteTagsResponse:
        r"""Lists the connected site tags for a Universal
        Analytics property. A maximum of 20 connected site tags
        will be returned. Note: this has no effect on GA4
        property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_list_connected_site_tags():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.ListConnectedSiteTagsRequest(
                )

                # Make the request
                response = await client.list_connected_site_tags(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.ListConnectedSiteTagsRequest, dict]]):
                The request object. Request message for
                ListConnectedSiteTags RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.ListConnectedSiteTagsResponse:
                Response message for
                ListConnectedSiteTags RPC.

        """
        # Create or coerce a protobuf request object.
        request = analytics_admin.ListConnectedSiteTagsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_connected_site_tags,
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

        # Done; return the response.
        return response

    async def fetch_connected_ga4_property(
        self,
        request: Optional[
            Union[analytics_admin.FetchConnectedGa4PropertyRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_admin.FetchConnectedGa4PropertyResponse:
        r"""Given a specified UA property, looks up the GA4
        property connected to it. Note: this cannot be used with
        GA4 properties.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_fetch_connected_ga4_property():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.FetchConnectedGa4PropertyRequest(
                    property="property_value",
                )

                # Make the request
                response = await client.fetch_connected_ga4_property(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.FetchConnectedGa4PropertyRequest, dict]]):
                The request object. Request for looking up GA4 property
                connected to a UA property.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.FetchConnectedGa4PropertyResponse:
                Response for looking up GA4 property
                connected to a UA property.

        """
        # Create or coerce a protobuf request object.
        request = analytics_admin.FetchConnectedGa4PropertyRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.fetch_connected_ga4_property,
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

        # Done; return the response.
        return response

    async def get_ad_sense_link(
        self,
        request: Optional[Union[analytics_admin.GetAdSenseLinkRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.AdSenseLink:
        r"""Looks up a single AdSenseLink.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_get_ad_sense_link():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.GetAdSenseLinkRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_ad_sense_link(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.GetAdSenseLinkRequest, dict]]):
                The request object. Request message to be passed to
                GetAdSenseLink method.
            name (:class:`str`):
                Required. Unique identifier for the
                AdSense Link requested. Format:
                properties/{propertyId}/adSenseLinks/{linkId}
                Example:
                properties/1234/adSenseLinks/5678

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.AdSenseLink:
                A link between a GA4 Property and an
                AdSense for Content ad client.

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

        request = analytics_admin.GetAdSenseLinkRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_ad_sense_link,
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

    async def create_ad_sense_link(
        self,
        request: Optional[Union[analytics_admin.CreateAdSenseLinkRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        adsense_link: Optional[resources.AdSenseLink] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.AdSenseLink:
        r"""Creates an AdSenseLink.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_create_ad_sense_link():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.CreateAdSenseLinkRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.create_ad_sense_link(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.CreateAdSenseLinkRequest, dict]]):
                The request object. Request message to be passed to
                CreateAdSenseLink method.
            parent (:class:`str`):
                Required. The property for which to
                create an AdSense Link. Format:
                properties/{propertyId} Example:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            adsense_link (:class:`google.analytics.admin_v1alpha.types.AdSenseLink`):
                Required. The AdSense Link to create
                This corresponds to the ``adsense_link`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.AdSenseLink:
                A link between a GA4 Property and an
                AdSense for Content ad client.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, adsense_link])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.CreateAdSenseLinkRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if adsense_link is not None:
            request.adsense_link = adsense_link

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_ad_sense_link,
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

    async def delete_ad_sense_link(
        self,
        request: Optional[Union[analytics_admin.DeleteAdSenseLinkRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an AdSenseLink.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_delete_ad_sense_link():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.DeleteAdSenseLinkRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_ad_sense_link(request=request)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.DeleteAdSenseLinkRequest, dict]]):
                The request object. Request message to be passed to
                DeleteAdSenseLink method.
            name (:class:`str`):
                Required. Unique identifier for the
                AdSense Link to be deleted. Format:
                properties/{propertyId}/adSenseLinks/{linkId}
                Example:
                properties/1234/adSenseLinks/5678

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

        request = analytics_admin.DeleteAdSenseLinkRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_ad_sense_link,
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

    async def list_ad_sense_links(
        self,
        request: Optional[Union[analytics_admin.ListAdSenseLinksRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAdSenseLinksAsyncPager:
        r"""Lists AdSenseLinks on a property.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_list_ad_sense_links():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.ListAdSenseLinksRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_ad_sense_links(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.ListAdSenseLinksRequest, dict]]):
                The request object. Request message to be passed to
                ListAdSenseLinks method.
            parent (:class:`str`):
                Required. Resource name of the parent
                property. Format:
                properties/{propertyId}
                Example: properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListAdSenseLinksAsyncPager:
                Response message for ListAdSenseLinks
                method.
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

        request = analytics_admin.ListAdSenseLinksRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_ad_sense_links,
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
        response = pagers.ListAdSenseLinksAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_event_create_rule(
        self,
        request: Optional[
            Union[analytics_admin.GetEventCreateRuleRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> event_create_and_edit.EventCreateRule:
        r"""Lookup for a single EventCreateRule.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_get_event_create_rule():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.GetEventCreateRuleRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_event_create_rule(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.GetEventCreateRuleRequest, dict]]):
                The request object. Request message for
                GetEventCreateRule RPC.
            name (:class:`str`):
                Required. The name of the
                EventCreateRule to get. Example format:
                properties/123/dataStreams/456/eventCreateRules/789

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.EventCreateRule:
                An Event Create Rule defines
                conditions that will trigger the
                creation of an entirely new event based
                upon matched criteria of a source event.
                Additional mutations of the parameters
                from the source event can be defined.
                Unlike Event Edit rules, Event Creation
                Rules have no defined order.  They will
                all be run independently.

                Event Edit and Event Create rules can't
                be used to modify an event created from
                an Event Create rule.

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

        request = analytics_admin.GetEventCreateRuleRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_event_create_rule,
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

    async def list_event_create_rules(
        self,
        request: Optional[
            Union[analytics_admin.ListEventCreateRulesRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListEventCreateRulesAsyncPager:
        r"""Lists EventCreateRules on a web data stream.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_list_event_create_rules():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.ListEventCreateRulesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_event_create_rules(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.ListEventCreateRulesRequest, dict]]):
                The request object. Request message for
                ListEventCreateRules RPC.
            parent (:class:`str`):
                Required. Example format:
                properties/123/dataStreams/456

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListEventCreateRulesAsyncPager:
                Response message for
                ListEventCreateRules RPC.
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

        request = analytics_admin.ListEventCreateRulesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_event_create_rules,
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
        response = pagers.ListEventCreateRulesAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_event_create_rule(
        self,
        request: Optional[
            Union[analytics_admin.CreateEventCreateRuleRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        event_create_rule: Optional[event_create_and_edit.EventCreateRule] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> event_create_and_edit.EventCreateRule:
        r"""Creates an EventCreateRule.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_create_event_create_rule():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                event_create_rule = admin_v1alpha.EventCreateRule()
                event_create_rule.destination_event = "destination_event_value"
                event_create_rule.event_conditions.field = "field_value"
                event_create_rule.event_conditions.comparison_type = "REGULAR_EXPRESSION_CASE_INSENSITIVE"
                event_create_rule.event_conditions.value = "value_value"

                request = admin_v1alpha.CreateEventCreateRuleRequest(
                    parent="parent_value",
                    event_create_rule=event_create_rule,
                )

                # Make the request
                response = await client.create_event_create_rule(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.CreateEventCreateRuleRequest, dict]]):
                The request object. Request message for
                CreateEventCreateRule RPC.
            parent (:class:`str`):
                Required. Example format:
                properties/123/dataStreams/456

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            event_create_rule (:class:`google.analytics.admin_v1alpha.types.EventCreateRule`):
                Required. The EventCreateRule to
                create.

                This corresponds to the ``event_create_rule`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.EventCreateRule:
                An Event Create Rule defines
                conditions that will trigger the
                creation of an entirely new event based
                upon matched criteria of a source event.
                Additional mutations of the parameters
                from the source event can be defined.
                Unlike Event Edit rules, Event Creation
                Rules have no defined order.  They will
                all be run independently.

                Event Edit and Event Create rules can't
                be used to modify an event created from
                an Event Create rule.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, event_create_rule])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.CreateEventCreateRuleRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if event_create_rule is not None:
            request.event_create_rule = event_create_rule

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_event_create_rule,
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

    async def update_event_create_rule(
        self,
        request: Optional[
            Union[analytics_admin.UpdateEventCreateRuleRequest, dict]
        ] = None,
        *,
        event_create_rule: Optional[event_create_and_edit.EventCreateRule] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> event_create_and_edit.EventCreateRule:
        r"""Updates an EventCreateRule.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_update_event_create_rule():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                event_create_rule = admin_v1alpha.EventCreateRule()
                event_create_rule.destination_event = "destination_event_value"
                event_create_rule.event_conditions.field = "field_value"
                event_create_rule.event_conditions.comparison_type = "REGULAR_EXPRESSION_CASE_INSENSITIVE"
                event_create_rule.event_conditions.value = "value_value"

                request = admin_v1alpha.UpdateEventCreateRuleRequest(
                    event_create_rule=event_create_rule,
                )

                # Make the request
                response = await client.update_event_create_rule(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.UpdateEventCreateRuleRequest, dict]]):
                The request object. Request message for
                UpdateEventCreateRule RPC.
            event_create_rule (:class:`google.analytics.admin_v1alpha.types.EventCreateRule`):
                Required. The EventCreateRule to update. The resource's
                ``name`` field is used to identify the EventCreateRule
                to be updated.

                This corresponds to the ``event_create_rule`` field
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
            google.analytics.admin_v1alpha.types.EventCreateRule:
                An Event Create Rule defines
                conditions that will trigger the
                creation of an entirely new event based
                upon matched criteria of a source event.
                Additional mutations of the parameters
                from the source event can be defined.
                Unlike Event Edit rules, Event Creation
                Rules have no defined order.  They will
                all be run independently.

                Event Edit and Event Create rules can't
                be used to modify an event created from
                an Event Create rule.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([event_create_rule, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_admin.UpdateEventCreateRuleRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if event_create_rule is not None:
            request.event_create_rule = event_create_rule
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_event_create_rule,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("event_create_rule.name", request.event_create_rule.name),)
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

    async def delete_event_create_rule(
        self,
        request: Optional[
            Union[analytics_admin.DeleteEventCreateRuleRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an EventCreateRule.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import admin_v1alpha

            async def sample_delete_event_create_rule():
                # Create a client
                client = admin_v1alpha.AnalyticsAdminServiceAsyncClient()

                # Initialize request argument(s)
                request = admin_v1alpha.DeleteEventCreateRuleRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_event_create_rule(request=request)

        Args:
            request (Optional[Union[google.analytics.admin_v1alpha.types.DeleteEventCreateRuleRequest, dict]]):
                The request object. Request message for
                DeleteEventCreateRule RPC.
            name (:class:`str`):
                Required. Example format:
                properties/123/dataStreams/456/eventCreateRules/789

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

        request = analytics_admin.DeleteEventCreateRuleRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_event_create_rule,
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

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("AnalyticsAdminServiceAsyncClient",)
