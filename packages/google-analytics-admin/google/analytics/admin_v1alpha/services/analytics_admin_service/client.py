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
from collections import OrderedDict
import os
import re
from typing import (
    Callable,
    Dict,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)
import warnings

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.analytics.admin_v1alpha import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore

from google.analytics.admin_v1alpha.services.analytics_admin_service import pagers
from google.analytics.admin_v1alpha.types import channel_group as gaa_channel_group
from google.analytics.admin_v1alpha.types import (
    expanded_data_set as gaa_expanded_data_set,
)
from google.analytics.admin_v1alpha.types import (
    subproperty_event_filter as gaa_subproperty_event_filter,
)
from google.analytics.admin_v1alpha.types import access_report, analytics_admin
from google.analytics.admin_v1alpha.types import audience
from google.analytics.admin_v1alpha.types import audience as gaa_audience
from google.analytics.admin_v1alpha.types import channel_group
from google.analytics.admin_v1alpha.types import event_create_and_edit
from google.analytics.admin_v1alpha.types import expanded_data_set
from google.analytics.admin_v1alpha.types import resources
from google.analytics.admin_v1alpha.types import subproperty_event_filter

from .transports.base import DEFAULT_CLIENT_INFO, AnalyticsAdminServiceTransport
from .transports.grpc import AnalyticsAdminServiceGrpcTransport
from .transports.grpc_asyncio import AnalyticsAdminServiceGrpcAsyncIOTransport
from .transports.rest import AnalyticsAdminServiceRestTransport


