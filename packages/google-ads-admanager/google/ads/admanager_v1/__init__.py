# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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

if sys.version_info >= (3, 8):  # pragma: NO COVER
    from importlib import metadata
else:  # pragma: NO COVER
    # TODO(https://github.com/googleapis/python-api-core/issues/835): Remove
    # this code path once we drop support for Python 3.7
    import importlib_metadata as metadata


from .services.ad_break_service import AdBreakServiceClient
from .services.ad_review_center_ad_service import AdReviewCenterAdServiceClient
from .services.ad_unit_service import AdUnitServiceClient
from .services.application_service import ApplicationServiceClient
from .services.audience_segment_service import AudienceSegmentServiceClient
from .services.bandwidth_group_service import BandwidthGroupServiceClient
from .services.browser_language_service import BrowserLanguageServiceClient
from .services.browser_service import BrowserServiceClient
from .services.cms_metadata_key_service import CmsMetadataKeyServiceClient
from .services.cms_metadata_value_service import CmsMetadataValueServiceClient
from .services.company_service import CompanyServiceClient
from .services.contact_service import ContactServiceClient
from .services.content_bundle_service import ContentBundleServiceClient
from .services.content_label_service import ContentLabelServiceClient
from .services.content_service import ContentServiceClient
from .services.creative_template_service import CreativeTemplateServiceClient
from .services.custom_field_service import CustomFieldServiceClient
from .services.custom_targeting_key_service import CustomTargetingKeyServiceClient
from .services.custom_targeting_value_service import CustomTargetingValueServiceClient
from .services.device_capability_service import DeviceCapabilityServiceClient
from .services.device_category_service import DeviceCategoryServiceClient
from .services.device_manufacturer_service import DeviceManufacturerServiceClient
from .services.entity_signals_mapping_service import EntitySignalsMappingServiceClient
from .services.geo_target_service import GeoTargetServiceClient
from .services.line_item_service import LineItemServiceClient
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
from .services.role_service import RoleServiceClient
from .services.site_service import SiteServiceClient
from .services.taxonomy_category_service import TaxonomyCategoryServiceClient
from .services.team_service import TeamServiceClient
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
from .types.ad_review_center_ad_enums import AdReviewCenterAdStatusEnum
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
from .types.application_messages import Application
from .types.application_service import (
    GetApplicationRequest,
    ListApplicationsRequest,
    ListApplicationsResponse,
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
from .types.cms_metadata_key_enums import CmsMetadataKeyStatusEnum
from .types.cms_metadata_key_messages import CmsMetadataKey
from .types.cms_metadata_key_service import (
    GetCmsMetadataKeyRequest,
    ListCmsMetadataKeysRequest,
    ListCmsMetadataKeysResponse,
)
from .types.cms_metadata_value_enums import CmsMetadataValueStatusEnum
from .types.cms_metadata_value_messages import CmsMetadataValue
from .types.cms_metadata_value_service import (
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
from .types.content_bundle_messages import ContentBundle
from .types.content_bundle_service import (
    GetContentBundleRequest,
    ListContentBundlesRequest,
    ListContentBundlesResponse,
)
from .types.content_label_messages import ContentLabel
from .types.content_label_service import (
    GetContentLabelRequest,
    ListContentLabelsRequest,
    ListContentLabelsResponse,
)
from .types.content_messages import Content
from .types.content_service import (
    GetContentRequest,
    ListContentRequest,
    ListContentResponse,
)
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
    GetCustomTargetingValueRequest,
    ListCustomTargetingValuesRequest,
    ListCustomTargetingValuesResponse,
)
from .types.deal_buyer_permission_type_enum import DealBuyerPermissionTypeEnum
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
from .types.frequency_cap import FrequencyCap
from .types.geo_target_messages import GeoTarget
from .types.geo_target_service import (
    GetGeoTargetRequest,
    ListGeoTargetsRequest,
    ListGeoTargetsResponse,
)
from .types.goal import Goal
from .types.goal_enums import GoalTypeEnum, UnitTypeEnum
from .types.label_messages import Label
from .types.line_item_enums import LineItemTypeEnum
from .types.line_item_messages import LineItem
from .types.line_item_service import (
    GetLineItemRequest,
    ListLineItemsRequest,
    ListLineItemsResponse,
)
from .types.live_stream_event_messages import LiveStreamEvent
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
from .types.order_service import GetOrderRequest, ListOrdersRequest, ListOrdersResponse
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
from .types.report_definition import ReportDefinition
from .types.report_messages import Report, ReportDataTable, ScheduleOptions
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
    RequestPlatformTargeting,
    Targeting,
    TechnologyTargeting,
    UserDomainTargeting,
    VideoPosition,
    VideoPositionTargeting,
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
from .types.time_unit_enum import TimeUnitEnum
from .types.user_messages import User
from .types.user_service import GetUserRequest
from .types.video_position_enum import VideoPositionEnum
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
        import sys
        import warnings

        _py_version_str = sys.version.split()[0]
        _package_label = "google.ads.admanager_v1"
        if sys.version_info < (3, 9):
            warnings.warn(
                "You are using a non-supported Python version "
                + f"({_py_version_str}).  Google will not post any further "
                + f"updates to {_package_label} supporting this Python version. "
                + "Please upgrade to the latest Python version, or at "
                + f"least to Python 3.9, and then update {_package_label}.",
                FutureWarning,
            )
        if sys.version_info[:2] == (3, 9):
            warnings.warn(
                f"You are using a Python version ({_py_version_str}) "
                + f"which Google will stop supporting in {_package_label} in "
                + "January 2026. Please "
                + "upgrade to the latest Python version, or at "
                + "least to Python 3.10, before then, and "
                + f"then update {_package_label}.",
                FutureWarning,
            )

        def parse_version_to_tuple(version_string: str):
            """Safely converts a semantic version string to a comparable tuple of integers.
            Example: "4.25.8" -> (4, 25, 8)
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
        _next_supported_version = "4.25.8"
        _next_supported_version_tuple = (4, 25, 8)
        _recommendation = " (we recommend 6.x)"
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
    "AdBreak",
    "AdBreakServiceClient",
    "AdBreakStateEnum",
    "AdManagerError",
    "AdReviewCenterAd",
    "AdReviewCenterAdServiceClient",
    "AdReviewCenterAdStatusEnum",
    "AdUnit",
    "AdUnitParent",
    "AdUnitServiceClient",
    "AdUnitSize",
    "AdUnitStatusEnum",
    "AdUnitTargeting",
    "Application",
    "ApplicationServiceClient",
    "AppliedLabel",
    "AudienceSegment",
    "AudienceSegmentServiceClient",
    "AudienceSegmentTargeting",
    "BandwidthGroup",
    "BandwidthGroupServiceClient",
    "BandwidthTargeting",
    "BatchActivateAdUnitsRequest",
    "BatchActivateAdUnitsResponse",
    "BatchActivateCustomFieldsRequest",
    "BatchActivateCustomFieldsResponse",
    "BatchActivateCustomTargetingKeysRequest",
    "BatchActivateCustomTargetingKeysResponse",
    "BatchActivatePlacementsRequest",
    "BatchActivatePlacementsResponse",
    "BatchActivateTeamsRequest",
    "BatchActivateTeamsResponse",
    "BatchAdReviewCenterAdsOperationMetadata",
    "BatchAllowAdReviewCenterAdsRequest",
    "BatchAllowAdReviewCenterAdsResponse",
    "BatchArchiveAdUnitsRequest",
    "BatchArchiveAdUnitsResponse",
    "BatchArchivePlacementsRequest",
    "BatchArchivePlacementsResponse",
    "BatchBlockAdReviewCenterAdsRequest",
    "BatchBlockAdReviewCenterAdsResponse",
    "BatchCreateAdUnitsRequest",
    "BatchCreateAdUnitsResponse",
    "BatchCreateContactsRequest",
    "BatchCreateContactsResponse",
    "BatchCreateCustomFieldsRequest",
    "BatchCreateCustomFieldsResponse",
    "BatchCreateCustomTargetingKeysRequest",
    "BatchCreateCustomTargetingKeysResponse",
    "BatchCreateEntitySignalsMappingsRequest",
    "BatchCreateEntitySignalsMappingsResponse",
    "BatchCreatePlacementsRequest",
    "BatchCreatePlacementsResponse",
    "BatchCreateSitesRequest",
    "BatchCreateSitesResponse",
    "BatchCreateTeamsRequest",
    "BatchCreateTeamsResponse",
    "BatchDeactivateAdUnitsRequest",
    "BatchDeactivateAdUnitsResponse",
    "BatchDeactivateCustomFieldsRequest",
    "BatchDeactivateCustomFieldsResponse",
    "BatchDeactivateCustomTargetingKeysRequest",
    "BatchDeactivateCustomTargetingKeysResponse",
    "BatchDeactivatePlacementsRequest",
    "BatchDeactivatePlacementsResponse",
    "BatchDeactivateSitesRequest",
    "BatchDeactivateSitesResponse",
    "BatchDeactivateTeamsRequest",
    "BatchDeactivateTeamsResponse",
    "BatchSubmitSitesForApprovalRequest",
    "BatchSubmitSitesForApprovalResponse",
    "BatchUpdateAdUnitsRequest",
    "BatchUpdateAdUnitsResponse",
    "BatchUpdateContactsRequest",
    "BatchUpdateContactsResponse",
    "BatchUpdateCustomFieldsRequest",
    "BatchUpdateCustomFieldsResponse",
    "BatchUpdateCustomTargetingKeysRequest",
    "BatchUpdateCustomTargetingKeysResponse",
    "BatchUpdateEntitySignalsMappingsRequest",
    "BatchUpdateEntitySignalsMappingsResponse",
    "BatchUpdatePlacementsRequest",
    "BatchUpdatePlacementsResponse",
    "BatchUpdateSitesRequest",
    "BatchUpdateSitesResponse",
    "BatchUpdateTeamsRequest",
    "BatchUpdateTeamsResponse",
    "Browser",
    "BrowserLanguage",
    "BrowserLanguageServiceClient",
    "BrowserLanguageTargeting",
    "BrowserServiceClient",
    "BrowserTargeting",
    "CmsMetadataKey",
    "CmsMetadataKeyServiceClient",
    "CmsMetadataKeyStatusEnum",
    "CmsMetadataTargeting",
    "CmsMetadataValue",
    "CmsMetadataValueServiceClient",
    "CmsMetadataValueStatusEnum",
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
    "ContentLabel",
    "ContentLabelServiceClient",
    "ContentServiceClient",
    "ContentTargeting",
    "CreateAdBreakRequest",
    "CreateAdUnitRequest",
    "CreateContactRequest",
    "CreateCustomFieldRequest",
    "CreateCustomTargetingKeyRequest",
    "CreateEntitySignalsMappingRequest",
    "CreatePlacementRequest",
    "CreatePrivateAuctionDealRequest",
    "CreatePrivateAuctionRequest",
    "CreateReportRequest",
    "CreateSiteRequest",
    "CreateTeamRequest",
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
    "DataSegmentTargeting",
    "DealBuyerPermissionTypeEnum",
    "DeleteAdBreakRequest",
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
    "EntitySignalsMapping",
    "EntitySignalsMappingServiceClient",
    "EnvironmentTypeEnum",
    "ExchangeSyndicationProductEnum",
    "FetchReportResultRowsRequest",
    "FetchReportResultRowsResponse",
    "FirstPartyMobileApplicationTargeting",
    "FrequencyCap",
    "GeoTarget",
    "GeoTargetServiceClient",
    "GeoTargeting",
    "GetAdBreakRequest",
    "GetAdUnitRequest",
    "GetApplicationRequest",
    "GetAudienceSegmentRequest",
    "GetBandwidthGroupRequest",
    "GetBrowserLanguageRequest",
    "GetBrowserRequest",
    "GetCmsMetadataKeyRequest",
    "GetCmsMetadataValueRequest",
    "GetCompanyRequest",
    "GetContactRequest",
    "GetContentBundleRequest",
    "GetContentLabelRequest",
    "GetContentRequest",
    "GetCreativeTemplateRequest",
    "GetCustomFieldRequest",
    "GetCustomTargetingKeyRequest",
    "GetCustomTargetingValueRequest",
    "GetDeviceCapabilityRequest",
    "GetDeviceCategoryRequest",
    "GetDeviceManufacturerRequest",
    "GetEntitySignalsMappingRequest",
    "GetGeoTargetRequest",
    "GetLineItemRequest",
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
    "GetRoleRequest",
    "GetSiteRequest",
    "GetTaxonomyCategoryRequest",
    "GetTeamRequest",
    "GetUserRequest",
    "Goal",
    "GoalTypeEnum",
    "InventoryTargeting",
    "Label",
    "LabelFrequencyCap",
    "LineItem",
    "LineItemServiceClient",
    "LineItemTypeEnum",
    "ListAdBreaksRequest",
    "ListAdBreaksResponse",
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
    "ListLineItemsRequest",
    "ListLineItemsResponse",
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
    "ListRolesRequest",
    "ListRolesResponse",
    "ListSitesRequest",
    "ListSitesResponse",
    "ListTaxonomyCategoriesRequest",
    "ListTaxonomyCategoriesResponse",
    "ListTeamsRequest",
    "ListTeamsResponse",
    "LiveStreamEvent",
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
    "OperatingSystem",
    "OperatingSystemServiceClient",
    "OperatingSystemTargeting",
    "OperatingSystemVersion",
    "OperatingSystemVersionServiceClient",
    "Order",
    "OrderServiceClient",
    "OrderStatusEnum",
    "Placement",
    "PlacementServiceClient",
    "PlacementStatusEnum",
    "PrivateAuction",
    "PrivateAuctionDeal",
    "PrivateAuctionDealServiceClient",
    "PrivateAuctionServiceClient",
    "PrivateMarketplaceDealStatusEnum",
    "ProgrammaticBuyer",
    "ProgrammaticBuyerServiceClient",
    "Report",
    "ReportDataTable",
    "ReportDefinition",
    "ReportServiceClient",
    "ReportValue",
    "RequestPlatformEnum",
    "RequestPlatformTargeting",
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
    "SmartSizeModeEnum",
    "TargetWindowEnum",
    "TargetedVideoBumperTypeEnum",
    "Targeting",
    "TaxonomyCategory",
    "TaxonomyCategoryServiceClient",
    "TaxonomyTypeEnum",
    "Team",
    "TeamAccessTypeEnum",
    "TeamServiceClient",
    "TeamStatusEnum",
    "TechnologyTargeting",
    "TimeUnitEnum",
    "UnitTypeEnum",
    "UpdateAdBreakRequest",
    "UpdateAdUnitRequest",
    "UpdateContactRequest",
    "UpdateCustomFieldRequest",
    "UpdateCustomTargetingKeyRequest",
    "UpdateEntitySignalsMappingRequest",
    "UpdatePlacementRequest",
    "UpdatePrivateAuctionDealRequest",
    "UpdatePrivateAuctionRequest",
    "UpdateReportRequest",
    "UpdateSiteRequest",
    "UpdateTeamRequest",
    "User",
    "UserDomainTargeting",
    "UserServiceClient",
    "VideoPosition",
    "VideoPositionEnum",
    "VideoPositionTargeting",
    "WebProperty",
)
