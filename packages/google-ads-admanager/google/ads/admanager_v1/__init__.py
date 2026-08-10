# -*- coding: utf-8 -*-
# Copyright 2026 Google LLC
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
import sys

import google.api_core as api_core

from google.ads.admanager_v1 import gapic_version as package_version

__version__ = package_version.__version__

from importlib import metadata

# PEP 0810: Explicit Lazy Imports
# Python 3.15+ natively intercepts and defers these imports.
# Developers can disable this behavior and force eager imports.
# For more information, see:
# https://docs.python.org/3.15/library/sys.html#sys.set_lazy_imports_filter
# Older Python versions safely ignore this variable.
__lazy_modules__ = {
    "google.ads.admanager_v1.services.ad_break_service",
    "google.ads.admanager_v1.services.ad_review_center_ad_service",
    "google.ads.admanager_v1.services.ad_rule_service",
    "google.ads.admanager_v1.services.ad_spot_service",
    "google.ads.admanager_v1.services.ad_unit_service",
    "google.ads.admanager_v1.services.application_service",
    "google.ads.admanager_v1.services.audience_segment_service",
    "google.ads.admanager_v1.services.bandwidth_group_service",
    "google.ads.admanager_v1.services.browser_language_service",
    "google.ads.admanager_v1.services.browser_service",
    "google.ads.admanager_v1.services.cdn_config_service",
    "google.ads.admanager_v1.services.cms_metadata_key_service",
    "google.ads.admanager_v1.services.cms_metadata_value_service",
    "google.ads.admanager_v1.services.company_service",
    "google.ads.admanager_v1.services.contact_service",
    "google.ads.admanager_v1.services.content_bundle_service",
    "google.ads.admanager_v1.services.content_label_service",
    "google.ads.admanager_v1.services.content_service",
    "google.ads.admanager_v1.services.creative_set_service",
    "google.ads.admanager_v1.services.creative_template_service",
    "google.ads.admanager_v1.services.custom_field_service",
    "google.ads.admanager_v1.services.custom_targeting_key_service",
    "google.ads.admanager_v1.services.custom_targeting_value_service",
    "google.ads.admanager_v1.services.device_capability_service",
    "google.ads.admanager_v1.services.device_category_service",
    "google.ads.admanager_v1.services.device_manufacturer_service",
    "google.ads.admanager_v1.services.entity_signals_mapping_service",
    "google.ads.admanager_v1.services.geo_target_service",
    "google.ads.admanager_v1.services.label_service",
    "google.ads.admanager_v1.services.line_item_service",
    "google.ads.admanager_v1.services.linked_device_service",
    "google.ads.admanager_v1.services.live_stream_service",
    "google.ads.admanager_v1.services.mcm_earnings_service",
    "google.ads.admanager_v1.services.mobile_carrier_service",
    "google.ads.admanager_v1.services.mobile_device_service",
    "google.ads.admanager_v1.services.mobile_device_submodel_service",
    "google.ads.admanager_v1.services.network_service",
    "google.ads.admanager_v1.services.operating_system_service",
    "google.ads.admanager_v1.services.operating_system_version_service",
    "google.ads.admanager_v1.services.order_service",
    "google.ads.admanager_v1.services.placement_service",
    "google.ads.admanager_v1.services.private_auction_deal_service",
    "google.ads.admanager_v1.services.private_auction_service",
    "google.ads.admanager_v1.services.programmatic_buyer_service",
    "google.ads.admanager_v1.services.report_service",
    "google.ads.admanager_v1.services.rich_media_ads_company_service",
    "google.ads.admanager_v1.services.role_service",
    "google.ads.admanager_v1.services.site_service",
    "google.ads.admanager_v1.services.slate_service",
    "google.ads.admanager_v1.services.suggested_ad_unit_service",
    "google.ads.admanager_v1.services.targeting_preset_service",
    "google.ads.admanager_v1.services.taxonomy_category_service",
    "google.ads.admanager_v1.services.team_service",
    "google.ads.admanager_v1.services.third_party_company_service",
    "google.ads.admanager_v1.services.user_service",
    "google.ads.admanager_v1.types.ad_break_messages",
    "google.ads.admanager_v1.types.ad_break_service",
    "google.ads.admanager_v1.types.ad_review_center_ad_enums",
    "google.ads.admanager_v1.types.ad_review_center_ad_messages",
    "google.ads.admanager_v1.types.ad_review_center_ad_service",
    "google.ads.admanager_v1.types.ad_rule_enums",
    "google.ads.admanager_v1.types.ad_rule_messages",
    "google.ads.admanager_v1.types.ad_rule_service",
    "google.ads.admanager_v1.types.ad_rule_slot_behavior_enum",
    "google.ads.admanager_v1.types.ad_rule_slot_bumper_enum",
    "google.ads.admanager_v1.types.ad_rule_slot_midroll_frequency_type_enum",
    "google.ads.admanager_v1.types.ad_spot_messages",
    "google.ads.admanager_v1.types.ad_spot_service",
    "google.ads.admanager_v1.types.ad_spot_targeting_type_enum",
    "google.ads.admanager_v1.types.ad_unit_enums",
    "google.ads.admanager_v1.types.ad_unit_messages",
    "google.ads.admanager_v1.types.ad_unit_service",
    "google.ads.admanager_v1.types.admanager_error",
    "google.ads.admanager_v1.types.application_enums",
    "google.ads.admanager_v1.types.application_messages",
    "google.ads.admanager_v1.types.application_service",
    "google.ads.admanager_v1.types.applied_label",
    "google.ads.admanager_v1.types.audience_segment_messages",
    "google.ads.admanager_v1.types.audience_segment_service",
    "google.ads.admanager_v1.types.bandwidth_group_messages",
    "google.ads.admanager_v1.types.bandwidth_group_service",
    "google.ads.admanager_v1.types.brand_lift_partner_enum",
    "google.ads.admanager_v1.types.browser_language_messages",
    "google.ads.admanager_v1.types.browser_language_service",
    "google.ads.admanager_v1.types.browser_messages",
    "google.ads.admanager_v1.types.browser_service",
    "google.ads.admanager_v1.types.cdn_config_messages",
    "google.ads.admanager_v1.types.cdn_config_service",
    "google.ads.admanager_v1.types.cdn_config_status_enum",
    "google.ads.admanager_v1.types.cdn_config_type_enum",
    "google.ads.admanager_v1.types.cdn_security_policy_enum",
    "google.ads.admanager_v1.types.cdn_security_policy_origin_forwarding_enum",
    "google.ads.admanager_v1.types.child_content_eligibility_enum",
    "google.ads.admanager_v1.types.child_publisher_messages",
    "google.ads.admanager_v1.types.cms_metadata_key_enums",
    "google.ads.admanager_v1.types.cms_metadata_key_messages",
    "google.ads.admanager_v1.types.cms_metadata_key_service",
    "google.ads.admanager_v1.types.cms_metadata_value_enums",
    "google.ads.admanager_v1.types.cms_metadata_value_messages",
    "google.ads.admanager_v1.types.cms_metadata_value_service",
    "google.ads.admanager_v1.types.company_enums",
    "google.ads.admanager_v1.types.company_messages",
    "google.ads.admanager_v1.types.company_service",
    "google.ads.admanager_v1.types.contact_enums",
    "google.ads.admanager_v1.types.contact_messages",
    "google.ads.admanager_v1.types.contact_service",
    "google.ads.admanager_v1.types.content_bundle_enums",
    "google.ads.admanager_v1.types.content_bundle_messages",
    "google.ads.admanager_v1.types.content_bundle_service",
    "google.ads.admanager_v1.types.content_enums",
    "google.ads.admanager_v1.types.content_label_messages",
    "google.ads.admanager_v1.types.content_label_service",
    "google.ads.admanager_v1.types.content_messages",
    "google.ads.admanager_v1.types.content_service",
    "google.ads.admanager_v1.types.creative_messages",
    "google.ads.admanager_v1.types.creative_placeholder",
    "google.ads.admanager_v1.types.creative_set_messages",
    "google.ads.admanager_v1.types.creative_set_service",
    "google.ads.admanager_v1.types.creative_targeting",
    "google.ads.admanager_v1.types.creative_template_enums",
    "google.ads.admanager_v1.types.creative_template_messages",
    "google.ads.admanager_v1.types.creative_template_service",
    "google.ads.admanager_v1.types.creative_template_variable_url_type_enum",
    "google.ads.admanager_v1.types.custom_field_enums",
    "google.ads.admanager_v1.types.custom_field_messages",
    "google.ads.admanager_v1.types.custom_field_service",
    "google.ads.admanager_v1.types.custom_field_value",
    "google.ads.admanager_v1.types.custom_pacing_curve",
    "google.ads.admanager_v1.types.custom_pacing_goal_unit_enum",
    "google.ads.admanager_v1.types.custom_targeting_key_enums",
    "google.ads.admanager_v1.types.custom_targeting_key_messages",
    "google.ads.admanager_v1.types.custom_targeting_key_service",
    "google.ads.admanager_v1.types.custom_targeting_value_enums",
    "google.ads.admanager_v1.types.custom_targeting_value_messages",
    "google.ads.admanager_v1.types.custom_targeting_value_service",
    "google.ads.admanager_v1.types.deal_buyer_permission_type_enum",
    "google.ads.admanager_v1.types.deal_priority_tier_enum",
    "google.ads.admanager_v1.types.delivery_enums",
    "google.ads.admanager_v1.types.delivery_indicator",
    "google.ads.admanager_v1.types.device_capability_messages",
    "google.ads.admanager_v1.types.device_capability_service",
    "google.ads.admanager_v1.types.device_category_messages",
    "google.ads.admanager_v1.types.device_category_service",
    "google.ads.admanager_v1.types.device_manufacturer_messages",
    "google.ads.admanager_v1.types.device_manufacturer_service",
    "google.ads.admanager_v1.types.discount_type_enum",
    "google.ads.admanager_v1.types.early_ad_break_notification_enums",
    "google.ads.admanager_v1.types.entity_signals_mapping_messages",
    "google.ads.admanager_v1.types.entity_signals_mapping_service",
    "google.ads.admanager_v1.types.environment_type_enum",
    "google.ads.admanager_v1.types.exchange_syndication_product_enum",
    "google.ads.admanager_v1.types.exclusion_scope_enum",
    "google.ads.admanager_v1.types.frequency_cap",
    "google.ads.admanager_v1.types.geo_target_messages",
    "google.ads.admanager_v1.types.geo_target_service",
    "google.ads.admanager_v1.types.goal",
    "google.ads.admanager_v1.types.goal_enums",
    "google.ads.admanager_v1.types.grp_provider_enum",
    "google.ads.admanager_v1.types.grp_settings",
    "google.ads.admanager_v1.types.grp_target_gender_enum",
    "google.ads.admanager_v1.types.label_enums",
    "google.ads.admanager_v1.types.label_messages",
    "google.ads.admanager_v1.types.label_service",
    "google.ads.admanager_v1.types.line_item_allowed_format_enum",
    "google.ads.admanager_v1.types.line_item_deal_info",
    "google.ads.admanager_v1.types.line_item_delivery_forecast_source_enum",
    "google.ads.admanager_v1.types.line_item_discount",
    "google.ads.admanager_v1.types.line_item_enums",
    "google.ads.admanager_v1.types.line_item_messages",
    "google.ads.admanager_v1.types.line_item_service",
    "google.ads.admanager_v1.types.line_item_stats",
    "google.ads.admanager_v1.types.linked_device_enums",
    "google.ads.admanager_v1.types.linked_device_messages",
    "google.ads.admanager_v1.types.linked_device_service",
    "google.ads.admanager_v1.types.live_stream_event_enums",
    "google.ads.admanager_v1.types.live_stream_event_messages",
    "google.ads.admanager_v1.types.live_stream_messages",
    "google.ads.admanager_v1.types.live_stream_service",
    "google.ads.admanager_v1.types.mcm_earnings_messages",
    "google.ads.admanager_v1.types.mcm_earnings_service",
    "google.ads.admanager_v1.types.mcm_enums",
    "google.ads.admanager_v1.types.mobile_carrier_messages",
    "google.ads.admanager_v1.types.mobile_carrier_service",
    "google.ads.admanager_v1.types.mobile_device_messages",
    "google.ads.admanager_v1.types.mobile_device_service",
    "google.ads.admanager_v1.types.mobile_device_submodel_messages",
    "google.ads.admanager_v1.types.mobile_device_submodel_service",
    "google.ads.admanager_v1.types.network_messages",
    "google.ads.admanager_v1.types.network_service",
    "google.ads.admanager_v1.types.nielsen_ctv_pacing_enum",
    "google.ads.admanager_v1.types.non_guaranteed_deal_priority",
    "google.ads.admanager_v1.types.operating_system_messages",
    "google.ads.admanager_v1.types.operating_system_service",
    "google.ads.admanager_v1.types.operating_system_version_messages",
    "google.ads.admanager_v1.types.operating_system_version_service",
    "google.ads.admanager_v1.types.order_enums",
    "google.ads.admanager_v1.types.order_messages",
    "google.ads.admanager_v1.types.order_service",
    "google.ads.admanager_v1.types.pacing_device_categorization_enum",
    "google.ads.admanager_v1.types.placement_enums",
    "google.ads.admanager_v1.types.placement_messages",
    "google.ads.admanager_v1.types.placement_service",
    "google.ads.admanager_v1.types.private_auction_deal_messages",
    "google.ads.admanager_v1.types.private_auction_deal_service",
    "google.ads.admanager_v1.types.private_auction_messages",
    "google.ads.admanager_v1.types.private_auction_service",
    "google.ads.admanager_v1.types.private_marketplace_enums",
    "google.ads.admanager_v1.types.programmatic_buyer_messages",
    "google.ads.admanager_v1.types.programmatic_buyer_service",
    "google.ads.admanager_v1.types.reach_partner_enum",
    "google.ads.admanager_v1.types.report_definition",
    "google.ads.admanager_v1.types.report_delivery",
    "google.ads.admanager_v1.types.report_messages",
    "google.ads.admanager_v1.types.report_service",
    "google.ads.admanager_v1.types.report_value",
    "google.ads.admanager_v1.types.request_platform_enum",
    "google.ads.admanager_v1.types.rich_media_ads_company_enums",
    "google.ads.admanager_v1.types.rich_media_ads_company_messages",
    "google.ads.admanager_v1.types.rich_media_ads_company_service",
    "google.ads.admanager_v1.types.role_enums",
    "google.ads.admanager_v1.types.role_messages",
    "google.ads.admanager_v1.types.role_service",
    "google.ads.admanager_v1.types.site_enums",
    "google.ads.admanager_v1.types.site_messages",
    "google.ads.admanager_v1.types.site_service",
    "google.ads.admanager_v1.types.size",
    "google.ads.admanager_v1.types.size_type_enum",
    "google.ads.admanager_v1.types.skippable_ad_type_enum",
    "google.ads.admanager_v1.types.slate_messages",
    "google.ads.admanager_v1.types.slate_service",
    "google.ads.admanager_v1.types.suggested_ad_unit_messages",
    "google.ads.admanager_v1.types.suggested_ad_unit_service",
    "google.ads.admanager_v1.types.target_platform_enum",
    "google.ads.admanager_v1.types.targeted_video_bumper_type_enum",
    "google.ads.admanager_v1.types.targeting",
    "google.ads.admanager_v1.types.targeting_preset_enums",
    "google.ads.admanager_v1.types.targeting_preset_messages",
    "google.ads.admanager_v1.types.targeting_preset_service",
    "google.ads.admanager_v1.types.taxonomy_category_messages",
    "google.ads.admanager_v1.types.taxonomy_category_service",
    "google.ads.admanager_v1.types.taxonomy_type_enum",
    "google.ads.admanager_v1.types.team_enums",
    "google.ads.admanager_v1.types.team_messages",
    "google.ads.admanager_v1.types.team_service",
    "google.ads.admanager_v1.types.third_party_company_enums",
    "google.ads.admanager_v1.types.third_party_company_messages",
    "google.ads.admanager_v1.types.third_party_company_service",
    "google.ads.admanager_v1.types.third_party_measurement_settings",
    "google.ads.admanager_v1.types.time_unit_enum",
    "google.ads.admanager_v1.types.user_messages",
    "google.ads.admanager_v1.types.user_service",
    "google.ads.admanager_v1.types.video_position_enum",
    "google.ads.admanager_v1.types.video_transcode_status_enum",
    "google.ads.admanager_v1.types.viewability_partner_enum",
    "google.ads.admanager_v1.types.web_property",
}


