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

import dataclasses
import json  # type: ignore
import re
from typing import Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, path_template, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore


from google.protobuf import empty_pb2  # type: ignore

from google.analytics.admin_v1beta.types import analytics_admin, resources

from .base import AnalyticsAdminServiceTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class AnalyticsAdminServiceRestInterceptor:
    """Interceptor for AnalyticsAdminService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the AnalyticsAdminServiceRestTransport.

    .. code-block:: python
        class MyCustomAnalyticsAdminServiceInterceptor(AnalyticsAdminServiceRestInterceptor):
            def pre_acknowledge_user_data_collection(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_acknowledge_user_data_collection(response):
                logging.log(f"Received response: {response}")

            def pre_archive_custom_dimension(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_archive_custom_metric(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_create_conversion_event(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_conversion_event(response):
                logging.log(f"Received response: {response}")

            def pre_create_custom_dimension(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_custom_dimension(response):
                logging.log(f"Received response: {response}")

            def pre_create_custom_metric(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_custom_metric(response):
                logging.log(f"Received response: {response}")

            def pre_create_data_stream(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_data_stream(response):
                logging.log(f"Received response: {response}")

            def pre_create_firebase_link(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_firebase_link(response):
                logging.log(f"Received response: {response}")

            def pre_create_google_ads_link(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_google_ads_link(response):
                logging.log(f"Received response: {response}")

            def pre_create_measurement_protocol_secret(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_measurement_protocol_secret(response):
                logging.log(f"Received response: {response}")

            def pre_create_property(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_property(response):
                logging.log(f"Received response: {response}")

            def pre_delete_account(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_conversion_event(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_data_stream(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_firebase_link(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_google_ads_link(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_measurement_protocol_secret(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_property(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_property(response):
                logging.log(f"Received response: {response}")

            def pre_get_account(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_account(response):
                logging.log(f"Received response: {response}")

            def pre_get_conversion_event(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_conversion_event(response):
                logging.log(f"Received response: {response}")

            def pre_get_custom_dimension(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_custom_dimension(response):
                logging.log(f"Received response: {response}")

            def pre_get_custom_metric(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_custom_metric(response):
                logging.log(f"Received response: {response}")

            def pre_get_data_retention_settings(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_data_retention_settings(response):
                logging.log(f"Received response: {response}")

            def pre_get_data_sharing_settings(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_data_sharing_settings(response):
                logging.log(f"Received response: {response}")

            def pre_get_data_stream(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_data_stream(response):
                logging.log(f"Received response: {response}")

            def pre_get_measurement_protocol_secret(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_measurement_protocol_secret(response):
                logging.log(f"Received response: {response}")

            def pre_get_property(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_property(response):
                logging.log(f"Received response: {response}")

            def pre_list_accounts(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_accounts(response):
                logging.log(f"Received response: {response}")

            def pre_list_account_summaries(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_account_summaries(response):
                logging.log(f"Received response: {response}")

            def pre_list_conversion_events(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_conversion_events(response):
                logging.log(f"Received response: {response}")

            def pre_list_custom_dimensions(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_custom_dimensions(response):
                logging.log(f"Received response: {response}")

            def pre_list_custom_metrics(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_custom_metrics(response):
                logging.log(f"Received response: {response}")

            def pre_list_data_streams(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_data_streams(response):
                logging.log(f"Received response: {response}")

            def pre_list_firebase_links(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_firebase_links(response):
                logging.log(f"Received response: {response}")

            def pre_list_google_ads_links(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_google_ads_links(response):
                logging.log(f"Received response: {response}")

            def pre_list_measurement_protocol_secrets(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_measurement_protocol_secrets(response):
                logging.log(f"Received response: {response}")

            def pre_list_properties(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_properties(response):
                logging.log(f"Received response: {response}")

            def pre_provision_account_ticket(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_provision_account_ticket(response):
                logging.log(f"Received response: {response}")

            def pre_search_change_history_events(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_search_change_history_events(response):
                logging.log(f"Received response: {response}")

            def pre_update_account(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_account(response):
                logging.log(f"Received response: {response}")

            def pre_update_custom_dimension(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_custom_dimension(response):
                logging.log(f"Received response: {response}")

            def pre_update_custom_metric(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_custom_metric(response):
                logging.log(f"Received response: {response}")

            def pre_update_data_retention_settings(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_data_retention_settings(response):
                logging.log(f"Received response: {response}")

            def pre_update_data_stream(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_data_stream(response):
                logging.log(f"Received response: {response}")

            def pre_update_google_ads_link(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_google_ads_link(response):
                logging.log(f"Received response: {response}")

            def pre_update_measurement_protocol_secret(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_measurement_protocol_secret(response):
                logging.log(f"Received response: {response}")

            def pre_update_property(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_property(response):
                logging.log(f"Received response: {response}")

        transport = AnalyticsAdminServiceRestTransport(interceptor=MyCustomAnalyticsAdminServiceInterceptor())
        client = AnalyticsAdminServiceClient(transport=transport)


    """

    def pre_acknowledge_user_data_collection(
        self,
        request: analytics_admin.AcknowledgeUserDataCollectionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.AcknowledgeUserDataCollectionRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for acknowledge_user_data_collection

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_acknowledge_user_data_collection(
        self, response: analytics_admin.AcknowledgeUserDataCollectionResponse
    ) -> analytics_admin.AcknowledgeUserDataCollectionResponse:
        """Post-rpc interceptor for acknowledge_user_data_collection

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_archive_custom_dimension(
        self,
        request: analytics_admin.ArchiveCustomDimensionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.ArchiveCustomDimensionRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for archive_custom_dimension

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def pre_archive_custom_metric(
        self,
        request: analytics_admin.ArchiveCustomMetricRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.ArchiveCustomMetricRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for archive_custom_metric

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def pre_create_conversion_event(
        self,
        request: analytics_admin.CreateConversionEventRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.CreateConversionEventRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_conversion_event

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_create_conversion_event(
        self, response: resources.ConversionEvent
    ) -> resources.ConversionEvent:
        """Post-rpc interceptor for create_conversion_event

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_create_custom_dimension(
        self,
        request: analytics_admin.CreateCustomDimensionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.CreateCustomDimensionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_custom_dimension

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_create_custom_dimension(
        self, response: resources.CustomDimension
    ) -> resources.CustomDimension:
        """Post-rpc interceptor for create_custom_dimension

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_create_custom_metric(
        self,
        request: analytics_admin.CreateCustomMetricRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.CreateCustomMetricRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_custom_metric

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_create_custom_metric(
        self, response: resources.CustomMetric
    ) -> resources.CustomMetric:
        """Post-rpc interceptor for create_custom_metric

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_create_data_stream(
        self,
        request: analytics_admin.CreateDataStreamRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.CreateDataStreamRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_data_stream

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_create_data_stream(
        self, response: resources.DataStream
    ) -> resources.DataStream:
        """Post-rpc interceptor for create_data_stream

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_create_firebase_link(
        self,
        request: analytics_admin.CreateFirebaseLinkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.CreateFirebaseLinkRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_firebase_link

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_create_firebase_link(
        self, response: resources.FirebaseLink
    ) -> resources.FirebaseLink:
        """Post-rpc interceptor for create_firebase_link

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_create_google_ads_link(
        self,
        request: analytics_admin.CreateGoogleAdsLinkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.CreateGoogleAdsLinkRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_google_ads_link

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_create_google_ads_link(
        self, response: resources.GoogleAdsLink
    ) -> resources.GoogleAdsLink:
        """Post-rpc interceptor for create_google_ads_link

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_create_measurement_protocol_secret(
        self,
        request: analytics_admin.CreateMeasurementProtocolSecretRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.CreateMeasurementProtocolSecretRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for create_measurement_protocol_secret

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_create_measurement_protocol_secret(
        self, response: resources.MeasurementProtocolSecret
    ) -> resources.MeasurementProtocolSecret:
        """Post-rpc interceptor for create_measurement_protocol_secret

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_create_property(
        self,
        request: analytics_admin.CreatePropertyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.CreatePropertyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_property

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_create_property(self, response: resources.Property) -> resources.Property:
        """Post-rpc interceptor for create_property

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_account(
        self,
        request: analytics_admin.DeleteAccountRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.DeleteAccountRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_account

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def pre_delete_conversion_event(
        self,
        request: analytics_admin.DeleteConversionEventRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.DeleteConversionEventRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_conversion_event

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def pre_delete_data_stream(
        self,
        request: analytics_admin.DeleteDataStreamRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.DeleteDataStreamRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_data_stream

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def pre_delete_firebase_link(
        self,
        request: analytics_admin.DeleteFirebaseLinkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.DeleteFirebaseLinkRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_firebase_link

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def pre_delete_google_ads_link(
        self,
        request: analytics_admin.DeleteGoogleAdsLinkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.DeleteGoogleAdsLinkRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_google_ads_link

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def pre_delete_measurement_protocol_secret(
        self,
        request: analytics_admin.DeleteMeasurementProtocolSecretRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.DeleteMeasurementProtocolSecretRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for delete_measurement_protocol_secret

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def pre_delete_property(
        self,
        request: analytics_admin.DeletePropertyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.DeletePropertyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_property

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_delete_property(self, response: resources.Property) -> resources.Property:
        """Post-rpc interceptor for delete_property

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_get_account(
        self,
        request: analytics_admin.GetAccountRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.GetAccountRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_account

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_get_account(self, response: resources.Account) -> resources.Account:
        """Post-rpc interceptor for get_account

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_get_conversion_event(
        self,
        request: analytics_admin.GetConversionEventRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.GetConversionEventRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_conversion_event

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_get_conversion_event(
        self, response: resources.ConversionEvent
    ) -> resources.ConversionEvent:
        """Post-rpc interceptor for get_conversion_event

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_get_custom_dimension(
        self,
        request: analytics_admin.GetCustomDimensionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.GetCustomDimensionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_custom_dimension

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_get_custom_dimension(
        self, response: resources.CustomDimension
    ) -> resources.CustomDimension:
        """Post-rpc interceptor for get_custom_dimension

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_get_custom_metric(
        self,
        request: analytics_admin.GetCustomMetricRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.GetCustomMetricRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_custom_metric

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_get_custom_metric(
        self, response: resources.CustomMetric
    ) -> resources.CustomMetric:
        """Post-rpc interceptor for get_custom_metric

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_get_data_retention_settings(
        self,
        request: analytics_admin.GetDataRetentionSettingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.GetDataRetentionSettingsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_data_retention_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_get_data_retention_settings(
        self, response: resources.DataRetentionSettings
    ) -> resources.DataRetentionSettings:
        """Post-rpc interceptor for get_data_retention_settings

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_get_data_sharing_settings(
        self,
        request: analytics_admin.GetDataSharingSettingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.GetDataSharingSettingsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_data_sharing_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_get_data_sharing_settings(
        self, response: resources.DataSharingSettings
    ) -> resources.DataSharingSettings:
        """Post-rpc interceptor for get_data_sharing_settings

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_get_data_stream(
        self,
        request: analytics_admin.GetDataStreamRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.GetDataStreamRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_data_stream

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_get_data_stream(
        self, response: resources.DataStream
    ) -> resources.DataStream:
        """Post-rpc interceptor for get_data_stream

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_get_measurement_protocol_secret(
        self,
        request: analytics_admin.GetMeasurementProtocolSecretRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.GetMeasurementProtocolSecretRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_measurement_protocol_secret

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_get_measurement_protocol_secret(
        self, response: resources.MeasurementProtocolSecret
    ) -> resources.MeasurementProtocolSecret:
        """Post-rpc interceptor for get_measurement_protocol_secret

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_get_property(
        self,
        request: analytics_admin.GetPropertyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.GetPropertyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_property

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_get_property(self, response: resources.Property) -> resources.Property:
        """Post-rpc interceptor for get_property

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_list_accounts(
        self,
        request: analytics_admin.ListAccountsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.ListAccountsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_accounts

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_list_accounts(
        self, response: analytics_admin.ListAccountsResponse
    ) -> analytics_admin.ListAccountsResponse:
        """Post-rpc interceptor for list_accounts

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_list_account_summaries(
        self,
        request: analytics_admin.ListAccountSummariesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.ListAccountSummariesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_account_summaries

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_list_account_summaries(
        self, response: analytics_admin.ListAccountSummariesResponse
    ) -> analytics_admin.ListAccountSummariesResponse:
        """Post-rpc interceptor for list_account_summaries

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_list_conversion_events(
        self,
        request: analytics_admin.ListConversionEventsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.ListConversionEventsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_conversion_events

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_list_conversion_events(
        self, response: analytics_admin.ListConversionEventsResponse
    ) -> analytics_admin.ListConversionEventsResponse:
        """Post-rpc interceptor for list_conversion_events

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_list_custom_dimensions(
        self,
        request: analytics_admin.ListCustomDimensionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.ListCustomDimensionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_custom_dimensions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_list_custom_dimensions(
        self, response: analytics_admin.ListCustomDimensionsResponse
    ) -> analytics_admin.ListCustomDimensionsResponse:
        """Post-rpc interceptor for list_custom_dimensions

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_list_custom_metrics(
        self,
        request: analytics_admin.ListCustomMetricsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.ListCustomMetricsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_custom_metrics

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_list_custom_metrics(
        self, response: analytics_admin.ListCustomMetricsResponse
    ) -> analytics_admin.ListCustomMetricsResponse:
        """Post-rpc interceptor for list_custom_metrics

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_list_data_streams(
        self,
        request: analytics_admin.ListDataStreamsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.ListDataStreamsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_data_streams

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_list_data_streams(
        self, response: analytics_admin.ListDataStreamsResponse
    ) -> analytics_admin.ListDataStreamsResponse:
        """Post-rpc interceptor for list_data_streams

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_list_firebase_links(
        self,
        request: analytics_admin.ListFirebaseLinksRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.ListFirebaseLinksRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_firebase_links

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_list_firebase_links(
        self, response: analytics_admin.ListFirebaseLinksResponse
    ) -> analytics_admin.ListFirebaseLinksResponse:
        """Post-rpc interceptor for list_firebase_links

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_list_google_ads_links(
        self,
        request: analytics_admin.ListGoogleAdsLinksRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.ListGoogleAdsLinksRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_google_ads_links

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_list_google_ads_links(
        self, response: analytics_admin.ListGoogleAdsLinksResponse
    ) -> analytics_admin.ListGoogleAdsLinksResponse:
        """Post-rpc interceptor for list_google_ads_links

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_list_measurement_protocol_secrets(
        self,
        request: analytics_admin.ListMeasurementProtocolSecretsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.ListMeasurementProtocolSecretsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_measurement_protocol_secrets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_list_measurement_protocol_secrets(
        self, response: analytics_admin.ListMeasurementProtocolSecretsResponse
    ) -> analytics_admin.ListMeasurementProtocolSecretsResponse:
        """Post-rpc interceptor for list_measurement_protocol_secrets

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_list_properties(
        self,
        request: analytics_admin.ListPropertiesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.ListPropertiesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_properties

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_list_properties(
        self, response: analytics_admin.ListPropertiesResponse
    ) -> analytics_admin.ListPropertiesResponse:
        """Post-rpc interceptor for list_properties

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_provision_account_ticket(
        self,
        request: analytics_admin.ProvisionAccountTicketRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.ProvisionAccountTicketRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for provision_account_ticket

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_provision_account_ticket(
        self, response: analytics_admin.ProvisionAccountTicketResponse
    ) -> analytics_admin.ProvisionAccountTicketResponse:
        """Post-rpc interceptor for provision_account_ticket

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_search_change_history_events(
        self,
        request: analytics_admin.SearchChangeHistoryEventsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.SearchChangeHistoryEventsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for search_change_history_events

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_search_change_history_events(
        self, response: analytics_admin.SearchChangeHistoryEventsResponse
    ) -> analytics_admin.SearchChangeHistoryEventsResponse:
        """Post-rpc interceptor for search_change_history_events

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_update_account(
        self,
        request: analytics_admin.UpdateAccountRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.UpdateAccountRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_account

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_update_account(self, response: resources.Account) -> resources.Account:
        """Post-rpc interceptor for update_account

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_update_custom_dimension(
        self,
        request: analytics_admin.UpdateCustomDimensionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.UpdateCustomDimensionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_custom_dimension

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_update_custom_dimension(
        self, response: resources.CustomDimension
    ) -> resources.CustomDimension:
        """Post-rpc interceptor for update_custom_dimension

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_update_custom_metric(
        self,
        request: analytics_admin.UpdateCustomMetricRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.UpdateCustomMetricRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_custom_metric

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_update_custom_metric(
        self, response: resources.CustomMetric
    ) -> resources.CustomMetric:
        """Post-rpc interceptor for update_custom_metric

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_update_data_retention_settings(
        self,
        request: analytics_admin.UpdateDataRetentionSettingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.UpdateDataRetentionSettingsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_data_retention_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_update_data_retention_settings(
        self, response: resources.DataRetentionSettings
    ) -> resources.DataRetentionSettings:
        """Post-rpc interceptor for update_data_retention_settings

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_update_data_stream(
        self,
        request: analytics_admin.UpdateDataStreamRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.UpdateDataStreamRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_data_stream

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_update_data_stream(
        self, response: resources.DataStream
    ) -> resources.DataStream:
        """Post-rpc interceptor for update_data_stream

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_update_google_ads_link(
        self,
        request: analytics_admin.UpdateGoogleAdsLinkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.UpdateGoogleAdsLinkRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_google_ads_link

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_update_google_ads_link(
        self, response: resources.GoogleAdsLink
    ) -> resources.GoogleAdsLink:
        """Post-rpc interceptor for update_google_ads_link

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_update_measurement_protocol_secret(
        self,
        request: analytics_admin.UpdateMeasurementProtocolSecretRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.UpdateMeasurementProtocolSecretRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for update_measurement_protocol_secret

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_update_measurement_protocol_secret(
        self, response: resources.MeasurementProtocolSecret
    ) -> resources.MeasurementProtocolSecret:
        """Post-rpc interceptor for update_measurement_protocol_secret

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_update_property(
        self,
        request: analytics_admin.UpdatePropertyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.UpdatePropertyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_property

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_update_property(self, response: resources.Property) -> resources.Property:
        """Post-rpc interceptor for update_property

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class AnalyticsAdminServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: AnalyticsAdminServiceRestInterceptor


class AnalyticsAdminServiceRestTransport(AnalyticsAdminServiceTransport):
    """REST backend transport for AnalyticsAdminService.

    Service Interface for the Analytics Admin API (GA4).

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    NOTE: This REST transport functionality is currently in a beta
    state (preview). We welcome your feedback via an issue in this
    library's source repository. Thank you!
    """

    def __init__(
        self,
        *,
        host: str = "analyticsadmin.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Sequence[str] = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[AnalyticsAdminServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        NOTE: This REST transport functionality is currently in a beta
        state (preview). We welcome your feedback via a GitHub issue in
        this library's repository. Thank you!

         Args:
             host (Optional[str]):
                  The hostname to connect to.
             credentials (Optional[google.auth.credentials.Credentials]): The
                 authorization credentials to attach to requests. These
                 credentials identify the application to the service; if none
                 are specified, the client will attempt to ascertain the
                 credentials from the environment.

             credentials_file (Optional[str]): A file with credentials that can
                 be loaded with :func:`google.auth.load_credentials_from_file`.
                 This argument is ignored if ``channel`` is provided.
             scopes (Optional(Sequence[str])): A list of scopes. This argument is
                 ignored if ``channel`` is provided.
             client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                 certificate to configure mutual TLS HTTP channel. It is ignored
                 if ``channel`` is provided.
             quota_project_id (Optional[str]): An optional project to use for billing
                 and quota.
             client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                 The client info used to send a user-agent string along with
                 API requests. If ``None``, then default info will be used.
                 Generally, you only need to set this if you are developing
                 your own client library.
             always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                 be used for service account credentials.
             url_scheme: the protocol scheme for the API endpoint.  Normally
                 "https", but for testing or local servers,
                 "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        maybe_url_match = re.match("^(?P<scheme>http(?:s)?://)?(?P<host>.*)$", host)
        if maybe_url_match is None:
            raise ValueError(
                f"Unexpected hostname structure: {host}"
            )  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or AnalyticsAdminServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _AcknowledgeUserDataCollection(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("AcknowledgeUserDataCollection")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.AcknowledgeUserDataCollectionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.AcknowledgeUserDataCollectionResponse:
            r"""Call the acknowledge user data
            collection method over HTTP.

                Args:
                    request (~.analytics_admin.AcknowledgeUserDataCollectionRequest):
                        The request object. Request message for
                    AcknowledgeUserDataCollection RPC.

                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.analytics_admin.AcknowledgeUserDataCollectionResponse:
                        Response message for
                    AcknowledgeUserDataCollection RPC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/{property=properties/*}:acknowledgeUserDataCollection",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_acknowledge_user_data_collection(
                request, metadata
            )
            pb_request = analytics_admin.AcknowledgeUserDataCollectionRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = analytics_admin.AcknowledgeUserDataCollectionResponse()
            pb_resp = analytics_admin.AcknowledgeUserDataCollectionResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_acknowledge_user_data_collection(resp)
            return resp

    class _ArchiveCustomDimension(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ArchiveCustomDimension")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.ArchiveCustomDimensionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the archive custom dimension method over HTTP.

            Args:
                request (~.analytics_admin.ArchiveCustomDimensionRequest):
                    The request object. Request message for
                ArchiveCustomDimension RPC.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/{name=properties/*/customDimensions/*}:archive",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_archive_custom_dimension(
                request, metadata
            )
            pb_request = analytics_admin.ArchiveCustomDimensionRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _ArchiveCustomMetric(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ArchiveCustomMetric")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.ArchiveCustomMetricRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the archive custom metric method over HTTP.

            Args:
                request (~.analytics_admin.ArchiveCustomMetricRequest):
                    The request object. Request message for
                ArchiveCustomMetric RPC.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/{name=properties/*/customMetrics/*}:archive",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_archive_custom_metric(
                request, metadata
            )
            pb_request = analytics_admin.ArchiveCustomMetricRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _CreateConversionEvent(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("CreateConversionEvent")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.CreateConversionEventRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.ConversionEvent:
            r"""Call the create conversion event method over HTTP.

            Args:
                request (~.analytics_admin.CreateConversionEventRequest):
                    The request object. Request message for
                CreateConversionEvent RPC

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.ConversionEvent:
                    A conversion event in a Google
                Analytics property.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/{parent=properties/*}/conversionEvents",
                    "body": "conversion_event",
                },
            ]
            request, metadata = self._interceptor.pre_create_conversion_event(
                request, metadata
            )
            pb_request = analytics_admin.CreateConversionEventRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.ConversionEvent()
            pb_resp = resources.ConversionEvent.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_conversion_event(resp)
            return resp

    class _CreateCustomDimension(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("CreateCustomDimension")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.CreateCustomDimensionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.CustomDimension:
            r"""Call the create custom dimension method over HTTP.

            Args:
                request (~.analytics_admin.CreateCustomDimensionRequest):
                    The request object. Request message for
                CreateCustomDimension RPC.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.CustomDimension:
                    A definition for a CustomDimension.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/{parent=properties/*}/customDimensions",
                    "body": "custom_dimension",
                },
            ]
            request, metadata = self._interceptor.pre_create_custom_dimension(
                request, metadata
            )
            pb_request = analytics_admin.CreateCustomDimensionRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.CustomDimension()
            pb_resp = resources.CustomDimension.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_custom_dimension(resp)
            return resp

    class _CreateCustomMetric(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("CreateCustomMetric")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.CreateCustomMetricRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.CustomMetric:
            r"""Call the create custom metric method over HTTP.

            Args:
                request (~.analytics_admin.CreateCustomMetricRequest):
                    The request object. Request message for
                CreateCustomMetric RPC.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.CustomMetric:
                    A definition for a custom metric.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/{parent=properties/*}/customMetrics",
                    "body": "custom_metric",
                },
            ]
            request, metadata = self._interceptor.pre_create_custom_metric(
                request, metadata
            )
            pb_request = analytics_admin.CreateCustomMetricRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.CustomMetric()
            pb_resp = resources.CustomMetric.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_custom_metric(resp)
            return resp

    class _CreateDataStream(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("CreateDataStream")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.CreateDataStreamRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.DataStream:
            r"""Call the create data stream method over HTTP.

            Args:
                request (~.analytics_admin.CreateDataStreamRequest):
                    The request object. Request message for CreateDataStream
                RPC.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.DataStream:
                    A resource message representing a
                data stream.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/{parent=properties/*}/dataStreams",
                    "body": "data_stream",
                },
            ]
            request, metadata = self._interceptor.pre_create_data_stream(
                request, metadata
            )
            pb_request = analytics_admin.CreateDataStreamRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.DataStream()
            pb_resp = resources.DataStream.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_data_stream(resp)
            return resp

    class _CreateFirebaseLink(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("CreateFirebaseLink")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.CreateFirebaseLinkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.FirebaseLink:
            r"""Call the create firebase link method over HTTP.

            Args:
                request (~.analytics_admin.CreateFirebaseLinkRequest):
                    The request object. Request message for
                CreateFirebaseLink RPC

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.FirebaseLink:
                    A link between a GA4 property and a
                Firebase project.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/{parent=properties/*}/firebaseLinks",
                    "body": "firebase_link",
                },
            ]
            request, metadata = self._interceptor.pre_create_firebase_link(
                request, metadata
            )
            pb_request = analytics_admin.CreateFirebaseLinkRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.FirebaseLink()
            pb_resp = resources.FirebaseLink.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_firebase_link(resp)
            return resp

    class _CreateGoogleAdsLink(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("CreateGoogleAdsLink")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.CreateGoogleAdsLinkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.GoogleAdsLink:
            r"""Call the create google ads link method over HTTP.

            Args:
                request (~.analytics_admin.CreateGoogleAdsLinkRequest):
                    The request object. Request message for
                CreateGoogleAdsLink RPC

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.GoogleAdsLink:
                    A link between a GA4 property and a
                Google Ads account.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/{parent=properties/*}/googleAdsLinks",
                    "body": "google_ads_link",
                },
            ]
            request, metadata = self._interceptor.pre_create_google_ads_link(
                request, metadata
            )
            pb_request = analytics_admin.CreateGoogleAdsLinkRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.GoogleAdsLink()
            pb_resp = resources.GoogleAdsLink.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_google_ads_link(resp)
            return resp

    class _CreateMeasurementProtocolSecret(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("CreateMeasurementProtocolSecret")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.CreateMeasurementProtocolSecretRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.MeasurementProtocolSecret:
            r"""Call the create measurement
            protocol secret method over HTTP.

                Args:
                    request (~.analytics_admin.CreateMeasurementProtocolSecretRequest):
                        The request object. Request message for
                    CreateMeasurementProtocolSecret RPC

                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.MeasurementProtocolSecret:
                        A secret value used for sending hits
                    to Measurement Protocol.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/{parent=properties/*/dataStreams/*}/measurementProtocolSecrets",
                    "body": "measurement_protocol_secret",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_create_measurement_protocol_secret(
                request, metadata
            )
            pb_request = analytics_admin.CreateMeasurementProtocolSecretRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.MeasurementProtocolSecret()
            pb_resp = resources.MeasurementProtocolSecret.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_measurement_protocol_secret(resp)
            return resp

    class _CreateProperty(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("CreateProperty")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.CreatePropertyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Property:
            r"""Call the create property method over HTTP.

            Args:
                request (~.analytics_admin.CreatePropertyRequest):
                    The request object. Request message for CreateProperty
                RPC.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Property:
                    A resource message representing a
                Google Analytics GA4 property.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/properties",
                    "body": "property",
                },
            ]
            request, metadata = self._interceptor.pre_create_property(request, metadata)
            pb_request = analytics_admin.CreatePropertyRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.Property()
            pb_resp = resources.Property.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_property(resp)
            return resp

    class _DeleteAccount(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("DeleteAccount")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.DeleteAccountRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete account method over HTTP.

            Args:
                request (~.analytics_admin.DeleteAccountRequest):
                    The request object. Request message for DeleteAccount
                RPC.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1beta/{name=accounts/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_account(request, metadata)
            pb_request = analytics_admin.DeleteAccountRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _DeleteConversionEvent(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("DeleteConversionEvent")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.DeleteConversionEventRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete conversion event method over HTTP.

            Args:
                request (~.analytics_admin.DeleteConversionEventRequest):
                    The request object. Request message for
                DeleteConversionEvent RPC

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1beta/{name=properties/*/conversionEvents/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_conversion_event(
                request, metadata
            )
            pb_request = analytics_admin.DeleteConversionEventRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _DeleteDataStream(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("DeleteDataStream")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.DeleteDataStreamRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete data stream method over HTTP.

            Args:
                request (~.analytics_admin.DeleteDataStreamRequest):
                    The request object. Request message for DeleteDataStream
                RPC.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1beta/{name=properties/*/dataStreams/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_data_stream(
                request, metadata
            )
            pb_request = analytics_admin.DeleteDataStreamRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _DeleteFirebaseLink(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("DeleteFirebaseLink")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.DeleteFirebaseLinkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete firebase link method over HTTP.

            Args:
                request (~.analytics_admin.DeleteFirebaseLinkRequest):
                    The request object. Request message for
                DeleteFirebaseLink RPC

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1beta/{name=properties/*/firebaseLinks/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_firebase_link(
                request, metadata
            )
            pb_request = analytics_admin.DeleteFirebaseLinkRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _DeleteGoogleAdsLink(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("DeleteGoogleAdsLink")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.DeleteGoogleAdsLinkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete google ads link method over HTTP.

            Args:
                request (~.analytics_admin.DeleteGoogleAdsLinkRequest):
                    The request object. Request message for
                DeleteGoogleAdsLink RPC.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1beta/{name=properties/*/googleAdsLinks/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_google_ads_link(
                request, metadata
            )
            pb_request = analytics_admin.DeleteGoogleAdsLinkRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _DeleteMeasurementProtocolSecret(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("DeleteMeasurementProtocolSecret")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.DeleteMeasurementProtocolSecretRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete measurement
            protocol secret method over HTTP.

                Args:
                    request (~.analytics_admin.DeleteMeasurementProtocolSecretRequest):
                        The request object. Request message for
                    DeleteMeasurementProtocolSecret RPC

                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1beta/{name=properties/*/dataStreams/*/measurementProtocolSecrets/*}",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_delete_measurement_protocol_secret(
                request, metadata
            )
            pb_request = analytics_admin.DeleteMeasurementProtocolSecretRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _DeleteProperty(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("DeleteProperty")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.DeletePropertyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Property:
            r"""Call the delete property method over HTTP.

            Args:
                request (~.analytics_admin.DeletePropertyRequest):
                    The request object. Request message for DeleteProperty
                RPC.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Property:
                    A resource message representing a
                Google Analytics GA4 property.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1beta/{name=properties/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_property(request, metadata)
            pb_request = analytics_admin.DeletePropertyRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.Property()
            pb_resp = resources.Property.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_property(resp)
            return resp

    class _GetAccount(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetAccount")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.GetAccountRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Account:
            r"""Call the get account method over HTTP.

            Args:
                request (~.analytics_admin.GetAccountRequest):
                    The request object. Request message for GetAccount RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Account:
                    A resource message representing a
                Google Analytics account.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{name=accounts/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_account(request, metadata)
            pb_request = analytics_admin.GetAccountRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.Account()
            pb_resp = resources.Account.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_account(resp)
            return resp

    class _GetConversionEvent(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetConversionEvent")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.GetConversionEventRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.ConversionEvent:
            r"""Call the get conversion event method over HTTP.

            Args:
                request (~.analytics_admin.GetConversionEventRequest):
                    The request object. Request message for
                GetConversionEvent RPC

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.ConversionEvent:
                    A conversion event in a Google
                Analytics property.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{name=properties/*/conversionEvents/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_conversion_event(
                request, metadata
            )
            pb_request = analytics_admin.GetConversionEventRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.ConversionEvent()
            pb_resp = resources.ConversionEvent.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_conversion_event(resp)
            return resp

    class _GetCustomDimension(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetCustomDimension")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.GetCustomDimensionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.CustomDimension:
            r"""Call the get custom dimension method over HTTP.

            Args:
                request (~.analytics_admin.GetCustomDimensionRequest):
                    The request object. Request message for
                GetCustomDimension RPC.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.CustomDimension:
                    A definition for a CustomDimension.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{name=properties/*/customDimensions/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_custom_dimension(
                request, metadata
            )
            pb_request = analytics_admin.GetCustomDimensionRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.CustomDimension()
            pb_resp = resources.CustomDimension.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_custom_dimension(resp)
            return resp

    class _GetCustomMetric(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetCustomMetric")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.GetCustomMetricRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.CustomMetric:
            r"""Call the get custom metric method over HTTP.

            Args:
                request (~.analytics_admin.GetCustomMetricRequest):
                    The request object. Request message for GetCustomMetric
                RPC.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.CustomMetric:
                    A definition for a custom metric.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{name=properties/*/customMetrics/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_custom_metric(
                request, metadata
            )
            pb_request = analytics_admin.GetCustomMetricRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.CustomMetric()
            pb_resp = resources.CustomMetric.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_custom_metric(resp)
            return resp

    class _GetDataRetentionSettings(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetDataRetentionSettings")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.GetDataRetentionSettingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.DataRetentionSettings:
            r"""Call the get data retention
            settings method over HTTP.

                Args:
                    request (~.analytics_admin.GetDataRetentionSettingsRequest):
                        The request object. Request message for
                    GetDataRetentionSettings RPC.

                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.DataRetentionSettings:
                        Settings values for data retention.
                    This is a singleton resource.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{name=properties/*/dataRetentionSettings}",
                },
            ]
            request, metadata = self._interceptor.pre_get_data_retention_settings(
                request, metadata
            )
            pb_request = analytics_admin.GetDataRetentionSettingsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.DataRetentionSettings()
            pb_resp = resources.DataRetentionSettings.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_data_retention_settings(resp)
            return resp

    class _GetDataSharingSettings(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetDataSharingSettings")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.GetDataSharingSettingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.DataSharingSettings:
            r"""Call the get data sharing settings method over HTTP.

            Args:
                request (~.analytics_admin.GetDataSharingSettingsRequest):
                    The request object. Request message for
                GetDataSharingSettings RPC.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.DataSharingSettings:
                    A resource message representing data
                sharing settings of a Google Analytics
                account.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{name=accounts/*/dataSharingSettings}",
                },
            ]
            request, metadata = self._interceptor.pre_get_data_sharing_settings(
                request, metadata
            )
            pb_request = analytics_admin.GetDataSharingSettingsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.DataSharingSettings()
            pb_resp = resources.DataSharingSettings.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_data_sharing_settings(resp)
            return resp

    class _GetDataStream(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetDataStream")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.GetDataStreamRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.DataStream:
            r"""Call the get data stream method over HTTP.

            Args:
                request (~.analytics_admin.GetDataStreamRequest):
                    The request object. Request message for GetDataStream
                RPC.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.DataStream:
                    A resource message representing a
                data stream.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{name=properties/*/dataStreams/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_data_stream(request, metadata)
            pb_request = analytics_admin.GetDataStreamRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.DataStream()
            pb_resp = resources.DataStream.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_data_stream(resp)
            return resp

    class _GetMeasurementProtocolSecret(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetMeasurementProtocolSecret")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.GetMeasurementProtocolSecretRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.MeasurementProtocolSecret:
            r"""Call the get measurement protocol
            secret method over HTTP.

                Args:
                    request (~.analytics_admin.GetMeasurementProtocolSecretRequest):
                        The request object. Request message for
                    GetMeasurementProtocolSecret RPC.

                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.MeasurementProtocolSecret:
                        A secret value used for sending hits
                    to Measurement Protocol.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{name=properties/*/dataStreams/*/measurementProtocolSecrets/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_measurement_protocol_secret(
                request, metadata
            )
            pb_request = analytics_admin.GetMeasurementProtocolSecretRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.MeasurementProtocolSecret()
            pb_resp = resources.MeasurementProtocolSecret.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_measurement_protocol_secret(resp)
            return resp

    class _GetProperty(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetProperty")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.GetPropertyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Property:
            r"""Call the get property method over HTTP.

            Args:
                request (~.analytics_admin.GetPropertyRequest):
                    The request object. Request message for GetProperty RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Property:
                    A resource message representing a
                Google Analytics GA4 property.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{name=properties/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_property(request, metadata)
            pb_request = analytics_admin.GetPropertyRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.Property()
            pb_resp = resources.Property.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_property(resp)
            return resp

    class _ListAccounts(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ListAccounts")

        def __call__(
            self,
            request: analytics_admin.ListAccountsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.ListAccountsResponse:
            r"""Call the list accounts method over HTTP.

            Args:
                request (~.analytics_admin.ListAccountsRequest):
                    The request object. Request message for ListAccounts RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_admin.ListAccountsResponse:
                    Request message for ListAccounts RPC.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/accounts",
                },
            ]
            request, metadata = self._interceptor.pre_list_accounts(request, metadata)
            pb_request = analytics_admin.ListAccountsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = analytics_admin.ListAccountsResponse()
            pb_resp = analytics_admin.ListAccountsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_accounts(resp)
            return resp

    class _ListAccountSummaries(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ListAccountSummaries")

        def __call__(
            self,
            request: analytics_admin.ListAccountSummariesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.ListAccountSummariesResponse:
            r"""Call the list account summaries method over HTTP.

            Args:
                request (~.analytics_admin.ListAccountSummariesRequest):
                    The request object. Request message for
                ListAccountSummaries RPC.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_admin.ListAccountSummariesResponse:
                    Response message for
                ListAccountSummaries RPC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/accountSummaries",
                },
            ]
            request, metadata = self._interceptor.pre_list_account_summaries(
                request, metadata
            )
            pb_request = analytics_admin.ListAccountSummariesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = analytics_admin.ListAccountSummariesResponse()
            pb_resp = analytics_admin.ListAccountSummariesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_account_summaries(resp)
            return resp

    class _ListConversionEvents(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ListConversionEvents")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.ListConversionEventsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.ListConversionEventsResponse:
            r"""Call the list conversion events method over HTTP.

            Args:
                request (~.analytics_admin.ListConversionEventsRequest):
                    The request object. Request message for
                ListConversionEvents RPC

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_admin.ListConversionEventsResponse:
                    Response message for
                ListConversionEvents RPC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{parent=properties/*}/conversionEvents",
                },
            ]
            request, metadata = self._interceptor.pre_list_conversion_events(
                request, metadata
            )
            pb_request = analytics_admin.ListConversionEventsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = analytics_admin.ListConversionEventsResponse()
            pb_resp = analytics_admin.ListConversionEventsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_conversion_events(resp)
            return resp

    class _ListCustomDimensions(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ListCustomDimensions")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.ListCustomDimensionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.ListCustomDimensionsResponse:
            r"""Call the list custom dimensions method over HTTP.

            Args:
                request (~.analytics_admin.ListCustomDimensionsRequest):
                    The request object. Request message for
                ListCustomDimensions RPC.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_admin.ListCustomDimensionsResponse:
                    Response message for
                ListCustomDimensions RPC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{parent=properties/*}/customDimensions",
                },
            ]
            request, metadata = self._interceptor.pre_list_custom_dimensions(
                request, metadata
            )
            pb_request = analytics_admin.ListCustomDimensionsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = analytics_admin.ListCustomDimensionsResponse()
            pb_resp = analytics_admin.ListCustomDimensionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_custom_dimensions(resp)
            return resp

    class _ListCustomMetrics(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ListCustomMetrics")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.ListCustomMetricsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.ListCustomMetricsResponse:
            r"""Call the list custom metrics method over HTTP.

            Args:
                request (~.analytics_admin.ListCustomMetricsRequest):
                    The request object. Request message for ListCustomMetrics
                RPC.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_admin.ListCustomMetricsResponse:
                    Response message for
                ListCustomMetrics RPC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{parent=properties/*}/customMetrics",
                },
            ]
            request, metadata = self._interceptor.pre_list_custom_metrics(
                request, metadata
            )
            pb_request = analytics_admin.ListCustomMetricsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = analytics_admin.ListCustomMetricsResponse()
            pb_resp = analytics_admin.ListCustomMetricsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_custom_metrics(resp)
            return resp

    class _ListDataStreams(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ListDataStreams")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.ListDataStreamsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.ListDataStreamsResponse:
            r"""Call the list data streams method over HTTP.

            Args:
                request (~.analytics_admin.ListDataStreamsRequest):
                    The request object. Request message for ListDataStreams
                RPC.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_admin.ListDataStreamsResponse:
                    Response message for ListDataStreams
                RPC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{parent=properties/*}/dataStreams",
                },
            ]
            request, metadata = self._interceptor.pre_list_data_streams(
                request, metadata
            )
            pb_request = analytics_admin.ListDataStreamsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = analytics_admin.ListDataStreamsResponse()
            pb_resp = analytics_admin.ListDataStreamsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_data_streams(resp)
            return resp

    class _ListFirebaseLinks(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ListFirebaseLinks")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.ListFirebaseLinksRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.ListFirebaseLinksResponse:
            r"""Call the list firebase links method over HTTP.

            Args:
                request (~.analytics_admin.ListFirebaseLinksRequest):
                    The request object. Request message for ListFirebaseLinks
                RPC

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_admin.ListFirebaseLinksResponse:
                    Response message for
                ListFirebaseLinks RPC

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{parent=properties/*}/firebaseLinks",
                },
            ]
            request, metadata = self._interceptor.pre_list_firebase_links(
                request, metadata
            )
            pb_request = analytics_admin.ListFirebaseLinksRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = analytics_admin.ListFirebaseLinksResponse()
            pb_resp = analytics_admin.ListFirebaseLinksResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_firebase_links(resp)
            return resp

    class _ListGoogleAdsLinks(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ListGoogleAdsLinks")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.ListGoogleAdsLinksRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.ListGoogleAdsLinksResponse:
            r"""Call the list google ads links method over HTTP.

            Args:
                request (~.analytics_admin.ListGoogleAdsLinksRequest):
                    The request object. Request message for
                ListGoogleAdsLinks RPC.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_admin.ListGoogleAdsLinksResponse:
                    Response message for
                ListGoogleAdsLinks RPC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{parent=properties/*}/googleAdsLinks",
                },
            ]
            request, metadata = self._interceptor.pre_list_google_ads_links(
                request, metadata
            )
            pb_request = analytics_admin.ListGoogleAdsLinksRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = analytics_admin.ListGoogleAdsLinksResponse()
            pb_resp = analytics_admin.ListGoogleAdsLinksResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_google_ads_links(resp)
            return resp

    class _ListMeasurementProtocolSecrets(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ListMeasurementProtocolSecrets")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.ListMeasurementProtocolSecretsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.ListMeasurementProtocolSecretsResponse:
            r"""Call the list measurement protocol
            secrets method over HTTP.

                Args:
                    request (~.analytics_admin.ListMeasurementProtocolSecretsRequest):
                        The request object. Request message for
                    ListMeasurementProtocolSecret RPC

                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.analytics_admin.ListMeasurementProtocolSecretsResponse:
                        Response message for
                    ListMeasurementProtocolSecret RPC

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/{parent=properties/*/dataStreams/*}/measurementProtocolSecrets",
                },
            ]
            request, metadata = self._interceptor.pre_list_measurement_protocol_secrets(
                request, metadata
            )
            pb_request = analytics_admin.ListMeasurementProtocolSecretsRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = analytics_admin.ListMeasurementProtocolSecretsResponse()
            pb_resp = analytics_admin.ListMeasurementProtocolSecretsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_measurement_protocol_secrets(resp)
            return resp

    class _ListProperties(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ListProperties")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {
            "filter": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.ListPropertiesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.ListPropertiesResponse:
            r"""Call the list properties method over HTTP.

            Args:
                request (~.analytics_admin.ListPropertiesRequest):
                    The request object. Request message for ListProperties
                RPC.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_admin.ListPropertiesResponse:
                    Response message for ListProperties
                RPC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1beta/properties",
                },
            ]
            request, metadata = self._interceptor.pre_list_properties(request, metadata)
            pb_request = analytics_admin.ListPropertiesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = analytics_admin.ListPropertiesResponse()
            pb_resp = analytics_admin.ListPropertiesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_properties(resp)
            return resp

    class _ProvisionAccountTicket(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ProvisionAccountTicket")

        def __call__(
            self,
            request: analytics_admin.ProvisionAccountTicketRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.ProvisionAccountTicketResponse:
            r"""Call the provision account ticket method over HTTP.

            Args:
                request (~.analytics_admin.ProvisionAccountTicketRequest):
                    The request object. Request message for
                ProvisionAccountTicket RPC.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_admin.ProvisionAccountTicketResponse:
                    Response message for
                ProvisionAccountTicket RPC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/accounts:provisionAccountTicket",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_provision_account_ticket(
                request, metadata
            )
            pb_request = analytics_admin.ProvisionAccountTicketRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = analytics_admin.ProvisionAccountTicketResponse()
            pb_resp = analytics_admin.ProvisionAccountTicketResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_provision_account_ticket(resp)
            return resp

    class _SearchChangeHistoryEvents(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("SearchChangeHistoryEvents")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.SearchChangeHistoryEventsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.SearchChangeHistoryEventsResponse:
            r"""Call the search change history
            events method over HTTP.

                Args:
                    request (~.analytics_admin.SearchChangeHistoryEventsRequest):
                        The request object. Request message for
                    SearchChangeHistoryEvents RPC.

                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.analytics_admin.SearchChangeHistoryEventsResponse:
                        Response message for SearchAccounts
                    RPC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/{account=accounts/*}:searchChangeHistoryEvents",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_search_change_history_events(
                request, metadata
            )
            pb_request = analytics_admin.SearchChangeHistoryEventsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = analytics_admin.SearchChangeHistoryEventsResponse()
            pb_resp = analytics_admin.SearchChangeHistoryEventsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_search_change_history_events(resp)
            return resp

    class _UpdateAccount(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("UpdateAccount")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {
            "updateMask": {},
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.UpdateAccountRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Account:
            r"""Call the update account method over HTTP.

            Args:
                request (~.analytics_admin.UpdateAccountRequest):
                    The request object. Request message for UpdateAccount
                RPC.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Account:
                    A resource message representing a
                Google Analytics account.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1beta/{account.name=accounts/*}",
                    "body": "account",
                },
            ]
            request, metadata = self._interceptor.pre_update_account(request, metadata)
            pb_request = analytics_admin.UpdateAccountRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.Account()
            pb_resp = resources.Account.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_account(resp)
            return resp

    class _UpdateCustomDimension(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("UpdateCustomDimension")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {
            "updateMask": {},
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.UpdateCustomDimensionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.CustomDimension:
            r"""Call the update custom dimension method over HTTP.

            Args:
                request (~.analytics_admin.UpdateCustomDimensionRequest):
                    The request object. Request message for
                UpdateCustomDimension RPC.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.CustomDimension:
                    A definition for a CustomDimension.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1beta/{custom_dimension.name=properties/*/customDimensions/*}",
                    "body": "custom_dimension",
                },
            ]
            request, metadata = self._interceptor.pre_update_custom_dimension(
                request, metadata
            )
            pb_request = analytics_admin.UpdateCustomDimensionRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.CustomDimension()
            pb_resp = resources.CustomDimension.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_custom_dimension(resp)
            return resp

    class _UpdateCustomMetric(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("UpdateCustomMetric")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {
            "updateMask": {},
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.UpdateCustomMetricRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.CustomMetric:
            r"""Call the update custom metric method over HTTP.

            Args:
                request (~.analytics_admin.UpdateCustomMetricRequest):
                    The request object. Request message for
                UpdateCustomMetric RPC.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.CustomMetric:
                    A definition for a custom metric.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1beta/{custom_metric.name=properties/*/customMetrics/*}",
                    "body": "custom_metric",
                },
            ]
            request, metadata = self._interceptor.pre_update_custom_metric(
                request, metadata
            )
            pb_request = analytics_admin.UpdateCustomMetricRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.CustomMetric()
            pb_resp = resources.CustomMetric.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_custom_metric(resp)
            return resp

    class _UpdateDataRetentionSettings(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("UpdateDataRetentionSettings")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {
            "updateMask": {},
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.UpdateDataRetentionSettingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.DataRetentionSettings:
            r"""Call the update data retention
            settings method over HTTP.

                Args:
                    request (~.analytics_admin.UpdateDataRetentionSettingsRequest):
                        The request object. Request message for
                    UpdateDataRetentionSettings RPC.

                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.DataRetentionSettings:
                        Settings values for data retention.
                    This is a singleton resource.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1beta/{data_retention_settings.name=properties/*/dataRetentionSettings}",
                    "body": "data_retention_settings",
                },
            ]
            request, metadata = self._interceptor.pre_update_data_retention_settings(
                request, metadata
            )
            pb_request = analytics_admin.UpdateDataRetentionSettingsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.DataRetentionSettings()
            pb_resp = resources.DataRetentionSettings.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_data_retention_settings(resp)
            return resp

    class _UpdateDataStream(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("UpdateDataStream")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {
            "updateMask": {},
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.UpdateDataStreamRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.DataStream:
            r"""Call the update data stream method over HTTP.

            Args:
                request (~.analytics_admin.UpdateDataStreamRequest):
                    The request object. Request message for UpdateDataStream
                RPC.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.DataStream:
                    A resource message representing a
                data stream.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1beta/{data_stream.name=properties/*/dataStreams/*}",
                    "body": "data_stream",
                },
            ]
            request, metadata = self._interceptor.pre_update_data_stream(
                request, metadata
            )
            pb_request = analytics_admin.UpdateDataStreamRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.DataStream()
            pb_resp = resources.DataStream.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_data_stream(resp)
            return resp

    class _UpdateGoogleAdsLink(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("UpdateGoogleAdsLink")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {
            "updateMask": {},
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.UpdateGoogleAdsLinkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.GoogleAdsLink:
            r"""Call the update google ads link method over HTTP.

            Args:
                request (~.analytics_admin.UpdateGoogleAdsLinkRequest):
                    The request object. Request message for
                UpdateGoogleAdsLink RPC

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.GoogleAdsLink:
                    A link between a GA4 property and a
                Google Ads account.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1beta/{google_ads_link.name=properties/*/googleAdsLinks/*}",
                    "body": "google_ads_link",
                },
            ]
            request, metadata = self._interceptor.pre_update_google_ads_link(
                request, metadata
            )
            pb_request = analytics_admin.UpdateGoogleAdsLinkRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.GoogleAdsLink()
            pb_resp = resources.GoogleAdsLink.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_google_ads_link(resp)
            return resp

    class _UpdateMeasurementProtocolSecret(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("UpdateMeasurementProtocolSecret")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.UpdateMeasurementProtocolSecretRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.MeasurementProtocolSecret:
            r"""Call the update measurement
            protocol secret method over HTTP.

                Args:
                    request (~.analytics_admin.UpdateMeasurementProtocolSecretRequest):
                        The request object. Request message for
                    UpdateMeasurementProtocolSecret RPC

                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.MeasurementProtocolSecret:
                        A secret value used for sending hits
                    to Measurement Protocol.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1beta/{measurement_protocol_secret.name=properties/*/dataStreams/*/measurementProtocolSecrets/*}",
                    "body": "measurement_protocol_secret",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_update_measurement_protocol_secret(
                request, metadata
            )
            pb_request = analytics_admin.UpdateMeasurementProtocolSecretRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.MeasurementProtocolSecret()
            pb_resp = resources.MeasurementProtocolSecret.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_measurement_protocol_secret(resp)
            return resp

    class _UpdateProperty(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("UpdateProperty")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {
            "updateMask": {},
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.UpdatePropertyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Property:
            r"""Call the update property method over HTTP.

            Args:
                request (~.analytics_admin.UpdatePropertyRequest):
                    The request object. Request message for UpdateProperty
                RPC.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Property:
                    A resource message representing a
                Google Analytics GA4 property.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1beta/{property.name=properties/*}",
                    "body": "property",
                },
            ]
            request, metadata = self._interceptor.pre_update_property(request, metadata)
            pb_request = analytics_admin.UpdatePropertyRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.Property()
            pb_resp = resources.Property.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_property(resp)
            return resp

    @property
    def acknowledge_user_data_collection(
        self,
    ) -> Callable[
        [analytics_admin.AcknowledgeUserDataCollectionRequest],
        analytics_admin.AcknowledgeUserDataCollectionResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AcknowledgeUserDataCollection(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def archive_custom_dimension(
        self,
    ) -> Callable[[analytics_admin.ArchiveCustomDimensionRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ArchiveCustomDimension(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def archive_custom_metric(
        self,
    ) -> Callable[[analytics_admin.ArchiveCustomMetricRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ArchiveCustomMetric(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_conversion_event(
        self,
    ) -> Callable[
        [analytics_admin.CreateConversionEventRequest], resources.ConversionEvent
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateConversionEvent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_custom_dimension(
        self,
    ) -> Callable[
        [analytics_admin.CreateCustomDimensionRequest], resources.CustomDimension
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCustomDimension(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_custom_metric(
        self,
    ) -> Callable[[analytics_admin.CreateCustomMetricRequest], resources.CustomMetric]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCustomMetric(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_data_stream(
        self,
    ) -> Callable[[analytics_admin.CreateDataStreamRequest], resources.DataStream]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateDataStream(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_firebase_link(
        self,
    ) -> Callable[[analytics_admin.CreateFirebaseLinkRequest], resources.FirebaseLink]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateFirebaseLink(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_google_ads_link(
        self,
    ) -> Callable[
        [analytics_admin.CreateGoogleAdsLinkRequest], resources.GoogleAdsLink
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateGoogleAdsLink(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_measurement_protocol_secret(
        self,
    ) -> Callable[
        [analytics_admin.CreateMeasurementProtocolSecretRequest],
        resources.MeasurementProtocolSecret,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateMeasurementProtocolSecret(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_property(
        self,
    ) -> Callable[[analytics_admin.CreatePropertyRequest], resources.Property]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateProperty(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_account(
        self,
    ) -> Callable[[analytics_admin.DeleteAccountRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAccount(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_conversion_event(
        self,
    ) -> Callable[[analytics_admin.DeleteConversionEventRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteConversionEvent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_data_stream(
        self,
    ) -> Callable[[analytics_admin.DeleteDataStreamRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteDataStream(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_firebase_link(
        self,
    ) -> Callable[[analytics_admin.DeleteFirebaseLinkRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteFirebaseLink(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_google_ads_link(
        self,
    ) -> Callable[[analytics_admin.DeleteGoogleAdsLinkRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteGoogleAdsLink(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_measurement_protocol_secret(
        self,
    ) -> Callable[
        [analytics_admin.DeleteMeasurementProtocolSecretRequest], empty_pb2.Empty
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteMeasurementProtocolSecret(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_property(
        self,
    ) -> Callable[[analytics_admin.DeletePropertyRequest], resources.Property]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteProperty(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_account(
        self,
    ) -> Callable[[analytics_admin.GetAccountRequest], resources.Account]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAccount(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_conversion_event(
        self,
    ) -> Callable[
        [analytics_admin.GetConversionEventRequest], resources.ConversionEvent
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetConversionEvent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_custom_dimension(
        self,
    ) -> Callable[
        [analytics_admin.GetCustomDimensionRequest], resources.CustomDimension
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCustomDimension(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_custom_metric(
        self,
    ) -> Callable[[analytics_admin.GetCustomMetricRequest], resources.CustomMetric]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCustomMetric(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_data_retention_settings(
        self,
    ) -> Callable[
        [analytics_admin.GetDataRetentionSettingsRequest],
        resources.DataRetentionSettings,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDataRetentionSettings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_data_sharing_settings(
        self,
    ) -> Callable[
        [analytics_admin.GetDataSharingSettingsRequest], resources.DataSharingSettings
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDataSharingSettings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_data_stream(
        self,
    ) -> Callable[[analytics_admin.GetDataStreamRequest], resources.DataStream]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDataStream(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_measurement_protocol_secret(
        self,
    ) -> Callable[
        [analytics_admin.GetMeasurementProtocolSecretRequest],
        resources.MeasurementProtocolSecret,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetMeasurementProtocolSecret(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_property(
        self,
    ) -> Callable[[analytics_admin.GetPropertyRequest], resources.Property]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetProperty(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_accounts(
        self,
    ) -> Callable[
        [analytics_admin.ListAccountsRequest], analytics_admin.ListAccountsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAccounts(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_account_summaries(
        self,
    ) -> Callable[
        [analytics_admin.ListAccountSummariesRequest],
        analytics_admin.ListAccountSummariesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAccountSummaries(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_conversion_events(
        self,
    ) -> Callable[
        [analytics_admin.ListConversionEventsRequest],
        analytics_admin.ListConversionEventsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListConversionEvents(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_custom_dimensions(
        self,
    ) -> Callable[
        [analytics_admin.ListCustomDimensionsRequest],
        analytics_admin.ListCustomDimensionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCustomDimensions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_custom_metrics(
        self,
    ) -> Callable[
        [analytics_admin.ListCustomMetricsRequest],
        analytics_admin.ListCustomMetricsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCustomMetrics(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_data_streams(
        self,
    ) -> Callable[
        [analytics_admin.ListDataStreamsRequest],
        analytics_admin.ListDataStreamsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDataStreams(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_firebase_links(
        self,
    ) -> Callable[
        [analytics_admin.ListFirebaseLinksRequest],
        analytics_admin.ListFirebaseLinksResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListFirebaseLinks(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_google_ads_links(
        self,
    ) -> Callable[
        [analytics_admin.ListGoogleAdsLinksRequest],
        analytics_admin.ListGoogleAdsLinksResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListGoogleAdsLinks(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_measurement_protocol_secrets(
        self,
    ) -> Callable[
        [analytics_admin.ListMeasurementProtocolSecretsRequest],
        analytics_admin.ListMeasurementProtocolSecretsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListMeasurementProtocolSecrets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_properties(
        self,
    ) -> Callable[
        [analytics_admin.ListPropertiesRequest], analytics_admin.ListPropertiesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListProperties(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def provision_account_ticket(
        self,
    ) -> Callable[
        [analytics_admin.ProvisionAccountTicketRequest],
        analytics_admin.ProvisionAccountTicketResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ProvisionAccountTicket(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def search_change_history_events(
        self,
    ) -> Callable[
        [analytics_admin.SearchChangeHistoryEventsRequest],
        analytics_admin.SearchChangeHistoryEventsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SearchChangeHistoryEvents(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_account(
        self,
    ) -> Callable[[analytics_admin.UpdateAccountRequest], resources.Account]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAccount(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_custom_dimension(
        self,
    ) -> Callable[
        [analytics_admin.UpdateCustomDimensionRequest], resources.CustomDimension
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCustomDimension(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_custom_metric(
        self,
    ) -> Callable[[analytics_admin.UpdateCustomMetricRequest], resources.CustomMetric]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCustomMetric(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_data_retention_settings(
        self,
    ) -> Callable[
        [analytics_admin.UpdateDataRetentionSettingsRequest],
        resources.DataRetentionSettings,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateDataRetentionSettings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_data_stream(
        self,
    ) -> Callable[[analytics_admin.UpdateDataStreamRequest], resources.DataStream]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateDataStream(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_google_ads_link(
        self,
    ) -> Callable[
        [analytics_admin.UpdateGoogleAdsLinkRequest], resources.GoogleAdsLink
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateGoogleAdsLink(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_measurement_protocol_secret(
        self,
    ) -> Callable[
        [analytics_admin.UpdateMeasurementProtocolSecretRequest],
        resources.MeasurementProtocolSecret,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateMeasurementProtocolSecret(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_property(
        self,
    ) -> Callable[[analytics_admin.UpdatePropertyRequest], resources.Property]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateProperty(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("AnalyticsAdminServiceRestTransport",)
