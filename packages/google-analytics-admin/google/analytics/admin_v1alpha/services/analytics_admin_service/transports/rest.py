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

import dataclasses
import json  # type: ignore
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
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
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.protobuf import empty_pb2  # type: ignore

from google.analytics.admin_v1alpha.types import channel_group as gaa_channel_group
from google.analytics.admin_v1alpha.types import (
    expanded_data_set as gaa_expanded_data_set,
)
from google.analytics.admin_v1alpha.types import (
    subproperty_event_filter as gaa_subproperty_event_filter,
)
from google.analytics.admin_v1alpha.types import analytics_admin
from google.analytics.admin_v1alpha.types import audience
from google.analytics.admin_v1alpha.types import audience as gaa_audience
from google.analytics.admin_v1alpha.types import channel_group
from google.analytics.admin_v1alpha.types import event_create_and_edit
from google.analytics.admin_v1alpha.types import expanded_data_set
from google.analytics.admin_v1alpha.types import resources
from google.analytics.admin_v1alpha.types import subproperty_event_filter

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
            def pre_acknowledge_user_data_collection(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_acknowledge_user_data_collection(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_approve_display_video360_advertiser_link_proposal(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_approve_display_video360_advertiser_link_proposal(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_archive_audience(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_archive_custom_dimension(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_archive_custom_metric(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_batch_create_access_bindings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_create_access_bindings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_batch_delete_access_bindings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_batch_get_access_bindings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_get_access_bindings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_batch_update_access_bindings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_update_access_bindings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_cancel_display_video360_advertiser_link_proposal(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_cancel_display_video360_advertiser_link_proposal(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_access_binding(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_access_binding(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_ad_sense_link(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_ad_sense_link(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_audience(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_audience(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_calculated_metric(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_calculated_metric(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_channel_group(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_channel_group(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_connected_site_tag(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_connected_site_tag(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_conversion_event(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_conversion_event(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_custom_dimension(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_custom_dimension(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_custom_metric(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_custom_metric(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_data_stream(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_data_stream(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_display_video360_advertiser_link(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_display_video360_advertiser_link(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_display_video360_advertiser_link_proposal(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_display_video360_advertiser_link_proposal(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_event_create_rule(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_event_create_rule(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_expanded_data_set(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_expanded_data_set(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_firebase_link(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_firebase_link(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_google_ads_link(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_google_ads_link(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_measurement_protocol_secret(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_measurement_protocol_secret(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_property(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_property(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_rollup_property(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_rollup_property(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_rollup_property_source_link(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_rollup_property_source_link(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_search_ads360_link(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_search_ads360_link(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_sk_ad_network_conversion_value_schema(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_sk_ad_network_conversion_value_schema(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_subproperty(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_subproperty(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_subproperty_event_filter(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_subproperty_event_filter(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_access_binding(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_account(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_ad_sense_link(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_calculated_metric(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_channel_group(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_connected_site_tag(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_conversion_event(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_data_stream(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_display_video360_advertiser_link(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_display_video360_advertiser_link_proposal(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_event_create_rule(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_expanded_data_set(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_firebase_link(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_google_ads_link(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_measurement_protocol_secret(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_property(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_property(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_rollup_property_source_link(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_search_ads360_link(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_sk_ad_network_conversion_value_schema(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_subproperty_event_filter(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_fetch_automated_ga4_configuration_opt_out(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_fetch_automated_ga4_configuration_opt_out(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_fetch_connected_ga4_property(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_fetch_connected_ga4_property(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_access_binding(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_access_binding(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_account(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_account(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_ad_sense_link(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_ad_sense_link(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_attribution_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_attribution_settings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_audience(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_audience(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_big_query_link(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_big_query_link(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_calculated_metric(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_calculated_metric(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_channel_group(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_channel_group(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_conversion_event(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_conversion_event(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_custom_dimension(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_custom_dimension(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_custom_metric(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_custom_metric(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_data_redaction_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_data_redaction_settings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_data_retention_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_data_retention_settings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_data_sharing_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_data_sharing_settings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_data_stream(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_data_stream(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_display_video360_advertiser_link(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_display_video360_advertiser_link(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_display_video360_advertiser_link_proposal(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_display_video360_advertiser_link_proposal(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_enhanced_measurement_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_enhanced_measurement_settings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_event_create_rule(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_event_create_rule(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_expanded_data_set(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_expanded_data_set(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_global_site_tag(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_global_site_tag(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_google_signals_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_google_signals_settings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_measurement_protocol_secret(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_measurement_protocol_secret(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_property(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_property(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_rollup_property_source_link(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_rollup_property_source_link(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_search_ads360_link(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_search_ads360_link(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_sk_ad_network_conversion_value_schema(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_sk_ad_network_conversion_value_schema(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_subproperty_event_filter(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_subproperty_event_filter(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_access_bindings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_access_bindings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_accounts(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_accounts(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_account_summaries(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_account_summaries(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_ad_sense_links(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_ad_sense_links(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_audiences(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_audiences(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_big_query_links(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_big_query_links(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_calculated_metrics(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_calculated_metrics(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_channel_groups(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_channel_groups(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_connected_site_tags(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_connected_site_tags(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_conversion_events(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_conversion_events(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_custom_dimensions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_custom_dimensions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_custom_metrics(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_custom_metrics(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_data_streams(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_data_streams(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_display_video360_advertiser_link_proposals(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_display_video360_advertiser_link_proposals(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_display_video360_advertiser_links(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_display_video360_advertiser_links(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_event_create_rules(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_event_create_rules(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_expanded_data_sets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_expanded_data_sets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_firebase_links(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_firebase_links(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_google_ads_links(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_google_ads_links(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_measurement_protocol_secrets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_measurement_protocol_secrets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_properties(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_properties(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_rollup_property_source_links(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_rollup_property_source_links(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_search_ads360_links(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_search_ads360_links(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_sk_ad_network_conversion_value_schemas(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_sk_ad_network_conversion_value_schemas(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_subproperty_event_filters(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_subproperty_event_filters(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_provision_account_ticket(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_provision_account_ticket(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_run_access_report(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_run_access_report(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_search_change_history_events(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_search_change_history_events(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_automated_ga4_configuration_opt_out(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_automated_ga4_configuration_opt_out(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_access_binding(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_access_binding(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_account(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_account(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_attribution_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_attribution_settings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_audience(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_audience(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_calculated_metric(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_calculated_metric(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_channel_group(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_channel_group(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_conversion_event(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_conversion_event(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_custom_dimension(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_custom_dimension(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_custom_metric(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_custom_metric(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_data_redaction_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_data_redaction_settings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_data_retention_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_data_retention_settings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_data_stream(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_data_stream(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_display_video360_advertiser_link(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_display_video360_advertiser_link(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_enhanced_measurement_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_enhanced_measurement_settings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_event_create_rule(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_event_create_rule(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_expanded_data_set(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_expanded_data_set(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_google_ads_link(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_google_ads_link(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_google_signals_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_google_signals_settings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_measurement_protocol_secret(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_measurement_protocol_secret(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_property(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_property(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_search_ads360_link(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_search_ads360_link(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_sk_ad_network_conversion_value_schema(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_sk_ad_network_conversion_value_schema(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_subproperty_event_filter(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_subproperty_event_filter(self, response):
                logging.log(f"Received response: {response}")
                return response

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

    def pre_approve_display_video360_advertiser_link_proposal(
        self,
        request: analytics_admin.ApproveDisplayVideo360AdvertiserLinkProposalRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.ApproveDisplayVideo360AdvertiserLinkProposalRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for approve_display_video360_advertiser_link_proposal

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_approve_display_video360_advertiser_link_proposal(
        self,
        response: analytics_admin.ApproveDisplayVideo360AdvertiserLinkProposalResponse,
    ) -> analytics_admin.ApproveDisplayVideo360AdvertiserLinkProposalResponse:
        """Post-rpc interceptor for approve_display_video360_advertiser_link_proposal

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_archive_audience(
        self,
        request: analytics_admin.ArchiveAudienceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.ArchiveAudienceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for archive_audience

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

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

    def pre_batch_create_access_bindings(
        self,
        request: analytics_admin.BatchCreateAccessBindingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.BatchCreateAccessBindingsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for batch_create_access_bindings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_batch_create_access_bindings(
        self, response: analytics_admin.BatchCreateAccessBindingsResponse
    ) -> analytics_admin.BatchCreateAccessBindingsResponse:
        """Post-rpc interceptor for batch_create_access_bindings

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_batch_delete_access_bindings(
        self,
        request: analytics_admin.BatchDeleteAccessBindingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.BatchDeleteAccessBindingsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for batch_delete_access_bindings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def pre_batch_get_access_bindings(
        self,
        request: analytics_admin.BatchGetAccessBindingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.BatchGetAccessBindingsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for batch_get_access_bindings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_batch_get_access_bindings(
        self, response: analytics_admin.BatchGetAccessBindingsResponse
    ) -> analytics_admin.BatchGetAccessBindingsResponse:
        """Post-rpc interceptor for batch_get_access_bindings

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_batch_update_access_bindings(
        self,
        request: analytics_admin.BatchUpdateAccessBindingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.BatchUpdateAccessBindingsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for batch_update_access_bindings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_batch_update_access_bindings(
        self, response: analytics_admin.BatchUpdateAccessBindingsResponse
    ) -> analytics_admin.BatchUpdateAccessBindingsResponse:
        """Post-rpc interceptor for batch_update_access_bindings

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_display_video360_advertiser_link_proposal(
        self,
        request: analytics_admin.CancelDisplayVideo360AdvertiserLinkProposalRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.CancelDisplayVideo360AdvertiserLinkProposalRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for cancel_display_video360_advertiser_link_proposal

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_cancel_display_video360_advertiser_link_proposal(
        self, response: resources.DisplayVideo360AdvertiserLinkProposal
    ) -> resources.DisplayVideo360AdvertiserLinkProposal:
        """Post-rpc interceptor for cancel_display_video360_advertiser_link_proposal

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_create_access_binding(
        self,
        request: analytics_admin.CreateAccessBindingRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.CreateAccessBindingRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_access_binding

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_create_access_binding(
        self, response: resources.AccessBinding
    ) -> resources.AccessBinding:
        """Post-rpc interceptor for create_access_binding

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_create_ad_sense_link(
        self,
        request: analytics_admin.CreateAdSenseLinkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.CreateAdSenseLinkRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_ad_sense_link

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_create_ad_sense_link(
        self, response: resources.AdSenseLink
    ) -> resources.AdSenseLink:
        """Post-rpc interceptor for create_ad_sense_link

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_create_audience(
        self,
        request: analytics_admin.CreateAudienceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.CreateAudienceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_audience

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_create_audience(
        self, response: gaa_audience.Audience
    ) -> gaa_audience.Audience:
        """Post-rpc interceptor for create_audience

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_create_calculated_metric(
        self,
        request: analytics_admin.CreateCalculatedMetricRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.CreateCalculatedMetricRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_calculated_metric

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_create_calculated_metric(
        self, response: resources.CalculatedMetric
    ) -> resources.CalculatedMetric:
        """Post-rpc interceptor for create_calculated_metric

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_create_channel_group(
        self,
        request: analytics_admin.CreateChannelGroupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.CreateChannelGroupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_channel_group

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_create_channel_group(
        self, response: gaa_channel_group.ChannelGroup
    ) -> gaa_channel_group.ChannelGroup:
        """Post-rpc interceptor for create_channel_group

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_create_connected_site_tag(
        self,
        request: analytics_admin.CreateConnectedSiteTagRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.CreateConnectedSiteTagRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_connected_site_tag

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_create_connected_site_tag(
        self, response: analytics_admin.CreateConnectedSiteTagResponse
    ) -> analytics_admin.CreateConnectedSiteTagResponse:
        """Post-rpc interceptor for create_connected_site_tag

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

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

    def pre_create_display_video360_advertiser_link(
        self,
        request: analytics_admin.CreateDisplayVideo360AdvertiserLinkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.CreateDisplayVideo360AdvertiserLinkRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for create_display_video360_advertiser_link

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_create_display_video360_advertiser_link(
        self, response: resources.DisplayVideo360AdvertiserLink
    ) -> resources.DisplayVideo360AdvertiserLink:
        """Post-rpc interceptor for create_display_video360_advertiser_link

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_create_display_video360_advertiser_link_proposal(
        self,
        request: analytics_admin.CreateDisplayVideo360AdvertiserLinkProposalRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.CreateDisplayVideo360AdvertiserLinkProposalRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for create_display_video360_advertiser_link_proposal

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_create_display_video360_advertiser_link_proposal(
        self, response: resources.DisplayVideo360AdvertiserLinkProposal
    ) -> resources.DisplayVideo360AdvertiserLinkProposal:
        """Post-rpc interceptor for create_display_video360_advertiser_link_proposal

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_create_event_create_rule(
        self,
        request: analytics_admin.CreateEventCreateRuleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.CreateEventCreateRuleRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_event_create_rule

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_create_event_create_rule(
        self, response: event_create_and_edit.EventCreateRule
    ) -> event_create_and_edit.EventCreateRule:
        """Post-rpc interceptor for create_event_create_rule

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_create_expanded_data_set(
        self,
        request: analytics_admin.CreateExpandedDataSetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.CreateExpandedDataSetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_expanded_data_set

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_create_expanded_data_set(
        self, response: gaa_expanded_data_set.ExpandedDataSet
    ) -> gaa_expanded_data_set.ExpandedDataSet:
        """Post-rpc interceptor for create_expanded_data_set

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

    def pre_create_rollup_property(
        self,
        request: analytics_admin.CreateRollupPropertyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.CreateRollupPropertyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_rollup_property

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_create_rollup_property(
        self, response: analytics_admin.CreateRollupPropertyResponse
    ) -> analytics_admin.CreateRollupPropertyResponse:
        """Post-rpc interceptor for create_rollup_property

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_create_rollup_property_source_link(
        self,
        request: analytics_admin.CreateRollupPropertySourceLinkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.CreateRollupPropertySourceLinkRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_rollup_property_source_link

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_create_rollup_property_source_link(
        self, response: resources.RollupPropertySourceLink
    ) -> resources.RollupPropertySourceLink:
        """Post-rpc interceptor for create_rollup_property_source_link

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_create_search_ads360_link(
        self,
        request: analytics_admin.CreateSearchAds360LinkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.CreateSearchAds360LinkRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_search_ads360_link

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_create_search_ads360_link(
        self, response: resources.SearchAds360Link
    ) -> resources.SearchAds360Link:
        """Post-rpc interceptor for create_search_ads360_link

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_create_sk_ad_network_conversion_value_schema(
        self,
        request: analytics_admin.CreateSKAdNetworkConversionValueSchemaRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.CreateSKAdNetworkConversionValueSchemaRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for create_sk_ad_network_conversion_value_schema

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_create_sk_ad_network_conversion_value_schema(
        self, response: resources.SKAdNetworkConversionValueSchema
    ) -> resources.SKAdNetworkConversionValueSchema:
        """Post-rpc interceptor for create_sk_ad_network_conversion_value_schema

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_create_subproperty(
        self,
        request: analytics_admin.CreateSubpropertyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.CreateSubpropertyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_subproperty

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_create_subproperty(
        self, response: analytics_admin.CreateSubpropertyResponse
    ) -> analytics_admin.CreateSubpropertyResponse:
        """Post-rpc interceptor for create_subproperty

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_create_subproperty_event_filter(
        self,
        request: analytics_admin.CreateSubpropertyEventFilterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.CreateSubpropertyEventFilterRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_subproperty_event_filter

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_create_subproperty_event_filter(
        self, response: gaa_subproperty_event_filter.SubpropertyEventFilter
    ) -> gaa_subproperty_event_filter.SubpropertyEventFilter:
        """Post-rpc interceptor for create_subproperty_event_filter

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_access_binding(
        self,
        request: analytics_admin.DeleteAccessBindingRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.DeleteAccessBindingRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_access_binding

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

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

    def pre_delete_ad_sense_link(
        self,
        request: analytics_admin.DeleteAdSenseLinkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.DeleteAdSenseLinkRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_ad_sense_link

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def pre_delete_calculated_metric(
        self,
        request: analytics_admin.DeleteCalculatedMetricRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.DeleteCalculatedMetricRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_calculated_metric

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def pre_delete_channel_group(
        self,
        request: analytics_admin.DeleteChannelGroupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.DeleteChannelGroupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_channel_group

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def pre_delete_connected_site_tag(
        self,
        request: analytics_admin.DeleteConnectedSiteTagRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.DeleteConnectedSiteTagRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_connected_site_tag

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

    def pre_delete_display_video360_advertiser_link(
        self,
        request: analytics_admin.DeleteDisplayVideo360AdvertiserLinkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.DeleteDisplayVideo360AdvertiserLinkRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for delete_display_video360_advertiser_link

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def pre_delete_display_video360_advertiser_link_proposal(
        self,
        request: analytics_admin.DeleteDisplayVideo360AdvertiserLinkProposalRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.DeleteDisplayVideo360AdvertiserLinkProposalRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for delete_display_video360_advertiser_link_proposal

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def pre_delete_event_create_rule(
        self,
        request: analytics_admin.DeleteEventCreateRuleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.DeleteEventCreateRuleRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_event_create_rule

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def pre_delete_expanded_data_set(
        self,
        request: analytics_admin.DeleteExpandedDataSetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.DeleteExpandedDataSetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_expanded_data_set

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

    def pre_delete_rollup_property_source_link(
        self,
        request: analytics_admin.DeleteRollupPropertySourceLinkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.DeleteRollupPropertySourceLinkRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_rollup_property_source_link

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def pre_delete_search_ads360_link(
        self,
        request: analytics_admin.DeleteSearchAds360LinkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.DeleteSearchAds360LinkRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_search_ads360_link

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def pre_delete_sk_ad_network_conversion_value_schema(
        self,
        request: analytics_admin.DeleteSKAdNetworkConversionValueSchemaRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.DeleteSKAdNetworkConversionValueSchemaRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for delete_sk_ad_network_conversion_value_schema

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def pre_delete_subproperty_event_filter(
        self,
        request: analytics_admin.DeleteSubpropertyEventFilterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.DeleteSubpropertyEventFilterRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_subproperty_event_filter

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def pre_fetch_automated_ga4_configuration_opt_out(
        self,
        request: analytics_admin.FetchAutomatedGa4ConfigurationOptOutRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.FetchAutomatedGa4ConfigurationOptOutRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for fetch_automated_ga4_configuration_opt_out

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_fetch_automated_ga4_configuration_opt_out(
        self, response: analytics_admin.FetchAutomatedGa4ConfigurationOptOutResponse
    ) -> analytics_admin.FetchAutomatedGa4ConfigurationOptOutResponse:
        """Post-rpc interceptor for fetch_automated_ga4_configuration_opt_out

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_fetch_connected_ga4_property(
        self,
        request: analytics_admin.FetchConnectedGa4PropertyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.FetchConnectedGa4PropertyRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for fetch_connected_ga4_property

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_fetch_connected_ga4_property(
        self, response: analytics_admin.FetchConnectedGa4PropertyResponse
    ) -> analytics_admin.FetchConnectedGa4PropertyResponse:
        """Post-rpc interceptor for fetch_connected_ga4_property

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_get_access_binding(
        self,
        request: analytics_admin.GetAccessBindingRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.GetAccessBindingRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_access_binding

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_get_access_binding(
        self, response: resources.AccessBinding
    ) -> resources.AccessBinding:
        """Post-rpc interceptor for get_access_binding

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

    def pre_get_ad_sense_link(
        self,
        request: analytics_admin.GetAdSenseLinkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.GetAdSenseLinkRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_ad_sense_link

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_get_ad_sense_link(
        self, response: resources.AdSenseLink
    ) -> resources.AdSenseLink:
        """Post-rpc interceptor for get_ad_sense_link

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_get_attribution_settings(
        self,
        request: analytics_admin.GetAttributionSettingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.GetAttributionSettingsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_attribution_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_get_attribution_settings(
        self, response: resources.AttributionSettings
    ) -> resources.AttributionSettings:
        """Post-rpc interceptor for get_attribution_settings

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_get_audience(
        self,
        request: analytics_admin.GetAudienceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.GetAudienceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_audience

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_get_audience(self, response: audience.Audience) -> audience.Audience:
        """Post-rpc interceptor for get_audience

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_get_big_query_link(
        self,
        request: analytics_admin.GetBigQueryLinkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.GetBigQueryLinkRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_big_query_link

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_get_big_query_link(
        self, response: resources.BigQueryLink
    ) -> resources.BigQueryLink:
        """Post-rpc interceptor for get_big_query_link

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_get_calculated_metric(
        self,
        request: analytics_admin.GetCalculatedMetricRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.GetCalculatedMetricRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_calculated_metric

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_get_calculated_metric(
        self, response: resources.CalculatedMetric
    ) -> resources.CalculatedMetric:
        """Post-rpc interceptor for get_calculated_metric

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_get_channel_group(
        self,
        request: analytics_admin.GetChannelGroupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.GetChannelGroupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_channel_group

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_get_channel_group(
        self, response: channel_group.ChannelGroup
    ) -> channel_group.ChannelGroup:
        """Post-rpc interceptor for get_channel_group

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

    def pre_get_data_redaction_settings(
        self,
        request: analytics_admin.GetDataRedactionSettingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.GetDataRedactionSettingsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_data_redaction_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_get_data_redaction_settings(
        self, response: resources.DataRedactionSettings
    ) -> resources.DataRedactionSettings:
        """Post-rpc interceptor for get_data_redaction_settings

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

    def pre_get_display_video360_advertiser_link(
        self,
        request: analytics_admin.GetDisplayVideo360AdvertiserLinkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.GetDisplayVideo360AdvertiserLinkRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for get_display_video360_advertiser_link

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_get_display_video360_advertiser_link(
        self, response: resources.DisplayVideo360AdvertiserLink
    ) -> resources.DisplayVideo360AdvertiserLink:
        """Post-rpc interceptor for get_display_video360_advertiser_link

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_get_display_video360_advertiser_link_proposal(
        self,
        request: analytics_admin.GetDisplayVideo360AdvertiserLinkProposalRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.GetDisplayVideo360AdvertiserLinkProposalRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for get_display_video360_advertiser_link_proposal

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_get_display_video360_advertiser_link_proposal(
        self, response: resources.DisplayVideo360AdvertiserLinkProposal
    ) -> resources.DisplayVideo360AdvertiserLinkProposal:
        """Post-rpc interceptor for get_display_video360_advertiser_link_proposal

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_get_enhanced_measurement_settings(
        self,
        request: analytics_admin.GetEnhancedMeasurementSettingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.GetEnhancedMeasurementSettingsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_enhanced_measurement_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_get_enhanced_measurement_settings(
        self, response: resources.EnhancedMeasurementSettings
    ) -> resources.EnhancedMeasurementSettings:
        """Post-rpc interceptor for get_enhanced_measurement_settings

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_get_event_create_rule(
        self,
        request: analytics_admin.GetEventCreateRuleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.GetEventCreateRuleRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_event_create_rule

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_get_event_create_rule(
        self, response: event_create_and_edit.EventCreateRule
    ) -> event_create_and_edit.EventCreateRule:
        """Post-rpc interceptor for get_event_create_rule

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_get_expanded_data_set(
        self,
        request: analytics_admin.GetExpandedDataSetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.GetExpandedDataSetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_expanded_data_set

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_get_expanded_data_set(
        self, response: expanded_data_set.ExpandedDataSet
    ) -> expanded_data_set.ExpandedDataSet:
        """Post-rpc interceptor for get_expanded_data_set

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_get_global_site_tag(
        self,
        request: analytics_admin.GetGlobalSiteTagRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.GetGlobalSiteTagRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_global_site_tag

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_get_global_site_tag(
        self, response: resources.GlobalSiteTag
    ) -> resources.GlobalSiteTag:
        """Post-rpc interceptor for get_global_site_tag

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_get_google_signals_settings(
        self,
        request: analytics_admin.GetGoogleSignalsSettingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.GetGoogleSignalsSettingsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_google_signals_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_get_google_signals_settings(
        self, response: resources.GoogleSignalsSettings
    ) -> resources.GoogleSignalsSettings:
        """Post-rpc interceptor for get_google_signals_settings

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

    def pre_get_rollup_property_source_link(
        self,
        request: analytics_admin.GetRollupPropertySourceLinkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.GetRollupPropertySourceLinkRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_rollup_property_source_link

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_get_rollup_property_source_link(
        self, response: resources.RollupPropertySourceLink
    ) -> resources.RollupPropertySourceLink:
        """Post-rpc interceptor for get_rollup_property_source_link

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_get_search_ads360_link(
        self,
        request: analytics_admin.GetSearchAds360LinkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.GetSearchAds360LinkRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_search_ads360_link

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_get_search_ads360_link(
        self, response: resources.SearchAds360Link
    ) -> resources.SearchAds360Link:
        """Post-rpc interceptor for get_search_ads360_link

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_get_sk_ad_network_conversion_value_schema(
        self,
        request: analytics_admin.GetSKAdNetworkConversionValueSchemaRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.GetSKAdNetworkConversionValueSchemaRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for get_sk_ad_network_conversion_value_schema

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_get_sk_ad_network_conversion_value_schema(
        self, response: resources.SKAdNetworkConversionValueSchema
    ) -> resources.SKAdNetworkConversionValueSchema:
        """Post-rpc interceptor for get_sk_ad_network_conversion_value_schema

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_get_subproperty_event_filter(
        self,
        request: analytics_admin.GetSubpropertyEventFilterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.GetSubpropertyEventFilterRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_subproperty_event_filter

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_get_subproperty_event_filter(
        self, response: subproperty_event_filter.SubpropertyEventFilter
    ) -> subproperty_event_filter.SubpropertyEventFilter:
        """Post-rpc interceptor for get_subproperty_event_filter

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_list_access_bindings(
        self,
        request: analytics_admin.ListAccessBindingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.ListAccessBindingsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_access_bindings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_list_access_bindings(
        self, response: analytics_admin.ListAccessBindingsResponse
    ) -> analytics_admin.ListAccessBindingsResponse:
        """Post-rpc interceptor for list_access_bindings

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

    def pre_list_ad_sense_links(
        self,
        request: analytics_admin.ListAdSenseLinksRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.ListAdSenseLinksRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_ad_sense_links

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_list_ad_sense_links(
        self, response: analytics_admin.ListAdSenseLinksResponse
    ) -> analytics_admin.ListAdSenseLinksResponse:
        """Post-rpc interceptor for list_ad_sense_links

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_list_audiences(
        self,
        request: analytics_admin.ListAudiencesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.ListAudiencesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_audiences

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_list_audiences(
        self, response: analytics_admin.ListAudiencesResponse
    ) -> analytics_admin.ListAudiencesResponse:
        """Post-rpc interceptor for list_audiences

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_list_big_query_links(
        self,
        request: analytics_admin.ListBigQueryLinksRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.ListBigQueryLinksRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_big_query_links

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_list_big_query_links(
        self, response: analytics_admin.ListBigQueryLinksResponse
    ) -> analytics_admin.ListBigQueryLinksResponse:
        """Post-rpc interceptor for list_big_query_links

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_list_calculated_metrics(
        self,
        request: analytics_admin.ListCalculatedMetricsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.ListCalculatedMetricsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_calculated_metrics

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_list_calculated_metrics(
        self, response: analytics_admin.ListCalculatedMetricsResponse
    ) -> analytics_admin.ListCalculatedMetricsResponse:
        """Post-rpc interceptor for list_calculated_metrics

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_list_channel_groups(
        self,
        request: analytics_admin.ListChannelGroupsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.ListChannelGroupsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_channel_groups

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_list_channel_groups(
        self, response: analytics_admin.ListChannelGroupsResponse
    ) -> analytics_admin.ListChannelGroupsResponse:
        """Post-rpc interceptor for list_channel_groups

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_list_connected_site_tags(
        self,
        request: analytics_admin.ListConnectedSiteTagsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.ListConnectedSiteTagsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_connected_site_tags

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_list_connected_site_tags(
        self, response: analytics_admin.ListConnectedSiteTagsResponse
    ) -> analytics_admin.ListConnectedSiteTagsResponse:
        """Post-rpc interceptor for list_connected_site_tags

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

    def pre_list_display_video360_advertiser_link_proposals(
        self,
        request: analytics_admin.ListDisplayVideo360AdvertiserLinkProposalsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.ListDisplayVideo360AdvertiserLinkProposalsRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for list_display_video360_advertiser_link_proposals

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_list_display_video360_advertiser_link_proposals(
        self,
        response: analytics_admin.ListDisplayVideo360AdvertiserLinkProposalsResponse,
    ) -> analytics_admin.ListDisplayVideo360AdvertiserLinkProposalsResponse:
        """Post-rpc interceptor for list_display_video360_advertiser_link_proposals

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_list_display_video360_advertiser_links(
        self,
        request: analytics_admin.ListDisplayVideo360AdvertiserLinksRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.ListDisplayVideo360AdvertiserLinksRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for list_display_video360_advertiser_links

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_list_display_video360_advertiser_links(
        self, response: analytics_admin.ListDisplayVideo360AdvertiserLinksResponse
    ) -> analytics_admin.ListDisplayVideo360AdvertiserLinksResponse:
        """Post-rpc interceptor for list_display_video360_advertiser_links

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_list_event_create_rules(
        self,
        request: analytics_admin.ListEventCreateRulesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.ListEventCreateRulesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_event_create_rules

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_list_event_create_rules(
        self, response: analytics_admin.ListEventCreateRulesResponse
    ) -> analytics_admin.ListEventCreateRulesResponse:
        """Post-rpc interceptor for list_event_create_rules

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_list_expanded_data_sets(
        self,
        request: analytics_admin.ListExpandedDataSetsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.ListExpandedDataSetsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_expanded_data_sets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_list_expanded_data_sets(
        self, response: analytics_admin.ListExpandedDataSetsResponse
    ) -> analytics_admin.ListExpandedDataSetsResponse:
        """Post-rpc interceptor for list_expanded_data_sets

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

    def pre_list_rollup_property_source_links(
        self,
        request: analytics_admin.ListRollupPropertySourceLinksRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.ListRollupPropertySourceLinksRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_rollup_property_source_links

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_list_rollup_property_source_links(
        self, response: analytics_admin.ListRollupPropertySourceLinksResponse
    ) -> analytics_admin.ListRollupPropertySourceLinksResponse:
        """Post-rpc interceptor for list_rollup_property_source_links

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_list_search_ads360_links(
        self,
        request: analytics_admin.ListSearchAds360LinksRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.ListSearchAds360LinksRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_search_ads360_links

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_list_search_ads360_links(
        self, response: analytics_admin.ListSearchAds360LinksResponse
    ) -> analytics_admin.ListSearchAds360LinksResponse:
        """Post-rpc interceptor for list_search_ads360_links

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_list_sk_ad_network_conversion_value_schemas(
        self,
        request: analytics_admin.ListSKAdNetworkConversionValueSchemasRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.ListSKAdNetworkConversionValueSchemasRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for list_sk_ad_network_conversion_value_schemas

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_list_sk_ad_network_conversion_value_schemas(
        self, response: analytics_admin.ListSKAdNetworkConversionValueSchemasResponse
    ) -> analytics_admin.ListSKAdNetworkConversionValueSchemasResponse:
        """Post-rpc interceptor for list_sk_ad_network_conversion_value_schemas

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_list_subproperty_event_filters(
        self,
        request: analytics_admin.ListSubpropertyEventFiltersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.ListSubpropertyEventFiltersRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_subproperty_event_filters

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_list_subproperty_event_filters(
        self, response: analytics_admin.ListSubpropertyEventFiltersResponse
    ) -> analytics_admin.ListSubpropertyEventFiltersResponse:
        """Post-rpc interceptor for list_subproperty_event_filters

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

    def pre_run_access_report(
        self,
        request: analytics_admin.RunAccessReportRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.RunAccessReportRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for run_access_report

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_run_access_report(
        self, response: analytics_admin.RunAccessReportResponse
    ) -> analytics_admin.RunAccessReportResponse:
        """Post-rpc interceptor for run_access_report

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

    def pre_set_automated_ga4_configuration_opt_out(
        self,
        request: analytics_admin.SetAutomatedGa4ConfigurationOptOutRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.SetAutomatedGa4ConfigurationOptOutRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for set_automated_ga4_configuration_opt_out

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_set_automated_ga4_configuration_opt_out(
        self, response: analytics_admin.SetAutomatedGa4ConfigurationOptOutResponse
    ) -> analytics_admin.SetAutomatedGa4ConfigurationOptOutResponse:
        """Post-rpc interceptor for set_automated_ga4_configuration_opt_out

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_update_access_binding(
        self,
        request: analytics_admin.UpdateAccessBindingRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.UpdateAccessBindingRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_access_binding

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_update_access_binding(
        self, response: resources.AccessBinding
    ) -> resources.AccessBinding:
        """Post-rpc interceptor for update_access_binding

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

    def pre_update_attribution_settings(
        self,
        request: analytics_admin.UpdateAttributionSettingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.UpdateAttributionSettingsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_attribution_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_update_attribution_settings(
        self, response: resources.AttributionSettings
    ) -> resources.AttributionSettings:
        """Post-rpc interceptor for update_attribution_settings

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_update_audience(
        self,
        request: analytics_admin.UpdateAudienceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.UpdateAudienceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_audience

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_update_audience(
        self, response: gaa_audience.Audience
    ) -> gaa_audience.Audience:
        """Post-rpc interceptor for update_audience

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_update_calculated_metric(
        self,
        request: analytics_admin.UpdateCalculatedMetricRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.UpdateCalculatedMetricRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_calculated_metric

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_update_calculated_metric(
        self, response: resources.CalculatedMetric
    ) -> resources.CalculatedMetric:
        """Post-rpc interceptor for update_calculated_metric

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_update_channel_group(
        self,
        request: analytics_admin.UpdateChannelGroupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.UpdateChannelGroupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_channel_group

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_update_channel_group(
        self, response: gaa_channel_group.ChannelGroup
    ) -> gaa_channel_group.ChannelGroup:
        """Post-rpc interceptor for update_channel_group

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_update_conversion_event(
        self,
        request: analytics_admin.UpdateConversionEventRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.UpdateConversionEventRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_conversion_event

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_update_conversion_event(
        self, response: resources.ConversionEvent
    ) -> resources.ConversionEvent:
        """Post-rpc interceptor for update_conversion_event

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

    def pre_update_data_redaction_settings(
        self,
        request: analytics_admin.UpdateDataRedactionSettingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.UpdateDataRedactionSettingsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_data_redaction_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_update_data_redaction_settings(
        self, response: resources.DataRedactionSettings
    ) -> resources.DataRedactionSettings:
        """Post-rpc interceptor for update_data_redaction_settings

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

    def pre_update_display_video360_advertiser_link(
        self,
        request: analytics_admin.UpdateDisplayVideo360AdvertiserLinkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.UpdateDisplayVideo360AdvertiserLinkRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for update_display_video360_advertiser_link

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_update_display_video360_advertiser_link(
        self, response: resources.DisplayVideo360AdvertiserLink
    ) -> resources.DisplayVideo360AdvertiserLink:
        """Post-rpc interceptor for update_display_video360_advertiser_link

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_update_enhanced_measurement_settings(
        self,
        request: analytics_admin.UpdateEnhancedMeasurementSettingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.UpdateEnhancedMeasurementSettingsRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for update_enhanced_measurement_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_update_enhanced_measurement_settings(
        self, response: resources.EnhancedMeasurementSettings
    ) -> resources.EnhancedMeasurementSettings:
        """Post-rpc interceptor for update_enhanced_measurement_settings

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_update_event_create_rule(
        self,
        request: analytics_admin.UpdateEventCreateRuleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.UpdateEventCreateRuleRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_event_create_rule

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_update_event_create_rule(
        self, response: event_create_and_edit.EventCreateRule
    ) -> event_create_and_edit.EventCreateRule:
        """Post-rpc interceptor for update_event_create_rule

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_update_expanded_data_set(
        self,
        request: analytics_admin.UpdateExpandedDataSetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[analytics_admin.UpdateExpandedDataSetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_expanded_data_set

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_update_expanded_data_set(
        self, response: gaa_expanded_data_set.ExpandedDataSet
    ) -> gaa_expanded_data_set.ExpandedDataSet:
        """Post-rpc interceptor for update_expanded_data_set

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

    def pre_update_google_signals_settings(
        self,
        request: analytics_admin.UpdateGoogleSignalsSettingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.UpdateGoogleSignalsSettingsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_google_signals_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_update_google_signals_settings(
        self, response: resources.GoogleSignalsSettings
    ) -> resources.GoogleSignalsSettings:
        """Post-rpc interceptor for update_google_signals_settings

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

    def pre_update_search_ads360_link(
        self,
        request: analytics_admin.UpdateSearchAds360LinkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.UpdateSearchAds360LinkRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_search_ads360_link

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_update_search_ads360_link(
        self, response: resources.SearchAds360Link
    ) -> resources.SearchAds360Link:
        """Post-rpc interceptor for update_search_ads360_link

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_update_sk_ad_network_conversion_value_schema(
        self,
        request: analytics_admin.UpdateSKAdNetworkConversionValueSchemaRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.UpdateSKAdNetworkConversionValueSchemaRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for update_sk_ad_network_conversion_value_schema

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_update_sk_ad_network_conversion_value_schema(
        self, response: resources.SKAdNetworkConversionValueSchema
    ) -> resources.SKAdNetworkConversionValueSchema:
        """Post-rpc interceptor for update_sk_ad_network_conversion_value_schema

        Override in a subclass to manipulate the response
        after it is returned by the AnalyticsAdminService server but before
        it is returned to user code.
        """
        return response

    def pre_update_subproperty_event_filter(
        self,
        request: analytics_admin.UpdateSubpropertyEventFilterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        analytics_admin.UpdateSubpropertyEventFilterRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_subproperty_event_filter

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AnalyticsAdminService server.
        """
        return request, metadata

    def post_update_subproperty_event_filter(
        self, response: gaa_subproperty_event_filter.SubpropertyEventFilter
    ) -> gaa_subproperty_event_filter.SubpropertyEventFilter:
        """Post-rpc interceptor for update_subproperty_event_filter

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

    """

    def __init__(
        self,
        *,
        host: str = "analyticsadmin.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[AnalyticsAdminServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'analyticsadmin.googleapis.com').
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

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{property=properties/*}:acknowledgeUserDataCollection",
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
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _ApproveDisplayVideo360AdvertiserLinkProposal(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ApproveDisplayVideo360AdvertiserLinkProposal")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.ApproveDisplayVideo360AdvertiserLinkProposalRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.ApproveDisplayVideo360AdvertiserLinkProposalResponse:
            r"""Call the approve display video360
            advertiser link proposal method over HTTP.

                Args:
                    request (~.analytics_admin.ApproveDisplayVideo360AdvertiserLinkProposalRequest):
                        The request object. Request message for
                    ApproveDisplayVideo360AdvertiserLinkProposal
                    RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.analytics_admin.ApproveDisplayVideo360AdvertiserLinkProposalResponse:
                        Response message for
                    ApproveDisplayVideo360AdvertiserLinkProposal
                    RPC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{name=properties/*/displayVideo360AdvertiserLinkProposals/*}:approve",
                    "body": "*",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_approve_display_video360_advertiser_link_proposal(
                request, metadata
            )
            pb_request = (
                analytics_admin.ApproveDisplayVideo360AdvertiserLinkProposalRequest.pb(
                    request
                )
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = (
                analytics_admin.ApproveDisplayVideo360AdvertiserLinkProposalResponse()
            )
            pb_resp = (
                analytics_admin.ApproveDisplayVideo360AdvertiserLinkProposalResponse.pb(
                    resp
                )
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_approve_display_video360_advertiser_link_proposal(
                resp
            )
            return resp

    class _ArchiveAudience(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ArchiveAudience")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.ArchiveAudienceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the archive audience method over HTTP.

            Args:
                request (~.analytics_admin.ArchiveAudienceRequest):
                    The request object. Request message for ArchiveAudience
                RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{name=properties/*/audiences/*}:archive",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_archive_audience(
                request, metadata
            )
            pb_request = analytics_admin.ArchiveAudienceRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _ArchiveCustomDimension(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ArchiveCustomDimension")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{name=properties/*/customDimensions/*}:archive",
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
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{name=properties/*/customMetrics/*}:archive",
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
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _BatchCreateAccessBindings(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("BatchCreateAccessBindings")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.BatchCreateAccessBindingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.BatchCreateAccessBindingsResponse:
            r"""Call the batch create access
            bindings method over HTTP.

                Args:
                    request (~.analytics_admin.BatchCreateAccessBindingsRequest):
                        The request object. Request message for
                    BatchCreateAccessBindings RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.analytics_admin.BatchCreateAccessBindingsResponse:
                        Response message for
                    BatchCreateAccessBindings RPC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=accounts/*}/accessBindings:batchCreate",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=properties/*}/accessBindings:batchCreate",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_batch_create_access_bindings(
                request, metadata
            )
            pb_request = analytics_admin.BatchCreateAccessBindingsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = analytics_admin.BatchCreateAccessBindingsResponse()
            pb_resp = analytics_admin.BatchCreateAccessBindingsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_create_access_bindings(resp)
            return resp

    class _BatchDeleteAccessBindings(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("BatchDeleteAccessBindings")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.BatchDeleteAccessBindingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the batch delete access
            bindings method over HTTP.

                Args:
                    request (~.analytics_admin.BatchDeleteAccessBindingsRequest):
                        The request object. Request message for
                    BatchDeleteAccessBindings RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=accounts/*}/accessBindings:batchDelete",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=properties/*}/accessBindings:batchDelete",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_batch_delete_access_bindings(
                request, metadata
            )
            pb_request = analytics_admin.BatchDeleteAccessBindingsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _BatchGetAccessBindings(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("BatchGetAccessBindings")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "names": "",
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
            request: analytics_admin.BatchGetAccessBindingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.BatchGetAccessBindingsResponse:
            r"""Call the batch get access bindings method over HTTP.

            Args:
                request (~.analytics_admin.BatchGetAccessBindingsRequest):
                    The request object. Request message for
                BatchGetAccessBindings RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_admin.BatchGetAccessBindingsResponse:
                    Response message for
                BatchGetAccessBindings RPC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=accounts/*}/accessBindings:batchGet",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=properties/*}/accessBindings:batchGet",
                },
            ]
            request, metadata = self._interceptor.pre_batch_get_access_bindings(
                request, metadata
            )
            pb_request = analytics_admin.BatchGetAccessBindingsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = analytics_admin.BatchGetAccessBindingsResponse()
            pb_resp = analytics_admin.BatchGetAccessBindingsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_get_access_bindings(resp)
            return resp

    class _BatchUpdateAccessBindings(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("BatchUpdateAccessBindings")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.BatchUpdateAccessBindingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.BatchUpdateAccessBindingsResponse:
            r"""Call the batch update access
            bindings method over HTTP.

                Args:
                    request (~.analytics_admin.BatchUpdateAccessBindingsRequest):
                        The request object. Request message for
                    BatchUpdateAccessBindings RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.analytics_admin.BatchUpdateAccessBindingsResponse:
                        Response message for
                    BatchUpdateAccessBindings RPC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=accounts/*}/accessBindings:batchUpdate",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=properties/*}/accessBindings:batchUpdate",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_batch_update_access_bindings(
                request, metadata
            )
            pb_request = analytics_admin.BatchUpdateAccessBindingsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = analytics_admin.BatchUpdateAccessBindingsResponse()
            pb_resp = analytics_admin.BatchUpdateAccessBindingsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_update_access_bindings(resp)
            return resp

    class _CancelDisplayVideo360AdvertiserLinkProposal(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("CancelDisplayVideo360AdvertiserLinkProposal")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.CancelDisplayVideo360AdvertiserLinkProposalRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.DisplayVideo360AdvertiserLinkProposal:
            r"""Call the cancel display video360
            advertiser link proposal method over HTTP.

                Args:
                    request (~.analytics_admin.CancelDisplayVideo360AdvertiserLinkProposalRequest):
                        The request object. Request message for
                    CancelDisplayVideo360AdvertiserLinkProposal
                    RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.DisplayVideo360AdvertiserLinkProposal:
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{name=properties/*/displayVideo360AdvertiserLinkProposals/*}:cancel",
                    "body": "*",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_cancel_display_video360_advertiser_link_proposal(
                request, metadata
            )
            pb_request = (
                analytics_admin.CancelDisplayVideo360AdvertiserLinkProposalRequest.pb(
                    request
                )
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.DisplayVideo360AdvertiserLinkProposal()
            pb_resp = resources.DisplayVideo360AdvertiserLinkProposal.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = (
                self._interceptor.post_cancel_display_video360_advertiser_link_proposal(
                    resp
                )
            )
            return resp

    class _CreateAccessBinding(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("CreateAccessBinding")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.CreateAccessBindingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.AccessBinding:
            r"""Call the create access binding method over HTTP.

            Args:
                request (~.analytics_admin.CreateAccessBindingRequest):
                    The request object. Request message for
                CreateAccessBinding RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.AccessBinding:
                    A binding of a user to a set of
                roles.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=accounts/*}/accessBindings",
                    "body": "access_binding",
                },
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=properties/*}/accessBindings",
                    "body": "access_binding",
                },
            ]
            request, metadata = self._interceptor.pre_create_access_binding(
                request, metadata
            )
            pb_request = analytics_admin.CreateAccessBindingRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.AccessBinding()
            pb_resp = resources.AccessBinding.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_access_binding(resp)
            return resp

    class _CreateAdSenseLink(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("CreateAdSenseLink")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.CreateAdSenseLinkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.AdSenseLink:
            r"""Call the create ad sense link method over HTTP.

            Args:
                request (~.analytics_admin.CreateAdSenseLinkRequest):
                    The request object. Request message to be passed to
                CreateAdSenseLink method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.AdSenseLink:
                    A link between a GA4 Property and an
                AdSense for Content ad client.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=properties/*}/adSenseLinks",
                    "body": "adsense_link",
                },
            ]
            request, metadata = self._interceptor.pre_create_ad_sense_link(
                request, metadata
            )
            pb_request = analytics_admin.CreateAdSenseLinkRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.AdSenseLink()
            pb_resp = resources.AdSenseLink.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_ad_sense_link(resp)
            return resp

    class _CreateAudience(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("CreateAudience")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.CreateAudienceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gaa_audience.Audience:
            r"""Call the create audience method over HTTP.

            Args:
                request (~.analytics_admin.CreateAudienceRequest):
                    The request object. Request message for CreateAudience
                RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gaa_audience.Audience:
                    A resource message representing a GA4
                Audience.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=properties/*}/audiences",
                    "body": "audience",
                },
            ]
            request, metadata = self._interceptor.pre_create_audience(request, metadata)
            pb_request = analytics_admin.CreateAudienceRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = gaa_audience.Audience()
            pb_resp = gaa_audience.Audience.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_audience(resp)
            return resp

    class _CreateCalculatedMetric(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("CreateCalculatedMetric")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "calculatedMetricId": "",
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
            request: analytics_admin.CreateCalculatedMetricRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.CalculatedMetric:
            r"""Call the create calculated metric method over HTTP.

            Args:
                request (~.analytics_admin.CreateCalculatedMetricRequest):
                    The request object. Request message for
                CreateCalculatedMetric RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.CalculatedMetric:
                    A definition for a calculated metric.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=properties/*}/calculatedMetrics",
                    "body": "calculated_metric",
                },
            ]
            request, metadata = self._interceptor.pre_create_calculated_metric(
                request, metadata
            )
            pb_request = analytics_admin.CreateCalculatedMetricRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.CalculatedMetric()
            pb_resp = resources.CalculatedMetric.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_calculated_metric(resp)
            return resp

    class _CreateChannelGroup(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("CreateChannelGroup")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.CreateChannelGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gaa_channel_group.ChannelGroup:
            r"""Call the create channel group method over HTTP.

            Args:
                request (~.analytics_admin.CreateChannelGroupRequest):
                    The request object. Request message for
                CreateChannelGroup RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gaa_channel_group.ChannelGroup:
                    A resource message representing a
                Channel Group.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=properties/*}/channelGroups",
                    "body": "channel_group",
                },
            ]
            request, metadata = self._interceptor.pre_create_channel_group(
                request, metadata
            )
            pb_request = analytics_admin.CreateChannelGroupRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = gaa_channel_group.ChannelGroup()
            pb_resp = gaa_channel_group.ChannelGroup.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_channel_group(resp)
            return resp

    class _CreateConnectedSiteTag(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("CreateConnectedSiteTag")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.CreateConnectedSiteTagRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.CreateConnectedSiteTagResponse:
            r"""Call the create connected site tag method over HTTP.

            Args:
                request (~.analytics_admin.CreateConnectedSiteTagRequest):
                    The request object. Request message for
                CreateConnectedSiteTag RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_admin.CreateConnectedSiteTagResponse:
                    Response message for
                CreateConnectedSiteTag RPC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/properties:createConnectedSiteTag",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_create_connected_site_tag(
                request, metadata
            )
            pb_request = analytics_admin.CreateConnectedSiteTagRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = analytics_admin.CreateConnectedSiteTagResponse()
            pb_resp = analytics_admin.CreateConnectedSiteTagResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_connected_site_tag(resp)
            return resp

    class _CreateConversionEvent(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("CreateConversionEvent")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{parent=properties/*}/conversionEvents",
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
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{parent=properties/*}/customDimensions",
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
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{parent=properties/*}/customMetrics",
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
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{parent=properties/*}/dataStreams",
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
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _CreateDisplayVideo360AdvertiserLink(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("CreateDisplayVideo360AdvertiserLink")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.CreateDisplayVideo360AdvertiserLinkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.DisplayVideo360AdvertiserLink:
            r"""Call the create display video360
            advertiser link method over HTTP.

                Args:
                    request (~.analytics_admin.CreateDisplayVideo360AdvertiserLinkRequest):
                        The request object. Request message for
                    CreateDisplayVideo360AdvertiserLink RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.DisplayVideo360AdvertiserLink:
                        A link between a GA4 property and a
                    Display & Video 360 advertiser.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=properties/*}/displayVideo360AdvertiserLinks",
                    "body": "display_video_360_advertiser_link",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_create_display_video360_advertiser_link(
                request, metadata
            )
            pb_request = analytics_admin.CreateDisplayVideo360AdvertiserLinkRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.DisplayVideo360AdvertiserLink()
            pb_resp = resources.DisplayVideo360AdvertiserLink.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_display_video360_advertiser_link(resp)
            return resp

    class _CreateDisplayVideo360AdvertiserLinkProposal(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("CreateDisplayVideo360AdvertiserLinkProposal")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.CreateDisplayVideo360AdvertiserLinkProposalRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.DisplayVideo360AdvertiserLinkProposal:
            r"""Call the create display video360
            advertiser link proposal method over HTTP.

                Args:
                    request (~.analytics_admin.CreateDisplayVideo360AdvertiserLinkProposalRequest):
                        The request object. Request message for
                    CreateDisplayVideo360AdvertiserLinkProposal
                    RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.DisplayVideo360AdvertiserLinkProposal:
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=properties/*}/displayVideo360AdvertiserLinkProposals",
                    "body": "display_video_360_advertiser_link_proposal",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_create_display_video360_advertiser_link_proposal(
                request, metadata
            )
            pb_request = (
                analytics_admin.CreateDisplayVideo360AdvertiserLinkProposalRequest.pb(
                    request
                )
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.DisplayVideo360AdvertiserLinkProposal()
            pb_resp = resources.DisplayVideo360AdvertiserLinkProposal.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = (
                self._interceptor.post_create_display_video360_advertiser_link_proposal(
                    resp
                )
            )
            return resp

    class _CreateEventCreateRule(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("CreateEventCreateRule")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.CreateEventCreateRuleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> event_create_and_edit.EventCreateRule:
            r"""Call the create event create rule method over HTTP.

            Args:
                request (~.analytics_admin.CreateEventCreateRuleRequest):
                    The request object. Request message for
                CreateEventCreateRule RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.event_create_and_edit.EventCreateRule:
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=properties/*/dataStreams/*}/eventCreateRules",
                    "body": "event_create_rule",
                },
            ]
            request, metadata = self._interceptor.pre_create_event_create_rule(
                request, metadata
            )
            pb_request = analytics_admin.CreateEventCreateRuleRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = event_create_and_edit.EventCreateRule()
            pb_resp = event_create_and_edit.EventCreateRule.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_event_create_rule(resp)
            return resp

    class _CreateExpandedDataSet(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("CreateExpandedDataSet")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.CreateExpandedDataSetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gaa_expanded_data_set.ExpandedDataSet:
            r"""Call the create expanded data set method over HTTP.

            Args:
                request (~.analytics_admin.CreateExpandedDataSetRequest):
                    The request object. Request message for
                CreateExpandedDataSet RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gaa_expanded_data_set.ExpandedDataSet:
                    A resource message representing a GA4
                ExpandedDataSet.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=properties/*}/expandedDataSets",
                    "body": "expanded_data_set",
                },
            ]
            request, metadata = self._interceptor.pre_create_expanded_data_set(
                request, metadata
            )
            pb_request = analytics_admin.CreateExpandedDataSetRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = gaa_expanded_data_set.ExpandedDataSet()
            pb_resp = gaa_expanded_data_set.ExpandedDataSet.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_expanded_data_set(resp)
            return resp

    class _CreateFirebaseLink(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("CreateFirebaseLink")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{parent=properties/*}/firebaseLinks",
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
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{parent=properties/*}/googleAdsLinks",
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
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{parent=properties/*/dataStreams/*}/measurementProtocolSecrets",
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
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/properties",
                    "body": "property",
                },
            ]
            request, metadata = self._interceptor.pre_create_property(request, metadata)
            pb_request = analytics_admin.CreatePropertyRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _CreateRollupProperty(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("CreateRollupProperty")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.CreateRollupPropertyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.CreateRollupPropertyResponse:
            r"""Call the create rollup property method over HTTP.

            Args:
                request (~.analytics_admin.CreateRollupPropertyRequest):
                    The request object. Request message for
                CreateRollupProperty RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_admin.CreateRollupPropertyResponse:
                    Response message for
                CreateRollupProperty RPC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/properties:createRollupProperty",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_create_rollup_property(
                request, metadata
            )
            pb_request = analytics_admin.CreateRollupPropertyRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = analytics_admin.CreateRollupPropertyResponse()
            pb_resp = analytics_admin.CreateRollupPropertyResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_rollup_property(resp)
            return resp

    class _CreateRollupPropertySourceLink(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("CreateRollupPropertySourceLink")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.CreateRollupPropertySourceLinkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.RollupPropertySourceLink:
            r"""Call the create rollup property
            source link method over HTTP.

                Args:
                    request (~.analytics_admin.CreateRollupPropertySourceLinkRequest):
                        The request object. Request message for
                    CreateRollupPropertySourceLink RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.RollupPropertySourceLink:
                        A link that references a source
                    property under the parent rollup
                    property.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=properties/*}/rollupPropertySourceLinks",
                    "body": "rollup_property_source_link",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_create_rollup_property_source_link(
                request, metadata
            )
            pb_request = analytics_admin.CreateRollupPropertySourceLinkRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.RollupPropertySourceLink()
            pb_resp = resources.RollupPropertySourceLink.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_rollup_property_source_link(resp)
            return resp

    class _CreateSearchAds360Link(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("CreateSearchAds360Link")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.CreateSearchAds360LinkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.SearchAds360Link:
            r"""Call the create search ads360 link method over HTTP.

            Args:
                request (~.analytics_admin.CreateSearchAds360LinkRequest):
                    The request object. Request message for
                CreateSearchAds360Link RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.SearchAds360Link:
                    A link between a GA4 property and a
                Search Ads 360 entity.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=properties/*}/searchAds360Links",
                    "body": "search_ads_360_link",
                },
            ]
            request, metadata = self._interceptor.pre_create_search_ads360_link(
                request, metadata
            )
            pb_request = analytics_admin.CreateSearchAds360LinkRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.SearchAds360Link()
            pb_resp = resources.SearchAds360Link.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_search_ads360_link(resp)
            return resp

    class _CreateSKAdNetworkConversionValueSchema(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("CreateSKAdNetworkConversionValueSchema")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.CreateSKAdNetworkConversionValueSchemaRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.SKAdNetworkConversionValueSchema:
            r"""Call the create sk ad network
            conversion value schema method over HTTP.

                Args:
                    request (~.analytics_admin.CreateSKAdNetworkConversionValueSchemaRequest):
                        The request object. Request message for
                    CreateSKAdNetworkConversionValueSchema
                    RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.SKAdNetworkConversionValueSchema:
                        SKAdNetwork conversion value schema
                    of an iOS stream.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=properties/*/dataStreams/*}/sKAdNetworkConversionValueSchema",
                    "body": "skadnetwork_conversion_value_schema",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_create_sk_ad_network_conversion_value_schema(
                request, metadata
            )
            pb_request = (
                analytics_admin.CreateSKAdNetworkConversionValueSchemaRequest.pb(
                    request
                )
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.SKAdNetworkConversionValueSchema()
            pb_resp = resources.SKAdNetworkConversionValueSchema.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_sk_ad_network_conversion_value_schema(
                resp
            )
            return resp

    class _CreateSubproperty(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("CreateSubproperty")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.CreateSubpropertyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.CreateSubpropertyResponse:
            r"""Call the create subproperty method over HTTP.

            Args:
                request (~.analytics_admin.CreateSubpropertyRequest):
                    The request object. Request message for CreateSubproperty
                RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_admin.CreateSubpropertyResponse:
                    Response message for
                CreateSubproperty RPC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/properties:createSubproperty",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_create_subproperty(
                request, metadata
            )
            pb_request = analytics_admin.CreateSubpropertyRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = analytics_admin.CreateSubpropertyResponse()
            pb_resp = analytics_admin.CreateSubpropertyResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_subproperty(resp)
            return resp

    class _CreateSubpropertyEventFilter(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("CreateSubpropertyEventFilter")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.CreateSubpropertyEventFilterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gaa_subproperty_event_filter.SubpropertyEventFilter:
            r"""Call the create subproperty event
            filter method over HTTP.

                Args:
                    request (~.analytics_admin.CreateSubpropertyEventFilterRequest):
                        The request object. Request message for
                    CreateSubpropertyEventFilter RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.gaa_subproperty_event_filter.SubpropertyEventFilter:
                        A resource message representing a GA4
                    Subproperty event filter.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{parent=properties/*}/subpropertyEventFilters",
                    "body": "subproperty_event_filter",
                },
            ]
            request, metadata = self._interceptor.pre_create_subproperty_event_filter(
                request, metadata
            )
            pb_request = analytics_admin.CreateSubpropertyEventFilterRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = gaa_subproperty_event_filter.SubpropertyEventFilter()
            pb_resp = gaa_subproperty_event_filter.SubpropertyEventFilter.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_subproperty_event_filter(resp)
            return resp

    class _DeleteAccessBinding(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("DeleteAccessBinding")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.DeleteAccessBindingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete access binding method over HTTP.

            Args:
                request (~.analytics_admin.DeleteAccessBindingRequest):
                    The request object. Request message for
                DeleteAccessBinding RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1alpha/{name=accounts/*/accessBindings/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v1alpha/{name=properties/*/accessBindings/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_access_binding(
                request, metadata
            )
            pb_request = analytics_admin.DeleteAccessBindingRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _DeleteAccount(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("DeleteAccount")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{name=accounts/*}",
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
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _DeleteAdSenseLink(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("DeleteAdSenseLink")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.DeleteAdSenseLinkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete ad sense link method over HTTP.

            Args:
                request (~.analytics_admin.DeleteAdSenseLinkRequest):
                    The request object. Request message to be passed to
                DeleteAdSenseLink method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1alpha/{name=properties/*/adSenseLinks/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_ad_sense_link(
                request, metadata
            )
            pb_request = analytics_admin.DeleteAdSenseLinkRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _DeleteCalculatedMetric(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("DeleteCalculatedMetric")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.DeleteCalculatedMetricRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete calculated metric method over HTTP.

            Args:
                request (~.analytics_admin.DeleteCalculatedMetricRequest):
                    The request object. Request message for
                DeleteCalculatedMetric RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1alpha/{name=properties/*/calculatedMetrics/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_calculated_metric(
                request, metadata
            )
            pb_request = analytics_admin.DeleteCalculatedMetricRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _DeleteChannelGroup(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("DeleteChannelGroup")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.DeleteChannelGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete channel group method over HTTP.

            Args:
                request (~.analytics_admin.DeleteChannelGroupRequest):
                    The request object. Request message for
                DeleteChannelGroup RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1alpha/{name=properties/*/channelGroups/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_channel_group(
                request, metadata
            )
            pb_request = analytics_admin.DeleteChannelGroupRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _DeleteConnectedSiteTag(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("DeleteConnectedSiteTag")

        def __call__(
            self,
            request: analytics_admin.DeleteConnectedSiteTagRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete connected site tag method over HTTP.

            Args:
                request (~.analytics_admin.DeleteConnectedSiteTagRequest):
                    The request object. Request message for
                DeleteConnectedSiteTag RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/properties:deleteConnectedSiteTag",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_delete_connected_site_tag(
                request, metadata
            )
            pb_request = analytics_admin.DeleteConnectedSiteTagRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _DeleteConversionEvent(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("DeleteConversionEvent")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{name=properties/*/conversionEvents/*}",
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
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{name=properties/*/dataStreams/*}",
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
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _DeleteDisplayVideo360AdvertiserLink(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("DeleteDisplayVideo360AdvertiserLink")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.DeleteDisplayVideo360AdvertiserLinkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete display video360
            advertiser link method over HTTP.

                Args:
                    request (~.analytics_admin.DeleteDisplayVideo360AdvertiserLinkRequest):
                        The request object. Request message for
                    DeleteDisplayVideo360AdvertiserLink RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1alpha/{name=properties/*/displayVideo360AdvertiserLinks/*}",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_delete_display_video360_advertiser_link(
                request, metadata
            )
            pb_request = analytics_admin.DeleteDisplayVideo360AdvertiserLinkRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _DeleteDisplayVideo360AdvertiserLinkProposal(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("DeleteDisplayVideo360AdvertiserLinkProposal")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.DeleteDisplayVideo360AdvertiserLinkProposalRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete display video360
            advertiser link proposal method over HTTP.

                Args:
                    request (~.analytics_admin.DeleteDisplayVideo360AdvertiserLinkProposalRequest):
                        The request object. Request message for
                    DeleteDisplayVideo360AdvertiserLinkProposal
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
                    "uri": "/v1alpha/{name=properties/*/displayVideo360AdvertiserLinkProposals/*}",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_delete_display_video360_advertiser_link_proposal(
                request, metadata
            )
            pb_request = (
                analytics_admin.DeleteDisplayVideo360AdvertiserLinkProposalRequest.pb(
                    request
                )
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _DeleteEventCreateRule(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("DeleteEventCreateRule")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.DeleteEventCreateRuleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete event create rule method over HTTP.

            Args:
                request (~.analytics_admin.DeleteEventCreateRuleRequest):
                    The request object. Request message for
                DeleteEventCreateRule RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1alpha/{name=properties/*/dataStreams/*/eventCreateRules/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_event_create_rule(
                request, metadata
            )
            pb_request = analytics_admin.DeleteEventCreateRuleRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _DeleteExpandedDataSet(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("DeleteExpandedDataSet")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.DeleteExpandedDataSetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete expanded data set method over HTTP.

            Args:
                request (~.analytics_admin.DeleteExpandedDataSetRequest):
                    The request object. Request message for
                DeleteExpandedDataSet RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1alpha/{name=properties/*/expandedDataSets/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_expanded_data_set(
                request, metadata
            )
            pb_request = analytics_admin.DeleteExpandedDataSetRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{name=properties/*/firebaseLinks/*}",
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
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{name=properties/*/googleAdsLinks/*}",
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
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{name=properties/*/dataStreams/*/measurementProtocolSecrets/*}",
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
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{name=properties/*}",
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
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _DeleteRollupPropertySourceLink(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("DeleteRollupPropertySourceLink")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.DeleteRollupPropertySourceLinkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete rollup property
            source link method over HTTP.

                Args:
                    request (~.analytics_admin.DeleteRollupPropertySourceLinkRequest):
                        The request object. Request message for
                    DeleteRollupPropertySourceLink RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1alpha/{name=properties/*/rollupPropertySourceLinks/*}",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_delete_rollup_property_source_link(
                request, metadata
            )
            pb_request = analytics_admin.DeleteRollupPropertySourceLinkRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _DeleteSearchAds360Link(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("DeleteSearchAds360Link")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.DeleteSearchAds360LinkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete search ads360 link method over HTTP.

            Args:
                request (~.analytics_admin.DeleteSearchAds360LinkRequest):
                    The request object. Request message for
                DeleteSearchAds360Link RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1alpha/{name=properties/*/searchAds360Links/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_search_ads360_link(
                request, metadata
            )
            pb_request = analytics_admin.DeleteSearchAds360LinkRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _DeleteSKAdNetworkConversionValueSchema(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("DeleteSKAdNetworkConversionValueSchema")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.DeleteSKAdNetworkConversionValueSchemaRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete sk ad network
            conversion value schema method over HTTP.

                Args:
                    request (~.analytics_admin.DeleteSKAdNetworkConversionValueSchemaRequest):
                        The request object. Request message for
                    DeleteSKAdNetworkConversionValueSchema
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
                    "uri": "/v1alpha/{name=properties/*/dataStreams/*/sKAdNetworkConversionValueSchema/*}",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_delete_sk_ad_network_conversion_value_schema(
                request, metadata
            )
            pb_request = (
                analytics_admin.DeleteSKAdNetworkConversionValueSchemaRequest.pb(
                    request
                )
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _DeleteSubpropertyEventFilter(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("DeleteSubpropertyEventFilter")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.DeleteSubpropertyEventFilterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete subproperty event
            filter method over HTTP.

                Args:
                    request (~.analytics_admin.DeleteSubpropertyEventFilterRequest):
                        The request object. Request message for
                    DeleteSubpropertyEventFilter RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1alpha/{name=properties/*/subpropertyEventFilters/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_subproperty_event_filter(
                request, metadata
            )
            pb_request = analytics_admin.DeleteSubpropertyEventFilterRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _FetchAutomatedGa4ConfigurationOptOut(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("FetchAutomatedGa4ConfigurationOptOut")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.FetchAutomatedGa4ConfigurationOptOutRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.FetchAutomatedGa4ConfigurationOptOutResponse:
            r"""Call the fetch automated ga4
            configuration opt out method over HTTP.

                Args:
                    request (~.analytics_admin.FetchAutomatedGa4ConfigurationOptOutRequest):
                        The request object. Request for fetching the opt out
                    status for the automated GA4 setup
                    process.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.analytics_admin.FetchAutomatedGa4ConfigurationOptOutResponse:
                        Response message for fetching the opt
                    out status for the automated GA4 setup
                    process.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/properties:fetchAutomatedGa4ConfigurationOptOut",
                    "body": "*",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_fetch_automated_ga4_configuration_opt_out(
                request, metadata
            )
            pb_request = analytics_admin.FetchAutomatedGa4ConfigurationOptOutRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = analytics_admin.FetchAutomatedGa4ConfigurationOptOutResponse()
            pb_resp = analytics_admin.FetchAutomatedGa4ConfigurationOptOutResponse.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_fetch_automated_ga4_configuration_opt_out(
                resp
            )
            return resp

    class _FetchConnectedGa4Property(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("FetchConnectedGa4Property")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "property": "",
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
            request: analytics_admin.FetchConnectedGa4PropertyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.FetchConnectedGa4PropertyResponse:
            r"""Call the fetch connected ga4
            property method over HTTP.

                Args:
                    request (~.analytics_admin.FetchConnectedGa4PropertyRequest):
                        The request object. Request for looking up GA4 property
                    connected to a UA property.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.analytics_admin.FetchConnectedGa4PropertyResponse:
                        Response for looking up GA4 property
                    connected to a UA property.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/properties:fetchConnectedGa4Property",
                },
            ]
            request, metadata = self._interceptor.pre_fetch_connected_ga4_property(
                request, metadata
            )
            pb_request = analytics_admin.FetchConnectedGa4PropertyRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = analytics_admin.FetchConnectedGa4PropertyResponse()
            pb_resp = analytics_admin.FetchConnectedGa4PropertyResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_fetch_connected_ga4_property(resp)
            return resp

    class _GetAccessBinding(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetAccessBinding")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.GetAccessBindingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.AccessBinding:
            r"""Call the get access binding method over HTTP.

            Args:
                request (~.analytics_admin.GetAccessBindingRequest):
                    The request object. Request message for GetAccessBinding
                RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.AccessBinding:
                    A binding of a user to a set of
                roles.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=accounts/*/accessBindings/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=properties/*/accessBindings/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_access_binding(
                request, metadata
            )
            pb_request = analytics_admin.GetAccessBindingRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.AccessBinding()
            pb_resp = resources.AccessBinding.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_access_binding(resp)
            return resp

    class _GetAccount(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetAccount")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{name=accounts/*}",
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
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _GetAdSenseLink(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetAdSenseLink")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.GetAdSenseLinkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.AdSenseLink:
            r"""Call the get ad sense link method over HTTP.

            Args:
                request (~.analytics_admin.GetAdSenseLinkRequest):
                    The request object. Request message to be passed to
                GetAdSenseLink method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.AdSenseLink:
                    A link between a GA4 Property and an
                AdSense for Content ad client.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=properties/*/adSenseLinks/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_ad_sense_link(
                request, metadata
            )
            pb_request = analytics_admin.GetAdSenseLinkRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.AdSenseLink()
            pb_resp = resources.AdSenseLink.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_ad_sense_link(resp)
            return resp

    class _GetAttributionSettings(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetAttributionSettings")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.GetAttributionSettingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.AttributionSettings:
            r"""Call the get attribution settings method over HTTP.

            Args:
                request (~.analytics_admin.GetAttributionSettingsRequest):
                    The request object. Request message for
                GetAttributionSettings RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.AttributionSettings:
                    The attribution settings used for a
                given property. This is a singleton
                resource.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=properties/*/attributionSettings}",
                },
            ]
            request, metadata = self._interceptor.pre_get_attribution_settings(
                request, metadata
            )
            pb_request = analytics_admin.GetAttributionSettingsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.AttributionSettings()
            pb_resp = resources.AttributionSettings.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_attribution_settings(resp)
            return resp

    class _GetAudience(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetAudience")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.GetAudienceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> audience.Audience:
            r"""Call the get audience method over HTTP.

            Args:
                request (~.analytics_admin.GetAudienceRequest):
                    The request object. Request message for GetAudience RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.audience.Audience:
                    A resource message representing a GA4
                Audience.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=properties/*/audiences/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_audience(request, metadata)
            pb_request = analytics_admin.GetAudienceRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = audience.Audience()
            pb_resp = audience.Audience.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_audience(resp)
            return resp

    class _GetBigQueryLink(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetBigQueryLink")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.GetBigQueryLinkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.BigQueryLink:
            r"""Call the get big query link method over HTTP.

            Args:
                request (~.analytics_admin.GetBigQueryLinkRequest):
                    The request object. Request message for GetBigQueryLink
                RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.BigQueryLink:
                    A link between a GA4 Property and
                BigQuery project.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=properties/*/bigQueryLinks/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_big_query_link(
                request, metadata
            )
            pb_request = analytics_admin.GetBigQueryLinkRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.BigQueryLink()
            pb_resp = resources.BigQueryLink.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_big_query_link(resp)
            return resp

    class _GetCalculatedMetric(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetCalculatedMetric")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.GetCalculatedMetricRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.CalculatedMetric:
            r"""Call the get calculated metric method over HTTP.

            Args:
                request (~.analytics_admin.GetCalculatedMetricRequest):
                    The request object. Request message for
                GetCalculatedMetric RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.CalculatedMetric:
                    A definition for a calculated metric.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=properties/*/calculatedMetrics/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_calculated_metric(
                request, metadata
            )
            pb_request = analytics_admin.GetCalculatedMetricRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.CalculatedMetric()
            pb_resp = resources.CalculatedMetric.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_calculated_metric(resp)
            return resp

    class _GetChannelGroup(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetChannelGroup")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.GetChannelGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> channel_group.ChannelGroup:
            r"""Call the get channel group method over HTTP.

            Args:
                request (~.analytics_admin.GetChannelGroupRequest):
                    The request object. Request message for GetChannelGroup
                RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.channel_group.ChannelGroup:
                    A resource message representing a
                Channel Group.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=properties/*/channelGroups/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_channel_group(
                request, metadata
            )
            pb_request = analytics_admin.GetChannelGroupRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = channel_group.ChannelGroup()
            pb_resp = channel_group.ChannelGroup.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_channel_group(resp)
            return resp

    class _GetConversionEvent(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetConversionEvent")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{name=properties/*/conversionEvents/*}",
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
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{name=properties/*/customDimensions/*}",
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
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{name=properties/*/customMetrics/*}",
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
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _GetDataRedactionSettings(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetDataRedactionSettings")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.GetDataRedactionSettingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.DataRedactionSettings:
            r"""Call the get data redaction
            settings method over HTTP.

                Args:
                    request (~.analytics_admin.GetDataRedactionSettingsRequest):
                        The request object. Request message for
                    GetDataRedactionSettings RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.DataRedactionSettings:
                        Settings for client-side data
                    redaction. Singleton resource under a
                    Web Stream.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=properties/*/dataStreams/*/dataRedactionSettings}",
                },
            ]
            request, metadata = self._interceptor.pre_get_data_redaction_settings(
                request, metadata
            )
            pb_request = analytics_admin.GetDataRedactionSettingsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.DataRedactionSettings()
            pb_resp = resources.DataRedactionSettings.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_data_redaction_settings(resp)
            return resp

    class _GetDataRetentionSettings(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetDataRetentionSettings")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{name=properties/*/dataRetentionSettings}",
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
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{name=accounts/*/dataSharingSettings}",
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
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{name=properties/*/dataStreams/*}",
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
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _GetDisplayVideo360AdvertiserLink(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetDisplayVideo360AdvertiserLink")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.GetDisplayVideo360AdvertiserLinkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.DisplayVideo360AdvertiserLink:
            r"""Call the get display video360
            advertiser link method over HTTP.

                Args:
                    request (~.analytics_admin.GetDisplayVideo360AdvertiserLinkRequest):
                        The request object. Request message for
                    GetDisplayVideo360AdvertiserLink RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.DisplayVideo360AdvertiserLink:
                        A link between a GA4 property and a
                    Display & Video 360 advertiser.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=properties/*/displayVideo360AdvertiserLinks/*}",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_get_display_video360_advertiser_link(
                request, metadata
            )
            pb_request = analytics_admin.GetDisplayVideo360AdvertiserLinkRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.DisplayVideo360AdvertiserLink()
            pb_resp = resources.DisplayVideo360AdvertiserLink.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_display_video360_advertiser_link(resp)
            return resp

    class _GetDisplayVideo360AdvertiserLinkProposal(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetDisplayVideo360AdvertiserLinkProposal")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.GetDisplayVideo360AdvertiserLinkProposalRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.DisplayVideo360AdvertiserLinkProposal:
            r"""Call the get display video360
            advertiser link proposal method over HTTP.

                Args:
                    request (~.analytics_admin.GetDisplayVideo360AdvertiserLinkProposalRequest):
                        The request object. Request message for
                    GetDisplayVideo360AdvertiserLinkProposal
                    RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.DisplayVideo360AdvertiserLinkProposal:
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=properties/*/displayVideo360AdvertiserLinkProposals/*}",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_get_display_video360_advertiser_link_proposal(
                request, metadata
            )
            pb_request = (
                analytics_admin.GetDisplayVideo360AdvertiserLinkProposalRequest.pb(
                    request
                )
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.DisplayVideo360AdvertiserLinkProposal()
            pb_resp = resources.DisplayVideo360AdvertiserLinkProposal.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_display_video360_advertiser_link_proposal(
                resp
            )
            return resp

    class _GetEnhancedMeasurementSettings(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetEnhancedMeasurementSettings")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.GetEnhancedMeasurementSettingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.EnhancedMeasurementSettings:
            r"""Call the get enhanced measurement
            settings method over HTTP.

                Args:
                    request (~.analytics_admin.GetEnhancedMeasurementSettingsRequest):
                        The request object. Request message for
                    GetEnhancedMeasurementSettings RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.EnhancedMeasurementSettings:
                        Singleton resource under a web
                    DataStream, configuring measurement of
                    additional site interactions and
                    content.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=properties/*/dataStreams/*/enhancedMeasurementSettings}",
                },
            ]
            request, metadata = self._interceptor.pre_get_enhanced_measurement_settings(
                request, metadata
            )
            pb_request = analytics_admin.GetEnhancedMeasurementSettingsRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.EnhancedMeasurementSettings()
            pb_resp = resources.EnhancedMeasurementSettings.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_enhanced_measurement_settings(resp)
            return resp

    class _GetEventCreateRule(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetEventCreateRule")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.GetEventCreateRuleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> event_create_and_edit.EventCreateRule:
            r"""Call the get event create rule method over HTTP.

            Args:
                request (~.analytics_admin.GetEventCreateRuleRequest):
                    The request object. Request message for
                GetEventCreateRule RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.event_create_and_edit.EventCreateRule:
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=properties/*/dataStreams/*/eventCreateRules/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_event_create_rule(
                request, metadata
            )
            pb_request = analytics_admin.GetEventCreateRuleRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = event_create_and_edit.EventCreateRule()
            pb_resp = event_create_and_edit.EventCreateRule.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_event_create_rule(resp)
            return resp

    class _GetExpandedDataSet(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetExpandedDataSet")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.GetExpandedDataSetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> expanded_data_set.ExpandedDataSet:
            r"""Call the get expanded data set method over HTTP.

            Args:
                request (~.analytics_admin.GetExpandedDataSetRequest):
                    The request object. Request message for
                GetExpandedDataSet RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.expanded_data_set.ExpandedDataSet:
                    A resource message representing a GA4
                ExpandedDataSet.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=properties/*/expandedDataSets/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_expanded_data_set(
                request, metadata
            )
            pb_request = analytics_admin.GetExpandedDataSetRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = expanded_data_set.ExpandedDataSet()
            pb_resp = expanded_data_set.ExpandedDataSet.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_expanded_data_set(resp)
            return resp

    class _GetGlobalSiteTag(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetGlobalSiteTag")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.GetGlobalSiteTagRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.GlobalSiteTag:
            r"""Call the get global site tag method over HTTP.

            Args:
                request (~.analytics_admin.GetGlobalSiteTagRequest):
                    The request object. Request message for GetGlobalSiteTag
                RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.GlobalSiteTag:
                    Read-only resource with the tag for
                sending data from a website to a
                DataStream. Only present for web
                DataStream resources.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=properties/*/dataStreams/*/globalSiteTag}",
                },
            ]
            request, metadata = self._interceptor.pre_get_global_site_tag(
                request, metadata
            )
            pb_request = analytics_admin.GetGlobalSiteTagRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.GlobalSiteTag()
            pb_resp = resources.GlobalSiteTag.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_global_site_tag(resp)
            return resp

    class _GetGoogleSignalsSettings(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetGoogleSignalsSettings")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.GetGoogleSignalsSettingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.GoogleSignalsSettings:
            r"""Call the get google signals
            settings method over HTTP.

                Args:
                    request (~.analytics_admin.GetGoogleSignalsSettingsRequest):
                        The request object. Request message for
                    GetGoogleSignalsSettings RPC
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.GoogleSignalsSettings:
                        Settings values for Google Signals.
                    This is a singleton resource.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=properties/*/googleSignalsSettings}",
                },
            ]
            request, metadata = self._interceptor.pre_get_google_signals_settings(
                request, metadata
            )
            pb_request = analytics_admin.GetGoogleSignalsSettingsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.GoogleSignalsSettings()
            pb_resp = resources.GoogleSignalsSettings.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_google_signals_settings(resp)
            return resp

    class _GetMeasurementProtocolSecret(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetMeasurementProtocolSecret")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{name=properties/*/dataStreams/*/measurementProtocolSecrets/*}",
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
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{name=properties/*}",
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
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _GetRollupPropertySourceLink(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetRollupPropertySourceLink")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.GetRollupPropertySourceLinkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.RollupPropertySourceLink:
            r"""Call the get rollup property
            source link method over HTTP.

                Args:
                    request (~.analytics_admin.GetRollupPropertySourceLinkRequest):
                        The request object. Request message for
                    GetRollupPropertySourceLink RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.RollupPropertySourceLink:
                        A link that references a source
                    property under the parent rollup
                    property.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=properties/*/rollupPropertySourceLinks/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_rollup_property_source_link(
                request, metadata
            )
            pb_request = analytics_admin.GetRollupPropertySourceLinkRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.RollupPropertySourceLink()
            pb_resp = resources.RollupPropertySourceLink.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_rollup_property_source_link(resp)
            return resp

    class _GetSearchAds360Link(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetSearchAds360Link")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.GetSearchAds360LinkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.SearchAds360Link:
            r"""Call the get search ads360 link method over HTTP.

            Args:
                request (~.analytics_admin.GetSearchAds360LinkRequest):
                    The request object. Request message for
                GetSearchAds360Link RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.SearchAds360Link:
                    A link between a GA4 property and a
                Search Ads 360 entity.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=properties/*/searchAds360Links/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_search_ads360_link(
                request, metadata
            )
            pb_request = analytics_admin.GetSearchAds360LinkRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.SearchAds360Link()
            pb_resp = resources.SearchAds360Link.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_search_ads360_link(resp)
            return resp

    class _GetSKAdNetworkConversionValueSchema(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetSKAdNetworkConversionValueSchema")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.GetSKAdNetworkConversionValueSchemaRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.SKAdNetworkConversionValueSchema:
            r"""Call the get sk ad network
            conversion value schema method over HTTP.

                Args:
                    request (~.analytics_admin.GetSKAdNetworkConversionValueSchemaRequest):
                        The request object. Request message for
                    GetSKAdNetworkConversionValueSchema RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.SKAdNetworkConversionValueSchema:
                        SKAdNetwork conversion value schema
                    of an iOS stream.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=properties/*/dataStreams/*/sKAdNetworkConversionValueSchema/*}",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_get_sk_ad_network_conversion_value_schema(
                request, metadata
            )
            pb_request = analytics_admin.GetSKAdNetworkConversionValueSchemaRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.SKAdNetworkConversionValueSchema()
            pb_resp = resources.SKAdNetworkConversionValueSchema.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_sk_ad_network_conversion_value_schema(
                resp
            )
            return resp

    class _GetSubpropertyEventFilter(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("GetSubpropertyEventFilter")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.GetSubpropertyEventFilterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> subproperty_event_filter.SubpropertyEventFilter:
            r"""Call the get subproperty event
            filter method over HTTP.

                Args:
                    request (~.analytics_admin.GetSubpropertyEventFilterRequest):
                        The request object. Request message for
                    GetSubpropertyEventFilter RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.subproperty_event_filter.SubpropertyEventFilter:
                        A resource message representing a GA4
                    Subproperty event filter.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{name=properties/*/subpropertyEventFilters/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_subproperty_event_filter(
                request, metadata
            )
            pb_request = analytics_admin.GetSubpropertyEventFilterRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = subproperty_event_filter.SubpropertyEventFilter()
            pb_resp = subproperty_event_filter.SubpropertyEventFilter.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_subproperty_event_filter(resp)
            return resp

    class _ListAccessBindings(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ListAccessBindings")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.ListAccessBindingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.ListAccessBindingsResponse:
            r"""Call the list access bindings method over HTTP.

            Args:
                request (~.analytics_admin.ListAccessBindingsRequest):
                    The request object. Request message for
                ListAccessBindings RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_admin.ListAccessBindingsResponse:
                    Response message for
                ListAccessBindings RPC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=accounts/*}/accessBindings",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=properties/*}/accessBindings",
                },
            ]
            request, metadata = self._interceptor.pre_list_access_bindings(
                request, metadata
            )
            pb_request = analytics_admin.ListAccessBindingsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = analytics_admin.ListAccessBindingsResponse()
            pb_resp = analytics_admin.ListAccessBindingsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_access_bindings(resp)
            return resp

    class _ListAccounts(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ListAccounts")

        def __call__(
            self,
            request: analytics_admin.ListAccountsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/accounts",
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
                    use_integers_for_enums=True,
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/accountSummaries",
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
                    use_integers_for_enums=True,
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _ListAdSenseLinks(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ListAdSenseLinks")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.ListAdSenseLinksRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.ListAdSenseLinksResponse:
            r"""Call the list ad sense links method over HTTP.

            Args:
                request (~.analytics_admin.ListAdSenseLinksRequest):
                    The request object. Request message to be passed to
                ListAdSenseLinks method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_admin.ListAdSenseLinksResponse:
                    Response message for ListAdSenseLinks
                method.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=properties/*}/adSenseLinks",
                },
            ]
            request, metadata = self._interceptor.pre_list_ad_sense_links(
                request, metadata
            )
            pb_request = analytics_admin.ListAdSenseLinksRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = analytics_admin.ListAdSenseLinksResponse()
            pb_resp = analytics_admin.ListAdSenseLinksResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_ad_sense_links(resp)
            return resp

    class _ListAudiences(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ListAudiences")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.ListAudiencesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.ListAudiencesResponse:
            r"""Call the list audiences method over HTTP.

            Args:
                request (~.analytics_admin.ListAudiencesRequest):
                    The request object. Request message for ListAudiences
                RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_admin.ListAudiencesResponse:
                    Response message for ListAudiences
                RPC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=properties/*}/audiences",
                },
            ]
            request, metadata = self._interceptor.pre_list_audiences(request, metadata)
            pb_request = analytics_admin.ListAudiencesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = analytics_admin.ListAudiencesResponse()
            pb_resp = analytics_admin.ListAudiencesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_audiences(resp)
            return resp

    class _ListBigQueryLinks(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ListBigQueryLinks")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.ListBigQueryLinksRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.ListBigQueryLinksResponse:
            r"""Call the list big query links method over HTTP.

            Args:
                request (~.analytics_admin.ListBigQueryLinksRequest):
                    The request object. Request message for ListBigQueryLinks
                RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_admin.ListBigQueryLinksResponse:
                    Response message for
                ListBigQueryLinks RPC

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=properties/*}/bigQueryLinks",
                },
            ]
            request, metadata = self._interceptor.pre_list_big_query_links(
                request, metadata
            )
            pb_request = analytics_admin.ListBigQueryLinksRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = analytics_admin.ListBigQueryLinksResponse()
            pb_resp = analytics_admin.ListBigQueryLinksResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_big_query_links(resp)
            return resp

    class _ListCalculatedMetrics(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ListCalculatedMetrics")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.ListCalculatedMetricsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.ListCalculatedMetricsResponse:
            r"""Call the list calculated metrics method over HTTP.

            Args:
                request (~.analytics_admin.ListCalculatedMetricsRequest):
                    The request object. Request message for
                ListCalculatedMetrics RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_admin.ListCalculatedMetricsResponse:
                    Response message for
                ListCalculatedMetrics RPC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=properties/*}/calculatedMetrics",
                },
            ]
            request, metadata = self._interceptor.pre_list_calculated_metrics(
                request, metadata
            )
            pb_request = analytics_admin.ListCalculatedMetricsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = analytics_admin.ListCalculatedMetricsResponse()
            pb_resp = analytics_admin.ListCalculatedMetricsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_calculated_metrics(resp)
            return resp

    class _ListChannelGroups(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ListChannelGroups")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.ListChannelGroupsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.ListChannelGroupsResponse:
            r"""Call the list channel groups method over HTTP.

            Args:
                request (~.analytics_admin.ListChannelGroupsRequest):
                    The request object. Request message for ListChannelGroups
                RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_admin.ListChannelGroupsResponse:
                    Response message for
                ListChannelGroups RPC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=properties/*}/channelGroups",
                },
            ]
            request, metadata = self._interceptor.pre_list_channel_groups(
                request, metadata
            )
            pb_request = analytics_admin.ListChannelGroupsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = analytics_admin.ListChannelGroupsResponse()
            pb_resp = analytics_admin.ListChannelGroupsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_channel_groups(resp)
            return resp

    class _ListConnectedSiteTags(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ListConnectedSiteTags")

        def __call__(
            self,
            request: analytics_admin.ListConnectedSiteTagsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.ListConnectedSiteTagsResponse:
            r"""Call the list connected site tags method over HTTP.

            Args:
                request (~.analytics_admin.ListConnectedSiteTagsRequest):
                    The request object. Request message for
                ListConnectedSiteTags RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_admin.ListConnectedSiteTagsResponse:
                    Response message for
                ListConnectedSiteTags RPC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/properties:listConnectedSiteTags",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_list_connected_site_tags(
                request, metadata
            )
            pb_request = analytics_admin.ListConnectedSiteTagsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = analytics_admin.ListConnectedSiteTagsResponse()
            pb_resp = analytics_admin.ListConnectedSiteTagsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_connected_site_tags(resp)
            return resp

    class _ListConversionEvents(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ListConversionEvents")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{parent=properties/*}/conversionEvents",
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
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{parent=properties/*}/customDimensions",
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
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{parent=properties/*}/customMetrics",
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
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{parent=properties/*}/dataStreams",
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
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _ListDisplayVideo360AdvertiserLinkProposals(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ListDisplayVideo360AdvertiserLinkProposals")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.ListDisplayVideo360AdvertiserLinkProposalsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.ListDisplayVideo360AdvertiserLinkProposalsResponse:
            r"""Call the list display video360
            advertiser link proposals method over HTTP.

                Args:
                    request (~.analytics_admin.ListDisplayVideo360AdvertiserLinkProposalsRequest):
                        The request object. Request message for
                    ListDisplayVideo360AdvertiserLinkProposals
                    RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.analytics_admin.ListDisplayVideo360AdvertiserLinkProposalsResponse:
                        Response message for
                    ListDisplayVideo360AdvertiserLinkProposals
                    RPC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=properties/*}/displayVideo360AdvertiserLinkProposals",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_list_display_video360_advertiser_link_proposals(
                request, metadata
            )
            pb_request = (
                analytics_admin.ListDisplayVideo360AdvertiserLinkProposalsRequest.pb(
                    request
                )
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = analytics_admin.ListDisplayVideo360AdvertiserLinkProposalsResponse()
            pb_resp = (
                analytics_admin.ListDisplayVideo360AdvertiserLinkProposalsResponse.pb(
                    resp
                )
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = (
                self._interceptor.post_list_display_video360_advertiser_link_proposals(
                    resp
                )
            )
            return resp

    class _ListDisplayVideo360AdvertiserLinks(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ListDisplayVideo360AdvertiserLinks")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.ListDisplayVideo360AdvertiserLinksRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.ListDisplayVideo360AdvertiserLinksResponse:
            r"""Call the list display video360
            advertiser links method over HTTP.

                Args:
                    request (~.analytics_admin.ListDisplayVideo360AdvertiserLinksRequest):
                        The request object. Request message for
                    ListDisplayVideo360AdvertiserLinks RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.analytics_admin.ListDisplayVideo360AdvertiserLinksResponse:
                        Response message for
                    ListDisplayVideo360AdvertiserLinks RPC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=properties/*}/displayVideo360AdvertiserLinks",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_list_display_video360_advertiser_links(
                request, metadata
            )
            pb_request = analytics_admin.ListDisplayVideo360AdvertiserLinksRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = analytics_admin.ListDisplayVideo360AdvertiserLinksResponse()
            pb_resp = analytics_admin.ListDisplayVideo360AdvertiserLinksResponse.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_display_video360_advertiser_links(resp)
            return resp

    class _ListEventCreateRules(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ListEventCreateRules")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.ListEventCreateRulesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.ListEventCreateRulesResponse:
            r"""Call the list event create rules method over HTTP.

            Args:
                request (~.analytics_admin.ListEventCreateRulesRequest):
                    The request object. Request message for
                ListEventCreateRules RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_admin.ListEventCreateRulesResponse:
                    Response message for
                ListEventCreateRules RPC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=properties/*/dataStreams/*}/eventCreateRules",
                },
            ]
            request, metadata = self._interceptor.pre_list_event_create_rules(
                request, metadata
            )
            pb_request = analytics_admin.ListEventCreateRulesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = analytics_admin.ListEventCreateRulesResponse()
            pb_resp = analytics_admin.ListEventCreateRulesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_event_create_rules(resp)
            return resp

    class _ListExpandedDataSets(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ListExpandedDataSets")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.ListExpandedDataSetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.ListExpandedDataSetsResponse:
            r"""Call the list expanded data sets method over HTTP.

            Args:
                request (~.analytics_admin.ListExpandedDataSetsRequest):
                    The request object. Request message for
                ListExpandedDataSets RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_admin.ListExpandedDataSetsResponse:
                    Response message for
                ListExpandedDataSets RPC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=properties/*}/expandedDataSets",
                },
            ]
            request, metadata = self._interceptor.pre_list_expanded_data_sets(
                request, metadata
            )
            pb_request = analytics_admin.ListExpandedDataSetsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = analytics_admin.ListExpandedDataSetsResponse()
            pb_resp = analytics_admin.ListExpandedDataSetsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_expanded_data_sets(resp)
            return resp

    class _ListFirebaseLinks(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ListFirebaseLinks")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{parent=properties/*}/firebaseLinks",
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
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{parent=properties/*}/googleAdsLinks",
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
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{parent=properties/*/dataStreams/*}/measurementProtocolSecrets",
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
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/properties",
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
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _ListRollupPropertySourceLinks(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ListRollupPropertySourceLinks")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.ListRollupPropertySourceLinksRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.ListRollupPropertySourceLinksResponse:
            r"""Call the list rollup property
            source links method over HTTP.

                Args:
                    request (~.analytics_admin.ListRollupPropertySourceLinksRequest):
                        The request object. Request message for
                    ListRollupPropertySourceLinks RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.analytics_admin.ListRollupPropertySourceLinksResponse:
                        Response message for
                    ListRollupPropertySourceLinks RPC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=properties/*}/rollupPropertySourceLinks",
                },
            ]
            request, metadata = self._interceptor.pre_list_rollup_property_source_links(
                request, metadata
            )
            pb_request = analytics_admin.ListRollupPropertySourceLinksRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = analytics_admin.ListRollupPropertySourceLinksResponse()
            pb_resp = analytics_admin.ListRollupPropertySourceLinksResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_rollup_property_source_links(resp)
            return resp

    class _ListSearchAds360Links(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ListSearchAds360Links")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.ListSearchAds360LinksRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.ListSearchAds360LinksResponse:
            r"""Call the list search ads360 links method over HTTP.

            Args:
                request (~.analytics_admin.ListSearchAds360LinksRequest):
                    The request object. Request message for
                ListSearchAds360Links RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_admin.ListSearchAds360LinksResponse:
                    Response message for
                ListSearchAds360Links RPC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=properties/*}/searchAds360Links",
                },
            ]
            request, metadata = self._interceptor.pre_list_search_ads360_links(
                request, metadata
            )
            pb_request = analytics_admin.ListSearchAds360LinksRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = analytics_admin.ListSearchAds360LinksResponse()
            pb_resp = analytics_admin.ListSearchAds360LinksResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_search_ads360_links(resp)
            return resp

    class _ListSKAdNetworkConversionValueSchemas(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ListSKAdNetworkConversionValueSchemas")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.ListSKAdNetworkConversionValueSchemasRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.ListSKAdNetworkConversionValueSchemasResponse:
            r"""Call the list sk ad network
            conversion value schemas method over HTTP.

                Args:
                    request (~.analytics_admin.ListSKAdNetworkConversionValueSchemasRequest):
                        The request object. Request message for
                    ListSKAdNetworkConversionValueSchemas
                    RPC
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.analytics_admin.ListSKAdNetworkConversionValueSchemasResponse:
                        Response message for
                    ListSKAdNetworkConversionValueSchemas
                    RPC

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=properties/*/dataStreams/*}/sKAdNetworkConversionValueSchema",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_list_sk_ad_network_conversion_value_schemas(
                request, metadata
            )
            pb_request = (
                analytics_admin.ListSKAdNetworkConversionValueSchemasRequest.pb(request)
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = analytics_admin.ListSKAdNetworkConversionValueSchemasResponse()
            pb_resp = analytics_admin.ListSKAdNetworkConversionValueSchemasResponse.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_sk_ad_network_conversion_value_schemas(
                resp
            )
            return resp

    class _ListSubpropertyEventFilters(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ListSubpropertyEventFilters")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.ListSubpropertyEventFiltersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.ListSubpropertyEventFiltersResponse:
            r"""Call the list subproperty event
            filters method over HTTP.

                Args:
                    request (~.analytics_admin.ListSubpropertyEventFiltersRequest):
                        The request object. Request message for
                    ListSubpropertyEventFilters RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.analytics_admin.ListSubpropertyEventFiltersResponse:
                        Response message for
                    ListSubpropertyEventFilter RPC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha/{parent=properties/*}/subpropertyEventFilters",
                },
            ]
            request, metadata = self._interceptor.pre_list_subproperty_event_filters(
                request, metadata
            )
            pb_request = analytics_admin.ListSubpropertyEventFiltersRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = analytics_admin.ListSubpropertyEventFiltersResponse()
            pb_resp = analytics_admin.ListSubpropertyEventFiltersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_subproperty_event_filters(resp)
            return resp

    class _ProvisionAccountTicket(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("ProvisionAccountTicket")

        def __call__(
            self,
            request: analytics_admin.ProvisionAccountTicketRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/accounts:provisionAccountTicket",
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
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _RunAccessReport(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("RunAccessReport")

        def __call__(
            self,
            request: analytics_admin.RunAccessReportRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.RunAccessReportResponse:
            r"""Call the run access report method over HTTP.

            Args:
                request (~.analytics_admin.RunAccessReportRequest):
                    The request object. The request for a Data Access Record
                Report.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.analytics_admin.RunAccessReportResponse:
                    The customized Data Access Record
                Report response.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/{entity=properties/*}:runAccessReport",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1alpha/{entity=accounts/*}:runAccessReport",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_run_access_report(
                request, metadata
            )
            pb_request = analytics_admin.RunAccessReportRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = analytics_admin.RunAccessReportResponse()
            pb_resp = analytics_admin.RunAccessReportResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_run_access_report(resp)
            return resp

    class _SearchChangeHistoryEvents(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("SearchChangeHistoryEvents")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{account=accounts/*}:searchChangeHistoryEvents",
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
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _SetAutomatedGa4ConfigurationOptOut(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("SetAutomatedGa4ConfigurationOptOut")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.SetAutomatedGa4ConfigurationOptOutRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> analytics_admin.SetAutomatedGa4ConfigurationOptOutResponse:
            r"""Call the set automated ga4
            configuration opt out method over HTTP.

                Args:
                    request (~.analytics_admin.SetAutomatedGa4ConfigurationOptOutRequest):
                        The request object. Request for setting the opt out
                    status for the automated GA4 setup
                    process.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.analytics_admin.SetAutomatedGa4ConfigurationOptOutResponse:
                        Response message for setting the opt
                    out status for the automated GA4 setup
                    process.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha/properties:setAutomatedGa4ConfigurationOptOut",
                    "body": "*",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_set_automated_ga4_configuration_opt_out(
                request, metadata
            )
            pb_request = analytics_admin.SetAutomatedGa4ConfigurationOptOutRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = analytics_admin.SetAutomatedGa4ConfigurationOptOutResponse()
            pb_resp = analytics_admin.SetAutomatedGa4ConfigurationOptOutResponse.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_automated_ga4_configuration_opt_out(resp)
            return resp

    class _UpdateAccessBinding(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("UpdateAccessBinding")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: analytics_admin.UpdateAccessBindingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.AccessBinding:
            r"""Call the update access binding method over HTTP.

            Args:
                request (~.analytics_admin.UpdateAccessBindingRequest):
                    The request object. Request message for
                UpdateAccessBinding RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.AccessBinding:
                    A binding of a user to a set of
                roles.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1alpha/{access_binding.name=accounts/*/accessBindings/*}",
                    "body": "access_binding",
                },
                {
                    "method": "patch",
                    "uri": "/v1alpha/{access_binding.name=properties/*/accessBindings/*}",
                    "body": "access_binding",
                },
            ]
            request, metadata = self._interceptor.pre_update_access_binding(
                request, metadata
            )
            pb_request = analytics_admin.UpdateAccessBindingRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.AccessBinding()
            pb_resp = resources.AccessBinding.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_access_binding(resp)
            return resp

    class _UpdateAccount(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("UpdateAccount")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{account.name=accounts/*}",
                    "body": "account",
                },
            ]
            request, metadata = self._interceptor.pre_update_account(request, metadata)
            pb_request = analytics_admin.UpdateAccountRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _UpdateAttributionSettings(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("UpdateAttributionSettings")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
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
            request: analytics_admin.UpdateAttributionSettingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.AttributionSettings:
            r"""Call the update attribution
            settings method over HTTP.

                Args:
                    request (~.analytics_admin.UpdateAttributionSettingsRequest):
                        The request object. Request message for
                    UpdateAttributionSettings RPC
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.AttributionSettings:
                        The attribution settings used for a
                    given property. This is a singleton
                    resource.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1alpha/{attribution_settings.name=properties/*/attributionSettings}",
                    "body": "attribution_settings",
                },
            ]
            request, metadata = self._interceptor.pre_update_attribution_settings(
                request, metadata
            )
            pb_request = analytics_admin.UpdateAttributionSettingsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.AttributionSettings()
            pb_resp = resources.AttributionSettings.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_attribution_settings(resp)
            return resp

    class _UpdateAudience(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("UpdateAudience")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
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
            request: analytics_admin.UpdateAudienceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gaa_audience.Audience:
            r"""Call the update audience method over HTTP.

            Args:
                request (~.analytics_admin.UpdateAudienceRequest):
                    The request object. Request message for UpdateAudience
                RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gaa_audience.Audience:
                    A resource message representing a GA4
                Audience.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1alpha/{audience.name=properties/*/audiences/*}",
                    "body": "audience",
                },
            ]
            request, metadata = self._interceptor.pre_update_audience(request, metadata)
            pb_request = analytics_admin.UpdateAudienceRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = gaa_audience.Audience()
            pb_resp = gaa_audience.Audience.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_audience(resp)
            return resp

    class _UpdateCalculatedMetric(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("UpdateCalculatedMetric")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
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
            request: analytics_admin.UpdateCalculatedMetricRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.CalculatedMetric:
            r"""Call the update calculated metric method over HTTP.

            Args:
                request (~.analytics_admin.UpdateCalculatedMetricRequest):
                    The request object. Request message for
                UpdateCalculatedMetric RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.CalculatedMetric:
                    A definition for a calculated metric.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1alpha/{calculated_metric.name=properties/*/calculatedMetrics/*}",
                    "body": "calculated_metric",
                },
            ]
            request, metadata = self._interceptor.pre_update_calculated_metric(
                request, metadata
            )
            pb_request = analytics_admin.UpdateCalculatedMetricRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.CalculatedMetric()
            pb_resp = resources.CalculatedMetric.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_calculated_metric(resp)
            return resp

    class _UpdateChannelGroup(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("UpdateChannelGroup")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
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
            request: analytics_admin.UpdateChannelGroupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gaa_channel_group.ChannelGroup:
            r"""Call the update channel group method over HTTP.

            Args:
                request (~.analytics_admin.UpdateChannelGroupRequest):
                    The request object. Request message for
                UpdateChannelGroup RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gaa_channel_group.ChannelGroup:
                    A resource message representing a
                Channel Group.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1alpha/{channel_group.name=properties/*/channelGroups/*}",
                    "body": "channel_group",
                },
            ]
            request, metadata = self._interceptor.pre_update_channel_group(
                request, metadata
            )
            pb_request = analytics_admin.UpdateChannelGroupRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = gaa_channel_group.ChannelGroup()
            pb_resp = gaa_channel_group.ChannelGroup.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_channel_group(resp)
            return resp

    class _UpdateConversionEvent(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("UpdateConversionEvent")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
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
            request: analytics_admin.UpdateConversionEventRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.ConversionEvent:
            r"""Call the update conversion event method over HTTP.

            Args:
                request (~.analytics_admin.UpdateConversionEventRequest):
                    The request object. Request message for
                UpdateConversionEvent RPC
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
                    "method": "patch",
                    "uri": "/v1alpha/{conversion_event.name=properties/*/conversionEvents/*}",
                    "body": "conversion_event",
                },
            ]
            request, metadata = self._interceptor.pre_update_conversion_event(
                request, metadata
            )
            pb_request = analytics_admin.UpdateConversionEventRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = self._interceptor.post_update_conversion_event(resp)
            return resp

    class _UpdateCustomDimension(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("UpdateCustomDimension")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{custom_dimension.name=properties/*/customDimensions/*}",
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
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{custom_metric.name=properties/*/customMetrics/*}",
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
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _UpdateDataRedactionSettings(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("UpdateDataRedactionSettings")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
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
            request: analytics_admin.UpdateDataRedactionSettingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.DataRedactionSettings:
            r"""Call the update data redaction
            settings method over HTTP.

                Args:
                    request (~.analytics_admin.UpdateDataRedactionSettingsRequest):
                        The request object. Request message for
                    UpdateDataRedactionSettings RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.DataRedactionSettings:
                        Settings for client-side data
                    redaction. Singleton resource under a
                    Web Stream.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1alpha/{data_redaction_settings.name=properties/*/dataStreams/*/dataRedactionSettings}",
                    "body": "data_redaction_settings",
                },
            ]
            request, metadata = self._interceptor.pre_update_data_redaction_settings(
                request, metadata
            )
            pb_request = analytics_admin.UpdateDataRedactionSettingsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.DataRedactionSettings()
            pb_resp = resources.DataRedactionSettings.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_data_redaction_settings(resp)
            return resp

    class _UpdateDataRetentionSettings(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("UpdateDataRetentionSettings")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{data_retention_settings.name=properties/*/dataRetentionSettings}",
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
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{data_stream.name=properties/*/dataStreams/*}",
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
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _UpdateDisplayVideo360AdvertiserLink(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("UpdateDisplayVideo360AdvertiserLink")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
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
            request: analytics_admin.UpdateDisplayVideo360AdvertiserLinkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.DisplayVideo360AdvertiserLink:
            r"""Call the update display video360
            advertiser link method over HTTP.

                Args:
                    request (~.analytics_admin.UpdateDisplayVideo360AdvertiserLinkRequest):
                        The request object. Request message for
                    UpdateDisplayVideo360AdvertiserLink RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.DisplayVideo360AdvertiserLink:
                        A link between a GA4 property and a
                    Display & Video 360 advertiser.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1alpha/{display_video_360_advertiser_link.name=properties/*/displayVideo360AdvertiserLinks/*}",
                    "body": "display_video_360_advertiser_link",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_update_display_video360_advertiser_link(
                request, metadata
            )
            pb_request = analytics_admin.UpdateDisplayVideo360AdvertiserLinkRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.DisplayVideo360AdvertiserLink()
            pb_resp = resources.DisplayVideo360AdvertiserLink.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_display_video360_advertiser_link(resp)
            return resp

    class _UpdateEnhancedMeasurementSettings(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("UpdateEnhancedMeasurementSettings")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
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
            request: analytics_admin.UpdateEnhancedMeasurementSettingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.EnhancedMeasurementSettings:
            r"""Call the update enhanced
            measurement settings method over HTTP.

                Args:
                    request (~.analytics_admin.UpdateEnhancedMeasurementSettingsRequest):
                        The request object. Request message for
                    UpdateEnhancedMeasurementSettings RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.EnhancedMeasurementSettings:
                        Singleton resource under a web
                    DataStream, configuring measurement of
                    additional site interactions and
                    content.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1alpha/{enhanced_measurement_settings.name=properties/*/dataStreams/*/enhancedMeasurementSettings}",
                    "body": "enhanced_measurement_settings",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_update_enhanced_measurement_settings(
                request, metadata
            )
            pb_request = analytics_admin.UpdateEnhancedMeasurementSettingsRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.EnhancedMeasurementSettings()
            pb_resp = resources.EnhancedMeasurementSettings.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_enhanced_measurement_settings(resp)
            return resp

    class _UpdateEventCreateRule(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("UpdateEventCreateRule")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
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
            request: analytics_admin.UpdateEventCreateRuleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> event_create_and_edit.EventCreateRule:
            r"""Call the update event create rule method over HTTP.

            Args:
                request (~.analytics_admin.UpdateEventCreateRuleRequest):
                    The request object. Request message for
                UpdateEventCreateRule RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.event_create_and_edit.EventCreateRule:
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1alpha/{event_create_rule.name=properties/*/dataStreams/*/eventCreateRules/*}",
                    "body": "event_create_rule",
                },
            ]
            request, metadata = self._interceptor.pre_update_event_create_rule(
                request, metadata
            )
            pb_request = analytics_admin.UpdateEventCreateRuleRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = event_create_and_edit.EventCreateRule()
            pb_resp = event_create_and_edit.EventCreateRule.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_event_create_rule(resp)
            return resp

    class _UpdateExpandedDataSet(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("UpdateExpandedDataSet")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
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
            request: analytics_admin.UpdateExpandedDataSetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gaa_expanded_data_set.ExpandedDataSet:
            r"""Call the update expanded data set method over HTTP.

            Args:
                request (~.analytics_admin.UpdateExpandedDataSetRequest):
                    The request object. Request message for
                UpdateExpandedDataSet RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gaa_expanded_data_set.ExpandedDataSet:
                    A resource message representing a GA4
                ExpandedDataSet.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1alpha/{expanded_data_set.name=properties/*/expandedDataSets/*}",
                    "body": "expanded_data_set",
                },
            ]
            request, metadata = self._interceptor.pre_update_expanded_data_set(
                request, metadata
            )
            pb_request = analytics_admin.UpdateExpandedDataSetRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = gaa_expanded_data_set.ExpandedDataSet()
            pb_resp = gaa_expanded_data_set.ExpandedDataSet.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_expanded_data_set(resp)
            return resp

    class _UpdateGoogleAdsLink(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("UpdateGoogleAdsLink")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{google_ads_link.name=properties/*/googleAdsLinks/*}",
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
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _UpdateGoogleSignalsSettings(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("UpdateGoogleSignalsSettings")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
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
            request: analytics_admin.UpdateGoogleSignalsSettingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.GoogleSignalsSettings:
            r"""Call the update google signals
            settings method over HTTP.

                Args:
                    request (~.analytics_admin.UpdateGoogleSignalsSettingsRequest):
                        The request object. Request message for
                    UpdateGoogleSignalsSettings RPC
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.GoogleSignalsSettings:
                        Settings values for Google Signals.
                    This is a singleton resource.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1alpha/{google_signals_settings.name=properties/*/googleSignalsSettings}",
                    "body": "google_signals_settings",
                },
            ]
            request, metadata = self._interceptor.pre_update_google_signals_settings(
                request, metadata
            )
            pb_request = analytics_admin.UpdateGoogleSignalsSettingsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.GoogleSignalsSettings()
            pb_resp = resources.GoogleSignalsSettings.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_google_signals_settings(resp)
            return resp

    class _UpdateMeasurementProtocolSecret(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("UpdateMeasurementProtocolSecret")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
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
            request: analytics_admin.UpdateMeasurementProtocolSecretRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{measurement_protocol_secret.name=properties/*/dataStreams/*/measurementProtocolSecrets/*}",
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
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
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
            timeout: Optional[float] = None,
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
                    "uri": "/v1alpha/{property.name=properties/*}",
                    "body": "property",
                },
            ]
            request, metadata = self._interceptor.pre_update_property(request, metadata)
            pb_request = analytics_admin.UpdatePropertyRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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

    class _UpdateSearchAds360Link(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("UpdateSearchAds360Link")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
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
            request: analytics_admin.UpdateSearchAds360LinkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.SearchAds360Link:
            r"""Call the update search ads360 link method over HTTP.

            Args:
                request (~.analytics_admin.UpdateSearchAds360LinkRequest):
                    The request object. Request message for
                UpdateSearchAds360Link RPC.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.SearchAds360Link:
                    A link between a GA4 property and a
                Search Ads 360 entity.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1alpha/{search_ads_360_link.name=properties/*/searchAds360Links/*}",
                    "body": "search_ads_360_link",
                },
            ]
            request, metadata = self._interceptor.pre_update_search_ads360_link(
                request, metadata
            )
            pb_request = analytics_admin.UpdateSearchAds360LinkRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.SearchAds360Link()
            pb_resp = resources.SearchAds360Link.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_search_ads360_link(resp)
            return resp

    class _UpdateSKAdNetworkConversionValueSchema(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("UpdateSKAdNetworkConversionValueSchema")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
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
            request: analytics_admin.UpdateSKAdNetworkConversionValueSchemaRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.SKAdNetworkConversionValueSchema:
            r"""Call the update sk ad network
            conversion value schema method over HTTP.

                Args:
                    request (~.analytics_admin.UpdateSKAdNetworkConversionValueSchemaRequest):
                        The request object. Request message for
                    UpdateSKAdNetworkConversionValueSchema
                    RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.SKAdNetworkConversionValueSchema:
                        SKAdNetwork conversion value schema
                    of an iOS stream.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1alpha/{skadnetwork_conversion_value_schema.name=properties/*/dataStreams/*/sKAdNetworkConversionValueSchema/*}",
                    "body": "skadnetwork_conversion_value_schema",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_update_sk_ad_network_conversion_value_schema(
                request, metadata
            )
            pb_request = (
                analytics_admin.UpdateSKAdNetworkConversionValueSchemaRequest.pb(
                    request
                )
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = resources.SKAdNetworkConversionValueSchema()
            pb_resp = resources.SKAdNetworkConversionValueSchema.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_sk_ad_network_conversion_value_schema(
                resp
            )
            return resp

    class _UpdateSubpropertyEventFilter(AnalyticsAdminServiceRestStub):
        def __hash__(self):
            return hash("UpdateSubpropertyEventFilter")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
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
            request: analytics_admin.UpdateSubpropertyEventFilterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gaa_subproperty_event_filter.SubpropertyEventFilter:
            r"""Call the update subproperty event
            filter method over HTTP.

                Args:
                    request (~.analytics_admin.UpdateSubpropertyEventFilterRequest):
                        The request object. Request message for
                    UpdateSubpropertyEventFilter RPC.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.gaa_subproperty_event_filter.SubpropertyEventFilter:
                        A resource message representing a GA4
                    Subproperty event filter.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1alpha/{subproperty_event_filter.name=properties/*/subpropertyEventFilters/*}",
                    "body": "subproperty_event_filter",
                },
            ]
            request, metadata = self._interceptor.pre_update_subproperty_event_filter(
                request, metadata
            )
            pb_request = analytics_admin.UpdateSubpropertyEventFilterRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

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
            resp = gaa_subproperty_event_filter.SubpropertyEventFilter()
            pb_resp = gaa_subproperty_event_filter.SubpropertyEventFilter.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_subproperty_event_filter(resp)
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
    def approve_display_video360_advertiser_link_proposal(
        self,
    ) -> Callable[
        [analytics_admin.ApproveDisplayVideo360AdvertiserLinkProposalRequest],
        analytics_admin.ApproveDisplayVideo360AdvertiserLinkProposalResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ApproveDisplayVideo360AdvertiserLinkProposal(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def archive_audience(
        self,
    ) -> Callable[[analytics_admin.ArchiveAudienceRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ArchiveAudience(self._session, self._host, self._interceptor)  # type: ignore

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
    def batch_create_access_bindings(
        self,
    ) -> Callable[
        [analytics_admin.BatchCreateAccessBindingsRequest],
        analytics_admin.BatchCreateAccessBindingsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchCreateAccessBindings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def batch_delete_access_bindings(
        self,
    ) -> Callable[[analytics_admin.BatchDeleteAccessBindingsRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchDeleteAccessBindings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def batch_get_access_bindings(
        self,
    ) -> Callable[
        [analytics_admin.BatchGetAccessBindingsRequest],
        analytics_admin.BatchGetAccessBindingsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchGetAccessBindings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def batch_update_access_bindings(
        self,
    ) -> Callable[
        [analytics_admin.BatchUpdateAccessBindingsRequest],
        analytics_admin.BatchUpdateAccessBindingsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchUpdateAccessBindings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def cancel_display_video360_advertiser_link_proposal(
        self,
    ) -> Callable[
        [analytics_admin.CancelDisplayVideo360AdvertiserLinkProposalRequest],
        resources.DisplayVideo360AdvertiserLinkProposal,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CancelDisplayVideo360AdvertiserLinkProposal(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_access_binding(
        self,
    ) -> Callable[
        [analytics_admin.CreateAccessBindingRequest], resources.AccessBinding
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAccessBinding(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_ad_sense_link(
        self,
    ) -> Callable[[analytics_admin.CreateAdSenseLinkRequest], resources.AdSenseLink]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAdSenseLink(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_audience(
        self,
    ) -> Callable[[analytics_admin.CreateAudienceRequest], gaa_audience.Audience]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAudience(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_calculated_metric(
        self,
    ) -> Callable[
        [analytics_admin.CreateCalculatedMetricRequest], resources.CalculatedMetric
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCalculatedMetric(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_channel_group(
        self,
    ) -> Callable[
        [analytics_admin.CreateChannelGroupRequest], gaa_channel_group.ChannelGroup
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateChannelGroup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_connected_site_tag(
        self,
    ) -> Callable[
        [analytics_admin.CreateConnectedSiteTagRequest],
        analytics_admin.CreateConnectedSiteTagResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateConnectedSiteTag(self._session, self._host, self._interceptor)  # type: ignore

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
    def create_display_video360_advertiser_link(
        self,
    ) -> Callable[
        [analytics_admin.CreateDisplayVideo360AdvertiserLinkRequest],
        resources.DisplayVideo360AdvertiserLink,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateDisplayVideo360AdvertiserLink(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_display_video360_advertiser_link_proposal(
        self,
    ) -> Callable[
        [analytics_admin.CreateDisplayVideo360AdvertiserLinkProposalRequest],
        resources.DisplayVideo360AdvertiserLinkProposal,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateDisplayVideo360AdvertiserLinkProposal(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_event_create_rule(
        self,
    ) -> Callable[
        [analytics_admin.CreateEventCreateRuleRequest],
        event_create_and_edit.EventCreateRule,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateEventCreateRule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_expanded_data_set(
        self,
    ) -> Callable[
        [analytics_admin.CreateExpandedDataSetRequest],
        gaa_expanded_data_set.ExpandedDataSet,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateExpandedDataSet(self._session, self._host, self._interceptor)  # type: ignore

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
    def create_rollup_property(
        self,
    ) -> Callable[
        [analytics_admin.CreateRollupPropertyRequest],
        analytics_admin.CreateRollupPropertyResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateRollupProperty(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_rollup_property_source_link(
        self,
    ) -> Callable[
        [analytics_admin.CreateRollupPropertySourceLinkRequest],
        resources.RollupPropertySourceLink,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateRollupPropertySourceLink(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_search_ads360_link(
        self,
    ) -> Callable[
        [analytics_admin.CreateSearchAds360LinkRequest], resources.SearchAds360Link
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateSearchAds360Link(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_sk_ad_network_conversion_value_schema(
        self,
    ) -> Callable[
        [analytics_admin.CreateSKAdNetworkConversionValueSchemaRequest],
        resources.SKAdNetworkConversionValueSchema,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateSKAdNetworkConversionValueSchema(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_subproperty(
        self,
    ) -> Callable[
        [analytics_admin.CreateSubpropertyRequest],
        analytics_admin.CreateSubpropertyResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateSubproperty(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_subproperty_event_filter(
        self,
    ) -> Callable[
        [analytics_admin.CreateSubpropertyEventFilterRequest],
        gaa_subproperty_event_filter.SubpropertyEventFilter,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateSubpropertyEventFilter(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_access_binding(
        self,
    ) -> Callable[[analytics_admin.DeleteAccessBindingRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAccessBinding(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_account(
        self,
    ) -> Callable[[analytics_admin.DeleteAccountRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAccount(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_ad_sense_link(
        self,
    ) -> Callable[[analytics_admin.DeleteAdSenseLinkRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAdSenseLink(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_calculated_metric(
        self,
    ) -> Callable[[analytics_admin.DeleteCalculatedMetricRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteCalculatedMetric(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_channel_group(
        self,
    ) -> Callable[[analytics_admin.DeleteChannelGroupRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteChannelGroup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_connected_site_tag(
        self,
    ) -> Callable[[analytics_admin.DeleteConnectedSiteTagRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteConnectedSiteTag(self._session, self._host, self._interceptor)  # type: ignore

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
    def delete_display_video360_advertiser_link(
        self,
    ) -> Callable[
        [analytics_admin.DeleteDisplayVideo360AdvertiserLinkRequest], empty_pb2.Empty
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteDisplayVideo360AdvertiserLink(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_display_video360_advertiser_link_proposal(
        self,
    ) -> Callable[
        [analytics_admin.DeleteDisplayVideo360AdvertiserLinkProposalRequest],
        empty_pb2.Empty,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteDisplayVideo360AdvertiserLinkProposal(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_event_create_rule(
        self,
    ) -> Callable[[analytics_admin.DeleteEventCreateRuleRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteEventCreateRule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_expanded_data_set(
        self,
    ) -> Callable[[analytics_admin.DeleteExpandedDataSetRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteExpandedDataSet(self._session, self._host, self._interceptor)  # type: ignore

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
    def delete_rollup_property_source_link(
        self,
    ) -> Callable[
        [analytics_admin.DeleteRollupPropertySourceLinkRequest], empty_pb2.Empty
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteRollupPropertySourceLink(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_search_ads360_link(
        self,
    ) -> Callable[[analytics_admin.DeleteSearchAds360LinkRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteSearchAds360Link(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_sk_ad_network_conversion_value_schema(
        self,
    ) -> Callable[
        [analytics_admin.DeleteSKAdNetworkConversionValueSchemaRequest], empty_pb2.Empty
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteSKAdNetworkConversionValueSchema(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_subproperty_event_filter(
        self,
    ) -> Callable[
        [analytics_admin.DeleteSubpropertyEventFilterRequest], empty_pb2.Empty
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteSubpropertyEventFilter(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def fetch_automated_ga4_configuration_opt_out(
        self,
    ) -> Callable[
        [analytics_admin.FetchAutomatedGa4ConfigurationOptOutRequest],
        analytics_admin.FetchAutomatedGa4ConfigurationOptOutResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FetchAutomatedGa4ConfigurationOptOut(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def fetch_connected_ga4_property(
        self,
    ) -> Callable[
        [analytics_admin.FetchConnectedGa4PropertyRequest],
        analytics_admin.FetchConnectedGa4PropertyResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FetchConnectedGa4Property(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_access_binding(
        self,
    ) -> Callable[[analytics_admin.GetAccessBindingRequest], resources.AccessBinding]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAccessBinding(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_account(
        self,
    ) -> Callable[[analytics_admin.GetAccountRequest], resources.Account]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAccount(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_ad_sense_link(
        self,
    ) -> Callable[[analytics_admin.GetAdSenseLinkRequest], resources.AdSenseLink]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAdSenseLink(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_attribution_settings(
        self,
    ) -> Callable[
        [analytics_admin.GetAttributionSettingsRequest], resources.AttributionSettings
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAttributionSettings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_audience(
        self,
    ) -> Callable[[analytics_admin.GetAudienceRequest], audience.Audience]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAudience(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_big_query_link(
        self,
    ) -> Callable[[analytics_admin.GetBigQueryLinkRequest], resources.BigQueryLink]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetBigQueryLink(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_calculated_metric(
        self,
    ) -> Callable[
        [analytics_admin.GetCalculatedMetricRequest], resources.CalculatedMetric
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCalculatedMetric(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_channel_group(
        self,
    ) -> Callable[[analytics_admin.GetChannelGroupRequest], channel_group.ChannelGroup]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetChannelGroup(self._session, self._host, self._interceptor)  # type: ignore

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
    def get_data_redaction_settings(
        self,
    ) -> Callable[
        [analytics_admin.GetDataRedactionSettingsRequest],
        resources.DataRedactionSettings,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDataRedactionSettings(self._session, self._host, self._interceptor)  # type: ignore

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
    def get_display_video360_advertiser_link(
        self,
    ) -> Callable[
        [analytics_admin.GetDisplayVideo360AdvertiserLinkRequest],
        resources.DisplayVideo360AdvertiserLink,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDisplayVideo360AdvertiserLink(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_display_video360_advertiser_link_proposal(
        self,
    ) -> Callable[
        [analytics_admin.GetDisplayVideo360AdvertiserLinkProposalRequest],
        resources.DisplayVideo360AdvertiserLinkProposal,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDisplayVideo360AdvertiserLinkProposal(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_enhanced_measurement_settings(
        self,
    ) -> Callable[
        [analytics_admin.GetEnhancedMeasurementSettingsRequest],
        resources.EnhancedMeasurementSettings,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetEnhancedMeasurementSettings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_event_create_rule(
        self,
    ) -> Callable[
        [analytics_admin.GetEventCreateRuleRequest],
        event_create_and_edit.EventCreateRule,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetEventCreateRule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_expanded_data_set(
        self,
    ) -> Callable[
        [analytics_admin.GetExpandedDataSetRequest], expanded_data_set.ExpandedDataSet
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetExpandedDataSet(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_global_site_tag(
        self,
    ) -> Callable[[analytics_admin.GetGlobalSiteTagRequest], resources.GlobalSiteTag]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetGlobalSiteTag(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_google_signals_settings(
        self,
    ) -> Callable[
        [analytics_admin.GetGoogleSignalsSettingsRequest],
        resources.GoogleSignalsSettings,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetGoogleSignalsSettings(self._session, self._host, self._interceptor)  # type: ignore

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
    def get_rollup_property_source_link(
        self,
    ) -> Callable[
        [analytics_admin.GetRollupPropertySourceLinkRequest],
        resources.RollupPropertySourceLink,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRollupPropertySourceLink(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_search_ads360_link(
        self,
    ) -> Callable[
        [analytics_admin.GetSearchAds360LinkRequest], resources.SearchAds360Link
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSearchAds360Link(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_sk_ad_network_conversion_value_schema(
        self,
    ) -> Callable[
        [analytics_admin.GetSKAdNetworkConversionValueSchemaRequest],
        resources.SKAdNetworkConversionValueSchema,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSKAdNetworkConversionValueSchema(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_subproperty_event_filter(
        self,
    ) -> Callable[
        [analytics_admin.GetSubpropertyEventFilterRequest],
        subproperty_event_filter.SubpropertyEventFilter,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSubpropertyEventFilter(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_access_bindings(
        self,
    ) -> Callable[
        [analytics_admin.ListAccessBindingsRequest],
        analytics_admin.ListAccessBindingsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAccessBindings(self._session, self._host, self._interceptor)  # type: ignore

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
    def list_ad_sense_links(
        self,
    ) -> Callable[
        [analytics_admin.ListAdSenseLinksRequest],
        analytics_admin.ListAdSenseLinksResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAdSenseLinks(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_audiences(
        self,
    ) -> Callable[
        [analytics_admin.ListAudiencesRequest], analytics_admin.ListAudiencesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAudiences(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_big_query_links(
        self,
    ) -> Callable[
        [analytics_admin.ListBigQueryLinksRequest],
        analytics_admin.ListBigQueryLinksResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListBigQueryLinks(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_calculated_metrics(
        self,
    ) -> Callable[
        [analytics_admin.ListCalculatedMetricsRequest],
        analytics_admin.ListCalculatedMetricsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCalculatedMetrics(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_channel_groups(
        self,
    ) -> Callable[
        [analytics_admin.ListChannelGroupsRequest],
        analytics_admin.ListChannelGroupsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListChannelGroups(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_connected_site_tags(
        self,
    ) -> Callable[
        [analytics_admin.ListConnectedSiteTagsRequest],
        analytics_admin.ListConnectedSiteTagsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListConnectedSiteTags(self._session, self._host, self._interceptor)  # type: ignore

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
    def list_display_video360_advertiser_link_proposals(
        self,
    ) -> Callable[
        [analytics_admin.ListDisplayVideo360AdvertiserLinkProposalsRequest],
        analytics_admin.ListDisplayVideo360AdvertiserLinkProposalsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDisplayVideo360AdvertiserLinkProposals(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_display_video360_advertiser_links(
        self,
    ) -> Callable[
        [analytics_admin.ListDisplayVideo360AdvertiserLinksRequest],
        analytics_admin.ListDisplayVideo360AdvertiserLinksResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDisplayVideo360AdvertiserLinks(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_event_create_rules(
        self,
    ) -> Callable[
        [analytics_admin.ListEventCreateRulesRequest],
        analytics_admin.ListEventCreateRulesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListEventCreateRules(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_expanded_data_sets(
        self,
    ) -> Callable[
        [analytics_admin.ListExpandedDataSetsRequest],
        analytics_admin.ListExpandedDataSetsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListExpandedDataSets(self._session, self._host, self._interceptor)  # type: ignore

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
    def list_rollup_property_source_links(
        self,
    ) -> Callable[
        [analytics_admin.ListRollupPropertySourceLinksRequest],
        analytics_admin.ListRollupPropertySourceLinksResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListRollupPropertySourceLinks(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_search_ads360_links(
        self,
    ) -> Callable[
        [analytics_admin.ListSearchAds360LinksRequest],
        analytics_admin.ListSearchAds360LinksResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSearchAds360Links(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_sk_ad_network_conversion_value_schemas(
        self,
    ) -> Callable[
        [analytics_admin.ListSKAdNetworkConversionValueSchemasRequest],
        analytics_admin.ListSKAdNetworkConversionValueSchemasResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSKAdNetworkConversionValueSchemas(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_subproperty_event_filters(
        self,
    ) -> Callable[
        [analytics_admin.ListSubpropertyEventFiltersRequest],
        analytics_admin.ListSubpropertyEventFiltersResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSubpropertyEventFilters(self._session, self._host, self._interceptor)  # type: ignore

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
    def run_access_report(
        self,
    ) -> Callable[
        [analytics_admin.RunAccessReportRequest],
        analytics_admin.RunAccessReportResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RunAccessReport(self._session, self._host, self._interceptor)  # type: ignore

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
    def set_automated_ga4_configuration_opt_out(
        self,
    ) -> Callable[
        [analytics_admin.SetAutomatedGa4ConfigurationOptOutRequest],
        analytics_admin.SetAutomatedGa4ConfigurationOptOutResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetAutomatedGa4ConfigurationOptOut(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_access_binding(
        self,
    ) -> Callable[
        [analytics_admin.UpdateAccessBindingRequest], resources.AccessBinding
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAccessBinding(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_account(
        self,
    ) -> Callable[[analytics_admin.UpdateAccountRequest], resources.Account]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAccount(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_attribution_settings(
        self,
    ) -> Callable[
        [analytics_admin.UpdateAttributionSettingsRequest],
        resources.AttributionSettings,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAttributionSettings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_audience(
        self,
    ) -> Callable[[analytics_admin.UpdateAudienceRequest], gaa_audience.Audience]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAudience(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_calculated_metric(
        self,
    ) -> Callable[
        [analytics_admin.UpdateCalculatedMetricRequest], resources.CalculatedMetric
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCalculatedMetric(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_channel_group(
        self,
    ) -> Callable[
        [analytics_admin.UpdateChannelGroupRequest], gaa_channel_group.ChannelGroup
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateChannelGroup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_conversion_event(
        self,
    ) -> Callable[
        [analytics_admin.UpdateConversionEventRequest], resources.ConversionEvent
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateConversionEvent(self._session, self._host, self._interceptor)  # type: ignore

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
    def update_data_redaction_settings(
        self,
    ) -> Callable[
        [analytics_admin.UpdateDataRedactionSettingsRequest],
        resources.DataRedactionSettings,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateDataRedactionSettings(self._session, self._host, self._interceptor)  # type: ignore

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
    def update_display_video360_advertiser_link(
        self,
    ) -> Callable[
        [analytics_admin.UpdateDisplayVideo360AdvertiserLinkRequest],
        resources.DisplayVideo360AdvertiserLink,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateDisplayVideo360AdvertiserLink(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_enhanced_measurement_settings(
        self,
    ) -> Callable[
        [analytics_admin.UpdateEnhancedMeasurementSettingsRequest],
        resources.EnhancedMeasurementSettings,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateEnhancedMeasurementSettings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_event_create_rule(
        self,
    ) -> Callable[
        [analytics_admin.UpdateEventCreateRuleRequest],
        event_create_and_edit.EventCreateRule,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateEventCreateRule(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_expanded_data_set(
        self,
    ) -> Callable[
        [analytics_admin.UpdateExpandedDataSetRequest],
        gaa_expanded_data_set.ExpandedDataSet,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateExpandedDataSet(self._session, self._host, self._interceptor)  # type: ignore

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
    def update_google_signals_settings(
        self,
    ) -> Callable[
        [analytics_admin.UpdateGoogleSignalsSettingsRequest],
        resources.GoogleSignalsSettings,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateGoogleSignalsSettings(self._session, self._host, self._interceptor)  # type: ignore

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
    def update_search_ads360_link(
        self,
    ) -> Callable[
        [analytics_admin.UpdateSearchAds360LinkRequest], resources.SearchAds360Link
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSearchAds360Link(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_sk_ad_network_conversion_value_schema(
        self,
    ) -> Callable[
        [analytics_admin.UpdateSKAdNetworkConversionValueSchemaRequest],
        resources.SKAdNetworkConversionValueSchema,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSKAdNetworkConversionValueSchema(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_subproperty_event_filter(
        self,
    ) -> Callable[
        [analytics_admin.UpdateSubpropertyEventFilterRequest],
        gaa_subproperty_event_filter.SubpropertyEventFilter,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSubpropertyEventFilter(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("AnalyticsAdminServiceRestTransport",)