from .services.ad_break_service import AdBreakServiceClient
from .services.ad_review_center_ad_service import AdReviewCenterAdServiceClient
from .services.ad_rule_service import AdRuleServiceClient
from .services.ad_spot_service import AdSpotServiceClient
from .services.ad_unit_service import AdUnitServiceClient
from .services.application_service import ApplicationServiceClient
from .services.audience_segment_service import AudienceSegmentServiceClient
from .services.bandwidth_group_service import BandwidthGroupServiceClient
from .services.browser_language_service import BrowserLanguageServiceClient
from .services.browser_service import BrowserServiceClient
from .services.cdn_config_service import CdnConfigServiceClient
from .services.cms_metadata_key_service import CmsMetadataKeyServiceClient
from .services.cms_metadata_value_service import CmsMetadataValueServiceClient
from .services.company_service import CompanyServiceClient
from .services.contact_service import ContactServiceClient
from .services.content_bundle_service import ContentBundleServiceClient
from .services.content_label_service import ContentLabelServiceClient
from .services.content_service import ContentServiceClient
from .services.creative_set_service import CreativeSetServiceClient
from .services.creative_template_service import CreativeTemplateServiceClient
from .services.custom_field_service import CustomFieldServiceClient
from .services.custom_targeting_key_service import CustomTargetingKeyServiceClient
from .services.custom_targeting_value_service import CustomTargetingValueServiceClient
from .services.device_capability_service import DeviceCapabilityServiceClient
from .services.device_category_service import DeviceCategoryServiceClient
from .services.device_manufacturer_service import DeviceManufacturerServiceClient
from .services.entity_signals_mapping_service import EntitySignalsMappingServiceClient
from .services.geo_target_service import GeoTargetServiceClient
from .services.label_service import LabelServiceClient
from .services.line_item_service import LineItemServiceClient
from .services.linked_device_service import LinkedDeviceServiceClient
from .services.live_stream_service import LiveStreamServiceClient
from .services.mcm_earnings_service import McmEarningsServiceClient
from .services.mobile_carrier_service import MobileCarrierServiceClient
from .services.mobile_device_service import MobileDeviceServiceClient
from .services.mobile_device_submodel_service import MobileDeviceSubmodelServiceClient
from .services.network_service import NetworkServiceClient
from .services.operating_system_service import OperatingSystemServiceClient
from .services.operating_system_version_service import (
    OperatingSystemVersionServiceClient,
)
from .services.order_service import OrderServiceClient
from .services.placement_service import PlacementServiceClient
from .services.private_auction_deal_service import PrivateAuctionDealServiceClient
from .services.private_auction_service import PrivateAuctionServiceClient
from .services.programmatic_buyer_service import ProgrammaticBuyerServiceClient
from .services.report_service import ReportServiceClient
from .services.rich_media_ads_company_service import RichMediaAdsCompanyServiceClient
from .services.role_service import RoleServiceClient
from .services.site_service import SiteServiceClient
from .services.slate_service import SlateServiceClient
from .services.suggested_ad_unit_service import SuggestedAdUnitServiceClient
from .services.targeting_preset_service import TargetingPresetServiceClient
from .services.taxonomy_category_service import TaxonomyCategoryServiceClient
from .services.team_service import TeamServiceClient
from .services.third_party_company_service import ThirdPartyCompanyServiceClient
from .services.user_service import UserServiceClient
from .types.ad_break_messages import AdBreak
from .types.ad_break_service import (
    CreateAdBreakRequest,
    DeleteAdBreakRequest,
    GetAdBreakRequest,
    ListAdBreaksRequest,
    ListAdBreaksResponse,
    UpdateAdBreakRequest,
)
from .types.ad_review_center_ad_enums import (
    AdReviewCenterAdStatusEnum,
    ManualAdReviewCenterAdStatusEnum,
)
from .types.ad_review_center_ad_messages import AdReviewCenterAd
from .types.ad_review_center_ad_service import (
    BatchAdReviewCenterAdsOperationMetadata,
    BatchAllowAdReviewCenterAdsRequest,
    BatchAllowAdReviewCenterAdsResponse,
    BatchBlockAdReviewCenterAdsRequest,
    BatchBlockAdReviewCenterAdsResponse,
    SearchAdReviewCenterAdsRequest,
    SearchAdReviewCenterAdsResponse,
)
from .types.ad_rule_enums import AdRuleFrequencyCapBehaviorEnum, AdRuleStatusEnum
from .types.ad_rule_messages import AdRule, AdRuleSlot
from .types.ad_rule_service import (
    BatchActivateAdRulesRequest,
    BatchActivateAdRulesResponse,
    BatchCreateAdRulesRequest,
    BatchCreateAdRulesResponse,
    BatchDeactivateAdRulesRequest,
    BatchDeactivateAdRulesResponse,
    BatchDeleteAdRulesRequest,
    BatchUpdateAdRulesRequest,
    BatchUpdateAdRulesResponse,
    CreateAdRuleRequest,
    GetAdRuleRequest,
    ListAdRulesRequest,
    ListAdRulesResponse,
    UpdateAdRuleRequest,
)
from .types.ad_rule_slot_behavior_enum import AdRuleSlotBehaviorEnum
from .types.ad_rule_slot_bumper_enum import AdRuleSlotBumperEnum
from .types.ad_rule_slot_midroll_frequency_type_enum import (
    AdRuleSlotMidrollFrequencyTypeEnum,
)
from .types.ad_spot_messages import AdSpot
from .types.ad_spot_service import (
    BatchCreateAdSpotsRequest,
    BatchCreateAdSpotsResponse,
    BatchUpdateAdSpotsRequest,
    BatchUpdateAdSpotsResponse,
    CreateAdSpotRequest,
    GetAdSpotRequest,
    ListAdSpotsRequest,
    ListAdSpotsResponse,
    UpdateAdSpotRequest,
)
from .types.ad_spot_targeting_type_enum import AdSpotTargetingTypeEnum
from .types.ad_unit_enums import AdUnitStatusEnum, SmartSizeModeEnum, TargetWindowEnum
from .types.ad_unit_messages import AdUnit, AdUnitParent, AdUnitSize, LabelFrequencyCap
from .types.ad_unit_service import (
    BatchActivateAdUnitsRequest,
    BatchActivateAdUnitsResponse,
    BatchArchiveAdUnitsRequest,
    BatchArchiveAdUnitsResponse,
    BatchCreateAdUnitsRequest,
    BatchCreateAdUnitsResponse,
    BatchDeactivateAdUnitsRequest,
    BatchDeactivateAdUnitsResponse,
    BatchUpdateAdUnitsRequest,
    BatchUpdateAdUnitsResponse,
    CreateAdUnitRequest,
    GetAdUnitRequest,
    ListAdUnitSizesRequest,
    ListAdUnitSizesResponse,
    ListAdUnitsRequest,
    ListAdUnitsResponse,
    UpdateAdUnitRequest,
)
from .types.admanager_error import AdManagerError
from .types.application_enums import (
    ApplicationApprovalStatusEnum,
    ApplicationPlatformEnum,
    ApplicationStoreEnum,
    WebviewClaimingStatusEnum,
)
from .types.application_messages import Application
from .types.application_service import (
    BatchArchiveApplicationsRequest,
    BatchArchiveApplicationsResponse,
    BatchCreateApplicationsRequest,
    BatchCreateApplicationsResponse,
    BatchUnarchiveApplicationsRequest,
    BatchUnarchiveApplicationsResponse,
    BatchUpdateApplicationsRequest,
    BatchUpdateApplicationsResponse,
    CreateApplicationRequest,
    GetApplicationRequest,
    ListApplicationsRequest,
    ListApplicationsResponse,
    UpdateApplicationRequest,
)
from .types.applied_label import AppliedLabel
from .types.audience_segment_messages import AudienceSegment
from .types.audience_segment_service import (
    GetAudienceSegmentRequest,
    ListAudienceSegmentsRequest,
    ListAudienceSegmentsResponse,
)
from .types.bandwidth_group_messages import BandwidthGroup
from .types.bandwidth_group_service import (
    GetBandwidthGroupRequest,
    ListBandwidthGroupsRequest,
    ListBandwidthGroupsResponse,
)
from .types.brand_lift_partner_enum import BrandLiftPartnerEnum
from .types.browser_language_messages import BrowserLanguage
from .types.browser_language_service import (
    GetBrowserLanguageRequest,
    ListBrowserLanguagesRequest,
    ListBrowserLanguagesResponse,
)
from .types.browser_messages import Browser
from .types.browser_service import (
    GetBrowserRequest,
    ListBrowsersRequest,
    ListBrowsersResponse,
)
from .types.cdn_config_messages import (
    AdMediaDeliveryConfig,
    CdnConfig,
    CdnSecurityPolicy,
    MediaLocation,
    SourceContentConfig,
)
from .types.cdn_config_service import (
    BatchActivateCdnConfigsRequest,
    BatchActivateCdnConfigsResponse,
    BatchArchiveCdnConfigsRequest,
    BatchArchiveCdnConfigsResponse,
    BatchCreateCdnConfigsRequest,
    BatchCreateCdnConfigsResponse,
    BatchUpdateCdnConfigsRequest,
    BatchUpdateCdnConfigsResponse,
    CreateCdnConfigRequest,
    GetCdnConfigRequest,
    ListCdnConfigsRequest,
    ListCdnConfigsResponse,
    UpdateCdnConfigRequest,
)
from .types.cdn_config_status_enum import CdnConfigStatusEnum
from .types.cdn_config_type_enum import CdnConfigTypeEnum
from .types.cdn_security_policy_enum import CdnSecurityPolicyTypeEnum
from .types.cdn_security_policy_origin_forwarding_enum import (
    CdnSecurityPolicyOriginForwardingEnum,
)
from .types.child_content_eligibility_enum import ChildContentEligibilityEnum
from .types.child_publisher_messages import ChildPublisher
from .types.cms_metadata_key_enums import CmsMetadataKeyStatusEnum
from .types.cms_metadata_key_messages import CmsMetadataKey
from .types.cms_metadata_key_service import (
    BatchActivateCmsMetadataKeysRequest,
    BatchActivateCmsMetadataKeysResponse,
    BatchDeactivateCmsMetadataKeysRequest,
    BatchDeactivateCmsMetadataKeysResponse,
    GetCmsMetadataKeyRequest,
    ListCmsMetadataKeysRequest,
    ListCmsMetadataKeysResponse,
)
from .types.cms_metadata_value_enums import CmsMetadataValueStatusEnum
from .types.cms_metadata_value_messages import CmsMetadataValue
from .types.cms_metadata_value_service import (
    BatchActivateCmsMetadataValuesRequest,
    BatchActivateCmsMetadataValuesResponse,
    BatchDeactivateCmsMetadataValuesRequest,
    BatchDeactivateCmsMetadataValuesResponse,
    GetCmsMetadataValueRequest,
    ListCmsMetadataValuesRequest,
    ListCmsMetadataValuesResponse,
)
from .types.company_enums import CompanyCreditStatusEnum, CompanyTypeEnum
from .types.company_messages import Company
from .types.company_service import (
    GetCompanyRequest,
    ListCompaniesRequest,
    ListCompaniesResponse,
)
from .types.contact_enums import ContactStatusEnum
from .types.contact_messages import Contact
from .types.contact_service import (
    BatchCreateContactsRequest,
    BatchCreateContactsResponse,
    BatchUpdateContactsRequest,
    BatchUpdateContactsResponse,
    CreateContactRequest,
    GetContactRequest,
    ListContactsRequest,
    ListContactsResponse,
    UpdateContactRequest,
)
from .types.content_bundle_enums import ContentBundleStatusEnum
from .types.content_bundle_messages import ContentBundle
from .types.content_bundle_service import (
    BatchActivateContentBundlesRequest,
    BatchActivateContentBundlesResponse,
    BatchDeactivateContentBundlesRequest,
    BatchDeactivateContentBundlesResponse,
    GetContentBundleRequest,
    ListContentBundlesRequest,
    ListContentBundlesResponse,
)
from .types.content_enums import (
    ContentStatusEnum,
    ContentStatusSourceEnum,
    DaiIngestErrorReasonEnum,
    DaiIngestStatusEnum,
)
from .types.content_label_messages import ContentLabel
from .types.content_label_service import (
    GetContentLabelRequest,
    ListContentLabelsRequest,
    ListContentLabelsResponse,
)
from .types.content_messages import CmsContent, Content, DaiIngestError
from .types.content_service import (
    GetContentRequest,
    ListContentRequest,
    ListContentResponse,
)
from .types.creative_messages import Creative
from .types.creative_placeholder import (
    CreativePlaceholder,
    CreativePlaceholderCompanion,
)
from .types.creative_set_messages import CreativeSet
from .types.creative_set_service import (
    CreateCreativeSetRequest,
    GetCreativeSetRequest,
    ListCreativeSetsRequest,
    ListCreativeSetsResponse,
    UpdateCreativeSetRequest,
)
from .types.creative_targeting import CreativeTargeting
from .types.creative_template_enums import (
    CreativeTemplateStatusEnum,
    CreativeTemplateTypeEnum,
)
from .types.creative_template_messages import CreativeTemplate, CreativeTemplateVariable
from .types.creative_template_service import (
    GetCreativeTemplateRequest,
    ListCreativeTemplatesRequest,
    ListCreativeTemplatesResponse,
)
from .types.creative_template_variable_url_type_enum import (
    CreativeTemplateVariableUrlTypeEnum,
)
from .types.custom_field_enums import (
    CustomFieldDataTypeEnum,
    CustomFieldEntityTypeEnum,
    CustomFieldStatusEnum,
    CustomFieldVisibilityEnum,
)
from .types.custom_field_messages import CustomField, CustomFieldOption
from .types.custom_field_service import (
    BatchActivateCustomFieldsRequest,
    BatchActivateCustomFieldsResponse,
    BatchCreateCustomFieldsRequest,
    BatchCreateCustomFieldsResponse,
    BatchDeactivateCustomFieldsRequest,
    BatchDeactivateCustomFieldsResponse,
    BatchUpdateCustomFieldsRequest,
    BatchUpdateCustomFieldsResponse,
    CreateCustomFieldRequest,
    GetCustomFieldRequest,
    ListCustomFieldsRequest,
    ListCustomFieldsResponse,
    UpdateCustomFieldRequest,
)
from .types.custom_field_value import CustomFieldValue
from .types.custom_pacing_curve import CustomPacingCurve, CustomPacingGoal
from .types.custom_pacing_goal_unit_enum import CustomPacingGoalUnitEnum
from .types.custom_targeting_key_enums import (
    CustomTargetingKeyReportableTypeEnum,
    CustomTargetingKeyStatusEnum,
    CustomTargetingKeyTypeEnum,
)
from .types.custom_targeting_key_messages import CustomTargetingKey
from .types.custom_targeting_key_service import (
    BatchActivateCustomTargetingKeysRequest,
    BatchActivateCustomTargetingKeysResponse,
    BatchCreateCustomTargetingKeysRequest,
    BatchCreateCustomTargetingKeysResponse,
    BatchDeactivateCustomTargetingKeysRequest,
    BatchDeactivateCustomTargetingKeysResponse,
    BatchUpdateCustomTargetingKeysRequest,
    BatchUpdateCustomTargetingKeysResponse,
    CreateCustomTargetingKeyRequest,
    GetCustomTargetingKeyRequest,
    ListCustomTargetingKeysRequest,
    ListCustomTargetingKeysResponse,
    UpdateCustomTargetingKeyRequest,
)
from .types.custom_targeting_value_enums import (
    CustomTargetingValueMatchTypeEnum,
    CustomTargetingValueStatusEnum,
)
from .types.custom_targeting_value_messages import CustomTargetingValue
from .types.custom_targeting_value_service import (
    ActivateCustomTargetingValueRequest,
    BatchActivateCustomTargetingValuesRequest,
    BatchActivateCustomTargetingValuesResponse,
    BatchCreateCustomTargetingValuesRequest,
    BatchCreateCustomTargetingValuesResponse,
    BatchDeactivateCustomTargetingValuesRequest,
    BatchDeactivateCustomTargetingValuesResponse,
    BatchUpdateCustomTargetingValuesRequest,
    BatchUpdateCustomTargetingValuesResponse,
    CreateCustomTargetingValueRequest,
    DeactivateCustomTargetingValueRequest,
    GetCustomTargetingValueRequest,
    ListCustomTargetingValuesRequest,
    ListCustomTargetingValuesResponse,
    UpdateCustomTargetingValueRequest,
)
from .types.deal_buyer_permission_type_enum import DealBuyerPermissionTypeEnum
from .types.deal_priority_tier_enum import DealPriorityTierEnum
from .types.delivery_enums import (
    CompanionDeliveryOptionEnum,
    CreativeRotationTypeEnum,
    LineItemDeliveryRateTypeEnum,
    RoadblockingTypeEnum,
)
from .types.delivery_indicator import DeliveryIndicator
from .types.device_capability_messages import DeviceCapability
from .types.device_capability_service import (
    GetDeviceCapabilityRequest,
    ListDeviceCapabilitiesRequest,
    ListDeviceCapabilitiesResponse,
)
from .types.device_category_messages import DeviceCategory
from .types.device_category_service import (
    GetDeviceCategoryRequest,
    ListDeviceCategoriesRequest,
    ListDeviceCategoriesResponse,
)
from .types.device_manufacturer_messages import DeviceManufacturer
from .types.device_manufacturer_service import (
    GetDeviceManufacturerRequest,
    ListDeviceManufacturersRequest,
    ListDeviceManufacturersResponse,
)
from .types.discount_type_enum import DiscountTypeEnum
from .types.early_ad_break_notification_enums import AdBreakStateEnum
from .types.entity_signals_mapping_messages import EntitySignalsMapping
from .types.entity_signals_mapping_service import (
    BatchCreateEntitySignalsMappingsRequest,
    BatchCreateEntitySignalsMappingsResponse,
    BatchUpdateEntitySignalsMappingsRequest,
    BatchUpdateEntitySignalsMappingsResponse,
    CreateEntitySignalsMappingRequest,
    GetEntitySignalsMappingRequest,
    ListEntitySignalsMappingsRequest,
    ListEntitySignalsMappingsResponse,
    UpdateEntitySignalsMappingRequest,
)
from .types.environment_type_enum import EnvironmentTypeEnum
from .types.exchange_syndication_product_enum import ExchangeSyndicationProductEnum
from .types.exclusion_scope_enum import ExclusionScopeEnum
from .types.frequency_cap import FrequencyCap
from .types.geo_target_messages import GeoTarget
from .types.geo_target_service import (
    GetGeoTargetRequest,
    ListGeoTargetsRequest,
    ListGeoTargetsResponse,
)
from .types.goal import Goal
from .types.goal_enums import GoalTypeEnum, UnitTypeEnum
from .types.grp_provider_enum import GrpProviderEnum
from .types.grp_settings import GrpSettings
from .types.grp_target_gender_enum import GrpTargetGenderEnum
from .types.label_enums import LabelTypeEnum
from .types.label_messages import Label
from .types.label_service import (
    BatchActivateLabelsRequest,
    BatchActivateLabelsResponse,
    BatchCreateLabelsRequest,
    BatchCreateLabelsResponse,
    BatchDeactivateLabelsRequest,
    BatchDeactivateLabelsResponse,
    BatchUpdateLabelsRequest,
    BatchUpdateLabelsResponse,
    CreateLabelRequest,
    GetLabelRequest,
    ListLabelsRequest,
    ListLabelsResponse,
    UpdateLabelRequest,
)
from .types.line_item_allowed_format_enum import LineItemAllowedFormatEnum
from .types.line_item_deal_info import LineItemDealInfo
from .types.line_item_delivery_forecast_source_enum import (
    LineItemDeliveryForecastSourceEnum,
)
from .types.line_item_discount import LineItemDiscount
from .types.line_item_enums import (
    LineItemComputedStatusEnum,
    LineItemCostTypeEnum,
    LineItemReservationStatusEnum,
    LineItemTypeEnum,
)
from .types.line_item_messages import LineItem
from .types.line_item_service import (
    GetLineItemRequest,
    ListLineItemsRequest,
    ListLineItemsResponse,
)
from .types.line_item_stats import LineItemStats
from .types.linked_device_enums import LinkedDeviceVisibilityEnum
from .types.linked_device_messages import LinkedDevice
from .types.linked_device_service import (
    GetLinkedDeviceRequest,
    ListLinkedDevicesRequest,
    ListLinkedDevicesResponse,
)
from .types.live_stream_event_enums import (
    AdBreakFillTypeEnum,
    AdBreakMarkupTypeEnum,
    DynamicAdInsertionTypeEnum,
    HlsMasterPlaylistRefreshTypeEnum,
    HlsSettingsPlaylistTypeEnum,
    LiveStreamEventStatusEnum,
    LiveStreamEventStreamingFormatEnum,
    SlateStatusEnum,
)
from .types.live_stream_event_messages import LiveStreamEvent
from .types.live_stream_messages import (
    AuxiliaryAdSettings,
    DashBridge,
    HlsSettings,
    LiveStream,
    LiveStreamConditioning,
    MasterPlaylistSettings,
    PrefetchSettings,
    PrerollSettings,
)
from .types.live_stream_service import (
    BatchActivateLiveStreamsRequest,
    BatchActivateLiveStreamsResponse,
    BatchArchiveLiveStreamsRequest,
    BatchArchiveLiveStreamsResponse,
    BatchCreateLiveStreamsRequest,
    BatchCreateLiveStreamsResponse,
    BatchPauseAdsLiveStreamsRequest,
    BatchPauseAdsLiveStreamsResponse,
    BatchPauseLiveStreamsRequest,
    BatchPauseLiveStreamsResponse,
    BatchRefreshMasterPlaylistsRequest,
    BatchRefreshMasterPlaylistsResponse,
    BatchUpdateLiveStreamsRequest,
    BatchUpdateLiveStreamsResponse,
    CreateLiveStreamRequest,
    GetLiveStreamRequest,
    ListLiveStreamsRequest,
    ListLiveStreamsResponse,
    UpdateLiveStreamRequest,
)
from .types.mcm_earnings_messages import EarningsProductBreakdown, McmEarnings
from .types.mcm_earnings_service import (
    FetchMcmEarningsRequest,
    FetchMcmEarningsResponse,
)
from .types.mcm_enums import DelegationTypeEnum, McmEarningsProductTypeEnum
from .types.mobile_carrier_messages import MobileCarrier
from .types.mobile_carrier_service import (
    GetMobileCarrierRequest,
    ListMobileCarriersRequest,
    ListMobileCarriersResponse,
)
from .types.mobile_device_messages import MobileDevice
from .types.mobile_device_service import (
    GetMobileDeviceRequest,
    ListMobileDevicesRequest,
    ListMobileDevicesResponse,
)
from .types.mobile_device_submodel_messages import MobileDeviceSubmodel
from .types.mobile_device_submodel_service import (
    GetMobileDeviceSubmodelRequest,
    ListMobileDeviceSubmodelsRequest,
    ListMobileDeviceSubmodelsResponse,
)
from .types.network_messages import Network
from .types.network_service import (
    GetNetworkRequest,
    ListNetworksRequest,
    ListNetworksResponse,
)
from .types.nielsen_ctv_pacing_enum import NielsenCtvPacingEnum
from .types.non_guaranteed_deal_priority import NonGuaranteedDealPriority
from .types.operating_system_messages import OperatingSystem
from .types.operating_system_service import (
    GetOperatingSystemRequest,
    ListOperatingSystemsRequest,
    ListOperatingSystemsResponse,
)
from .types.operating_system_version_messages import OperatingSystemVersion
from .types.operating_system_version_service import (
    GetOperatingSystemVersionRequest,
    ListOperatingSystemVersionsRequest,
    ListOperatingSystemVersionsResponse,
)
from .types.order_enums import OrderStatusEnum
from .types.order_messages import Order
from .types.order_service import (
    BatchApproveAndOverbookOrdersRequest,
    BatchApproveAndOverbookOrdersResponse,
    BatchApproveOrdersRequest,
    BatchApproveOrdersResponse,
    BatchApproveOrdersWithoutReservationRequest,
    BatchApproveOrdersWithoutReservationResponse,
    BatchArchiveOrdersRequest,
    BatchArchiveOrdersResponse,
    BatchCreateOrdersRequest,
    BatchCreateOrdersResponse,
    BatchDeleteOrdersRequest,
    BatchDeleteOrdersResponse,
    BatchDisapproveOrdersRequest,
    BatchDisapproveOrdersResponse,
    BatchDisapproveOrdersWithoutReservationChangesRequest,
    BatchDisapproveOrdersWithoutReservationChangesResponse,
    BatchPauseOrdersRequest,
    BatchPauseOrdersResponse,
    BatchResumeAndOverbookOrdersRequest,
    BatchResumeAndOverbookOrdersResponse,
    BatchResumeOrdersRequest,
    BatchResumeOrdersResponse,
    BatchRetractOrdersRequest,
    BatchRetractOrdersResponse,
    BatchRetractOrdersWithoutReservationChangesRequest,
    BatchRetractOrdersWithoutReservationChangesResponse,
    BatchSubmitOrdersForApprovalAndOverbookRequest,
    BatchSubmitOrdersForApprovalAndOverbookResponse,
    BatchSubmitOrdersForApprovalRequest,
    BatchSubmitOrdersForApprovalResponse,
    BatchSubmitOrdersForApprovalWithoutReservationChangesRequest,
    BatchSubmitOrdersForApprovalWithoutReservationChangesResponse,
    BatchUnarchiveOrdersRequest,
    BatchUnarchiveOrdersResponse,
    BatchUpdateOrdersRequest,
    BatchUpdateOrdersResponse,
    CreateOrderRequest,
    GetOrderRequest,
    ListOrdersRequest,
    ListOrdersResponse,
    UpdateOrderRequest,
)
from .types.pacing_device_categorization_enum import PacingDeviceCategorizationEnum
from .types.placement_enums import PlacementStatusEnum
from .types.placement_messages import Placement
from .types.placement_service import (
    BatchActivatePlacementsRequest,
    BatchActivatePlacementsResponse,
    BatchArchivePlacementsRequest,
    BatchArchivePlacementsResponse,
    BatchCreatePlacementsRequest,
    BatchCreatePlacementsResponse,
    BatchDeactivatePlacementsRequest,
    BatchDeactivatePlacementsResponse,
    BatchUpdatePlacementsRequest,
    BatchUpdatePlacementsResponse,
    CreatePlacementRequest,
    GetPlacementRequest,
    ListPlacementsRequest,
    ListPlacementsResponse,
    UpdatePlacementRequest,
)
from .types.private_auction_deal_messages import PrivateAuctionDeal
from .types.private_auction_deal_service import (
    CreatePrivateAuctionDealRequest,
    GetPrivateAuctionDealRequest,
    ListPrivateAuctionDealsRequest,
    ListPrivateAuctionDealsResponse,
    UpdatePrivateAuctionDealRequest,
)
from .types.private_auction_messages import PrivateAuction
from .types.private_auction_service import (
    CreatePrivateAuctionRequest,
    GetPrivateAuctionRequest,
    ListPrivateAuctionsRequest,
    ListPrivateAuctionsResponse,
    UpdatePrivateAuctionRequest,
)
from .types.private_marketplace_enums import PrivateMarketplaceDealStatusEnum
from .types.programmatic_buyer_messages import ProgrammaticBuyer
from .types.programmatic_buyer_service import (
    GetProgrammaticBuyerRequest,
    ListProgrammaticBuyersRequest,
    ListProgrammaticBuyersResponse,
)
from .types.reach_partner_enum import ReachPartnerEnum
from .types.report_definition import ReportDefinition
from .types.report_delivery import ScheduleOptions
from .types.report_messages import Report, ReportDataTable
from .types.report_service import (
    CreateReportRequest,
    FetchReportResultRowsRequest,
    FetchReportResultRowsResponse,
    GetReportRequest,
    ListReportsRequest,
    ListReportsResponse,
    RunReportMetadata,
    RunReportRequest,
    RunReportResponse,
    UpdateReportRequest,
)
from .types.report_value import ReportValue
from .types.request_platform_enum import RequestPlatformEnum
from .types.rich_media_ads_company_enums import RichMediaAdsCompanyGdprStatusEnum
from .types.rich_media_ads_company_messages import RichMediaAdsCompany
from .types.rich_media_ads_company_service import (
    GetRichMediaAdsCompanyRequest,
    ListRichMediaAdsCompaniesRequest,
    ListRichMediaAdsCompaniesResponse,
)
from .types.role_enums import RoleStatusEnum
from .types.role_messages import Role
from .types.role_service import GetRoleRequest, ListRolesRequest, ListRolesResponse
from .types.site_enums import SiteApprovalStatusEnum, SiteDisapprovalReasonEnum
from .types.site_messages import DisapprovalReason, Site
from .types.site_service import (
    BatchCreateSitesRequest,
    BatchCreateSitesResponse,
    BatchDeactivateSitesRequest,
    BatchDeactivateSitesResponse,
    BatchSubmitSitesForApprovalRequest,
    BatchSubmitSitesForApprovalResponse,
    BatchUpdateSitesRequest,
    BatchUpdateSitesResponse,
    CreateSiteRequest,
    GetSiteRequest,
    ListSitesRequest,
    ListSitesResponse,
    UpdateSiteRequest,
)
from .types.size import Size
from .types.size_type_enum import SizeTypeEnum
from .types.skippable_ad_type_enum import SkippableAdTypeEnum
from .types.slate_messages import Slate
from .types.slate_service import (
    BatchArchiveSlatesRequest,
    BatchArchiveSlatesResponse,
    BatchCreateSlatesRequest,
    BatchCreateSlatesResponse,
    BatchUnarchiveSlatesRequest,
    BatchUnarchiveSlatesResponse,
    BatchUpdateSlatesRequest,
    BatchUpdateSlatesResponse,
    CreateSlateRequest,
    GetSlateRequest,
    ListSlatesRequest,
    ListSlatesResponse,
    UpdateSlateRequest,
)
from .types.suggested_ad_unit_messages import SuggestedAdUnit
from .types.suggested_ad_unit_service import (
    BatchApproveSuggestedAdUnitsRequest,
    BatchApproveSuggestedAdUnitsResponse,
    GetSuggestedAdUnitRequest,
    ListSuggestedAdUnitsRequest,
    ListSuggestedAdUnitsResponse,
)
from .types.target_platform_enum import TargetPlatformEnum
from .types.targeted_video_bumper_type_enum import TargetedVideoBumperTypeEnum
from .types.targeting import (
    AdUnitTargeting,
    AudienceSegmentTargeting,
    BandwidthTargeting,
    BrowserLanguageTargeting,
    BrowserTargeting,
    CmsMetadataTargeting,
    ContentTargeting,
    CustomTargeting,
    CustomTargetingClause,
    CustomTargetingLiteral,
    DataSegmentTargeting,
    DeviceCapabilityTargeting,
    DeviceCategoryTargeting,
    DeviceManufacturerTargeting,
    FirstPartyMobileApplicationTargeting,
    GeoTargeting,
    InventoryTargeting,
    MobileApplicationTargeting,
    MobileCarrierTargeting,
    OperatingSystemTargeting,
    RequestFormatTargeting,
    RequestPlatformTargeting,
    Targeting,
    TechnologyTargeting,
    UserDomainTargeting,
    VideoPosition,
    VideoPositionTargeting,
)
from .types.targeting_preset_enums import TargetingPresetStatusEnum
from .types.targeting_preset_messages import TargetingPreset
from .types.targeting_preset_service import (
    BatchCreateTargetingPresetsRequest,
    BatchCreateTargetingPresetsResponse,
    BatchDeactivateTargetingPresetsRequest,
    BatchDeactivateTargetingPresetsResponse,
    BatchUpdateTargetingPresetsRequest,
    BatchUpdateTargetingPresetsResponse,
    CreateTargetingPresetRequest,
    DeactivateTargetingPresetRequest,
    GetTargetingPresetRequest,
    ListTargetingPresetsRequest,
    ListTargetingPresetsResponse,
    UpdateTargetingPresetRequest,
)
from .types.taxonomy_category_messages import TaxonomyCategory
from .types.taxonomy_category_service import (
    GetTaxonomyCategoryRequest,
    ListTaxonomyCategoriesRequest,
    ListTaxonomyCategoriesResponse,
)
from .types.taxonomy_type_enum import TaxonomyTypeEnum
from .types.team_enums import TeamAccessTypeEnum, TeamStatusEnum
from .types.team_messages import Team
from .types.team_service import (
    BatchActivateTeamsRequest,
    BatchActivateTeamsResponse,
    BatchCreateTeamsRequest,
    BatchCreateTeamsResponse,
    BatchDeactivateTeamsRequest,
    BatchDeactivateTeamsResponse,
    BatchUpdateTeamsRequest,
    BatchUpdateTeamsResponse,
    CreateTeamRequest,
    GetTeamRequest,
    ListTeamsRequest,
    ListTeamsResponse,
    UpdateTeamRequest,
)
from .types.third_party_company_enums import (
    ThirdPartyCompanyStatusEnum,
    ThirdPartyCompanyTypeEnum,
)
from .types.third_party_company_messages import ThirdPartyCompany
from .types.third_party_company_service import (
    GetThirdPartyCompanyRequest,
    ListThirdPartyCompaniesRequest,
    ListThirdPartyCompaniesResponse,
)
from .types.third_party_measurement_settings import ThirdPartyMeasurementSettings
from .types.time_unit_enum import TimeUnitEnum
from .types.user_messages import User
from .types.user_service import GetUserRequest
from .types.video_position_enum import VideoPositionEnum
from .types.video_transcode_status_enum import VideoTranscodeStatusEnum
from .types.viewability_partner_enum import ViewabilityPartnerEnum
from .types.web_property import WebProperty

