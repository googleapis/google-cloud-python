# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from google.api_core import retry_async as retries
from google.api_core.client_options import ClientOptions
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.analytics.data_v1alpha import gapic_version as package_version

try:
    OptionalRetry = Union[retries.AsyncRetry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.AsyncRetry, object]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.analytics.data_v1alpha.services.alpha_analytics_data import pagers
from google.analytics.data_v1alpha.types import analytics_data_api, data

from .client import AlphaAnalyticsDataClient
from .transports.base import DEFAULT_CLIENT_INFO, AlphaAnalyticsDataTransport
from .transports.grpc_asyncio import AlphaAnalyticsDataGrpcAsyncIOTransport


class AlphaAnalyticsDataAsyncClient:
    """Google Analytics reporting data service."""

    _client: AlphaAnalyticsDataClient

    DEFAULT_ENDPOINT = AlphaAnalyticsDataClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = AlphaAnalyticsDataClient.DEFAULT_MTLS_ENDPOINT

    audience_list_path = staticmethod(AlphaAnalyticsDataClient.audience_list_path)
    parse_audience_list_path = staticmethod(
        AlphaAnalyticsDataClient.parse_audience_list_path
    )
    recurring_audience_list_path = staticmethod(
        AlphaAnalyticsDataClient.recurring_audience_list_path
    )
    parse_recurring_audience_list_path = staticmethod(
        AlphaAnalyticsDataClient.parse_recurring_audience_list_path
    )
    common_billing_account_path = staticmethod(
        AlphaAnalyticsDataClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        AlphaAnalyticsDataClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(AlphaAnalyticsDataClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        AlphaAnalyticsDataClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        AlphaAnalyticsDataClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        AlphaAnalyticsDataClient.parse_common_organization_path
    )
    common_project_path = staticmethod(AlphaAnalyticsDataClient.common_project_path)
    parse_common_project_path = staticmethod(
        AlphaAnalyticsDataClient.parse_common_project_path
    )
    common_location_path = staticmethod(AlphaAnalyticsDataClient.common_location_path)
    parse_common_location_path = staticmethod(
        AlphaAnalyticsDataClient.parse_common_location_path
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
            AlphaAnalyticsDataAsyncClient: The constructed client.
        """
        return AlphaAnalyticsDataClient.from_service_account_info.__func__(AlphaAnalyticsDataAsyncClient, info, *args, **kwargs)  # type: ignore

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
            AlphaAnalyticsDataAsyncClient: The constructed client.
        """
        return AlphaAnalyticsDataClient.from_service_account_file.__func__(AlphaAnalyticsDataAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return AlphaAnalyticsDataClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> AlphaAnalyticsDataTransport:
        """Returns the transport used by the client instance.

        Returns:
            AlphaAnalyticsDataTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(AlphaAnalyticsDataClient).get_transport_class,
        type(AlphaAnalyticsDataClient),
    )

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, AlphaAnalyticsDataTransport] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the alpha analytics data client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.AlphaAnalyticsDataTransport]): The
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
        self._client = AlphaAnalyticsDataClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def run_funnel_report(
        self,
        request: Optional[
            Union[analytics_data_api.RunFunnelReportRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_data_api.RunFunnelReportResponse:
        r"""Returns a customized funnel report of your Google Analytics
        event data. The data returned from the API is as a table with
        columns for the requested dimensions and metrics.

        Funnel exploration lets you visualize the steps your users take
        to complete a task and quickly see how well they are succeeding
        or failing at each step. For example, how do prospects become
        shoppers and then become buyers? How do one time buyers become
        repeat buyers? With this information, you can improve
        inefficient or abandoned customer journeys. To learn more, see
        `GA4 Funnel
        Explorations <https://support.google.com/analytics/answer/9327974>`__.

        This method is introduced at alpha stability with the intention
        of gathering feedback on syntax and capabilities before entering
        beta. To give your feedback on this API, complete the `Google
        Analytics Data API Funnel Reporting
        Feedback <https://docs.google.com/forms/d/e/1FAIpQLSdwOlQDJAUoBiIgUZZ3S_Lwi8gr7Bb0k1jhvc-DEg7Rol3UjA/viewform>`__.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import data_v1alpha

            async def sample_run_funnel_report():
                # Create a client
                client = data_v1alpha.AlphaAnalyticsDataAsyncClient()

                # Initialize request argument(s)
                request = data_v1alpha.RunFunnelReportRequest(
                )

                # Make the request
                response = await client.run_funnel_report(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.data_v1alpha.types.RunFunnelReportRequest, dict]]):
                The request object. The request for a funnel report.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.data_v1alpha.types.RunFunnelReportResponse:
                The funnel report response contains
                two sub reports. The two sub reports are
                different combinations of dimensions and
                metrics.

        """
        # Create or coerce a protobuf request object.
        request = analytics_data_api.RunFunnelReportRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.run_funnel_report,
            default_timeout=60.0,
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

    async def create_audience_list(
        self,
        request: Optional[
            Union[analytics_data_api.CreateAudienceListRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        audience_list: Optional[analytics_data_api.AudienceList] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates an audience list for later retrieval. This method
        quickly returns the audience list's resource name and initiates
        a long running asynchronous request to form an audience list. To
        list the users in an audience list, first create the audience
        list through this method and then send the audience resource
        name to the ``QueryAudienceList`` method.

        See `Creating an Audience
        List <https://developers.google.com/analytics/devguides/reporting/data/v1/audience-list-basics>`__
        for an introduction to Audience Lists with examples.

        An audience list is a snapshot of the users currently in the
        audience at the time of audience list creation. Creating
        audience lists for one audience on different days will return
        different results as users enter and exit the audience.

        Audiences in Google Analytics 4 allow you to segment your users
        in the ways that are important to your business. To learn more,
        see https://support.google.com/analytics/answer/9267572.
        Audience lists contain the users in each audience.

        This method is available at beta stability at
        `audienceExports.create <https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties.audienceExports/create>`__.
        To give your feedback on this API, complete the `Google
        Analytics Audience Export API
        Feedback <https://forms.gle/EeA5u5LW6PEggtCEA>`__ form.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import data_v1alpha

            async def sample_create_audience_list():
                # Create a client
                client = data_v1alpha.AlphaAnalyticsDataAsyncClient()

                # Initialize request argument(s)
                audience_list = data_v1alpha.AudienceList()
                audience_list.audience = "audience_value"

                request = data_v1alpha.CreateAudienceListRequest(
                    parent="parent_value",
                    audience_list=audience_list,
                )

                # Make the request
                operation = client.create_audience_list(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.data_v1alpha.types.CreateAudienceListRequest, dict]]):
                The request object. A request to create a new audience
                list.
            parent (:class:`str`):
                Required. The parent resource where this audience list
                will be created. Format: ``properties/{property}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            audience_list (:class:`google.analytics.data_v1alpha.types.AudienceList`):
                Required. The audience list to
                create.

                This corresponds to the ``audience_list`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.analytics.data_v1alpha.types.AudienceList` An audience list is a list of users in an audience at the time of the list's
                   creation. One audience may have multiple audience
                   lists created for different days.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, audience_list])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_data_api.CreateAudienceListRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if audience_list is not None:
            request.audience_list = audience_list

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_audience_list,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            analytics_data_api.AudienceList,
            metadata_type=analytics_data_api.AudienceListMetadata,
        )

        # Done; return the response.
        return response

    async def query_audience_list(
        self,
        request: Optional[
            Union[analytics_data_api.QueryAudienceListRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_data_api.QueryAudienceListResponse:
        r"""Retrieves an audience list of users. After creating an audience,
        the users are not immediately available for listing. First, a
        request to ``CreateAudienceList`` is necessary to create an
        audience list of users, and then second, this method is used to
        retrieve the users in the audience list.

        See `Creating an Audience
        List <https://developers.google.com/analytics/devguides/reporting/data/v1/audience-list-basics>`__
        for an introduction to Audience Lists with examples.

        Audiences in Google Analytics 4 allow you to segment your users
        in the ways that are important to your business. To learn more,
        see https://support.google.com/analytics/answer/9267572.

        This method is available at beta stability at
        `audienceExports.query <https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties.audienceExports/query>`__.
        To give your feedback on this API, complete the `Google
        Analytics Audience Export API
        Feedback <https://forms.gle/EeA5u5LW6PEggtCEA>`__ form.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import data_v1alpha

            async def sample_query_audience_list():
                # Create a client
                client = data_v1alpha.AlphaAnalyticsDataAsyncClient()

                # Initialize request argument(s)
                request = data_v1alpha.QueryAudienceListRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.query_audience_list(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.data_v1alpha.types.QueryAudienceListRequest, dict]]):
                The request object. A request to list users in an
                audience list.
            name (:class:`str`):
                Required. The name of the audience list to retrieve
                users from. Format:
                ``properties/{property}/audienceLists/{audience_list}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.data_v1alpha.types.QueryAudienceListResponse:
                A list of users in an audience list.
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

        request = analytics_data_api.QueryAudienceListRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.query_audience_list,
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

    async def sheet_export_audience_list(
        self,
        request: Optional[
            Union[analytics_data_api.SheetExportAudienceListRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_data_api.SheetExportAudienceListResponse:
        r"""Exports an audience list of users to a Google Sheet. After
        creating an audience, the users are not immediately available
        for listing. First, a request to ``CreateAudienceList`` is
        necessary to create an audience list of users, and then second,
        this method is used to export those users in the audience list
        to a Google Sheet.

        See `Creating an Audience
        List <https://developers.google.com/analytics/devguides/reporting/data/v1/audience-list-basics>`__
        for an introduction to Audience Lists with examples.

        Audiences in Google Analytics 4 allow you to segment your users
        in the ways that are important to your business. To learn more,
        see https://support.google.com/analytics/answer/9267572.

        This method is introduced at alpha stability with the intention
        of gathering feedback on syntax and capabilities before entering
        beta. To give your feedback on this API, complete the `Google
        Analytics Audience Export API
        Feedback <https://forms.gle/EeA5u5LW6PEggtCEA>`__ form.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import data_v1alpha

            async def sample_sheet_export_audience_list():
                # Create a client
                client = data_v1alpha.AlphaAnalyticsDataAsyncClient()

                # Initialize request argument(s)
                request = data_v1alpha.SheetExportAudienceListRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.sheet_export_audience_list(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.data_v1alpha.types.SheetExportAudienceListRequest, dict]]):
                The request object. A request to export users in an
                audience list to a Google Sheet.
            name (:class:`str`):
                Required. The name of the audience list to retrieve
                users from. Format:
                ``properties/{property}/audienceLists/{audience_list}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.data_v1alpha.types.SheetExportAudienceListResponse:
                The created Google Sheet with the
                list of users in an audience list.

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

        request = analytics_data_api.SheetExportAudienceListRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.sheet_export_audience_list,
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

    async def get_audience_list(
        self,
        request: Optional[
            Union[analytics_data_api.GetAudienceListRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_data_api.AudienceList:
        r"""Gets configuration metadata about a specific audience list. This
        method can be used to understand an audience list after it has
        been created.

        See `Creating an Audience
        List <https://developers.google.com/analytics/devguides/reporting/data/v1/audience-list-basics>`__
        for an introduction to Audience Lists with examples.

        This method is available at beta stability at
        `audienceExports.get <https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties.audienceExports/get>`__.
        To give your feedback on this API, complete the `Google
        Analytics Audience Export API
        Feedback <https://forms.gle/EeA5u5LW6PEggtCEA>`__ form.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import data_v1alpha

            async def sample_get_audience_list():
                # Create a client
                client = data_v1alpha.AlphaAnalyticsDataAsyncClient()

                # Initialize request argument(s)
                request = data_v1alpha.GetAudienceListRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_audience_list(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.data_v1alpha.types.GetAudienceListRequest, dict]]):
                The request object. A request to retrieve configuration
                metadata about a specific audience list.
            name (:class:`str`):
                Required. The audience list resource name. Format:
                ``properties/{property}/audienceLists/{audience_list}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.data_v1alpha.types.AudienceList:
                An audience list is a list of users
                in an audience at the time of the list's
                creation. One audience may have multiple
                audience lists created for different
                days.

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

        request = analytics_data_api.GetAudienceListRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_audience_list,
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

    async def list_audience_lists(
        self,
        request: Optional[
            Union[analytics_data_api.ListAudienceListsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAudienceListsAsyncPager:
        r"""Lists all audience lists for a property. This method can be used
        for you to find and reuse existing audience lists rather than
        creating unnecessary new audience lists. The same audience can
        have multiple audience lists that represent the list of users
        that were in an audience on different days.

        See `Creating an Audience
        List <https://developers.google.com/analytics/devguides/reporting/data/v1/audience-list-basics>`__
        for an introduction to Audience Lists with examples.

        This method is available at beta stability at
        `audienceExports.list <https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties.audienceExports/list>`__.
        To give your feedback on this API, complete the `Google
        Analytics Audience Export API
        Feedback <https://forms.gle/EeA5u5LW6PEggtCEA>`__ form.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import data_v1alpha

            async def sample_list_audience_lists():
                # Create a client
                client = data_v1alpha.AlphaAnalyticsDataAsyncClient()

                # Initialize request argument(s)
                request = data_v1alpha.ListAudienceListsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_audience_lists(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.analytics.data_v1alpha.types.ListAudienceListsRequest, dict]]):
                The request object. A request to list all audience lists
                for a property.
            parent (:class:`str`):
                Required. All audience lists for this property will be
                listed in the response. Format:
                ``properties/{property}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.data_v1alpha.services.alpha_analytics_data.pagers.ListAudienceListsAsyncPager:
                A list of all audience lists for a
                property.
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

        request = analytics_data_api.ListAudienceListsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_audience_lists,
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
        response = pagers.ListAudienceListsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_recurring_audience_list(
        self,
        request: Optional[
            Union[analytics_data_api.CreateRecurringAudienceListRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        recurring_audience_list: Optional[
            analytics_data_api.RecurringAudienceList
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_data_api.RecurringAudienceList:
        r"""Creates a recurring audience list. Recurring audience lists
        produces new audience lists each day. Audience lists are users
        in an audience at the time of the list's creation.

        A recurring audience list ensures that you have audience list
        based on the most recent data available for use each day. If you
        manually create audience list, you don't know when an audience
        list based on an additional day's data is available. This
        recurring audience list automates the creation of an audience
        list when an additional day's data is available. You will
        consume fewer quota tokens by using recurring audience list
        versus manually creating audience list at various times of day
        trying to guess when an additional day's data is ready.

        This method is introduced at alpha stability with the intention
        of gathering feedback on syntax and capabilities before entering
        beta. To give your feedback on this API, complete the `Google
        Analytics Audience Export API
        Feedback <https://forms.gle/EeA5u5LW6PEggtCEA>`__ form.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import data_v1alpha

            async def sample_create_recurring_audience_list():
                # Create a client
                client = data_v1alpha.AlphaAnalyticsDataAsyncClient()

                # Initialize request argument(s)
                recurring_audience_list = data_v1alpha.RecurringAudienceList()
                recurring_audience_list.audience = "audience_value"

                request = data_v1alpha.CreateRecurringAudienceListRequest(
                    parent="parent_value",
                    recurring_audience_list=recurring_audience_list,
                )

                # Make the request
                response = await client.create_recurring_audience_list(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.data_v1alpha.types.CreateRecurringAudienceListRequest, dict]]):
                The request object. A request to create a new recurring
                audience list.
            parent (:class:`str`):
                Required. The parent resource where this recurring
                audience list will be created. Format:
                ``properties/{property}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            recurring_audience_list (:class:`google.analytics.data_v1alpha.types.RecurringAudienceList`):
                Required. The recurring audience list
                to create.

                This corresponds to the ``recurring_audience_list`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.data_v1alpha.types.RecurringAudienceList:
                A recurring audience list produces
                new audience lists each day. Audience
                lists are users in an audience at the
                time of the list's creation. A recurring
                audience list ensures that you have
                audience list based on the most recent
                data available for use each day.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, recurring_audience_list])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = analytics_data_api.CreateRecurringAudienceListRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if recurring_audience_list is not None:
            request.recurring_audience_list = recurring_audience_list

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_recurring_audience_list,
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

    async def get_recurring_audience_list(
        self,
        request: Optional[
            Union[analytics_data_api.GetRecurringAudienceListRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_data_api.RecurringAudienceList:
        r"""Gets configuration metadata about a specific recurring audience
        list. This method can be used to understand a recurring audience
        list's state after it has been created. For example, a recurring
        audience list resource will generate audience list instances for
        each day, and this method can be used to get the resource name
        of the most recent audience list instance.

        This method is introduced at alpha stability with the intention
        of gathering feedback on syntax and capabilities before entering
        beta. To give your feedback on this API, complete the `Google
        Analytics Audience Export API
        Feedback <https://forms.gle/EeA5u5LW6PEggtCEA>`__ form.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import data_v1alpha

            async def sample_get_recurring_audience_list():
                # Create a client
                client = data_v1alpha.AlphaAnalyticsDataAsyncClient()

                # Initialize request argument(s)
                request = data_v1alpha.GetRecurringAudienceListRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_recurring_audience_list(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.analytics.data_v1alpha.types.GetRecurringAudienceListRequest, dict]]):
                The request object. A request to retrieve configuration
                metadata about a specific recurring
                audience list.
            name (:class:`str`):
                Required. The recurring audience list resource name.
                Format:
                ``properties/{property}/recurringAudienceLists/{recurring_audience_list}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.data_v1alpha.types.RecurringAudienceList:
                A recurring audience list produces
                new audience lists each day. Audience
                lists are users in an audience at the
                time of the list's creation. A recurring
                audience list ensures that you have
                audience list based on the most recent
                data available for use each day.

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

        request = analytics_data_api.GetRecurringAudienceListRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_recurring_audience_list,
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

    async def list_recurring_audience_lists(
        self,
        request: Optional[
            Union[analytics_data_api.ListRecurringAudienceListsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListRecurringAudienceListsAsyncPager:
        r"""Lists all recurring audience lists for a property. This method
        can be used for you to find and reuse existing recurring
        audience lists rather than creating unnecessary new recurring
        audience lists. The same audience can have multiple recurring
        audience lists that represent different dimension combinations;
        for example, just the dimension ``deviceId`` or both the
        dimensions ``deviceId`` and ``userId``.

        This method is introduced at alpha stability with the intention
        of gathering feedback on syntax and capabilities before entering
        beta. To give your feedback on this API, complete the `Google
        Analytics Audience Export API
        Feedback <https://forms.gle/EeA5u5LW6PEggtCEA>`__ form.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.analytics import data_v1alpha

            async def sample_list_recurring_audience_lists():
                # Create a client
                client = data_v1alpha.AlphaAnalyticsDataAsyncClient()

                # Initialize request argument(s)
                request = data_v1alpha.ListRecurringAudienceListsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_recurring_audience_lists(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.analytics.data_v1alpha.types.ListRecurringAudienceListsRequest, dict]]):
                The request object. A request to list all recurring
                audience lists for a property.
            parent (:class:`str`):
                Required. All recurring audience lists for this property
                will be listed in the response. Format:
                ``properties/{property}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.data_v1alpha.services.alpha_analytics_data.pagers.ListRecurringAudienceListsAsyncPager:
                A list of all recurring audience
                lists for a property.
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

        request = analytics_data_api.ListRecurringAudienceListsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_recurring_audience_lists,
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
        response = pagers.ListRecurringAudienceListsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self) -> "AlphaAnalyticsDataAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("AlphaAnalyticsDataAsyncClient",)