class AnalyticsAdminServiceClientMeta(type):
    """Metaclass for the AnalyticsAdminService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[AnalyticsAdminServiceTransport]]
    _transport_registry["grpc"] = AnalyticsAdminServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = AnalyticsAdminServiceGrpcAsyncIOTransport
    _transport_registry["rest"] = AnalyticsAdminServiceRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[AnalyticsAdminServiceTransport]:
        """Returns an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class AnalyticsAdminServiceClient(metaclass=AnalyticsAdminServiceClientMeta):
    """Service Interface for the Analytics Admin API (GA4)."""

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Converts api endpoint to mTLS endpoint.

        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    # Note: DEFAULT_ENDPOINT is deprecated. Use _DEFAULT_ENDPOINT_TEMPLATE instead.
    DEFAULT_ENDPOINT = "analyticsadmin.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    _DEFAULT_ENDPOINT_TEMPLATE = "analyticsadmin.{UNIVERSE_DOMAIN}"
    _DEFAULT_UNIVERSE = "googleapis.com"

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            AnalyticsAdminServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(info)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

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
            AnalyticsAdminServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> AnalyticsAdminServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            AnalyticsAdminServiceTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def access_binding_path(
        account: str,
        access_binding: str,
    ) -> str:
        """Returns a fully-qualified access_binding string."""
        return "accounts/{account}/accessBindings/{access_binding}".format(
            account=account,
            access_binding=access_binding,
        )

    @staticmethod
    def parse_access_binding_path(path: str) -> Dict[str, str]:
        """Parses a access_binding path into its component segments."""
        m = re.match(
            r"^accounts/(?P<account>.+?)/accessBindings/(?P<access_binding>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def account_path(
        account: str,
    ) -> str:
        """Returns a fully-qualified account string."""
        return "accounts/{account}".format(
            account=account,
        )

    @staticmethod
    def parse_account_path(path: str) -> Dict[str, str]:
        """Parses a account path into its component segments."""
        m = re.match(r"^accounts/(?P<account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def account_summary_path(
        account_summary: str,
    ) -> str:
        """Returns a fully-qualified account_summary string."""
        return "accountSummaries/{account_summary}".format(
            account_summary=account_summary,
        )

    @staticmethod
    def parse_account_summary_path(path: str) -> Dict[str, str]:
        """Parses a account_summary path into its component segments."""
        m = re.match(r"^accountSummaries/(?P<account_summary>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def ad_sense_link_path(
        property: str,
        adsense_link: str,
    ) -> str:
        """Returns a fully-qualified ad_sense_link string."""
        return "properties/{property}/adSenseLinks/{adsense_link}".format(
            property=property,
            adsense_link=adsense_link,
        )

    @staticmethod
    def parse_ad_sense_link_path(path: str) -> Dict[str, str]:
        """Parses a ad_sense_link path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/adSenseLinks/(?P<adsense_link>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def attribution_settings_path(
        property: str,
    ) -> str:
        """Returns a fully-qualified attribution_settings string."""
        return "properties/{property}/attributionSettings".format(
            property=property,
        )

    @staticmethod
    def parse_attribution_settings_path(path: str) -> Dict[str, str]:
        """Parses a attribution_settings path into its component segments."""
        m = re.match(r"^properties/(?P<property>.+?)/attributionSettings$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def audience_path(
        property: str,
        audience: str,
    ) -> str:
        """Returns a fully-qualified audience string."""
        return "properties/{property}/audiences/{audience}".format(
            property=property,
            audience=audience,
        )

    @staticmethod
    def parse_audience_path(path: str) -> Dict[str, str]:
        """Parses a audience path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/audiences/(?P<audience>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def big_query_link_path(
        property: str,
        bigquery_link: str,
    ) -> str:
        """Returns a fully-qualified big_query_link string."""
        return "properties/{property}/bigQueryLinks/{bigquery_link}".format(
            property=property,
            bigquery_link=bigquery_link,
        )

    @staticmethod
    def parse_big_query_link_path(path: str) -> Dict[str, str]:
        """Parses a big_query_link path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/bigQueryLinks/(?P<bigquery_link>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def calculated_metric_path(
        property: str,
        calculated_metric: str,
    ) -> str:
        """Returns a fully-qualified calculated_metric string."""
        return "properties/{property}/calculatedMetrics/{calculated_metric}".format(
            property=property,
            calculated_metric=calculated_metric,
        )

    @staticmethod
    def parse_calculated_metric_path(path: str) -> Dict[str, str]:
        """Parses a calculated_metric path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/calculatedMetrics/(?P<calculated_metric>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def channel_group_path(
        property: str,
        channel_group: str,
    ) -> str:
        """Returns a fully-qualified channel_group string."""
        return "properties/{property}/channelGroups/{channel_group}".format(
            property=property,
            channel_group=channel_group,
        )

    @staticmethod
    def parse_channel_group_path(path: str) -> Dict[str, str]:
        """Parses a channel_group path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/channelGroups/(?P<channel_group>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def conversion_event_path(
        property: str,
        conversion_event: str,
    ) -> str:
        """Returns a fully-qualified conversion_event string."""
        return "properties/{property}/conversionEvents/{conversion_event}".format(
            property=property,
            conversion_event=conversion_event,
        )

    @staticmethod
    def parse_conversion_event_path(path: str) -> Dict[str, str]:
        """Parses a conversion_event path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/conversionEvents/(?P<conversion_event>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def custom_dimension_path(
        property: str,
        custom_dimension: str,
    ) -> str:
        """Returns a fully-qualified custom_dimension string."""
        return "properties/{property}/customDimensions/{custom_dimension}".format(
            property=property,
            custom_dimension=custom_dimension,
        )

    @staticmethod
    def parse_custom_dimension_path(path: str) -> Dict[str, str]:
        """Parses a custom_dimension path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/customDimensions/(?P<custom_dimension>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def custom_metric_path(
        property: str,
        custom_metric: str,
    ) -> str:
        """Returns a fully-qualified custom_metric string."""
        return "properties/{property}/customMetrics/{custom_metric}".format(
            property=property,
            custom_metric=custom_metric,
        )

    @staticmethod
    def parse_custom_metric_path(path: str) -> Dict[str, str]:
        """Parses a custom_metric path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/customMetrics/(?P<custom_metric>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def data_redaction_settings_path(
        property: str,
        data_stream: str,
    ) -> str:
        """Returns a fully-qualified data_redaction_settings string."""
        return "properties/{property}/dataStreams/{data_stream}/dataRedactionSettings".format(
            property=property,
            data_stream=data_stream,
        )

    @staticmethod
    def parse_data_redaction_settings_path(path: str) -> Dict[str, str]:
        """Parses a data_redaction_settings path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/dataStreams/(?P<data_stream>.+?)/dataRedactionSettings$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def data_retention_settings_path(
        property: str,
    ) -> str:
        """Returns a fully-qualified data_retention_settings string."""
        return "properties/{property}/dataRetentionSettings".format(
            property=property,
        )

    @staticmethod
    def parse_data_retention_settings_path(path: str) -> Dict[str, str]:
        """Parses a data_retention_settings path into its component segments."""
        m = re.match(r"^properties/(?P<property>.+?)/dataRetentionSettings$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def data_sharing_settings_path(
        account: str,
    ) -> str:
        """Returns a fully-qualified data_sharing_settings string."""
        return "accounts/{account}/dataSharingSettings".format(
            account=account,
        )

    @staticmethod
    def parse_data_sharing_settings_path(path: str) -> Dict[str, str]:
        """Parses a data_sharing_settings path into its component segments."""
        m = re.match(r"^accounts/(?P<account>.+?)/dataSharingSettings$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def data_stream_path(
        property: str,
        data_stream: str,
    ) -> str:
        """Returns a fully-qualified data_stream string."""
        return "properties/{property}/dataStreams/{data_stream}".format(
            property=property,
            data_stream=data_stream,
        )

    @staticmethod
    def parse_data_stream_path(path: str) -> Dict[str, str]:
        """Parses a data_stream path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/dataStreams/(?P<data_stream>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def display_video360_advertiser_link_path(
        property: str,
        display_video_360_advertiser_link: str,
    ) -> str:
        """Returns a fully-qualified display_video360_advertiser_link string."""
        return "properties/{property}/displayVideo360AdvertiserLinks/{display_video_360_advertiser_link}".format(
            property=property,
            display_video_360_advertiser_link=display_video_360_advertiser_link,
        )

    @staticmethod
    def parse_display_video360_advertiser_link_path(path: str) -> Dict[str, str]:
        """Parses a display_video360_advertiser_link path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/displayVideo360AdvertiserLinks/(?P<display_video_360_advertiser_link>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def display_video360_advertiser_link_proposal_path(
        property: str,
        display_video_360_advertiser_link_proposal: str,
    ) -> str:
        """Returns a fully-qualified display_video360_advertiser_link_proposal string."""
        return "properties/{property}/displayVideo360AdvertiserLinkProposals/{display_video_360_advertiser_link_proposal}".format(
            property=property,
            display_video_360_advertiser_link_proposal=display_video_360_advertiser_link_proposal,
        )

    @staticmethod
    def parse_display_video360_advertiser_link_proposal_path(
        path: str,
    ) -> Dict[str, str]:
        """Parses a display_video360_advertiser_link_proposal path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/displayVideo360AdvertiserLinkProposals/(?P<display_video_360_advertiser_link_proposal>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def enhanced_measurement_settings_path(
        property: str,
        data_stream: str,
    ) -> str:
        """Returns a fully-qualified enhanced_measurement_settings string."""
        return "properties/{property}/dataStreams/{data_stream}/enhancedMeasurementSettings".format(
            property=property,
            data_stream=data_stream,
        )

    @staticmethod
    def parse_enhanced_measurement_settings_path(path: str) -> Dict[str, str]:
        """Parses a enhanced_measurement_settings path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/dataStreams/(?P<data_stream>.+?)/enhancedMeasurementSettings$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def event_create_rule_path(
        property: str,
        data_stream: str,
        event_create_rule: str,
    ) -> str:
        """Returns a fully-qualified event_create_rule string."""
        return "properties/{property}/dataStreams/{data_stream}/eventCreateRules/{event_create_rule}".format(
            property=property,
            data_stream=data_stream,
            event_create_rule=event_create_rule,
        )

    @staticmethod
    def parse_event_create_rule_path(path: str) -> Dict[str, str]:
        """Parses a event_create_rule path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/dataStreams/(?P<data_stream>.+?)/eventCreateRules/(?P<event_create_rule>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def event_edit_rule_path(
        property: str,
        data_stream: str,
        event_edit_rule: str,
    ) -> str:
        """Returns a fully-qualified event_edit_rule string."""
        return "properties/{property}/dataStreams/{data_stream}/eventEditRules/{event_edit_rule}".format(
            property=property,
            data_stream=data_stream,
            event_edit_rule=event_edit_rule,
        )

    @staticmethod
    def parse_event_edit_rule_path(path: str) -> Dict[str, str]:
        """Parses a event_edit_rule path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/dataStreams/(?P<data_stream>.+?)/eventEditRules/(?P<event_edit_rule>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def expanded_data_set_path(
        property: str,
        expanded_data_set: str,
    ) -> str:
        """Returns a fully-qualified expanded_data_set string."""
        return "properties/{property}/expandedDataSets/{expanded_data_set}".format(
            property=property,
            expanded_data_set=expanded_data_set,
        )

    @staticmethod
    def parse_expanded_data_set_path(path: str) -> Dict[str, str]:
        """Parses a expanded_data_set path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/expandedDataSets/(?P<expanded_data_set>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def firebase_link_path(
        property: str,
        firebase_link: str,
    ) -> str:
        """Returns a fully-qualified firebase_link string."""
        return "properties/{property}/firebaseLinks/{firebase_link}".format(
            property=property,
            firebase_link=firebase_link,
        )

    @staticmethod
    def parse_firebase_link_path(path: str) -> Dict[str, str]:
        """Parses a firebase_link path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/firebaseLinks/(?P<firebase_link>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def global_site_tag_path(
        property: str,
        data_stream: str,
    ) -> str:
        """Returns a fully-qualified global_site_tag string."""
        return "properties/{property}/dataStreams/{data_stream}/globalSiteTag".format(
            property=property,
            data_stream=data_stream,
        )

    @staticmethod
    def parse_global_site_tag_path(path: str) -> Dict[str, str]:
        """Parses a global_site_tag path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/dataStreams/(?P<data_stream>.+?)/globalSiteTag$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def google_ads_link_path(
        property: str,
        google_ads_link: str,
    ) -> str:
        """Returns a fully-qualified google_ads_link string."""
        return "properties/{property}/googleAdsLinks/{google_ads_link}".format(
            property=property,
            google_ads_link=google_ads_link,
        )

    @staticmethod
    def parse_google_ads_link_path(path: str) -> Dict[str, str]:
        """Parses a google_ads_link path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/googleAdsLinks/(?P<google_ads_link>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def google_signals_settings_path(
        property: str,
    ) -> str:
        """Returns a fully-qualified google_signals_settings string."""
        return "properties/{property}/googleSignalsSettings".format(
            property=property,
        )

    @staticmethod
    def parse_google_signals_settings_path(path: str) -> Dict[str, str]:
        """Parses a google_signals_settings path into its component segments."""
        m = re.match(r"^properties/(?P<property>.+?)/googleSignalsSettings$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def key_event_path(
        property: str,
        key_event: str,
    ) -> str:
        """Returns a fully-qualified key_event string."""
        return "properties/{property}/keyEvents/{key_event}".format(
            property=property,
            key_event=key_event,
        )

    @staticmethod
    def parse_key_event_path(path: str) -> Dict[str, str]:
        """Parses a key_event path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/keyEvents/(?P<key_event>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def measurement_protocol_secret_path(
        property: str,
        data_stream: str,
        measurement_protocol_secret: str,
    ) -> str:
        """Returns a fully-qualified measurement_protocol_secret string."""
        return "properties/{property}/dataStreams/{data_stream}/measurementProtocolSecrets/{measurement_protocol_secret}".format(
            property=property,
            data_stream=data_stream,
            measurement_protocol_secret=measurement_protocol_secret,
        )

    @staticmethod
    def parse_measurement_protocol_secret_path(path: str) -> Dict[str, str]:
        """Parses a measurement_protocol_secret path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/dataStreams/(?P<data_stream>.+?)/measurementProtocolSecrets/(?P<measurement_protocol_secret>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def organization_path(
        organization: str,
    ) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(
            organization=organization,
        )

    @staticmethod
    def parse_organization_path(path: str) -> Dict[str, str]:
        """Parses a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def property_path(
        property: str,
    ) -> str:
        """Returns a fully-qualified property string."""
        return "properties/{property}".format(
            property=property,
        )

    @staticmethod
    def parse_property_path(path: str) -> Dict[str, str]:
        """Parses a property path into its component segments."""
        m = re.match(r"^properties/(?P<property>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def rollup_property_source_link_path(
        property: str,
        rollup_property_source_link: str,
    ) -> str:
        """Returns a fully-qualified rollup_property_source_link string."""
        return "properties/{property}/rollupPropertySourceLinks/{rollup_property_source_link}".format(
            property=property,
            rollup_property_source_link=rollup_property_source_link,
        )

    @staticmethod
    def parse_rollup_property_source_link_path(path: str) -> Dict[str, str]:
        """Parses a rollup_property_source_link path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/rollupPropertySourceLinks/(?P<rollup_property_source_link>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def search_ads360_link_path(
        property: str,
        search_ads_360_link: str,
    ) -> str:
        """Returns a fully-qualified search_ads360_link string."""
        return "properties/{property}/searchAds360Links/{search_ads_360_link}".format(
            property=property,
            search_ads_360_link=search_ads_360_link,
        )

    @staticmethod
    def parse_search_ads360_link_path(path: str) -> Dict[str, str]:
        """Parses a search_ads360_link path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/searchAds360Links/(?P<search_ads_360_link>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def sk_ad_network_conversion_value_schema_path(
        property: str,
        data_stream: str,
        skadnetwork_conversion_value_schema: str,
    ) -> str:
        """Returns a fully-qualified sk_ad_network_conversion_value_schema string."""
        return "properties/{property}/dataStreams/{data_stream}/sKAdNetworkConversionValueSchema/{skadnetwork_conversion_value_schema}".format(
            property=property,
            data_stream=data_stream,
            skadnetwork_conversion_value_schema=skadnetwork_conversion_value_schema,
        )

    @staticmethod
    def parse_sk_ad_network_conversion_value_schema_path(path: str) -> Dict[str, str]:
        """Parses a sk_ad_network_conversion_value_schema path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/dataStreams/(?P<data_stream>.+?)/sKAdNetworkConversionValueSchema/(?P<skadnetwork_conversion_value_schema>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def subproperty_event_filter_path(
        property: str,
        sub_property_event_filter: str,
    ) -> str:
        """Returns a fully-qualified subproperty_event_filter string."""
        return "properties/{property}/subpropertyEventFilters/{sub_property_event_filter}".format(
            property=property,
            sub_property_event_filter=sub_property_event_filter,
        )

    @staticmethod
    def parse_subproperty_event_filter_path(path: str) -> Dict[str, str]:
        """Parses a subproperty_event_filter path into its component segments."""
        m = re.match(
            r"^properties/(?P<property>.+?)/subpropertyEventFilters/(?P<sub_property_event_filter>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(
        billing_account: str,
    ) -> str:
        """Returns a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(
            billing_account=billing_account,
        )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str, str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(
        folder: str,
    ) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(
            folder=folder,
        )

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(
        organization: str,
    ) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(
            organization=organization,
        )

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(
        project: str,
    ) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(
            project=project,
        )

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(
        project: str,
        location: str,
    ) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project,
            location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[client_options_lib.ClientOptions] = None
    ):
        """Deprecated. Return the API endpoint and client cert source for mutual TLS.

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

        warnings.warn(
            "get_mtls_endpoint_and_cert_source is deprecated. Use the api_endpoint property instead.",
            DeprecationWarning,
        )
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        use_client_cert = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
        if use_client_cert not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
            )
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError(
                "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
            )

        # Figure out the client cert source to use.
        client_cert_source = None
        if use_client_cert == "true":
            if client_options.client_cert_source:
                client_cert_source = client_options.client_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        elif use_mtls_endpoint == "always" or (
            use_mtls_endpoint == "auto" and client_cert_source
        ):
            api_endpoint = cls.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = cls.DEFAULT_ENDPOINT

        return api_endpoint, client_cert_source

    @staticmethod
    def _read_environment_variables():
        """Returns the environment variables used by the client.

        Returns:
            Tuple[bool, str, str]: returns the GOOGLE_API_USE_CLIENT_CERTIFICATE,
            GOOGLE_API_USE_MTLS_ENDPOINT, and GOOGLE_CLOUD_UNIVERSE_DOMAIN environment variables.

        Raises:
            ValueError: If GOOGLE_API_USE_CLIENT_CERTIFICATE is not
                any of ["true", "false"].
            google.auth.exceptions.MutualTLSChannelError: If GOOGLE_API_USE_MTLS_ENDPOINT
                is not any of ["auto", "never", "always"].
        """
        use_client_cert = os.getenv(
            "GOOGLE_API_USE_CLIENT_CERTIFICATE", "false"
        ).lower()
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto").lower()
        universe_domain_env = os.getenv("GOOGLE_CLOUD_UNIVERSE_DOMAIN")
        if use_client_cert not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
            )
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError(
                "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
            )
        return use_client_cert == "true", use_mtls_endpoint, universe_domain_env

    @staticmethod
    def _get_client_cert_source(provided_cert_source, use_cert_flag):
        """Return the client cert source to be used by the client.

        Args:
            provided_cert_source (bytes): The client certificate source provided.
            use_cert_flag (bool): A flag indicating whether to use the client certificate.

        Returns:
            bytes or None: The client cert source to be used by the client.
        """
        client_cert_source = None
        if use_cert_flag:
            if provided_cert_source:
                client_cert_source = provided_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()
        return client_cert_source

    @staticmethod
    def _get_api_endpoint(
        api_override, client_cert_source, universe_domain, use_mtls_endpoint
    ):
        """Return the API endpoint used by the client.

        Args:
            api_override (str): The API endpoint override. If specified, this is always
                the return value of this function and the other arguments are not used.
            client_cert_source (bytes): The client certificate source used by the client.
            universe_domain (str): The universe domain used by the client.
            use_mtls_endpoint (str): How to use the mTLS endpoint, which depends also on the other parameters.
                Possible values are "always", "auto", or "never".

        Returns:
            str: The API endpoint to be used by the client.
        """
        if api_override is not None:
            api_endpoint = api_override
        elif use_mtls_endpoint == "always" or (
            use_mtls_endpoint == "auto" and client_cert_source
        ):
            _default_universe = AnalyticsAdminServiceClient._DEFAULT_UNIVERSE
            if universe_domain != _default_universe:
                raise MutualTLSChannelError(
                    f"mTLS is not supported in any universe other than {_default_universe}."
                )
            api_endpoint = AnalyticsAdminServiceClient.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = (
                AnalyticsAdminServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=universe_domain
                )
            )
        return api_endpoint

    @staticmethod
    def _get_universe_domain(
        client_universe_domain: Optional[str], universe_domain_env: Optional[str]
    ) -> str:
        """Return the universe domain used by the client.

        Args:
            client_universe_domain (Optional[str]): The universe domain configured via the client options.
            universe_domain_env (Optional[str]): The universe domain configured via the "GOOGLE_CLOUD_UNIVERSE_DOMAIN" environment variable.

        Returns:
            str: The universe domain to be used by the client.

        Raises:
            ValueError: If the universe domain is an empty string.
        """
        universe_domain = AnalyticsAdminServiceClient._DEFAULT_UNIVERSE
        if client_universe_domain is not None:
            universe_domain = client_universe_domain
        elif universe_domain_env is not None:
            universe_domain = universe_domain_env
        if len(universe_domain.strip()) == 0:
            raise ValueError("Universe Domain cannot be an empty string.")
        return universe_domain

    def _validate_universe_domain(self):
        """Validates client's and credentials' universe domains are consistent.

        Returns:
            bool: True iff the configured universe domain is valid.

        Raises:
            ValueError: If the configured universe domain is not valid.
        """

        # NOTE (b/349488459): universe validation is disabled until further notice.
        return True

    @property
    def api_endpoint(self):
        """Return the API endpoint used by the client instance.

        Returns:
            str: The API endpoint used by the client instance.
        """
        return self._api_endpoint

    @property
    def universe_domain(self) -> str:
        """Return the universe domain used by the client instance.

        Returns:
            str: The universe domain used by the client instance.
        """
        return self._universe_domain

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[
            Union[
                str,
                AnalyticsAdminServiceTransport,
                Callable[..., AnalyticsAdminServiceTransport],
            ]
        ] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the analytics admin service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,AnalyticsAdminServiceTransport,Callable[..., AnalyticsAdminServiceTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the AnalyticsAdminServiceTransport constructor.
                If set to None, a transport is chosen automatically.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]):
                Custom options for the client.

                1. The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client when ``transport`` is
                not explicitly provided. Only if this property is not set and
                ``transport`` was not explicitly provided, the endpoint is
                determined by the GOOGLE_API_USE_MTLS_ENDPOINT environment
                variable, which have one of the following values:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto-switch to the
                default mTLS endpoint if client certificate is present; this is
                the default value).

                2. If the GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide a client certificate for mTLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

                3. The ``universe_domain`` property can be used to override the
                default "googleapis.com" universe. Note that the ``api_endpoint``
                property still takes precedence; and ``universe_domain`` is
                currently not supported for mTLS.

            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client_options = client_options
        if isinstance(self._client_options, dict):
            self._client_options = client_options_lib.from_dict(self._client_options)
        if self._client_options is None:
            self._client_options = client_options_lib.ClientOptions()
        self._client_options = cast(
            client_options_lib.ClientOptions, self._client_options
        )

        universe_domain_opt = getattr(self._client_options, "universe_domain", None)

        (
            self._use_client_cert,
            self._use_mtls_endpoint,
            self._universe_domain_env,
        ) = AnalyticsAdminServiceClient._read_environment_variables()
        self._client_cert_source = AnalyticsAdminServiceClient._get_client_cert_source(
            self._client_options.client_cert_source, self._use_client_cert
        )
        self._universe_domain = AnalyticsAdminServiceClient._get_universe_domain(
            universe_domain_opt, self._universe_domain_env
        )
        self._api_endpoint = None  # updated below, depending on `transport`

        # Initialize the universe domain validation.
        self._is_universe_domain_valid = False

        api_key_value = getattr(self._client_options, "api_key", None)
        if api_key_value and credentials:
            raise ValueError(
                "client_options.api_key and credentials are mutually exclusive"
            )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        transport_provided = isinstance(transport, AnalyticsAdminServiceTransport)
        if transport_provided:
            # transport is a AnalyticsAdminServiceTransport instance.
            if credentials or self._client_options.credentials_file or api_key_value:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if self._client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = cast(AnalyticsAdminServiceTransport, transport)
            self._api_endpoint = self._transport.host

        self._api_endpoint = (
            self._api_endpoint
            or AnalyticsAdminServiceClient._get_api_endpoint(
                self._client_options.api_endpoint,
                self._client_cert_source,
                self._universe_domain,
                self._use_mtls_endpoint,
            )
        )

        if not transport_provided:
            import google.auth._default  # type: ignore

            if api_key_value and hasattr(
                google.auth._default, "get_api_key_credentials"
            ):
                credentials = google.auth._default.get_api_key_credentials(
                    api_key_value
                )

            transport_init: Union[
                Type[AnalyticsAdminServiceTransport],
                Callable[..., AnalyticsAdminServiceTransport],
            ] = (
                AnalyticsAdminServiceClient.get_transport_class(transport)
                if isinstance(transport, str) or transport is None
                else cast(Callable[..., AnalyticsAdminServiceTransport], transport)
            )
            # initialize with the provided callable or the passed in class
            self._transport = transport_init(
                credentials=credentials,
                credentials_file=self._client_options.credentials_file,
                host=self._api_endpoint,
                scopes=self._client_options.scopes,
                client_cert_source_for_mtls=self._client_cert_source,
                quota_project_id=self._client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=True,
                api_audience=self._client_options.api_audience,
            )

    def get_account(
        self,
        request: Optional[Union[analytics_admin.GetAccountRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Account:
        r"""Lookup for a single Account.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetAccountRequest, dict]):
                The request object. Request message for GetAccount RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.GetAccountRequest):
            request = analytics_admin.GetAccountRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_account]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_accounts(
        self,
        request: Optional[Union[analytics_admin.ListAccountsRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAccountsPager:
        r"""Returns all accounts accessible by the caller.

        Note that these accounts might not currently have GA4
        properties. Soft-deleted (ie: "trashed") accounts are
        excluded by default. Returns an empty list if no
        relevant accounts are found.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ListAccountsRequest, dict]):
                The request object. Request message for ListAccounts RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListAccountsPager:
                Request message for ListAccounts RPC.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.ListAccountsRequest):
            request = analytics_admin.ListAccountsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_accounts]

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListAccountsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_account(
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
        Properties, GoogleAdsLinks, Streams, AccessBindings)
        will be permanently purged.
        https://support.google.com/analytics/answer/6154772

        Returns an error if the target is not found.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.DeleteAccountRequest, dict]):
                The request object. Request message for DeleteAccount
                RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.DeleteAccountRequest):
            request = analytics_admin.DeleteAccountRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_account]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def update_account(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.UpdateAccountRequest, dict]):
                The request object. Request message for UpdateAccount
                RPC.
            account (google.analytics.admin_v1alpha.types.Account):
                Required. The account to update. The account's ``name``
                field is used to identify the account.

                This corresponds to the ``account`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([account, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.UpdateAccountRequest):
            request = analytics_admin.UpdateAccountRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if account is not None:
                request.account = account
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_account]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("account.name", request.account.name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def provision_account_ticket(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ProvisionAccountTicketRequest, dict]):
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
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.ProvisionAccountTicketRequest):
            request = analytics_admin.ProvisionAccountTicketRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.provision_account_ticket]

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_account_summaries(
        self,
        request: Optional[
            Union[analytics_admin.ListAccountSummariesRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAccountSummariesPager:
        r"""Returns summaries of all accounts accessible by the
        caller.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ListAccountSummariesRequest, dict]):
                The request object. Request message for
                ListAccountSummaries RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListAccountSummariesPager:
                Response message for
                ListAccountSummaries RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.ListAccountSummariesRequest):
            request = analytics_admin.ListAccountSummariesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_account_summaries]

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListAccountSummariesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_property(
        self,
        request: Optional[Union[analytics_admin.GetPropertyRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Property:
        r"""Lookup for a single "GA4" Property.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetPropertyRequest, dict]):
                The request object. Request message for GetProperty RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.GetPropertyRequest):
            request = analytics_admin.GetPropertyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_property]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_properties(
        self,
        request: Optional[Union[analytics_admin.ListPropertiesRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListPropertiesPager:
        r"""Returns child Properties under the specified parent
        Account.
        Only "GA4" properties will be returned.
        Properties will be excluded if the caller does not have
        access. Soft-deleted (ie: "trashed") properties are
        excluded by default. Returns an empty list if no
        relevant properties are found.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ListPropertiesRequest, dict]):
                The request object. Request message for ListProperties
                RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListPropertiesPager:
                Response message for ListProperties
                RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.ListPropertiesRequest):
            request = analytics_admin.ListPropertiesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_properties]

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListPropertiesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_property(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.CreatePropertyRequest, dict]):
                The request object. Request message for CreateProperty
                RPC.
            property (google.analytics.admin_v1alpha.types.Property):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([property])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.CreatePropertyRequest):
            request = analytics_admin.CreatePropertyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if property is not None:
                request.property = property

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_property]

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_property(
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
        GoogleAdsLinks, Streams, AccessBindings) will be
        permanently purged.
        https://support.google.com/analytics/answer/6154772

        Returns an error if the target is not found, or is not a
        GA4 Property.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.DeletePropertyRequest, dict]):
                The request object. Request message for DeleteProperty
                RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.DeletePropertyRequest):
            request = analytics_admin.DeletePropertyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_property]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_property(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.UpdatePropertyRequest, dict]):
                The request object. Request message for UpdateProperty
                RPC.
            property (google.analytics.admin_v1alpha.types.Property):
                Required. The property to update. The property's
                ``name`` field is used to identify the property to be
                updated.

                This corresponds to the ``property`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([property, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.UpdatePropertyRequest):
            request = analytics_admin.UpdatePropertyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if property is not None:
                request.property = property
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_property]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("property.name", request.property.name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_firebase_link(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.CreateFirebaseLinkRequest, dict]):
                The request object. Request message for
                CreateFirebaseLink RPC
            parent (str):
                Required. Format: properties/{property_id}

                Example: ``properties/1234``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            firebase_link (google.analytics.admin_v1alpha.types.FirebaseLink):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, firebase_link])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.CreateFirebaseLinkRequest):
            request = analytics_admin.CreateFirebaseLinkRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if firebase_link is not None:
                request.firebase_link = firebase_link

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_firebase_link]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_firebase_link(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.DeleteFirebaseLinkRequest, dict]):
                The request object. Request message for
                DeleteFirebaseLink RPC
            name (str):
                Required. Format:
                properties/{property_id}/firebaseLinks/{firebase_link_id}

                Example: ``properties/1234/firebaseLinks/5678``

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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.DeleteFirebaseLinkRequest):
            request = analytics_admin.DeleteFirebaseLinkRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_firebase_link]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def list_firebase_links(
        self,
        request: Optional[Union[analytics_admin.ListFirebaseLinksRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListFirebaseLinksPager:
        r"""Lists FirebaseLinks on a property.
        Properties can have at most one FirebaseLink.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ListFirebaseLinksRequest, dict]):
                The request object. Request message for ListFirebaseLinks
                RPC
            parent (str):
                Required. Format: properties/{property_id}

                Example: ``properties/1234``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListFirebaseLinksPager:
                Response message for
                ListFirebaseLinks RPC
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.ListFirebaseLinksRequest):
            request = analytics_admin.ListFirebaseLinksRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_firebase_links]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListFirebaseLinksPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_global_site_tag(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetGlobalSiteTagRequest, dict]):
                The request object. Request message for GetGlobalSiteTag
                RPC.
            name (str):
                Required. The name of the site tag to lookup. Note that
                site tags are singletons and do not have unique IDs.
                Format:
                properties/{property_id}/dataStreams/{stream_id}/globalSiteTag

                Example:
                ``properties/123/dataStreams/456/globalSiteTag``

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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.GetGlobalSiteTagRequest):
            request = analytics_admin.GetGlobalSiteTagRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_global_site_tag]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_google_ads_link(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.CreateGoogleAdsLinkRequest, dict]):
                The request object. Request message for
                CreateGoogleAdsLink RPC
            parent (str):
                Required. Example format:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            google_ads_link (google.analytics.admin_v1alpha.types.GoogleAdsLink):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, google_ads_link])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.CreateGoogleAdsLinkRequest):
            request = analytics_admin.CreateGoogleAdsLinkRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if google_ads_link is not None:
                request.google_ads_link = google_ads_link

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_google_ads_link]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_google_ads_link(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.UpdateGoogleAdsLinkRequest, dict]):
                The request object. Request message for
                UpdateGoogleAdsLink RPC
            google_ads_link (google.analytics.admin_v1alpha.types.GoogleAdsLink):
                The GoogleAdsLink to update
                This corresponds to the ``google_ads_link`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([google_ads_link, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.UpdateGoogleAdsLinkRequest):
            request = analytics_admin.UpdateGoogleAdsLinkRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if google_ads_link is not None:
                request.google_ads_link = google_ads_link
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_google_ads_link]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("google_ads_link.name", request.google_ads_link.name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_google_ads_link(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.DeleteGoogleAdsLinkRequest, dict]):
                The request object. Request message for
                DeleteGoogleAdsLink RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.DeleteGoogleAdsLinkRequest):
            request = analytics_admin.DeleteGoogleAdsLinkRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_google_ads_link]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def list_google_ads_links(
        self,
        request: Optional[
            Union[analytics_admin.ListGoogleAdsLinksRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListGoogleAdsLinksPager:
        r"""Lists GoogleAdsLinks on a property.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ListGoogleAdsLinksRequest, dict]):
                The request object. Request message for
                ListGoogleAdsLinks RPC.
            parent (str):
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListGoogleAdsLinksPager:
                Response message for
                ListGoogleAdsLinks RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.ListGoogleAdsLinksRequest):
            request = analytics_admin.ListGoogleAdsLinksRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_google_ads_links]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListGoogleAdsLinksPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_data_sharing_settings(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetDataSharingSettingsRequest, dict]):
                The request object. Request message for
                GetDataSharingSettings RPC.
            name (str):
                Required. The name of the settings to lookup. Format:
                accounts/{account}/dataSharingSettings

                Example: ``accounts/1000/dataSharingSettings``

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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.GetDataSharingSettingsRequest):
            request = analytics_admin.GetDataSharingSettingsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_data_sharing_settings
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_measurement_protocol_secret(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetMeasurementProtocolSecretRequest, dict]):
                The request object. Request message for
                GetMeasurementProtocolSecret RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.GetMeasurementProtocolSecretRequest):
            request = analytics_admin.GetMeasurementProtocolSecretRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_measurement_protocol_secret
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_measurement_protocol_secrets(
        self,
        request: Optional[
            Union[analytics_admin.ListMeasurementProtocolSecretsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListMeasurementProtocolSecretsPager:
        r"""Returns child MeasurementProtocolSecrets under the
        specified parent Property.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ListMeasurementProtocolSecretsRequest, dict]):
                The request object. Request message for
                ListMeasurementProtocolSecret RPC
            parent (str):
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListMeasurementProtocolSecretsPager:
                Response message for
                ListMeasurementProtocolSecret RPC
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, analytics_admin.ListMeasurementProtocolSecretsRequest
        ):
            request = analytics_admin.ListMeasurementProtocolSecretsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_measurement_protocol_secrets
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListMeasurementProtocolSecretsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_measurement_protocol_secret(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.CreateMeasurementProtocolSecretRequest, dict]):
                The request object. Request message for
                CreateMeasurementProtocolSecret RPC
            parent (str):
                Required. The parent resource where
                this secret will be created. Format:
                properties/{property}/dataStreams/{dataStream}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            measurement_protocol_secret (google.analytics.admin_v1alpha.types.MeasurementProtocolSecret):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, measurement_protocol_secret])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, analytics_admin.CreateMeasurementProtocolSecretRequest
        ):
            request = analytics_admin.CreateMeasurementProtocolSecretRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if measurement_protocol_secret is not None:
                request.measurement_protocol_secret = measurement_protocol_secret

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_measurement_protocol_secret
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_measurement_protocol_secret(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.DeleteMeasurementProtocolSecretRequest, dict]):
                The request object. Request message for
                DeleteMeasurementProtocolSecret RPC
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, analytics_admin.DeleteMeasurementProtocolSecretRequest
        ):
            request = analytics_admin.DeleteMeasurementProtocolSecretRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_measurement_protocol_secret
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def update_measurement_protocol_secret(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.UpdateMeasurementProtocolSecretRequest, dict]):
                The request object. Request message for
                UpdateMeasurementProtocolSecret RPC
            measurement_protocol_secret (google.analytics.admin_v1alpha.types.MeasurementProtocolSecret):
                Required. The measurement protocol
                secret to update.

                This corresponds to the ``measurement_protocol_secret`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. The list of fields to be
                updated. Omitted fields will not be
                updated.

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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([measurement_protocol_secret, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, analytics_admin.UpdateMeasurementProtocolSecretRequest
        ):
            request = analytics_admin.UpdateMeasurementProtocolSecretRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if measurement_protocol_secret is not None:
                request.measurement_protocol_secret = measurement_protocol_secret
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_measurement_protocol_secret
        ]

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

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def acknowledge_user_data_collection(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.AcknowledgeUserDataCollectionRequest, dict]):
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
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, analytics_admin.AcknowledgeUserDataCollectionRequest
        ):
            request = analytics_admin.AcknowledgeUserDataCollectionRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.acknowledge_user_data_collection
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("property", request.property),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_sk_ad_network_conversion_value_schema(
        self,
        request: Optional[
            Union[analytics_admin.GetSKAdNetworkConversionValueSchemaRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.SKAdNetworkConversionValueSchema:
        r"""Looks up a single SKAdNetworkConversionValueSchema.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetSKAdNetworkConversionValueSchemaRequest, dict]):
                The request object. Request message for
                GetSKAdNetworkConversionValueSchema RPC.
            name (str):
                Required. The resource name of SKAdNetwork conversion
                value schema to look up. Format:
                properties/{property}/dataStreams/{dataStream}/sKAdNetworkConversionValueSchema/{skadnetwork_conversion_value_schema}

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.SKAdNetworkConversionValueSchema:
                SKAdNetwork conversion value schema
                of an iOS stream.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, analytics_admin.GetSKAdNetworkConversionValueSchemaRequest
        ):
            request = analytics_admin.GetSKAdNetworkConversionValueSchemaRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_sk_ad_network_conversion_value_schema
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_sk_ad_network_conversion_value_schema(
        self,
        request: Optional[
            Union[analytics_admin.CreateSKAdNetworkConversionValueSchemaRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        skadnetwork_conversion_value_schema: Optional[
            resources.SKAdNetworkConversionValueSchema
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.SKAdNetworkConversionValueSchema:
        r"""Creates a SKAdNetworkConversionValueSchema.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.CreateSKAdNetworkConversionValueSchemaRequest, dict]):
                The request object. Request message for
                CreateSKAdNetworkConversionValueSchema
                RPC.
            parent (str):
                Required. The parent resource where
                this schema will be created. Format:
                properties/{property}/dataStreams/{dataStream}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            skadnetwork_conversion_value_schema (google.analytics.admin_v1alpha.types.SKAdNetworkConversionValueSchema):
                Required. SKAdNetwork conversion
                value schema to create.

                This corresponds to the ``skadnetwork_conversion_value_schema`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.SKAdNetworkConversionValueSchema:
                SKAdNetwork conversion value schema
                of an iOS stream.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, skadnetwork_conversion_value_schema])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, analytics_admin.CreateSKAdNetworkConversionValueSchemaRequest
        ):
            request = analytics_admin.CreateSKAdNetworkConversionValueSchemaRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if skadnetwork_conversion_value_schema is not None:
                request.skadnetwork_conversion_value_schema = (
                    skadnetwork_conversion_value_schema
                )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_sk_ad_network_conversion_value_schema
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_sk_ad_network_conversion_value_schema(
        self,
        request: Optional[
            Union[analytics_admin.DeleteSKAdNetworkConversionValueSchemaRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes target SKAdNetworkConversionValueSchema.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.DeleteSKAdNetworkConversionValueSchemaRequest, dict]):
                The request object. Request message for
                DeleteSKAdNetworkConversionValueSchema
                RPC.
            name (str):
                Required. The name of the
                SKAdNetworkConversionValueSchema to delete. Format:
                properties/{property}/dataStreams/{dataStream}/sKAdNetworkConversionValueSchema/{skadnetwork_conversion_value_schema}

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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, analytics_admin.DeleteSKAdNetworkConversionValueSchemaRequest
        ):
            request = analytics_admin.DeleteSKAdNetworkConversionValueSchemaRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_sk_ad_network_conversion_value_schema
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def update_sk_ad_network_conversion_value_schema(
        self,
        request: Optional[
            Union[analytics_admin.UpdateSKAdNetworkConversionValueSchemaRequest, dict]
        ] = None,
        *,
        skadnetwork_conversion_value_schema: Optional[
            resources.SKAdNetworkConversionValueSchema
        ] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.SKAdNetworkConversionValueSchema:
        r"""Updates a SKAdNetworkConversionValueSchema.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.UpdateSKAdNetworkConversionValueSchemaRequest, dict]):
                The request object. Request message for
                UpdateSKAdNetworkConversionValueSchema
                RPC.
            skadnetwork_conversion_value_schema (google.analytics.admin_v1alpha.types.SKAdNetworkConversionValueSchema):
                Required. SKAdNetwork conversion
                value schema to update.

                This corresponds to the ``skadnetwork_conversion_value_schema`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. The list of fields to be
                updated. Omitted fields will not be
                updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.SKAdNetworkConversionValueSchema:
                SKAdNetwork conversion value schema
                of an iOS stream.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([skadnetwork_conversion_value_schema, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, analytics_admin.UpdateSKAdNetworkConversionValueSchemaRequest
        ):
            request = analytics_admin.UpdateSKAdNetworkConversionValueSchemaRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if skadnetwork_conversion_value_schema is not None:
                request.skadnetwork_conversion_value_schema = (
                    skadnetwork_conversion_value_schema
                )
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_sk_ad_network_conversion_value_schema
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    (
                        "skadnetwork_conversion_value_schema.name",
                        request.skadnetwork_conversion_value_schema.name,
                    ),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_sk_ad_network_conversion_value_schemas(
        self,
        request: Optional[
            Union[analytics_admin.ListSKAdNetworkConversionValueSchemasRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListSKAdNetworkConversionValueSchemasPager:
        r"""Lists SKAdNetworkConversionValueSchema on a stream.
        Properties can have at most one
        SKAdNetworkConversionValueSchema.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ListSKAdNetworkConversionValueSchemasRequest, dict]):
                The request object. Request message for
                ListSKAdNetworkConversionValueSchemas
                RPC
            parent (str):
                Required. The DataStream resource to list schemas for.
                Format:
                properties/{property_id}/dataStreams/{dataStream}
                Example: properties/1234/dataStreams/5678

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListSKAdNetworkConversionValueSchemasPager:
                Response message for
                ListSKAdNetworkConversionValueSchemas
                RPC  Iterating over this object will
                yield results and resolve additional
                pages automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, analytics_admin.ListSKAdNetworkConversionValueSchemasRequest
        ):
            request = analytics_admin.ListSKAdNetworkConversionValueSchemasRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_sk_ad_network_conversion_value_schemas
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListSKAdNetworkConversionValueSchemasPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def search_change_history_events(
        self,
        request: Optional[
            Union[analytics_admin.SearchChangeHistoryEventsRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.SearchChangeHistoryEventsPager:
        r"""Searches through all changes to an account or its
        children given the specified set of filters.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.SearchChangeHistoryEventsRequest, dict]):
                The request object. Request message for
                SearchChangeHistoryEvents RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.SearchChangeHistoryEventsPager:
                Response message for SearchAccounts
                RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.SearchChangeHistoryEventsRequest):
            request = analytics_admin.SearchChangeHistoryEventsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.search_change_history_events
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("account", request.account),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.SearchChangeHistoryEventsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_google_signals_settings(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetGoogleSignalsSettingsRequest, dict]):
                The request object. Request message for
                GetGoogleSignalsSettings RPC
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.GetGoogleSignalsSettingsRequest):
            request = analytics_admin.GetGoogleSignalsSettingsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_google_signals_settings
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_google_signals_settings(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.UpdateGoogleSignalsSettingsRequest, dict]):
                The request object. Request message for
                UpdateGoogleSignalsSettings RPC
            google_signals_settings (google.analytics.admin_v1alpha.types.GoogleSignalsSettings):
                Required. The settings to update. The ``name`` field is
                used to identify the settings to be updated.

                This corresponds to the ``google_signals_settings`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([google_signals_settings, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.UpdateGoogleSignalsSettingsRequest):
            request = analytics_admin.UpdateGoogleSignalsSettingsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if google_signals_settings is not None:
                request.google_signals_settings = google_signals_settings
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_google_signals_settings
        ]

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

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_conversion_event(
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
        r"""Deprecated: Use ``CreateKeyEvent`` instead. Creates a conversion
        event with the specified attributes.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.CreateConversionEventRequest, dict]):
                The request object. Request message for
                CreateConversionEvent RPC
            parent (str):
                Required. The resource name of the
                parent property where this conversion
                event will be created. Format:
                properties/123

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            conversion_event (google.analytics.admin_v1alpha.types.ConversionEvent):
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
        warnings.warn(
            "AnalyticsAdminServiceClient.create_conversion_event is deprecated",
            DeprecationWarning,
        )

        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, conversion_event])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.CreateConversionEventRequest):
            request = analytics_admin.CreateConversionEventRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if conversion_event is not None:
                request.conversion_event = conversion_event

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_conversion_event]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_conversion_event(
        self,
        request: Optional[
            Union[analytics_admin.UpdateConversionEventRequest, dict]
        ] = None,
        *,
        conversion_event: Optional[resources.ConversionEvent] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.ConversionEvent:
        r"""Deprecated: Use ``UpdateKeyEvent`` instead. Updates a conversion
        event with the specified attributes.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.UpdateConversionEventRequest, dict]):
                The request object. Request message for
                UpdateConversionEvent RPC
            conversion_event (google.analytics.admin_v1alpha.types.ConversionEvent):
                Required. The conversion event to update. The ``name``
                field is used to identify the settings to be updated.

                This corresponds to the ``conversion_event`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
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
            google.analytics.admin_v1alpha.types.ConversionEvent:
                A conversion event in a Google
                Analytics property.

        """
        warnings.warn(
            "AnalyticsAdminServiceClient.update_conversion_event is deprecated",
            DeprecationWarning,
        )

        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([conversion_event, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.UpdateConversionEventRequest):
            request = analytics_admin.UpdateConversionEventRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if conversion_event is not None:
                request.conversion_event = conversion_event
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_conversion_event]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("conversion_event.name", request.conversion_event.name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_conversion_event(
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
        r"""Deprecated: Use ``GetKeyEvent`` instead. Retrieve a single
        conversion event.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetConversionEventRequest, dict]):
                The request object. Request message for
                GetConversionEvent RPC
            name (str):
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
        warnings.warn(
            "AnalyticsAdminServiceClient.get_conversion_event is deprecated",
            DeprecationWarning,
        )

        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.GetConversionEventRequest):
            request = analytics_admin.GetConversionEventRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_conversion_event]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_conversion_event(
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
        r"""Deprecated: Use ``DeleteKeyEvent`` instead. Deletes a conversion
        event in a property.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.DeleteConversionEventRequest, dict]):
                The request object. Request message for
                DeleteConversionEvent RPC
            name (str):
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
        warnings.warn(
            "AnalyticsAdminServiceClient.delete_conversion_event is deprecated",
            DeprecationWarning,
        )

        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.DeleteConversionEventRequest):
            request = analytics_admin.DeleteConversionEventRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_conversion_event]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def list_conversion_events(
        self,
        request: Optional[
            Union[analytics_admin.ListConversionEventsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListConversionEventsPager:
        r"""Deprecated: Use ``ListKeyEvents`` instead. Returns a list of
        conversion events in the specified parent property.

        Returns an empty list if no conversion events are found.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ListConversionEventsRequest, dict]):
                The request object. Request message for
                ListConversionEvents RPC
            parent (str):
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListConversionEventsPager:
                Response message for
                ListConversionEvents RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        warnings.warn(
            "AnalyticsAdminServiceClient.list_conversion_events is deprecated",
            DeprecationWarning,
        )

        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.ListConversionEventsRequest):
            request = analytics_admin.ListConversionEventsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_conversion_events]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListConversionEventsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_key_event(
        self,
        request: Optional[Union[analytics_admin.CreateKeyEventRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        key_event: Optional[resources.KeyEvent] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.KeyEvent:
        r"""Creates a Key Event.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.CreateKeyEventRequest, dict]):
                The request object. Request message for CreateKeyEvent
                RPC
            parent (str):
                Required. The resource name of the
                parent property where this Key Event
                will be created. Format: properties/123

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            key_event (google.analytics.admin_v1alpha.types.KeyEvent):
                Required. The Key Event to create.
                This corresponds to the ``key_event`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.KeyEvent:
                A key event in a Google Analytics
                property.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, key_event])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.CreateKeyEventRequest):
            request = analytics_admin.CreateKeyEventRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if key_event is not None:
                request.key_event = key_event

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_key_event]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_key_event(
        self,
        request: Optional[Union[analytics_admin.UpdateKeyEventRequest, dict]] = None,
        *,
        key_event: Optional[resources.KeyEvent] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.KeyEvent:
        r"""Updates a Key Event.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.UpdateKeyEventRequest, dict]):
                The request object. Request message for UpdateKeyEvent
                RPC
            key_event (google.analytics.admin_v1alpha.types.KeyEvent):
                Required. The Key Event to update. The ``name`` field is
                used to identify the settings to be updated.

                This corresponds to the ``key_event`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
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
            google.analytics.admin_v1alpha.types.KeyEvent:
                A key event in a Google Analytics
                property.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([key_event, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.UpdateKeyEventRequest):
            request = analytics_admin.UpdateKeyEventRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if key_event is not None:
                request.key_event = key_event
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_key_event]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("key_event.name", request.key_event.name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_key_event(
        self,
        request: Optional[Union[analytics_admin.GetKeyEventRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.KeyEvent:
        r"""Retrieve a single Key Event.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetKeyEventRequest, dict]):
                The request object. Request message for GetKeyEvent RPC
            name (str):
                Required. The resource name of the Key Event to
                retrieve. Format:
                properties/{property}/keyEvents/{key_event} Example:
                "properties/123/keyEvents/456"

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.KeyEvent:
                A key event in a Google Analytics
                property.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.GetKeyEventRequest):
            request = analytics_admin.GetKeyEventRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_key_event]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_key_event(
        self,
        request: Optional[Union[analytics_admin.DeleteKeyEventRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a Key Event.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.DeleteKeyEventRequest, dict]):
                The request object. Request message for DeleteKeyEvent
                RPC
            name (str):
                Required. The resource name of the Key Event to delete.
                Format: properties/{property}/keyEvents/{key_event}
                Example: "properties/123/keyEvents/456"

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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.DeleteKeyEventRequest):
            request = analytics_admin.DeleteKeyEventRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_key_event]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def list_key_events(
        self,
        request: Optional[Union[analytics_admin.ListKeyEventsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListKeyEventsPager:
        r"""Returns a list of Key Events in the specified parent
        property. Returns an empty list if no Key Events are
        found.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ListKeyEventsRequest, dict]):
                The request object. Request message for ListKeyEvents RPC
            parent (str):
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListKeyEventsPager:
                Response message for ListKeyEvents
                RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.ListKeyEventsRequest):
            request = analytics_admin.ListKeyEventsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_key_events]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListKeyEventsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_display_video360_advertiser_link(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetDisplayVideo360AdvertiserLinkRequest, dict]):
                The request object. Request message for
                GetDisplayVideo360AdvertiserLink RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, analytics_admin.GetDisplayVideo360AdvertiserLinkRequest
        ):
            request = analytics_admin.GetDisplayVideo360AdvertiserLinkRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_display_video360_advertiser_link
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_display_video360_advertiser_links(
        self,
        request: Optional[
            Union[analytics_admin.ListDisplayVideo360AdvertiserLinksRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDisplayVideo360AdvertiserLinksPager:
        r"""Lists all DisplayVideo360AdvertiserLinks on a
        property.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ListDisplayVideo360AdvertiserLinksRequest, dict]):
                The request object. Request message for
                ListDisplayVideo360AdvertiserLinks RPC.
            parent (str):
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListDisplayVideo360AdvertiserLinksPager:
                Response message for
                ListDisplayVideo360AdvertiserLinks RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, analytics_admin.ListDisplayVideo360AdvertiserLinksRequest
        ):
            request = analytics_admin.ListDisplayVideo360AdvertiserLinksRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_display_video360_advertiser_links
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListDisplayVideo360AdvertiserLinksPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_display_video360_advertiser_link(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.CreateDisplayVideo360AdvertiserLinkRequest, dict]):
                The request object. Request message for
                CreateDisplayVideo360AdvertiserLink RPC.
            parent (str):
                Required. Example format:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            display_video_360_advertiser_link (google.analytics.admin_v1alpha.types.DisplayVideo360AdvertiserLink):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, display_video_360_advertiser_link])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, analytics_admin.CreateDisplayVideo360AdvertiserLinkRequest
        ):
            request = analytics_admin.CreateDisplayVideo360AdvertiserLinkRequest(
                request
            )
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
        rpc = self._transport._wrapped_methods[
            self._transport.create_display_video360_advertiser_link
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_display_video360_advertiser_link(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.DeleteDisplayVideo360AdvertiserLinkRequest, dict]):
                The request object. Request message for
                DeleteDisplayVideo360AdvertiserLink RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, analytics_admin.DeleteDisplayVideo360AdvertiserLinkRequest
        ):
            request = analytics_admin.DeleteDisplayVideo360AdvertiserLinkRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_display_video360_advertiser_link
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def update_display_video360_advertiser_link(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.UpdateDisplayVideo360AdvertiserLinkRequest, dict]):
                The request object. Request message for
                UpdateDisplayVideo360AdvertiserLink RPC.
            display_video_360_advertiser_link (google.analytics.admin_v1alpha.types.DisplayVideo360AdvertiserLink):
                The DisplayVideo360AdvertiserLink to
                update

                This corresponds to the ``display_video_360_advertiser_link`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([display_video_360_advertiser_link, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, analytics_admin.UpdateDisplayVideo360AdvertiserLinkRequest
        ):
            request = analytics_admin.UpdateDisplayVideo360AdvertiserLinkRequest(
                request
            )
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
        rpc = self._transport._wrapped_methods[
            self._transport.update_display_video360_advertiser_link
        ]

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

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_display_video360_advertiser_link_proposal(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetDisplayVideo360AdvertiserLinkProposalRequest, dict]):
                The request object. Request message for
                GetDisplayVideo360AdvertiserLinkProposal
                RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, analytics_admin.GetDisplayVideo360AdvertiserLinkProposalRequest
        ):
            request = analytics_admin.GetDisplayVideo360AdvertiserLinkProposalRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_display_video360_advertiser_link_proposal
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_display_video360_advertiser_link_proposals(
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
    ) -> pagers.ListDisplayVideo360AdvertiserLinkProposalsPager:
        r"""Lists DisplayVideo360AdvertiserLinkProposals on a
        property.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ListDisplayVideo360AdvertiserLinkProposalsRequest, dict]):
                The request object. Request message for
                ListDisplayVideo360AdvertiserLinkProposals
                RPC.
            parent (str):
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListDisplayVideo360AdvertiserLinkProposalsPager:
                Response message for
                ListDisplayVideo360AdvertiserLinkProposals
                RPC.  Iterating over this object will
                yield results and resolve additional
                pages automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, analytics_admin.ListDisplayVideo360AdvertiserLinkProposalsRequest
        ):
            request = analytics_admin.ListDisplayVideo360AdvertiserLinkProposalsRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_display_video360_advertiser_link_proposals
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListDisplayVideo360AdvertiserLinkProposalsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_display_video360_advertiser_link_proposal(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.CreateDisplayVideo360AdvertiserLinkProposalRequest, dict]):
                The request object. Request message for
                CreateDisplayVideo360AdvertiserLinkProposal
                RPC.
            parent (str):
                Required. Example format:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            display_video_360_advertiser_link_proposal (google.analytics.admin_v1alpha.types.DisplayVideo360AdvertiserLinkProposal):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, display_video_360_advertiser_link_proposal])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, analytics_admin.CreateDisplayVideo360AdvertiserLinkProposalRequest
        ):
            request = (
                analytics_admin.CreateDisplayVideo360AdvertiserLinkProposalRequest(
                    request
                )
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
        rpc = self._transport._wrapped_methods[
            self._transport.create_display_video360_advertiser_link_proposal
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_display_video360_advertiser_link_proposal(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.DeleteDisplayVideo360AdvertiserLinkProposalRequest, dict]):
                The request object. Request message for
                DeleteDisplayVideo360AdvertiserLinkProposal
                RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, analytics_admin.DeleteDisplayVideo360AdvertiserLinkProposalRequest
        ):
            request = (
                analytics_admin.DeleteDisplayVideo360AdvertiserLinkProposalRequest(
                    request
                )
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_display_video360_advertiser_link_proposal
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def approve_display_video360_advertiser_link_proposal(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ApproveDisplayVideo360AdvertiserLinkProposalRequest, dict]):
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
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, analytics_admin.ApproveDisplayVideo360AdvertiserLinkProposalRequest
        ):
            request = (
                analytics_admin.ApproveDisplayVideo360AdvertiserLinkProposalRequest(
                    request
                )
            )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.approve_display_video360_advertiser_link_proposal
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def cancel_display_video360_advertiser_link_proposal(
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
          360
        - Withdrawing a proposal initiated from Google Analytics
          After being cancelled, a proposal will eventually be
          deleted automatically.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.CancelDisplayVideo360AdvertiserLinkProposalRequest, dict]):
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
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, analytics_admin.CancelDisplayVideo360AdvertiserLinkProposalRequest
        ):
            request = (
                analytics_admin.CancelDisplayVideo360AdvertiserLinkProposalRequest(
                    request
                )
            )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.cancel_display_video360_advertiser_link_proposal
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_custom_dimension(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.CreateCustomDimensionRequest, dict]):
                The request object. Request message for
                CreateCustomDimension RPC.
            parent (str):
                Required. Example format:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            custom_dimension (google.analytics.admin_v1alpha.types.CustomDimension):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, custom_dimension])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.CreateCustomDimensionRequest):
            request = analytics_admin.CreateCustomDimensionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if custom_dimension is not None:
                request.custom_dimension = custom_dimension

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_custom_dimension]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_custom_dimension(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.UpdateCustomDimensionRequest, dict]):
                The request object. Request message for
                UpdateCustomDimension RPC.
            custom_dimension (google.analytics.admin_v1alpha.types.CustomDimension):
                The CustomDimension to update
                This corresponds to the ``custom_dimension`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([custom_dimension, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.UpdateCustomDimensionRequest):
            request = analytics_admin.UpdateCustomDimensionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if custom_dimension is not None:
                request.custom_dimension = custom_dimension
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_custom_dimension]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("custom_dimension.name", request.custom_dimension.name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_custom_dimensions(
        self,
        request: Optional[
            Union[analytics_admin.ListCustomDimensionsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCustomDimensionsPager:
        r"""Lists CustomDimensions on a property.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ListCustomDimensionsRequest, dict]):
                The request object. Request message for
                ListCustomDimensions RPC.
            parent (str):
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListCustomDimensionsPager:
                Response message for
                ListCustomDimensions RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.ListCustomDimensionsRequest):
            request = analytics_admin.ListCustomDimensionsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_custom_dimensions]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListCustomDimensionsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def archive_custom_dimension(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ArchiveCustomDimensionRequest, dict]):
                The request object. Request message for
                ArchiveCustomDimension RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.ArchiveCustomDimensionRequest):
            request = analytics_admin.ArchiveCustomDimensionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.archive_custom_dimension]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def get_custom_dimension(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetCustomDimensionRequest, dict]):
                The request object. Request message for
                GetCustomDimension RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.GetCustomDimensionRequest):
            request = analytics_admin.GetCustomDimensionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_custom_dimension]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_custom_metric(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.CreateCustomMetricRequest, dict]):
                The request object. Request message for
                CreateCustomMetric RPC.
            parent (str):
                Required. Example format:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            custom_metric (google.analytics.admin_v1alpha.types.CustomMetric):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, custom_metric])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.CreateCustomMetricRequest):
            request = analytics_admin.CreateCustomMetricRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if custom_metric is not None:
                request.custom_metric = custom_metric

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_custom_metric]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_custom_metric(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.UpdateCustomMetricRequest, dict]):
                The request object. Request message for
                UpdateCustomMetric RPC.
            custom_metric (google.analytics.admin_v1alpha.types.CustomMetric):
                The CustomMetric to update
                This corresponds to the ``custom_metric`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([custom_metric, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.UpdateCustomMetricRequest):
            request = analytics_admin.UpdateCustomMetricRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if custom_metric is not None:
                request.custom_metric = custom_metric
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_custom_metric]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("custom_metric.name", request.custom_metric.name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_custom_metrics(
        self,
        request: Optional[Union[analytics_admin.ListCustomMetricsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCustomMetricsPager:
        r"""Lists CustomMetrics on a property.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ListCustomMetricsRequest, dict]):
                The request object. Request message for ListCustomMetrics
                RPC.
            parent (str):
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListCustomMetricsPager:
                Response message for
                ListCustomMetrics RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.ListCustomMetricsRequest):
            request = analytics_admin.ListCustomMetricsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_custom_metrics]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListCustomMetricsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def archive_custom_metric(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ArchiveCustomMetricRequest, dict]):
                The request object. Request message for
                ArchiveCustomMetric RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.ArchiveCustomMetricRequest):
            request = analytics_admin.ArchiveCustomMetricRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.archive_custom_metric]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def get_custom_metric(
        self,
        request: Optional[Union[analytics_admin.GetCustomMetricRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.CustomMetric:
        r"""Lookup for a single CustomMetric.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetCustomMetricRequest, dict]):
                The request object. Request message for GetCustomMetric
                RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.GetCustomMetricRequest):
            request = analytics_admin.GetCustomMetricRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_custom_metric]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_data_retention_settings(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetDataRetentionSettingsRequest, dict]):
                The request object. Request message for
                GetDataRetentionSettings RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.GetDataRetentionSettingsRequest):
            request = analytics_admin.GetDataRetentionSettingsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_data_retention_settings
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_data_retention_settings(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.UpdateDataRetentionSettingsRequest, dict]):
                The request object. Request message for
                UpdateDataRetentionSettings RPC.
            data_retention_settings (google.analytics.admin_v1alpha.types.DataRetentionSettings):
                Required. The settings to update. The ``name`` field is
                used to identify the settings to be updated.

                This corresponds to the ``data_retention_settings`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([data_retention_settings, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.UpdateDataRetentionSettingsRequest):
            request = analytics_admin.UpdateDataRetentionSettingsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if data_retention_settings is not None:
                request.data_retention_settings = data_retention_settings
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_data_retention_settings
        ]

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

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_data_stream(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.CreateDataStreamRequest, dict]):
                The request object. Request message for CreateDataStream
                RPC.
            parent (str):
                Required. Example format:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            data_stream (google.analytics.admin_v1alpha.types.DataStream):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, data_stream])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.CreateDataStreamRequest):
            request = analytics_admin.CreateDataStreamRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if data_stream is not None:
                request.data_stream = data_stream

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_data_stream]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_data_stream(
        self,
        request: Optional[Union[analytics_admin.DeleteDataStreamRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a DataStream on a property.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.DeleteDataStreamRequest, dict]):
                The request object. Request message for DeleteDataStream
                RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.DeleteDataStreamRequest):
            request = analytics_admin.DeleteDataStreamRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_data_stream]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def update_data_stream(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.UpdateDataStreamRequest, dict]):
                The request object. Request message for UpdateDataStream
                RPC.
            data_stream (google.analytics.admin_v1alpha.types.DataStream):
                The DataStream to update
                This corresponds to the ``data_stream`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([data_stream, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.UpdateDataStreamRequest):
            request = analytics_admin.UpdateDataStreamRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if data_stream is not None:
                request.data_stream = data_stream
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_data_stream]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("data_stream.name", request.data_stream.name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_data_streams(
        self,
        request: Optional[Union[analytics_admin.ListDataStreamsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDataStreamsPager:
        r"""Lists DataStreams on a property.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ListDataStreamsRequest, dict]):
                The request object. Request message for ListDataStreams
                RPC.
            parent (str):
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListDataStreamsPager:
                Response message for ListDataStreams
                RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.ListDataStreamsRequest):
            request = analytics_admin.ListDataStreamsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_data_streams]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListDataStreamsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_data_stream(
        self,
        request: Optional[Union[analytics_admin.GetDataStreamRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.DataStream:
        r"""Lookup for a single DataStream.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetDataStreamRequest, dict]):
                The request object. Request message for GetDataStream
                RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.GetDataStreamRequest):
            request = analytics_admin.GetDataStreamRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_data_stream]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_audience(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetAudienceRequest, dict]):
                The request object. Request message for GetAudience RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.GetAudienceRequest):
            request = analytics_admin.GetAudienceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_audience]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_audiences(
        self,
        request: Optional[Union[analytics_admin.ListAudiencesRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAudiencesPager:
        r"""Lists Audiences on a property.
        Audiences created before 2020 may not be supported.
        Default audiences will not show filter definitions.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ListAudiencesRequest, dict]):
                The request object. Request message for ListAudiences
                RPC.
            parent (str):
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListAudiencesPager:
                Response message for ListAudiences
                RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.ListAudiencesRequest):
            request = analytics_admin.ListAudiencesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_audiences]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListAudiencesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_audience(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.CreateAudienceRequest, dict]):
                The request object. Request message for CreateAudience
                RPC.
            parent (str):
                Required. Example format:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            audience (google.analytics.admin_v1alpha.types.Audience):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, audience])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.CreateAudienceRequest):
            request = analytics_admin.CreateAudienceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if audience is not None:
                request.audience = audience

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_audience]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_audience(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.UpdateAudienceRequest, dict]):
                The request object. Request message for UpdateAudience
                RPC.
            audience (google.analytics.admin_v1alpha.types.Audience):
                Required. The audience to update. The audience's
                ``name`` field is used to identify the audience to be
                updated.

                This corresponds to the ``audience`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([audience, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.UpdateAudienceRequest):
            request = analytics_admin.UpdateAudienceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if audience is not None:
                request.audience = audience
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_audience]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("audience.name", request.audience.name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def archive_audience(
        self,
        request: Optional[Union[analytics_admin.ArchiveAudienceRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Archives an Audience on a property.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ArchiveAudienceRequest, dict]):
                The request object. Request message for ArchiveAudience
                RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.ArchiveAudienceRequest):
            request = analytics_admin.ArchiveAudienceRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.archive_audience]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def get_search_ads360_link(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetSearchAds360LinkRequest, dict]):
                The request object. Request message for
                GetSearchAds360Link RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.GetSearchAds360LinkRequest):
            request = analytics_admin.GetSearchAds360LinkRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_search_ads360_link]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_search_ads360_links(
        self,
        request: Optional[
            Union[analytics_admin.ListSearchAds360LinksRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListSearchAds360LinksPager:
        r"""Lists all SearchAds360Links on a property.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ListSearchAds360LinksRequest, dict]):
                The request object. Request message for
                ListSearchAds360Links RPC.
            parent (str):
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListSearchAds360LinksPager:
                Response message for
                ListSearchAds360Links RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.ListSearchAds360LinksRequest):
            request = analytics_admin.ListSearchAds360LinksRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_search_ads360_links]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListSearchAds360LinksPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_search_ads360_link(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.CreateSearchAds360LinkRequest, dict]):
                The request object. Request message for
                CreateSearchAds360Link RPC.
            parent (str):
                Required. Example format:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            search_ads_360_link (google.analytics.admin_v1alpha.types.SearchAds360Link):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, search_ads_360_link])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.CreateSearchAds360LinkRequest):
            request = analytics_admin.CreateSearchAds360LinkRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if search_ads_360_link is not None:
                request.search_ads_360_link = search_ads_360_link

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_search_ads360_link
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_search_ads360_link(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.DeleteSearchAds360LinkRequest, dict]):
                The request object. Request message for
                DeleteSearchAds360Link RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.DeleteSearchAds360LinkRequest):
            request = analytics_admin.DeleteSearchAds360LinkRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_search_ads360_link
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def update_search_ads360_link(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.UpdateSearchAds360LinkRequest, dict]):
                The request object. Request message for
                UpdateSearchAds360Link RPC.
            search_ads_360_link (google.analytics.admin_v1alpha.types.SearchAds360Link):
                The SearchAds360Link to update
                This corresponds to the ``search_ads_360_link`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([search_ads_360_link, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.UpdateSearchAds360LinkRequest):
            request = analytics_admin.UpdateSearchAds360LinkRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if search_ads_360_link is not None:
                request.search_ads_360_link = search_ads_360_link
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_search_ads360_link
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("search_ads_360_link.name", request.search_ads_360_link.name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_attribution_settings(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetAttributionSettingsRequest, dict]):
                The request object. Request message for
                GetAttributionSettings RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.GetAttributionSettingsRequest):
            request = analytics_admin.GetAttributionSettingsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_attribution_settings]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_attribution_settings(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.UpdateAttributionSettingsRequest, dict]):
                The request object. Request message for
                UpdateAttributionSettings RPC
            attribution_settings (google.analytics.admin_v1alpha.types.AttributionSettings):
                Required. The attribution settings to update. The
                ``name`` field is used to identify the settings to be
                updated.

                This corresponds to the ``attribution_settings`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([attribution_settings, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.UpdateAttributionSettingsRequest):
            request = analytics_admin.UpdateAttributionSettingsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if attribution_settings is not None:
                request.attribution_settings = attribution_settings
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_attribution_settings
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("attribution_settings.name", request.attribution_settings.name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def run_access_report(
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

        Data Access Reports can be requested for a property. Reports may
        be requested for any property, but dimensions that aren't
        related to quota can only be requested on Google Analytics 360
        properties. This method is only available to Administrators.

        These data access records include GA4 UI Reporting, GA4 UI
        Explorations, GA4 Data API, and other products like Firebase &
        Admob that can retrieve data from Google Analytics through a
        linkage. These records don't include property configuration
        changes like adding a stream or changing a property's time zone.
        For configuration change history, see
        `searchChangeHistoryEvents <https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/accounts/searchChangeHistoryEvents>`__.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.RunAccessReportRequest, dict]):
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
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.RunAccessReportRequest):
            request = analytics_admin.RunAccessReportRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.run_access_report]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("entity", request.entity),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_access_binding(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.CreateAccessBindingRequest, dict]):
                The request object. Request message for
                CreateAccessBinding RPC.
            parent (str):
                Required. Formats:

                - accounts/{account}
                - properties/{property}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            access_binding (google.analytics.admin_v1alpha.types.AccessBinding):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, access_binding])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.CreateAccessBindingRequest):
            request = analytics_admin.CreateAccessBindingRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if access_binding is not None:
                request.access_binding = access_binding

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_access_binding]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_access_binding(
        self,
        request: Optional[Union[analytics_admin.GetAccessBindingRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.AccessBinding:
        r"""Gets information about an access binding.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetAccessBindingRequest, dict]):
                The request object. Request message for GetAccessBinding
                RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.GetAccessBindingRequest):
            request = analytics_admin.GetAccessBindingRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_access_binding]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_access_binding(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.UpdateAccessBindingRequest, dict]):
                The request object. Request message for
                UpdateAccessBinding RPC.
            access_binding (google.analytics.admin_v1alpha.types.AccessBinding):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([access_binding])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.UpdateAccessBindingRequest):
            request = analytics_admin.UpdateAccessBindingRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if access_binding is not None:
                request.access_binding = access_binding

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_access_binding]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("access_binding.name", request.access_binding.name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_access_binding(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.DeleteAccessBindingRequest, dict]):
                The request object. Request message for
                DeleteAccessBinding RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.DeleteAccessBindingRequest):
            request = analytics_admin.DeleteAccessBindingRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_access_binding]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def list_access_bindings(
        self,
        request: Optional[
            Union[analytics_admin.ListAccessBindingsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAccessBindingsPager:
        r"""Lists all access bindings on an account or property.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ListAccessBindingsRequest, dict]):
                The request object. Request message for
                ListAccessBindings RPC.
            parent (str):
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListAccessBindingsPager:
                Response message for
                ListAccessBindings RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.ListAccessBindingsRequest):
            request = analytics_admin.ListAccessBindingsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_access_bindings]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListAccessBindingsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def batch_create_access_bindings(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.BatchCreateAccessBindingsRequest, dict]):
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
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.BatchCreateAccessBindingsRequest):
            request = analytics_admin.BatchCreateAccessBindingsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.batch_create_access_bindings
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def batch_get_access_bindings(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.BatchGetAccessBindingsRequest, dict]):
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
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.BatchGetAccessBindingsRequest):
            request = analytics_admin.BatchGetAccessBindingsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.batch_get_access_bindings
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def batch_update_access_bindings(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.BatchUpdateAccessBindingsRequest, dict]):
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
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.BatchUpdateAccessBindingsRequest):
            request = analytics_admin.BatchUpdateAccessBindingsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.batch_update_access_bindings
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def batch_delete_access_bindings(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.BatchDeleteAccessBindingsRequest, dict]):
                The request object. Request message for
                BatchDeleteAccessBindings RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.BatchDeleteAccessBindingsRequest):
            request = analytics_admin.BatchDeleteAccessBindingsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.batch_delete_access_bindings
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def get_expanded_data_set(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetExpandedDataSetRequest, dict]):
                The request object. Request message for
                GetExpandedDataSet RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.GetExpandedDataSetRequest):
            request = analytics_admin.GetExpandedDataSetRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_expanded_data_set]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_expanded_data_sets(
        self,
        request: Optional[
            Union[analytics_admin.ListExpandedDataSetsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListExpandedDataSetsPager:
        r"""Lists ExpandedDataSets on a property.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ListExpandedDataSetsRequest, dict]):
                The request object. Request message for
                ListExpandedDataSets RPC.
            parent (str):
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListExpandedDataSetsPager:
                Response message for
                ListExpandedDataSets RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.ListExpandedDataSetsRequest):
            request = analytics_admin.ListExpandedDataSetsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_expanded_data_sets]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListExpandedDataSetsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_expanded_data_set(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.CreateExpandedDataSetRequest, dict]):
                The request object. Request message for
                CreateExpandedDataSet RPC.
            parent (str):
                Required. Example format:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            expanded_data_set (google.analytics.admin_v1alpha.types.ExpandedDataSet):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, expanded_data_set])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.CreateExpandedDataSetRequest):
            request = analytics_admin.CreateExpandedDataSetRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if expanded_data_set is not None:
                request.expanded_data_set = expanded_data_set

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_expanded_data_set]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_expanded_data_set(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.UpdateExpandedDataSetRequest, dict]):
                The request object. Request message for
                UpdateExpandedDataSet RPC.
            expanded_data_set (google.analytics.admin_v1alpha.types.ExpandedDataSet):
                Required. The ExpandedDataSet to update. The resource's
                ``name`` field is used to identify the ExpandedDataSet
                to be updated.

                This corresponds to the ``expanded_data_set`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([expanded_data_set, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.UpdateExpandedDataSetRequest):
            request = analytics_admin.UpdateExpandedDataSetRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if expanded_data_set is not None:
                request.expanded_data_set = expanded_data_set
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_expanded_data_set]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("expanded_data_set.name", request.expanded_data_set.name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_expanded_data_set(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.DeleteExpandedDataSetRequest, dict]):
                The request object. Request message for
                DeleteExpandedDataSet RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.DeleteExpandedDataSetRequest):
            request = analytics_admin.DeleteExpandedDataSetRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_expanded_data_set]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def get_channel_group(
        self,
        request: Optional[Union[analytics_admin.GetChannelGroupRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> channel_group.ChannelGroup:
        r"""Lookup for a single ChannelGroup.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetChannelGroupRequest, dict]):
                The request object. Request message for GetChannelGroup
                RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.GetChannelGroupRequest):
            request = analytics_admin.GetChannelGroupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_channel_group]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_channel_groups(
        self,
        request: Optional[Union[analytics_admin.ListChannelGroupsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListChannelGroupsPager:
        r"""Lists ChannelGroups on a property.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ListChannelGroupsRequest, dict]):
                The request object. Request message for ListChannelGroups
                RPC.
            parent (str):
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListChannelGroupsPager:
                Response message for
                ListChannelGroups RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.ListChannelGroupsRequest):
            request = analytics_admin.ListChannelGroupsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_channel_groups]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListChannelGroupsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_channel_group(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.CreateChannelGroupRequest, dict]):
                The request object. Request message for
                CreateChannelGroup RPC.
            parent (str):
                Required. The property for which to
                create a ChannelGroup. Example format:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            channel_group (google.analytics.admin_v1alpha.types.ChannelGroup):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, channel_group])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.CreateChannelGroupRequest):
            request = analytics_admin.CreateChannelGroupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if channel_group is not None:
                request.channel_group = channel_group

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_channel_group]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_channel_group(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.UpdateChannelGroupRequest, dict]):
                The request object. Request message for
                UpdateChannelGroup RPC.
            channel_group (google.analytics.admin_v1alpha.types.ChannelGroup):
                Required. The ChannelGroup to update. The resource's
                ``name`` field is used to identify the ChannelGroup to
                be updated.

                This corresponds to the ``channel_group`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([channel_group, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.UpdateChannelGroupRequest):
            request = analytics_admin.UpdateChannelGroupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if channel_group is not None:
                request.channel_group = channel_group
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_channel_group]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("channel_group.name", request.channel_group.name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_channel_group(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.DeleteChannelGroupRequest, dict]):
                The request object. Request message for
                DeleteChannelGroup RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.DeleteChannelGroupRequest):
            request = analytics_admin.DeleteChannelGroupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_channel_group]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def set_automated_ga4_configuration_opt_out(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.SetAutomatedGa4ConfigurationOptOutRequest, dict]):
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
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, analytics_admin.SetAutomatedGa4ConfigurationOptOutRequest
        ):
            request = analytics_admin.SetAutomatedGa4ConfigurationOptOutRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.set_automated_ga4_configuration_opt_out
        ]

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def fetch_automated_ga4_configuration_opt_out(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.FetchAutomatedGa4ConfigurationOptOutRequest, dict]):
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
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, analytics_admin.FetchAutomatedGa4ConfigurationOptOutRequest
        ):
            request = analytics_admin.FetchAutomatedGa4ConfigurationOptOutRequest(
                request
            )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.fetch_automated_ga4_configuration_opt_out
        ]

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_big_query_link(
        self,
        request: Optional[
            Union[analytics_admin.CreateBigQueryLinkRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        bigquery_link: Optional[resources.BigQueryLink] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.BigQueryLink:
        r"""Creates a BigQueryLink.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.CreateBigQueryLinkRequest, dict]):
                The request object. Request message for
                CreateBigQueryLink RPC.
            parent (str):
                Required. Example format:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            bigquery_link (google.analytics.admin_v1alpha.types.BigQueryLink):
                Required. The BigQueryLink to create.
                This corresponds to the ``bigquery_link`` field
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, bigquery_link])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.CreateBigQueryLinkRequest):
            request = analytics_admin.CreateBigQueryLinkRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if bigquery_link is not None:
                request.bigquery_link = bigquery_link

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_big_query_link]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_big_query_link(
        self,
        request: Optional[Union[analytics_admin.GetBigQueryLinkRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.BigQueryLink:
        r"""Lookup for a single BigQuery Link.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetBigQueryLinkRequest, dict]):
                The request object. Request message for GetBigQueryLink
                RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.GetBigQueryLinkRequest):
            request = analytics_admin.GetBigQueryLinkRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_big_query_link]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_big_query_links(
        self,
        request: Optional[Union[analytics_admin.ListBigQueryLinksRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListBigQueryLinksPager:
        r"""Lists BigQuery Links on a property.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ListBigQueryLinksRequest, dict]):
                The request object. Request message for ListBigQueryLinks
                RPC.
            parent (str):
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListBigQueryLinksPager:
                Response message for
                ListBigQueryLinks RPC
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.ListBigQueryLinksRequest):
            request = analytics_admin.ListBigQueryLinksRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_big_query_links]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListBigQueryLinksPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_big_query_link(
        self,
        request: Optional[
            Union[analytics_admin.DeleteBigQueryLinkRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a BigQueryLink on a property.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.DeleteBigQueryLinkRequest, dict]):
                The request object. Request message for
                DeleteBigQueryLink RPC.
            name (str):
                Required. The BigQueryLink to delete.
                Example format:
                properties/1234/bigQueryLinks/5678

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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.DeleteBigQueryLinkRequest):
            request = analytics_admin.DeleteBigQueryLinkRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_big_query_link]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def update_big_query_link(
        self,
        request: Optional[
            Union[analytics_admin.UpdateBigQueryLinkRequest, dict]
        ] = None,
        *,
        bigquery_link: Optional[resources.BigQueryLink] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.BigQueryLink:
        r"""Updates a BigQueryLink.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.UpdateBigQueryLinkRequest, dict]):
                The request object. Request message for
                UpdateBigQueryLink RPC.
            bigquery_link (google.analytics.admin_v1alpha.types.BigQueryLink):
                Required. The settings to update. The ``name`` field is
                used to identify the settings to be updated.

                This corresponds to the ``bigquery_link`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
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
            google.analytics.admin_v1alpha.types.BigQueryLink:
                A link between a GA4 Property and
                BigQuery project.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([bigquery_link, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.UpdateBigQueryLinkRequest):
            request = analytics_admin.UpdateBigQueryLinkRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if bigquery_link is not None:
                request.bigquery_link = bigquery_link
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_big_query_link]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("bigquery_link.name", request.bigquery_link.name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_enhanced_measurement_settings(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetEnhancedMeasurementSettingsRequest, dict]):
                The request object. Request message for
                GetEnhancedMeasurementSettings RPC.
            name (str):
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
                Singleton resource under a web
                DataStream, configuring measurement of
                additional site interactions and
                content.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, analytics_admin.GetEnhancedMeasurementSettingsRequest
        ):
            request = analytics_admin.GetEnhancedMeasurementSettingsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_enhanced_measurement_settings
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_enhanced_measurement_settings(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.UpdateEnhancedMeasurementSettingsRequest, dict]):
                The request object. Request message for
                UpdateEnhancedMeasurementSettings RPC.
            enhanced_measurement_settings (google.analytics.admin_v1alpha.types.EnhancedMeasurementSettings):
                Required. The settings to update. The ``name`` field is
                used to identify the settings to be updated.

                This corresponds to the ``enhanced_measurement_settings`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
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
                Singleton resource under a web
                DataStream, configuring measurement of
                additional site interactions and
                content.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([enhanced_measurement_settings, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, analytics_admin.UpdateEnhancedMeasurementSettingsRequest
        ):
            request = analytics_admin.UpdateEnhancedMeasurementSettingsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if enhanced_measurement_settings is not None:
                request.enhanced_measurement_settings = enhanced_measurement_settings
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_enhanced_measurement_settings
        ]

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

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_connected_site_tag(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.CreateConnectedSiteTagRequest, dict]):
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
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.CreateConnectedSiteTagRequest):
            request = analytics_admin.CreateConnectedSiteTagRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_connected_site_tag
        ]

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_connected_site_tag(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.DeleteConnectedSiteTagRequest, dict]):
                The request object. Request message for
                DeleteConnectedSiteTag RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.DeleteConnectedSiteTagRequest):
            request = analytics_admin.DeleteConnectedSiteTagRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_connected_site_tag
        ]

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def list_connected_site_tags(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ListConnectedSiteTagsRequest, dict]):
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
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.ListConnectedSiteTagsRequest):
            request = analytics_admin.ListConnectedSiteTagsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_connected_site_tags]

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def fetch_connected_ga4_property(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.FetchConnectedGa4PropertyRequest, dict]):
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
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.FetchConnectedGa4PropertyRequest):
            request = analytics_admin.FetchConnectedGa4PropertyRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.fetch_connected_ga4_property
        ]

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_ad_sense_link(
        self,
        request: Optional[Union[analytics_admin.GetAdSenseLinkRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.AdSenseLink:
        r"""Looks up a single AdSenseLink.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetAdSenseLinkRequest, dict]):
                The request object. Request message to be passed to
                GetAdSenseLink method.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.GetAdSenseLinkRequest):
            request = analytics_admin.GetAdSenseLinkRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_ad_sense_link]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_ad_sense_link(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.CreateAdSenseLinkRequest, dict]):
                The request object. Request message to be passed to
                CreateAdSenseLink method.
            parent (str):
                Required. The property for which to
                create an AdSense Link. Format:
                properties/{propertyId} Example:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            adsense_link (google.analytics.admin_v1alpha.types.AdSenseLink):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, adsense_link])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.CreateAdSenseLinkRequest):
            request = analytics_admin.CreateAdSenseLinkRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if adsense_link is not None:
                request.adsense_link = adsense_link

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_ad_sense_link]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_ad_sense_link(
        self,
        request: Optional[Union[analytics_admin.DeleteAdSenseLinkRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an AdSenseLink.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.DeleteAdSenseLinkRequest, dict]):
                The request object. Request message to be passed to
                DeleteAdSenseLink method.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.DeleteAdSenseLinkRequest):
            request = analytics_admin.DeleteAdSenseLinkRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_ad_sense_link]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def list_ad_sense_links(
        self,
        request: Optional[Union[analytics_admin.ListAdSenseLinksRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAdSenseLinksPager:
        r"""Lists AdSenseLinks on a property.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ListAdSenseLinksRequest, dict]):
                The request object. Request message to be passed to
                ListAdSenseLinks method.
            parent (str):
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListAdSenseLinksPager:
                Response message for ListAdSenseLinks
                method.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.ListAdSenseLinksRequest):
            request = analytics_admin.ListAdSenseLinksRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_ad_sense_links]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListAdSenseLinksPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_event_create_rule(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetEventCreateRuleRequest, dict]):
                The request object. Request message for
                GetEventCreateRule RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.GetEventCreateRuleRequest):
            request = analytics_admin.GetEventCreateRuleRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_event_create_rule]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_event_create_rules(
        self,
        request: Optional[
            Union[analytics_admin.ListEventCreateRulesRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListEventCreateRulesPager:
        r"""Lists EventCreateRules on a web data stream.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ListEventCreateRulesRequest, dict]):
                The request object. Request message for
                ListEventCreateRules RPC.
            parent (str):
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListEventCreateRulesPager:
                Response message for
                ListEventCreateRules RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.ListEventCreateRulesRequest):
            request = analytics_admin.ListEventCreateRulesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_event_create_rules]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListEventCreateRulesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_event_create_rule(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.CreateEventCreateRuleRequest, dict]):
                The request object. Request message for
                CreateEventCreateRule RPC.
            parent (str):
                Required. Example format:
                properties/123/dataStreams/456

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            event_create_rule (google.analytics.admin_v1alpha.types.EventCreateRule):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, event_create_rule])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.CreateEventCreateRuleRequest):
            request = analytics_admin.CreateEventCreateRuleRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if event_create_rule is not None:
                request.event_create_rule = event_create_rule

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_event_create_rule]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_event_create_rule(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.UpdateEventCreateRuleRequest, dict]):
                The request object. Request message for
                UpdateEventCreateRule RPC.
            event_create_rule (google.analytics.admin_v1alpha.types.EventCreateRule):
                Required. The EventCreateRule to update. The resource's
                ``name`` field is used to identify the EventCreateRule
                to be updated.

                This corresponds to the ``event_create_rule`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([event_create_rule, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.UpdateEventCreateRuleRequest):
            request = analytics_admin.UpdateEventCreateRuleRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if event_create_rule is not None:
                request.event_create_rule = event_create_rule
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_event_create_rule]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("event_create_rule.name", request.event_create_rule.name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_event_create_rule(
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

        Args:
            request (Union[google.analytics.admin_v1alpha.types.DeleteEventCreateRuleRequest, dict]):
                The request object. Request message for
                DeleteEventCreateRule RPC.
            name (str):
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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.DeleteEventCreateRuleRequest):
            request = analytics_admin.DeleteEventCreateRuleRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_event_create_rule]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def get_event_edit_rule(
        self,
        request: Optional[Union[analytics_admin.GetEventEditRuleRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> event_create_and_edit.EventEditRule:
        r"""Lookup for a single EventEditRule.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetEventEditRuleRequest, dict]):
                The request object. Request message for GetEventEditRule
                RPC.
            name (str):
                Required. The name of the
                EventEditRule to get. Example format:
                properties/123/dataStreams/456/eventEditRules/789

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.EventEditRule:
                An Event Edit Rule defines conditions
                that will trigger the creation of an
                entirely new event based upon matched
                criteria of a source event. Additional
                mutations of the parameters from the
                source event can be defined.

                Unlike Event Create rules, Event Edit
                Rules are applied in their defined
                order.

                Event Edit rules can't be used to modify
                an event created from an Event Create
                rule.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.GetEventEditRuleRequest):
            request = analytics_admin.GetEventEditRuleRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_event_edit_rule]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_event_edit_rules(
        self,
        request: Optional[
            Union[analytics_admin.ListEventEditRulesRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListEventEditRulesPager:
        r"""Lists EventEditRules on a web data stream.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ListEventEditRulesRequest, dict]):
                The request object. Request message for
                ListEventEditRules RPC.
            parent (str):
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListEventEditRulesPager:
                Response message for
                ListEventEditRules RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.ListEventEditRulesRequest):
            request = analytics_admin.ListEventEditRulesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_event_edit_rules]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListEventEditRulesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_event_edit_rule(
        self,
        request: Optional[
            Union[analytics_admin.CreateEventEditRuleRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        event_edit_rule: Optional[event_create_and_edit.EventEditRule] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> event_create_and_edit.EventEditRule:
        r"""Creates an EventEditRule.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.CreateEventEditRuleRequest, dict]):
                The request object. Request message for
                CreateEventEditRule RPC.
            parent (str):
                Required. Example format:
                properties/123/dataStreams/456

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            event_edit_rule (google.analytics.admin_v1alpha.types.EventEditRule):
                Required. The EventEditRule to
                create.

                This corresponds to the ``event_edit_rule`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.EventEditRule:
                An Event Edit Rule defines conditions
                that will trigger the creation of an
                entirely new event based upon matched
                criteria of a source event. Additional
                mutations of the parameters from the
                source event can be defined.

                Unlike Event Create rules, Event Edit
                Rules are applied in their defined
                order.

                Event Edit rules can't be used to modify
                an event created from an Event Create
                rule.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, event_edit_rule])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.CreateEventEditRuleRequest):
            request = analytics_admin.CreateEventEditRuleRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if event_edit_rule is not None:
                request.event_edit_rule = event_edit_rule

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_event_edit_rule]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_event_edit_rule(
        self,
        request: Optional[
            Union[analytics_admin.UpdateEventEditRuleRequest, dict]
        ] = None,
        *,
        event_edit_rule: Optional[event_create_and_edit.EventEditRule] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> event_create_and_edit.EventEditRule:
        r"""Updates an EventEditRule.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.UpdateEventEditRuleRequest, dict]):
                The request object. Request message for
                UpdateEventEditRule RPC.
            event_edit_rule (google.analytics.admin_v1alpha.types.EventEditRule):
                Required. The EventEditRule to update. The resource's
                ``name`` field is used to identify the EventEditRule to
                be updated.

                This corresponds to the ``event_edit_rule`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
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
            google.analytics.admin_v1alpha.types.EventEditRule:
                An Event Edit Rule defines conditions
                that will trigger the creation of an
                entirely new event based upon matched
                criteria of a source event. Additional
                mutations of the parameters from the
                source event can be defined.

                Unlike Event Create rules, Event Edit
                Rules are applied in their defined
                order.

                Event Edit rules can't be used to modify
                an event created from an Event Create
                rule.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([event_edit_rule, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.UpdateEventEditRuleRequest):
            request = analytics_admin.UpdateEventEditRuleRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if event_edit_rule is not None:
                request.event_edit_rule = event_edit_rule
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_event_edit_rule]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("event_edit_rule.name", request.event_edit_rule.name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_event_edit_rule(
        self,
        request: Optional[
            Union[analytics_admin.DeleteEventEditRuleRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an EventEditRule.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.DeleteEventEditRuleRequest, dict]):
                The request object. Request message for
                DeleteEventEditRule RPC.
            name (str):
                Required. Example format:
                properties/123/dataStreams/456/eventEditRules/789

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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.DeleteEventEditRuleRequest):
            request = analytics_admin.DeleteEventEditRuleRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_event_edit_rule]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def reorder_event_edit_rules(
        self,
        request: Optional[
            Union[analytics_admin.ReorderEventEditRulesRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Changes the processing order of event edit rules on
        the specified stream.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ReorderEventEditRulesRequest, dict]):
                The request object. Request message for
                ReorderEventEditRules RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.ReorderEventEditRulesRequest):
            request = analytics_admin.ReorderEventEditRulesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.reorder_event_edit_rules]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def update_data_redaction_settings(
        self,
        request: Optional[
            Union[analytics_admin.UpdateDataRedactionSettingsRequest, dict]
        ] = None,
        *,
        data_redaction_settings: Optional[resources.DataRedactionSettings] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.DataRedactionSettings:
        r"""Updates a DataRedactionSettings on a property.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.UpdateDataRedactionSettingsRequest, dict]):
                The request object. Request message for
                UpdateDataRedactionSettings RPC.
            data_redaction_settings (google.analytics.admin_v1alpha.types.DataRedactionSettings):
                Required. The settings to update. The ``name`` field is
                used to identify the settings to be updated.

                This corresponds to the ``data_redaction_settings`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
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
            google.analytics.admin_v1alpha.types.DataRedactionSettings:
                Settings for client-side data
                redaction. Singleton resource under a
                Web Stream.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([data_redaction_settings, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.UpdateDataRedactionSettingsRequest):
            request = analytics_admin.UpdateDataRedactionSettingsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if data_redaction_settings is not None:
                request.data_redaction_settings = data_redaction_settings
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_data_redaction_settings
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    (
                        "data_redaction_settings.name",
                        request.data_redaction_settings.name,
                    ),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_data_redaction_settings(
        self,
        request: Optional[
            Union[analytics_admin.GetDataRedactionSettingsRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.DataRedactionSettings:
        r"""Lookup for a single DataRedactionSettings.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetDataRedactionSettingsRequest, dict]):
                The request object. Request message for
                GetDataRedactionSettings RPC.
            name (str):
                Required. The name of the settings to lookup. Format:
                properties/{property}/dataStreams/{data_stream}/dataRedactionSettings
                Example:
                "properties/1000/dataStreams/2000/dataRedactionSettings"

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.DataRedactionSettings:
                Settings for client-side data
                redaction. Singleton resource under a
                Web Stream.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.GetDataRedactionSettingsRequest):
            request = analytics_admin.GetDataRedactionSettingsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_data_redaction_settings
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_calculated_metric(
        self,
        request: Optional[
            Union[analytics_admin.GetCalculatedMetricRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.CalculatedMetric:
        r"""Lookup for a single CalculatedMetric.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetCalculatedMetricRequest, dict]):
                The request object. Request message for
                GetCalculatedMetric RPC.
            name (str):
                Required. The name of the CalculatedMetric to get.
                Format:
                properties/{property_id}/calculatedMetrics/{calculated_metric_id}
                Example: properties/1234/calculatedMetrics/Metric01

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.CalculatedMetric:
                A definition for a calculated metric.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.GetCalculatedMetricRequest):
            request = analytics_admin.GetCalculatedMetricRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_calculated_metric]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_calculated_metric(
        self,
        request: Optional[
            Union[analytics_admin.CreateCalculatedMetricRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        calculated_metric: Optional[resources.CalculatedMetric] = None,
        calculated_metric_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.CalculatedMetric:
        r"""Creates a CalculatedMetric.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.CreateCalculatedMetricRequest, dict]):
                The request object. Request message for
                CreateCalculatedMetric RPC.
            parent (str):
                Required. Format: properties/{property_id} Example:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            calculated_metric (google.analytics.admin_v1alpha.types.CalculatedMetric):
                Required. The CalculatedMetric to
                create.

                This corresponds to the ``calculated_metric`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            calculated_metric_id (str):
                Required. The ID to use for the calculated metric which
                will become the final component of the calculated
                metric's resource name.

                This value should be 1-80 characters and valid
                characters are `[a-zA-Z0-9_]`, no spaces allowed.
                calculated_metric_id must be unique between all
                calculated metrics under a property. The
                calculated_metric_id is used when referencing this
                calculated metric from external APIs, for example,
                "calcMetric:{calculated_metric_id}".

                This corresponds to the ``calculated_metric_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.CalculatedMetric:
                A definition for a calculated metric.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, calculated_metric, calculated_metric_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.CreateCalculatedMetricRequest):
            request = analytics_admin.CreateCalculatedMetricRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if calculated_metric is not None:
                request.calculated_metric = calculated_metric
            if calculated_metric_id is not None:
                request.calculated_metric_id = calculated_metric_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_calculated_metric]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_calculated_metrics(
        self,
        request: Optional[
            Union[analytics_admin.ListCalculatedMetricsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCalculatedMetricsPager:
        r"""Lists CalculatedMetrics on a property.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ListCalculatedMetricsRequest, dict]):
                The request object. Request message for
                ListCalculatedMetrics RPC.
            parent (str):
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
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListCalculatedMetricsPager:
                Response message for
                ListCalculatedMetrics RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.ListCalculatedMetricsRequest):
            request = analytics_admin.ListCalculatedMetricsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_calculated_metrics]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListCalculatedMetricsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_calculated_metric(
        self,
        request: Optional[
            Union[analytics_admin.UpdateCalculatedMetricRequest, dict]
        ] = None,
        *,
        calculated_metric: Optional[resources.CalculatedMetric] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.CalculatedMetric:
        r"""Updates a CalculatedMetric on a property.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.UpdateCalculatedMetricRequest, dict]):
                The request object. Request message for
                UpdateCalculatedMetric RPC.
            calculated_metric (google.analytics.admin_v1alpha.types.CalculatedMetric):
                Required. The CalculatedMetric to
                update

                This corresponds to the ``calculated_metric`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
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
            google.analytics.admin_v1alpha.types.CalculatedMetric:
                A definition for a calculated metric.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([calculated_metric, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.UpdateCalculatedMetricRequest):
            request = analytics_admin.UpdateCalculatedMetricRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if calculated_metric is not None:
                request.calculated_metric = calculated_metric
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_calculated_metric]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("calculated_metric.name", request.calculated_metric.name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_calculated_metric(
        self,
        request: Optional[
            Union[analytics_admin.DeleteCalculatedMetricRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a CalculatedMetric on a property.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.DeleteCalculatedMetricRequest, dict]):
                The request object. Request message for
                DeleteCalculatedMetric RPC.
            name (str):
                Required. The name of the CalculatedMetric to delete.
                Format:
                properties/{property_id}/calculatedMetrics/{calculated_metric_id}
                Example: properties/1234/calculatedMetrics/Metric01

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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.DeleteCalculatedMetricRequest):
            request = analytics_admin.DeleteCalculatedMetricRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_calculated_metric]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def create_rollup_property(
        self,
        request: Optional[
            Union[analytics_admin.CreateRollupPropertyRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_admin.CreateRollupPropertyResponse:
        r"""Create a roll-up property and all roll-up property
        source links.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.CreateRollupPropertyRequest, dict]):
                The request object. Request message for
                CreateRollupProperty RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.CreateRollupPropertyResponse:
                Response message for
                CreateRollupProperty RPC.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.CreateRollupPropertyRequest):
            request = analytics_admin.CreateRollupPropertyRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_rollup_property]

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_rollup_property_source_link(
        self,
        request: Optional[
            Union[analytics_admin.GetRollupPropertySourceLinkRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.RollupPropertySourceLink:
        r"""Lookup for a single roll-up property source Link.
        Only roll-up properties can have source links, so this
        method will throw an error if used on other types of
        properties.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetRollupPropertySourceLinkRequest, dict]):
                The request object. Request message for
                GetRollupPropertySourceLink RPC.
            name (str):
                Required. The name of the roll-up property source link
                to lookup. Format:
                properties/{property_id}/rollupPropertySourceLinks/{rollup_property_source_link_id}
                Example: properties/123/rollupPropertySourceLinks/456

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.RollupPropertySourceLink:
                A link that references a source
                property under the parent rollup
                property.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.GetRollupPropertySourceLinkRequest):
            request = analytics_admin.GetRollupPropertySourceLinkRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_rollup_property_source_link
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_rollup_property_source_links(
        self,
        request: Optional[
            Union[analytics_admin.ListRollupPropertySourceLinksRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListRollupPropertySourceLinksPager:
        r"""Lists roll-up property source Links on a property.
        Only roll-up properties can have source links, so this
        method will throw an error if used on other types of
        properties.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ListRollupPropertySourceLinksRequest, dict]):
                The request object. Request message for
                ListRollupPropertySourceLinks RPC.
            parent (str):
                Required. The name of the roll-up property to list
                roll-up property source links under. Format:
                properties/{property_id} Example: properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListRollupPropertySourceLinksPager:
                Response message for
                ListRollupPropertySourceLinks RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, analytics_admin.ListRollupPropertySourceLinksRequest
        ):
            request = analytics_admin.ListRollupPropertySourceLinksRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_rollup_property_source_links
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListRollupPropertySourceLinksPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_rollup_property_source_link(
        self,
        request: Optional[
            Union[analytics_admin.CreateRollupPropertySourceLinkRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        rollup_property_source_link: Optional[
            resources.RollupPropertySourceLink
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.RollupPropertySourceLink:
        r"""Creates a roll-up property source link.
        Only roll-up properties can have source links, so this
        method will throw an error if used on other types of
        properties.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.CreateRollupPropertySourceLinkRequest, dict]):
                The request object. Request message for
                CreateRollupPropertySourceLink RPC.
            parent (str):
                Required. Format: properties/{property_id} Example:
                properties/1234

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            rollup_property_source_link (google.analytics.admin_v1alpha.types.RollupPropertySourceLink):
                Required. The roll-up property source
                link to create.

                This corresponds to the ``rollup_property_source_link`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.RollupPropertySourceLink:
                A link that references a source
                property under the parent rollup
                property.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, rollup_property_source_link])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, analytics_admin.CreateRollupPropertySourceLinkRequest
        ):
            request = analytics_admin.CreateRollupPropertySourceLinkRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if rollup_property_source_link is not None:
                request.rollup_property_source_link = rollup_property_source_link

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_rollup_property_source_link
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_rollup_property_source_link(
        self,
        request: Optional[
            Union[analytics_admin.DeleteRollupPropertySourceLinkRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a roll-up property source link.
        Only roll-up properties can have source links, so this
        method will throw an error if used on other types of
        properties.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.DeleteRollupPropertySourceLinkRequest, dict]):
                The request object. Request message for
                DeleteRollupPropertySourceLink RPC.
            name (str):
                Required. Format:
                properties/{property_id}/rollupPropertySourceLinks/{rollup_property_source_link_id}
                Example: properties/1234/rollupPropertySourceLinks/5678

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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, analytics_admin.DeleteRollupPropertySourceLinkRequest
        ):
            request = analytics_admin.DeleteRollupPropertySourceLinkRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_rollup_property_source_link
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def provision_subproperty(
        self,
        request: Optional[
            Union[analytics_admin.ProvisionSubpropertyRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> analytics_admin.ProvisionSubpropertyResponse:
        r"""Create a subproperty and a subproperty event filter
        that applies to the created subproperty.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ProvisionSubpropertyRequest, dict]):
                The request object. Request message for CreateSubproperty
                RPC.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.ProvisionSubpropertyResponse:
                Response message for
                ProvisionSubproperty RPC.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.ProvisionSubpropertyRequest):
            request = analytics_admin.ProvisionSubpropertyRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.provision_subproperty]

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_subproperty_event_filter(
        self,
        request: Optional[
            Union[analytics_admin.CreateSubpropertyEventFilterRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        subproperty_event_filter: Optional[
            gaa_subproperty_event_filter.SubpropertyEventFilter
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gaa_subproperty_event_filter.SubpropertyEventFilter:
        r"""Creates a subproperty Event Filter.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.CreateSubpropertyEventFilterRequest, dict]):
                The request object. Request message for
                CreateSubpropertyEventFilter RPC.
            parent (str):
                Required. The ordinary property for which to create a
                subproperty event filter. Format: properties/property_id
                Example: properties/123

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            subproperty_event_filter (google.analytics.admin_v1alpha.types.SubpropertyEventFilter):
                Required. The subproperty event
                filter to create.

                This corresponds to the ``subproperty_event_filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.SubpropertyEventFilter:
                A resource message representing a GA4
                Subproperty event filter.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, subproperty_event_filter])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.CreateSubpropertyEventFilterRequest):
            request = analytics_admin.CreateSubpropertyEventFilterRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if subproperty_event_filter is not None:
                request.subproperty_event_filter = subproperty_event_filter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_subproperty_event_filter
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_subproperty_event_filter(
        self,
        request: Optional[
            Union[analytics_admin.GetSubpropertyEventFilterRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> subproperty_event_filter.SubpropertyEventFilter:
        r"""Lookup for a single subproperty Event Filter.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.GetSubpropertyEventFilterRequest, dict]):
                The request object. Request message for
                GetSubpropertyEventFilter RPC.
            name (str):
                Required. Resource name of the subproperty event filter
                to lookup. Format:
                properties/property_id/subpropertyEventFilters/subproperty_event_filter
                Example: properties/123/subpropertyEventFilters/456

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.types.SubpropertyEventFilter:
                A resource message representing a GA4
                Subproperty event filter.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.GetSubpropertyEventFilterRequest):
            request = analytics_admin.GetSubpropertyEventFilterRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_subproperty_event_filter
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_subproperty_event_filters(
        self,
        request: Optional[
            Union[analytics_admin.ListSubpropertyEventFiltersRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListSubpropertyEventFiltersPager:
        r"""List all subproperty Event Filters on a property.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.ListSubpropertyEventFiltersRequest, dict]):
                The request object. Request message for
                ListSubpropertyEventFilters RPC.
            parent (str):
                Required. Resource name of the ordinary property.
                Format: properties/property_id Example: properties/123

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.analytics.admin_v1alpha.services.analytics_admin_service.pagers.ListSubpropertyEventFiltersPager:
                Response message for
                ListSubpropertyEventFilter RPC.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.ListSubpropertyEventFiltersRequest):
            request = analytics_admin.ListSubpropertyEventFiltersRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_subproperty_event_filters
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListSubpropertyEventFiltersPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_subproperty_event_filter(
        self,
        request: Optional[
            Union[analytics_admin.UpdateSubpropertyEventFilterRequest, dict]
        ] = None,
        *,
        subproperty_event_filter: Optional[
            gaa_subproperty_event_filter.SubpropertyEventFilter
        ] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gaa_subproperty_event_filter.SubpropertyEventFilter:
        r"""Updates a subproperty Event Filter.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.UpdateSubpropertyEventFilterRequest, dict]):
                The request object. Request message for
                UpdateSubpropertyEventFilter RPC.
            subproperty_event_filter (google.analytics.admin_v1alpha.types.SubpropertyEventFilter):
                Required. The subproperty event
                filter to update.

                This corresponds to the ``subproperty_event_filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. The list of fields to update. Field names must
                be in snake case (for example, "field_to_update").
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
            google.analytics.admin_v1alpha.types.SubpropertyEventFilter:
                A resource message representing a GA4
                Subproperty event filter.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([subproperty_event_filter, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.UpdateSubpropertyEventFilterRequest):
            request = analytics_admin.UpdateSubpropertyEventFilterRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if subproperty_event_filter is not None:
                request.subproperty_event_filter = subproperty_event_filter
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_subproperty_event_filter
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    (
                        "subproperty_event_filter.name",
                        request.subproperty_event_filter.name,
                    ),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_subproperty_event_filter(
        self,
        request: Optional[
            Union[analytics_admin.DeleteSubpropertyEventFilterRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a subproperty event filter.

        Args:
            request (Union[google.analytics.admin_v1alpha.types.DeleteSubpropertyEventFilterRequest, dict]):
                The request object. Request message for
                DeleteSubpropertyEventFilter RPC.
            name (str):
                Required. Resource name of the subproperty event filter
                to delete. Format:
                properties/property_id/subpropertyEventFilters/subproperty_event_filter
                Example: properties/123/subpropertyEventFilters/456

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
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, analytics_admin.DeleteSubpropertyEventFilterRequest):
            request = analytics_admin.DeleteSubpropertyEventFilterRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_subproperty_event_filter
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def __enter__(self) -> "AnalyticsAdminServiceClient":
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("AnalyticsAdminServiceClient",)