if hasattr(api_core, "check_python_version") and hasattr(
    api_core, "check_dependency_versions"
):  # pragma: NO COVER
    api_core.check_python_version("google.ads.admanager_v1")  # type: ignore
    api_core.check_dependency_versions("google.ads.admanager_v1")  # type: ignore
else:  # pragma: NO COVER
    # An older version of api_core is installed which does not define the
    # functions above. We do equivalent checks manually.
    try:
        import warnings

        _py_version_str = sys.version.split()[0]
        _package_label = "google.ads.admanager_v1"
        if sys.version_info < (3, 10):
            warnings.warn(
                "You are using a non-supported Python version "
                + f"({_py_version_str}).  Google will not post any further "
                + f"updates to {_package_label} supporting this Python version. "
                + "Please upgrade to the latest Python version, or at "
                + f"least to Python 3.10, and then update {_package_label}.",
                FutureWarning,
            )

        def parse_version_to_tuple(version_string: str):
            """Safely converts a semantic version string to a comparable tuple of integers.
            Example: "6.33.5" -> (6, 33, 5)
            Ignores non-numeric parts and handles common version formats.
            Args:
                version_string: Version string in the format "x.y.z" or "x.y.z<suffix>"
            Returns:
                Tuple of integers for the parsed version string.
            """
            parts = []
            for part in version_string.split("."):
                try:
                    parts.append(int(part))
                except ValueError:
                    # If it's a non-numeric part (e.g., '1.0.0b1' -> 'b1'), stop here.
                    # This is a simplification compared to 'packaging.parse_version', but sufficient
                    # for comparing strictly numeric semantic versions.
                    break
            return tuple(parts)

        def _get_version(dependency_name):
            try:
                version_string: str = metadata.version(dependency_name)
                parsed_version = parse_version_to_tuple(version_string)
                return (parsed_version, version_string)
            except Exception:
                # Catch exceptions from metadata.version() (e.g., PackageNotFoundError)
                # or errors during parse_version_to_tuple
                return (None, "--")

        _dependency_package = "google.protobuf"
        _next_supported_version = "6.33.5"
        _next_supported_version_tuple = (6, 33, 5)
        _recommendation = " (we recommend 7.x)"
        (_version_used, _version_used_string) = _get_version(_dependency_package)
        if _version_used and _version_used < _next_supported_version_tuple:
            warnings.warn(
                f"Package {_package_label} depends on "
                + f"{_dependency_package}, currently installed at version "
                + f"{_version_used_string}. Future updates to "
                + f"{_package_label} will require {_dependency_package} at "
                + f"version {_next_supported_version} or higher{_recommendation}."
                + " Please ensure "
                + "that either (a) your Python environment doesn't pin the "
                + f"version of {_dependency_package}, so that updates to "
                + f"{_package_label} can require the higher version, or "
                + "(b) you manually update your Python environment to use at "
                + f"least version {_next_supported_version} of "
                + f"{_dependency_package}.",
                FutureWarning,
            )
    except Exception:
        warnings.warn(
            "Could not determine the version of Python "
            + "currently being used. To continue receiving "
            + "updates for {_package_label}, ensure you are "
            + "using a supported version of Python; see "
            + "https://devguide.python.org/versions/"
        )

__all__ = (
    "ActivateCustomTargetingValueRequest",
    "AdBreak",
    "AdBreakFillTypeEnum",
    "AdBreakMarkupTypeEnum",
    "AdBreakServiceClient",
    "AdBreakStateEnum",
    "AdManagerError",
    "AdMediaDeliveryConfig",
    "AdReviewCenterAd",
    "AdReviewCenterAdServiceClient",
    "AdReviewCenterAdStatusEnum",
    "AdRule",
    "AdRuleFrequencyCapBehaviorEnum",
    "AdRuleServiceClient",
    "AdRuleSlot",
    "AdRuleSlotBehaviorEnum",
    "AdRuleSlotBumperEnum",
    "AdRuleSlotMidrollFrequencyTypeEnum",
    "AdRuleStatusEnum",
    "AdSpot",
    "AdSpotServiceClient",
    "AdSpotTargetingTypeEnum",
    "AdUnit",
    "AdUnitParent",
    "AdUnitServiceClient",
    "AdUnitSize",
    "AdUnitStatusEnum",
    "AdUnitTargeting",
    "Application",
    "ApplicationApprovalStatusEnum",
    "ApplicationPlatformEnum",
    "ApplicationServiceClient",
    "ApplicationStoreEnum",
    "AppliedLabel",
    "AudienceSegment",
    "AudienceSegmentServiceClient",
    "AudienceSegmentTargeting",
    "AuxiliaryAdSettings",
    "BandwidthGroup",
    "BandwidthGroupServiceClient",
    "BandwidthTargeting",
    "BatchActivateAdRulesRequest",
    "BatchActivateAdRulesResponse",
    "BatchActivateAdUnitsRequest",
    "BatchActivateAdUnitsResponse",
    "BatchActivateCdnConfigsRequest",
    "BatchActivateCdnConfigsResponse",
    "BatchActivateCmsMetadataKeysRequest",
    "BatchActivateCmsMetadataKeysResponse",
    "BatchActivateCmsMetadataValuesRequest",
    "BatchActivateCmsMetadataValuesResponse",
    "BatchActivateContentBundlesRequest",
    "BatchActivateContentBundlesResponse",
    "BatchActivateCustomFieldsRequest",
    "BatchActivateCustomFieldsResponse",
    "BatchActivateCustomTargetingKeysRequest",
    "BatchActivateCustomTargetingKeysResponse",
    "BatchActivateCustomTargetingValuesRequest",
    "BatchActivateCustomTargetingValuesResponse",
    "BatchActivateLabelsRequest",
    "BatchActivateLabelsResponse",
    "BatchActivateLiveStreamsRequest",
    "BatchActivateLiveStreamsResponse",
    "BatchActivatePlacementsRequest",
    "BatchActivatePlacementsResponse",
    "BatchActivateTeamsRequest",
    "BatchActivateTeamsResponse",
    "BatchAdReviewCenterAdsOperationMetadata",
    "BatchAllowAdReviewCenterAdsRequest",
    "BatchAllowAdReviewCenterAdsResponse",
    "BatchApproveAndOverbookOrdersRequest",
    "BatchApproveAndOverbookOrdersResponse",
    "BatchApproveOrdersRequest",
    "BatchApproveOrdersResponse",
    "BatchApproveOrdersWithoutReservationRequest",
    "BatchApproveOrdersWithoutReservationResponse",
    "BatchApproveSuggestedAdUnitsRequest",
    "BatchApproveSuggestedAdUnitsResponse",
    "BatchArchiveAdUnitsRequest",
    "BatchArchiveAdUnitsResponse",
    "BatchArchiveApplicationsRequest",
    "BatchArchiveApplicationsResponse",
    "BatchArchiveCdnConfigsRequest",
    "BatchArchiveCdnConfigsResponse",
    "BatchArchiveLiveStreamsRequest",
    "BatchArchiveLiveStreamsResponse",
    "BatchArchiveOrdersRequest",
    "BatchArchiveOrdersResponse",
    "BatchArchivePlacementsRequest",
    "BatchArchivePlacementsResponse",
    "BatchArchiveSlatesRequest",
    "BatchArchiveSlatesResponse",
    "BatchBlockAdReviewCenterAdsRequest",
    "BatchBlockAdReviewCenterAdsResponse",
    "BatchCreateAdRulesRequest",
    "BatchCreateAdRulesResponse",
    "BatchCreateAdSpotsRequest",
    "BatchCreateAdSpotsResponse",
    "BatchCreateAdUnitsRequest",
    "BatchCreateAdUnitsResponse",
    "BatchCreateApplicationsRequest",
    "BatchCreateApplicationsResponse",
    "BatchCreateCdnConfigsRequest",
    "BatchCreateCdnConfigsResponse",
    "BatchCreateContactsRequest",
    "BatchCreateContactsResponse",
    "BatchCreateCustomFieldsRequest",
    "BatchCreateCustomFieldsResponse",
    "BatchCreateCustomTargetingKeysRequest",
    "BatchCreateCustomTargetingKeysResponse",
    "BatchCreateCustomTargetingValuesRequest",
    "BatchCreateCustomTargetingValuesResponse",
    "BatchCreateEntitySignalsMappingsRequest",
    "BatchCreateEntitySignalsMappingsResponse",
    "BatchCreateLabelsRequest",
    "BatchCreateLabelsResponse",
    "BatchCreateLiveStreamsRequest",
    "BatchCreateLiveStreamsResponse",
    "BatchCreateOrdersRequest",
    "BatchCreateOrdersResponse",
    "BatchCreatePlacementsRequest",
    "BatchCreatePlacementsResponse",
    "BatchCreateSitesRequest",
    "BatchCreateSitesResponse",
    "BatchCreateSlatesRequest",
    "BatchCreateSlatesResponse",
    "BatchCreateTargetingPresetsRequest",
    "BatchCreateTargetingPresetsResponse",
    "BatchCreateTeamsRequest",
    "BatchCreateTeamsResponse",
    "BatchDeactivateAdRulesRequest",
    "BatchDeactivateAdRulesResponse",
    "BatchDeactivateAdUnitsRequest",
    "BatchDeactivateAdUnitsResponse",
    "BatchDeactivateCmsMetadataKeysRequest",
    "BatchDeactivateCmsMetadataKeysResponse",
    "BatchDeactivateCmsMetadataValuesRequest",
    "BatchDeactivateCmsMetadataValuesResponse",
    "BatchDeactivateContentBundlesRequest",
    "BatchDeactivateContentBundlesResponse",
    "BatchDeactivateCustomFieldsRequest",
    "BatchDeactivateCustomFieldsResponse",
    "BatchDeactivateCustomTargetingKeysRequest",
    "BatchDeactivateCustomTargetingKeysResponse",
    "BatchDeactivateCustomTargetingValuesRequest",
    "BatchDeactivateCustomTargetingValuesResponse",
    "BatchDeactivateLabelsRequest",
    "BatchDeactivateLabelsResponse",
    "BatchDeactivatePlacementsRequest",
    "BatchDeactivatePlacementsResponse",
    "BatchDeactivateSitesRequest",
    "BatchDeactivateSitesResponse",
    "BatchDeactivateTargetingPresetsRequest",
    "BatchDeactivateTargetingPresetsResponse",
    "BatchDeactivateTeamsRequest",
    "BatchDeactivateTeamsResponse",
    "BatchDeleteAdRulesRequest",
    "BatchDeleteOrdersRequest",
    "BatchDeleteOrdersResponse",
    "BatchDisapproveOrdersRequest",
    "BatchDisapproveOrdersResponse",
    "BatchDisapproveOrdersWithoutReservationChangesRequest",
    "BatchDisapproveOrdersWithoutReservationChangesResponse",
    "BatchPauseAdsLiveStreamsRequest",
    "BatchPauseAdsLiveStreamsResponse",
    "BatchPauseLiveStreamsRequest",
    "BatchPauseLiveStreamsResponse",
    "BatchPauseOrdersRequest",
    "BatchPauseOrdersResponse",
    "BatchRefreshMasterPlaylistsRequest",
    "BatchRefreshMasterPlaylistsResponse",
    "BatchResumeAndOverbookOrdersRequest",
    "BatchResumeAndOverbookOrdersResponse",
    "BatchResumeOrdersRequest",
    "BatchResumeOrdersResponse",
    "BatchRetractOrdersRequest",
    "BatchRetractOrdersResponse",
    "BatchRetractOrdersWithoutReservationChangesRequest",
    "BatchRetractOrdersWithoutReservationChangesResponse",
    "BatchSubmitOrdersForApprovalAndOverbookRequest",
    "BatchSubmitOrdersForApprovalAndOverbookResponse",
    "BatchSubmitOrdersForApprovalRequest",
    "BatchSubmitOrdersForApprovalResponse",
    "BatchSubmitOrdersForApprovalWithoutReservationChangesRequest",
    "BatchSubmitOrdersForApprovalWithoutReservationChangesResponse",
    "BatchSubmitSitesForApprovalRequest",
    "BatchSubmitSitesForApprovalResponse",
    "BatchUnarchiveApplicationsRequest",
    "BatchUnarchiveApplicationsResponse",
    "BatchUnarchiveOrdersRequest",
    "BatchUnarchiveOrdersResponse",
    "BatchUnarchiveSlatesRequest",
    "BatchUnarchiveSlatesResponse",
    "BatchUpdateAdRulesRequest",
    "BatchUpdateAdRulesResponse",
    "BatchUpdateAdSpotsRequest",
    "BatchUpdateAdSpotsResponse",
    "BatchUpdateAdUnitsRequest",
    "BatchUpdateAdUnitsResponse",
    "BatchUpdateApplicationsRequest",
    "BatchUpdateApplicationsResponse",
    "BatchUpdateCdnConfigsRequest",
    "BatchUpdateCdnConfigsResponse",
    "BatchUpdateContactsRequest",
    "BatchUpdateContactsResponse",
    "BatchUpdateCustomFieldsRequest",
    "BatchUpdateCustomFieldsResponse",
    "BatchUpdateCustomTargetingKeysRequest",
    "BatchUpdateCustomTargetingKeysResponse",
    "BatchUpdateCustomTargetingValuesRequest",
    "BatchUpdateCustomTargetingValuesResponse",
    "BatchUpdateEntitySignalsMappingsRequest",
    "BatchUpdateEntitySignalsMappingsResponse",
    "BatchUpdateLabelsRequest",
    "BatchUpdateLabelsResponse",
    "BatchUpdateLiveStreamsRequest",
    "BatchUpdateLiveStreamsResponse",
    "BatchUpdateOrdersRequest",
    "BatchUpdateOrdersResponse",
    "BatchUpdatePlacementsRequest",
    "BatchUpdatePlacementsResponse",
    "BatchUpdateSitesRequest",
    "BatchUpdateSitesResponse",
    "BatchUpdateSlatesRequest",
    "BatchUpdateSlatesResponse",
    "BatchUpdateTargetingPresetsRequest",
    "BatchUpdateTargetingPresetsResponse",
    "BatchUpdateTeamsRequest",
    "BatchUpdateTeamsResponse",
    "BrandLiftPartnerEnum",
    "Browser",
    "BrowserLanguage",
    "BrowserLanguageServiceClient",
    "BrowserLanguageTargeting",
    "BrowserServiceClient",
    "BrowserTargeting",
    "CdnConfig",
    "CdnConfigServiceClient",
    "CdnConfigStatusEnum",
    "CdnConfigTypeEnum",
    "CdnSecurityPolicy",
    "CdnSecurityPolicyOriginForwardingEnum",
    "CdnSecurityPolicyTypeEnum",
    "ChildContentEligibilityEnum",
    "ChildPublisher",
    "CmsContent",
    "CmsMetadataKey",
    "CmsMetadataKeyServiceClient",
    "CmsMetadataKeyStatusEnum",
    "CmsMetadataTargeting",
    "CmsMetadataValue",
    "CmsMetadataValueServiceClient",
    "CmsMetadataValueStatusEnum",
    "CompanionDeliveryOptionEnum",
    "Company",
    "CompanyCreditStatusEnum",
    "CompanyServiceClient",
    "CompanyTypeEnum",
    "Contact",
    "ContactServiceClient",
    "ContactStatusEnum",
    "Content",
    "ContentBundle",
    "ContentBundleServiceClient",
    "ContentBundleStatusEnum",
    "ContentLabel",
    "ContentLabelServiceClient",
    "ContentServiceClient",
    "ContentStatusEnum",
    "ContentStatusSourceEnum",
    "ContentTargeting",
    "CreateAdBreakRequest",
    "CreateAdRuleRequest",
    "CreateAdSpotRequest",
    "CreateAdUnitRequest",
    "CreateApplicationRequest",
    "CreateCdnConfigRequest",
    "CreateContactRequest",
    "CreateCreativeSetRequest",
    "CreateCustomFieldRequest",
    "CreateCustomTargetingKeyRequest",
    "CreateCustomTargetingValueRequest",
    "CreateEntitySignalsMappingRequest",
    "CreateLabelRequest",
    "CreateLiveStreamRequest",
    "CreateOrderRequest",
    "CreatePlacementRequest",
    "CreatePrivateAuctionDealRequest",
    "CreatePrivateAuctionRequest",
    "CreateReportRequest",
    "CreateSiteRequest",
    "CreateSlateRequest",
    "CreateTargetingPresetRequest",
    "CreateTeamRequest",
    "Creative",
    "CreativePlaceholder",
    "CreativePlaceholderCompanion",
    "CreativeRotationTypeEnum",
    "CreativeSet",
    "CreativeSetServiceClient",
    "CreativeTargeting",
    "CreativeTemplate",
    "CreativeTemplateServiceClient",
    "CreativeTemplateStatusEnum",
    "CreativeTemplateTypeEnum",
    "CreativeTemplateVariable",
    "CreativeTemplateVariableUrlTypeEnum",
    "CustomField",
    "CustomFieldDataTypeEnum",
    "CustomFieldEntityTypeEnum",
    "CustomFieldOption",
    "CustomFieldServiceClient",
    "CustomFieldStatusEnum",
    "CustomFieldValue",
    "CustomFieldVisibilityEnum",
    "CustomPacingCurve",
    "CustomPacingGoal",
    "CustomPacingGoalUnitEnum",
    "CustomTargeting",
    "CustomTargetingClause",
    "CustomTargetingKey",
    "CustomTargetingKeyReportableTypeEnum",
    "CustomTargetingKeyServiceClient",
    "CustomTargetingKeyStatusEnum",
    "CustomTargetingKeyTypeEnum",
    "CustomTargetingLiteral",
    "CustomTargetingValue",
    "CustomTargetingValueMatchTypeEnum",
    "CustomTargetingValueServiceClient",
    "CustomTargetingValueStatusEnum",
    "DaiIngestError",
    "DaiIngestErrorReasonEnum",
    "DaiIngestStatusEnum",
    "DashBridge",
    "DataSegmentTargeting",
    "DeactivateCustomTargetingValueRequest",
    "DeactivateTargetingPresetRequest",
    "DealBuyerPermissionTypeEnum",
    "DealPriorityTierEnum",
    "DelegationTypeEnum",
    "DeleteAdBreakRequest",
    "DeliveryIndicator",
    "DeviceCapability",
    "DeviceCapabilityServiceClient",
    "DeviceCapabilityTargeting",
    "DeviceCategory",
    "DeviceCategoryServiceClient",
    "DeviceCategoryTargeting",
    "DeviceManufacturer",
    "DeviceManufacturerServiceClient",
    "DeviceManufacturerTargeting",
    "DisapprovalReason",
    "DiscountTypeEnum",
    "DynamicAdInsertionTypeEnum",
    "EarningsProductBreakdown",
    "EntitySignalsMapping",
    "EntitySignalsMappingServiceClient",
    "EnvironmentTypeEnum",
    "ExchangeSyndicationProductEnum",
    "ExclusionScopeEnum",
    "FetchMcmEarningsRequest",
    "FetchMcmEarningsResponse",
    "FetchReportResultRowsRequest",
    "FetchReportResultRowsResponse",
    "FirstPartyMobileApplicationTargeting",
    "FrequencyCap",
    "GeoTarget",
    "GeoTargetServiceClient",
    "GeoTargeting",
    "GetAdBreakRequest",
    "GetAdRuleRequest",
    "GetAdSpotRequest",
    "GetAdUnitRequest",
    "GetApplicationRequest",
    "GetAudienceSegmentRequest",
    "GetBandwidthGroupRequest",
    "GetBrowserLanguageRequest",
    "GetBrowserRequest",
    "GetCdnConfigRequest",
    "GetCmsMetadataKeyRequest",
    "GetCmsMetadataValueRequest",
    "GetCompanyRequest",
    "GetContactRequest",
    "GetContentBundleRequest",
    "GetContentLabelRequest",
    "GetContentRequest",
    "GetCreativeSetRequest",
    "GetCreativeTemplateRequest",
    "GetCustomFieldRequest",
    "GetCustomTargetingKeyRequest",
    "GetCustomTargetingValueRequest",
    "GetDeviceCapabilityRequest",
    "GetDeviceCategoryRequest",
    "GetDeviceManufacturerRequest",
    "GetEntitySignalsMappingRequest",
    "GetGeoTargetRequest",
    "GetLabelRequest",
    "GetLineItemRequest",
    "GetLinkedDeviceRequest",
    "GetLiveStreamRequest",
    "GetMobileCarrierRequest",
    "GetMobileDeviceRequest",
    "GetMobileDeviceSubmodelRequest",
    "GetNetworkRequest",
    "GetOperatingSystemRequest",
    "GetOperatingSystemVersionRequest",
    "GetOrderRequest",
    "GetPlacementRequest",
    "GetPrivateAuctionDealRequest",
    "GetPrivateAuctionRequest",
    "GetProgrammaticBuyerRequest",
    "GetReportRequest",
    "GetRichMediaAdsCompanyRequest",
    "GetRoleRequest",
    "GetSiteRequest",
    "GetSlateRequest",
    "GetSuggestedAdUnitRequest",
    "GetTargetingPresetRequest",
    "GetTaxonomyCategoryRequest",
    "GetTeamRequest",
    "GetThirdPartyCompanyRequest",
    "GetUserRequest",
    "Goal",
    "GoalTypeEnum",
    "GrpProviderEnum",
    "GrpSettings",
    "GrpTargetGenderEnum",
    "HlsMasterPlaylistRefreshTypeEnum",
    "HlsSettings",
    "HlsSettingsPlaylistTypeEnum",
    "InventoryTargeting",
    "Label",
    "LabelFrequencyCap",
    "LabelServiceClient",
    "LabelTypeEnum",
    "LineItem",
    "LineItemAllowedFormatEnum",
    "LineItemComputedStatusEnum",
    "LineItemCostTypeEnum",
    "LineItemDealInfo",
    "LineItemDeliveryForecastSourceEnum",
    "LineItemDeliveryRateTypeEnum",
    "LineItemDiscount",
    "LineItemReservationStatusEnum",
    "LineItemServiceClient",
    "LineItemStats",
    "LineItemTypeEnum",
    "LinkedDevice",
    "LinkedDeviceServiceClient",
    "LinkedDeviceVisibilityEnum",
    "ListAdBreaksRequest",
    "ListAdBreaksResponse",
    "ListAdRulesRequest",
    "ListAdRulesResponse",
    "ListAdSpotsRequest",
    "ListAdSpotsResponse",
    "ListAdUnitSizesRequest",
    "ListAdUnitSizesResponse",
    "ListAdUnitsRequest",
    "ListAdUnitsResponse",
    "ListApplicationsRequest",
    "ListApplicationsResponse",
    "ListAudienceSegmentsRequest",
    "ListAudienceSegmentsResponse",
    "ListBandwidthGroupsRequest",
    "ListBandwidthGroupsResponse",
    "ListBrowserLanguagesRequest",
    "ListBrowserLanguagesResponse",
    "ListBrowsersRequest",
    "ListBrowsersResponse",
    "ListCdnConfigsRequest",
    "ListCdnConfigsResponse",
    "ListCmsMetadataKeysRequest",
    "ListCmsMetadataKeysResponse",
    "ListCmsMetadataValuesRequest",
    "ListCmsMetadataValuesResponse",
    "ListCompaniesRequest",
    "ListCompaniesResponse",
    "ListContactsRequest",
    "ListContactsResponse",
    "ListContentBundlesRequest",
    "ListContentBundlesResponse",
    "ListContentLabelsRequest",
    "ListContentLabelsResponse",
    "ListContentRequest",
    "ListContentResponse",
    "ListCreativeSetsRequest",
    "ListCreativeSetsResponse",
    "ListCreativeTemplatesRequest",
    "ListCreativeTemplatesResponse",
    "ListCustomFieldsRequest",
    "ListCustomFieldsResponse",
    "ListCustomTargetingKeysRequest",
    "ListCustomTargetingKeysResponse",
    "ListCustomTargetingValuesRequest",
    "ListCustomTargetingValuesResponse",
    "ListDeviceCapabilitiesRequest",
    "ListDeviceCapabilitiesResponse",
    "ListDeviceCategoriesRequest",
    "ListDeviceCategoriesResponse",
    "ListDeviceManufacturersRequest",
    "ListDeviceManufacturersResponse",
    "ListEntitySignalsMappingsRequest",
    "ListEntitySignalsMappingsResponse",
    "ListGeoTargetsRequest",
    "ListGeoTargetsResponse",
    "ListLabelsRequest",
    "ListLabelsResponse",
    "ListLineItemsRequest",
    "ListLineItemsResponse",
    "ListLinkedDevicesRequest",
    "ListLinkedDevicesResponse",
    "ListLiveStreamsRequest",
    "ListLiveStreamsResponse",
    "ListMobileCarriersRequest",
    "ListMobileCarriersResponse",
    "ListMobileDeviceSubmodelsRequest",
    "ListMobileDeviceSubmodelsResponse",
    "ListMobileDevicesRequest",
    "ListMobileDevicesResponse",
    "ListNetworksRequest",
    "ListNetworksResponse",
    "ListOperatingSystemVersionsRequest",
    "ListOperatingSystemVersionsResponse",
    "ListOperatingSystemsRequest",
    "ListOperatingSystemsResponse",
    "ListOrdersRequest",
    "ListOrdersResponse",
    "ListPlacementsRequest",
    "ListPlacementsResponse",
    "ListPrivateAuctionDealsRequest",
    "ListPrivateAuctionDealsResponse",
    "ListPrivateAuctionsRequest",
    "ListPrivateAuctionsResponse",
    "ListProgrammaticBuyersRequest",
    "ListProgrammaticBuyersResponse",
    "ListReportsRequest",
    "ListReportsResponse",
    "ListRichMediaAdsCompaniesRequest",
    "ListRichMediaAdsCompaniesResponse",
    "ListRolesRequest",
    "ListRolesResponse",
    "ListSitesRequest",
    "ListSitesResponse",
    "ListSlatesRequest",
    "ListSlatesResponse",
    "ListSuggestedAdUnitsRequest",
    "ListSuggestedAdUnitsResponse",
    "ListTargetingPresetsRequest",
    "ListTargetingPresetsResponse",
    "ListTaxonomyCategoriesRequest",
    "ListTaxonomyCategoriesResponse",
    "ListTeamsRequest",
    "ListTeamsResponse",
    "ListThirdPartyCompaniesRequest",
    "ListThirdPartyCompaniesResponse",
    "LiveStream",
    "LiveStreamConditioning",
    "LiveStreamEvent",
    "LiveStreamEventStatusEnum",
    "LiveStreamEventStreamingFormatEnum",
    "LiveStreamServiceClient",
    "ManualAdReviewCenterAdStatusEnum",
    "MasterPlaylistSettings",
    "McmEarnings",
    "McmEarningsProductTypeEnum",
    "McmEarningsServiceClient",
    "MediaLocation",
    "MobileApplicationTargeting",
    "MobileCarrier",
    "MobileCarrierServiceClient",
    "MobileCarrierTargeting",
    "MobileDevice",
    "MobileDeviceServiceClient",
    "MobileDeviceSubmodel",
    "MobileDeviceSubmodelServiceClient",
    "Network",
    "NetworkServiceClient",
    "NielsenCtvPacingEnum",
    "NonGuaranteedDealPriority",
    "OperatingSystem",
    "OperatingSystemServiceClient",
    "OperatingSystemTargeting",
    "OperatingSystemVersion",
    "OperatingSystemVersionServiceClient",
    "Order",
    "OrderServiceClient",
    "OrderStatusEnum",
    "PacingDeviceCategorizationEnum",
    "Placement",
    "PlacementServiceClient",
    "PlacementStatusEnum",
    "PrefetchSettings",
    "PrerollSettings",
    "PrivateAuction",
    "PrivateAuctionDeal",
    "PrivateAuctionDealServiceClient",
    "PrivateAuctionServiceClient",
    "PrivateMarketplaceDealStatusEnum",
    "ProgrammaticBuyer",
    "ProgrammaticBuyerServiceClient",
    "ReachPartnerEnum",
    "Report",
    "ReportDataTable",
    "ReportDefinition",
    "ReportServiceClient",
    "ReportValue",
    "RequestFormatTargeting",
    "RequestPlatformEnum",
    "RequestPlatformTargeting",
    "RichMediaAdsCompany",
    "RichMediaAdsCompanyGdprStatusEnum",
    "RichMediaAdsCompanyServiceClient",
    "RoadblockingTypeEnum",
    "Role",
    "RoleServiceClient",
    "RoleStatusEnum",
    "RunReportMetadata",
    "RunReportRequest",
    "RunReportResponse",
    "ScheduleOptions",
    "SearchAdReviewCenterAdsRequest",
    "SearchAdReviewCenterAdsResponse",
    "Site",
    "SiteApprovalStatusEnum",
    "SiteDisapprovalReasonEnum",
    "SiteServiceClient",
    "Size",
    "SizeTypeEnum",
    "SkippableAdTypeEnum",
    "Slate",
    "SlateServiceClient",
    "SlateStatusEnum",
    "SmartSizeModeEnum",
    "SourceContentConfig",
    "SuggestedAdUnit",
    "SuggestedAdUnitServiceClient",
    "TargetPlatformEnum",
    "TargetWindowEnum",
    "TargetedVideoBumperTypeEnum",
    "Targeting",
    "TargetingPreset",
    "TargetingPresetServiceClient",
    "TargetingPresetStatusEnum",
    "TaxonomyCategory",
    "TaxonomyCategoryServiceClient",
    "TaxonomyTypeEnum",
    "Team",
    "TeamAccessTypeEnum",
    "TeamServiceClient",
    "TeamStatusEnum",
    "TechnologyTargeting",
    "ThirdPartyCompany",
    "ThirdPartyCompanyServiceClient",
    "ThirdPartyCompanyStatusEnum",
    "ThirdPartyCompanyTypeEnum",
    "ThirdPartyMeasurementSettings",
    "TimeUnitEnum",
    "UnitTypeEnum",
    "UpdateAdBreakRequest",
    "UpdateAdRuleRequest",
    "UpdateAdSpotRequest",
    "UpdateAdUnitRequest",
    "UpdateApplicationRequest",
    "UpdateCdnConfigRequest",
    "UpdateContactRequest",
    "UpdateCreativeSetRequest",
    "UpdateCustomFieldRequest",
    "UpdateCustomTargetingKeyRequest",
    "UpdateCustomTargetingValueRequest",
    "UpdateEntitySignalsMappingRequest",
    "UpdateLabelRequest",
    "UpdateLiveStreamRequest",
    "UpdateOrderRequest",
    "UpdatePlacementRequest",
    "UpdatePrivateAuctionDealRequest",
    "UpdatePrivateAuctionRequest",
    "UpdateReportRequest",
    "UpdateSiteRequest",
    "UpdateSlateRequest",
    "UpdateTargetingPresetRequest",
    "UpdateTeamRequest",
    "User",
    "UserDomainTargeting",
    "UserServiceClient",
    "VideoPosition",
    "VideoPositionEnum",
    "VideoPositionTargeting",
    "VideoTranscodeStatusEnum",
    "ViewabilityPartnerEnum",
    "WebProperty",
    "WebviewClaimingStatusEnum",
)
