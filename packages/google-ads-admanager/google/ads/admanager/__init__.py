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
from google.ads.admanager import gapic_version as package_version

__version__ = package_version.__version__


from google.ads.admanager_v1.services.ad_break_service.client import (
    AdBreakServiceClient,
)
from google.ads.admanager_v1.services.ad_review_center_ad_service.client import (
    AdReviewCenterAdServiceClient,
)
from google.ads.admanager_v1.services.ad_unit_service.client import AdUnitServiceClient
from google.ads.admanager_v1.services.application_service.client import (
    ApplicationServiceClient,
)
from google.ads.admanager_v1.services.audience_segment_service.client import (
    AudienceSegmentServiceClient,
)
from google.ads.admanager_v1.services.bandwidth_group_service.client import (
    BandwidthGroupServiceClient,
)
from google.ads.admanager_v1.services.browser_language_service.client import (
    BrowserLanguageServiceClient,
)
from google.ads.admanager_v1.services.browser_service.client import BrowserServiceClient
from google.ads.admanager_v1.services.cms_metadata_key_service.client import (
    CmsMetadataKeyServiceClient,
)
from google.ads.admanager_v1.services.cms_metadata_value_service.client import (
    CmsMetadataValueServiceClient,
)
from google.ads.admanager_v1.services.company_service.client import CompanyServiceClient
from google.ads.admanager_v1.services.contact_service.client import ContactServiceClient
from google.ads.admanager_v1.services.content_bundle_service.client import (
    ContentBundleServiceClient,
)
from google.ads.admanager_v1.services.content_label_service.client import (
    ContentLabelServiceClient,
)
from google.ads.admanager_v1.services.content_service.client import ContentServiceClient
from google.ads.admanager_v1.services.creative_template_service.client import (
    CreativeTemplateServiceClient,
)
from google.ads.admanager_v1.services.custom_field_service.client import (
    CustomFieldServiceClient,
)
from google.ads.admanager_v1.services.custom_targeting_key_service.client import (
    CustomTargetingKeyServiceClient,
)
from google.ads.admanager_v1.services.custom_targeting_value_service.client import (
    CustomTargetingValueServiceClient,
)
from google.ads.admanager_v1.services.device_capability_service.client import (
    DeviceCapabilityServiceClient,
)
from google.ads.admanager_v1.services.device_category_service.client import (
    DeviceCategoryServiceClient,
)
from google.ads.admanager_v1.services.device_manufacturer_service.client import (
    DeviceManufacturerServiceClient,
)
from google.ads.admanager_v1.services.entity_signals_mapping_service.client import (
    EntitySignalsMappingServiceClient,
)
from google.ads.admanager_v1.services.geo_target_service.client import (
    GeoTargetServiceClient,
)
from google.ads.admanager_v1.services.line_item_service.client import (
    LineItemServiceClient,
)
from google.ads.admanager_v1.services.mobile_carrier_service.client import (
    MobileCarrierServiceClient,
)
from google.ads.admanager_v1.services.mobile_device_service.client import (
    MobileDeviceServiceClient,
)
from google.ads.admanager_v1.services.mobile_device_submodel_service.client import (
    MobileDeviceSubmodelServiceClient,
)
from google.ads.admanager_v1.services.network_service.client import NetworkServiceClient
from google.ads.admanager_v1.services.operating_system_service.client import (
    OperatingSystemServiceClient,
)
from google.ads.admanager_v1.services.operating_system_version_service.client import (
    OperatingSystemVersionServiceClient,
)
from google.ads.admanager_v1.services.order_service.client import OrderServiceClient
from google.ads.admanager_v1.services.placement_service.client import (
    PlacementServiceClient,
)
from google.ads.admanager_v1.services.private_auction_deal_service.client import (
    PrivateAuctionDealServiceClient,
)
from google.ads.admanager_v1.services.private_auction_service.client import (
    PrivateAuctionServiceClient,
)
from google.ads.admanager_v1.services.programmatic_buyer_service.client import (
    ProgrammaticBuyerServiceClient,
)
from google.ads.admanager_v1.services.report_service.client import ReportServiceClient
from google.ads.admanager_v1.services.role_service.client import RoleServiceClient
from google.ads.admanager_v1.services.site_service.client import SiteServiceClient
from google.ads.admanager_v1.services.taxonomy_category_service.client import (
    TaxonomyCategoryServiceClient,
)
from google.ads.admanager_v1.services.team_service.client import TeamServiceClient
from google.ads.admanager_v1.services.user_service.client import UserServiceClient
from google.ads.admanager_v1.types.ad_break_messages import AdBreak
from google.ads.admanager_v1.types.ad_break_service import (
    CreateAdBreakRequest,
    DeleteAdBreakRequest,
    GetAdBreakRequest,
    ListAdBreaksRequest,
    ListAdBreaksResponse,
    UpdateAdBreakRequest,
)
from google.ads.admanager_v1.types.ad_review_center_ad_enums import (
    AdReviewCenterAdStatusEnum,
)
from google.ads.admanager_v1.types.ad_review_center_ad_messages import AdReviewCenterAd
from google.ads.admanager_v1.types.ad_review_center_ad_service import (
    BatchAdReviewCenterAdsOperationMetadata,
    BatchAllowAdReviewCenterAdsRequest,
    BatchAllowAdReviewCenterAdsResponse,
    BatchBlockAdReviewCenterAdsRequest,
    BatchBlockAdReviewCenterAdsResponse,
    SearchAdReviewCenterAdsRequest,
    SearchAdReviewCenterAdsResponse,
)
from google.ads.admanager_v1.types.ad_unit_enums import (
    AdUnitStatusEnum,
    SmartSizeModeEnum,
    TargetWindowEnum,
)
from google.ads.admanager_v1.types.ad_unit_messages import (
    AdUnit,
    AdUnitParent,
    AdUnitSize,
    LabelFrequencyCap,
)
from google.ads.admanager_v1.types.ad_unit_service import (
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
from google.ads.admanager_v1.types.admanager_error import AdManagerError
from google.ads.admanager_v1.types.application_messages import Application
from google.ads.admanager_v1.types.application_service import (
    GetApplicationRequest,
    ListApplicationsRequest,
    ListApplicationsResponse,
)
from google.ads.admanager_v1.types.applied_label import AppliedLabel
from google.ads.admanager_v1.types.audience_segment_messages import AudienceSegment
from google.ads.admanager_v1.types.audience_segment_service import (
    GetAudienceSegmentRequest,
    ListAudienceSegmentsRequest,
    ListAudienceSegmentsResponse,
)
from google.ads.admanager_v1.types.bandwidth_group_messages import BandwidthGroup
from google.ads.admanager_v1.types.bandwidth_group_service import (
    GetBandwidthGroupRequest,
    ListBandwidthGroupsRequest,
    ListBandwidthGroupsResponse,
)
from google.ads.admanager_v1.types.browser_language_messages import BrowserLanguage
from google.ads.admanager_v1.types.browser_language_service import (
    GetBrowserLanguageRequest,
    ListBrowserLanguagesRequest,
    ListBrowserLanguagesResponse,
)
from google.ads.admanager_v1.types.browser_messages import Browser
from google.ads.admanager_v1.types.browser_service import (
    GetBrowserRequest,
    ListBrowsersRequest,
    ListBrowsersResponse,
)
from google.ads.admanager_v1.types.cms_metadata_key_enums import (
    CmsMetadataKeyStatusEnum,
)
from google.ads.admanager_v1.types.cms_metadata_key_messages import CmsMetadataKey
from google.ads.admanager_v1.types.cms_metadata_key_service import (
    GetCmsMetadataKeyRequest,
    ListCmsMetadataKeysRequest,
    ListCmsMetadataKeysResponse,
)
from google.ads.admanager_v1.types.cms_metadata_value_enums import (
    CmsMetadataValueStatusEnum,
)
from google.ads.admanager_v1.types.cms_metadata_value_messages import CmsMetadataValue
from google.ads.admanager_v1.types.cms_metadata_value_service import (
    GetCmsMetadataValueRequest,
    ListCmsMetadataValuesRequest,
    ListCmsMetadataValuesResponse,
)
from google.ads.admanager_v1.types.company_enums import (
    CompanyCreditStatusEnum,
    CompanyTypeEnum,
)
from google.ads.admanager_v1.types.company_messages import Company
from google.ads.admanager_v1.types.company_service import (
    GetCompanyRequest,
    ListCompaniesRequest,
    ListCompaniesResponse,
)
from google.ads.admanager_v1.types.contact_enums import ContactStatusEnum
from google.ads.admanager_v1.types.contact_messages import Contact
from google.ads.admanager_v1.types.contact_service import (
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
from google.ads.admanager_v1.types.content_bundle_messages import ContentBundle
from google.ads.admanager_v1.types.content_bundle_service import (
    GetContentBundleRequest,
    ListContentBundlesRequest,
    ListContentBundlesResponse,
)
from google.ads.admanager_v1.types.content_label_messages import ContentLabel
from google.ads.admanager_v1.types.content_label_service import (
    GetContentLabelRequest,
    ListContentLabelsRequest,
    ListContentLabelsResponse,
)
from google.ads.admanager_v1.types.content_messages import Content
from google.ads.admanager_v1.types.content_service import (
    GetContentRequest,
    ListContentRequest,
    ListContentResponse,
)
from google.ads.admanager_v1.types.creative_template_enums import (
    CreativeTemplateStatusEnum,
    CreativeTemplateTypeEnum,
)
from google.ads.admanager_v1.types.creative_template_messages import (
    CreativeTemplate,
    CreativeTemplateVariable,
)
from google.ads.admanager_v1.types.creative_template_service import (
    GetCreativeTemplateRequest,
    ListCreativeTemplatesRequest,
    ListCreativeTemplatesResponse,
)
from google.ads.admanager_v1.types.creative_template_variable_url_type_enum import (
    CreativeTemplateVariableUrlTypeEnum,
)
from google.ads.admanager_v1.types.custom_field_enums import (
    CustomFieldDataTypeEnum,
    CustomFieldEntityTypeEnum,
    CustomFieldStatusEnum,
    CustomFieldVisibilityEnum,
)
from google.ads.admanager_v1.types.custom_field_messages import (
    CustomField,
    CustomFieldOption,
)
from google.ads.admanager_v1.types.custom_field_service import (
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
from google.ads.admanager_v1.types.custom_field_value import CustomFieldValue
from google.ads.admanager_v1.types.custom_targeting_key_enums import (
    CustomTargetingKeyReportableTypeEnum,
    CustomTargetingKeyStatusEnum,
    CustomTargetingKeyTypeEnum,
)
from google.ads.admanager_v1.types.custom_targeting_key_messages import (
    CustomTargetingKey,
)
from google.ads.admanager_v1.types.custom_targeting_key_service import (
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
from google.ads.admanager_v1.types.custom_targeting_value_enums import (
    CustomTargetingValueMatchTypeEnum,
    CustomTargetingValueStatusEnum,
)
from google.ads.admanager_v1.types.custom_targeting_value_messages import (
    CustomTargetingValue,
)
from google.ads.admanager_v1.types.custom_targeting_value_service import (
    GetCustomTargetingValueRequest,
    ListCustomTargetingValuesRequest,
    ListCustomTargetingValuesResponse,
)
from google.ads.admanager_v1.types.deal_buyer_permission_type_enum import (
    DealBuyerPermissionTypeEnum,
)
from google.ads.admanager_v1.types.device_capability_messages import DeviceCapability
from google.ads.admanager_v1.types.device_capability_service import (
    GetDeviceCapabilityRequest,
    ListDeviceCapabilitiesRequest,
    ListDeviceCapabilitiesResponse,
)
from google.ads.admanager_v1.types.device_category_messages import DeviceCategory
from google.ads.admanager_v1.types.device_category_service import (
    GetDeviceCategoryRequest,
    ListDeviceCategoriesRequest,
    ListDeviceCategoriesResponse,
)
from google.ads.admanager_v1.types.device_manufacturer_messages import (
    DeviceManufacturer,
)
from google.ads.admanager_v1.types.device_manufacturer_service import (
    GetDeviceManufacturerRequest,
    ListDeviceManufacturersRequest,
    ListDeviceManufacturersResponse,
)
from google.ads.admanager_v1.types.early_ad_break_notification_enums import (
    AdBreakStateEnum,
)
from google.ads.admanager_v1.types.entity_signals_mapping_messages import (
    EntitySignalsMapping,
)
from google.ads.admanager_v1.types.entity_signals_mapping_service import (
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
from google.ads.admanager_v1.types.environment_type_enum import EnvironmentTypeEnum
from google.ads.admanager_v1.types.exchange_syndication_product_enum import (
    ExchangeSyndicationProductEnum,
)
from google.ads.admanager_v1.types.frequency_cap import FrequencyCap
from google.ads.admanager_v1.types.geo_target_messages import GeoTarget
from google.ads.admanager_v1.types.geo_target_service import (
    GetGeoTargetRequest,
    ListGeoTargetsRequest,
    ListGeoTargetsResponse,
)
from google.ads.admanager_v1.types.goal import Goal
from google.ads.admanager_v1.types.goal_enums import GoalTypeEnum, UnitTypeEnum
from google.ads.admanager_v1.types.label_messages import Label
from google.ads.admanager_v1.types.line_item_enums import LineItemTypeEnum
from google.ads.admanager_v1.types.line_item_messages import LineItem
from google.ads.admanager_v1.types.line_item_service import (
    GetLineItemRequest,
    ListLineItemsRequest,
    ListLineItemsResponse,
)
from google.ads.admanager_v1.types.live_stream_event_messages import LiveStreamEvent
from google.ads.admanager_v1.types.mobile_carrier_messages import MobileCarrier
from google.ads.admanager_v1.types.mobile_carrier_service import (
    GetMobileCarrierRequest,
    ListMobileCarriersRequest,
    ListMobileCarriersResponse,
)
from google.ads.admanager_v1.types.mobile_device_messages import MobileDevice
from google.ads.admanager_v1.types.mobile_device_service import (
    GetMobileDeviceRequest,
    ListMobileDevicesRequest,
    ListMobileDevicesResponse,
)
from google.ads.admanager_v1.types.mobile_device_submodel_messages import (
    MobileDeviceSubmodel,
)
from google.ads.admanager_v1.types.mobile_device_submodel_service import (
    GetMobileDeviceSubmodelRequest,
    ListMobileDeviceSubmodelsRequest,
    ListMobileDeviceSubmodelsResponse,
)
from google.ads.admanager_v1.types.network_messages import Network
from google.ads.admanager_v1.types.network_service import (
    GetNetworkRequest,
    ListNetworksRequest,
    ListNetworksResponse,
)
from google.ads.admanager_v1.types.operating_system_messages import OperatingSystem
from google.ads.admanager_v1.types.operating_system_service import (
    GetOperatingSystemRequest,
    ListOperatingSystemsRequest,
    ListOperatingSystemsResponse,
)
from google.ads.admanager_v1.types.operating_system_version_messages import (
    OperatingSystemVersion,
)
from google.ads.admanager_v1.types.operating_system_version_service import (
    GetOperatingSystemVersionRequest,
    ListOperatingSystemVersionsRequest,
    ListOperatingSystemVersionsResponse,
)
from google.ads.admanager_v1.types.order_enums import OrderStatusEnum
from google.ads.admanager_v1.types.order_messages import Order
from google.ads.admanager_v1.types.order_service import (
    GetOrderRequest,
    ListOrdersRequest,
    ListOrdersResponse,
)
from google.ads.admanager_v1.types.placement_enums import PlacementStatusEnum
from google.ads.admanager_v1.types.placement_messages import Placement
from google.ads.admanager_v1.types.placement_service import (
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
from google.ads.admanager_v1.types.private_auction_deal_messages import (
    PrivateAuctionDeal,
)
from google.ads.admanager_v1.types.private_auction_deal_service import (
    CreatePrivateAuctionDealRequest,
    GetPrivateAuctionDealRequest,
    ListPrivateAuctionDealsRequest,
    ListPrivateAuctionDealsResponse,
    UpdatePrivateAuctionDealRequest,
)
from google.ads.admanager_v1.types.private_auction_messages import PrivateAuction
from google.ads.admanager_v1.types.private_auction_service import (
    CreatePrivateAuctionRequest,
    GetPrivateAuctionRequest,
    ListPrivateAuctionsRequest,
    ListPrivateAuctionsResponse,
    UpdatePrivateAuctionRequest,
)
from google.ads.admanager_v1.types.private_marketplace_enums import (
    PrivateMarketplaceDealStatusEnum,
)
from google.ads.admanager_v1.types.programmatic_buyer_messages import ProgrammaticBuyer
from google.ads.admanager_v1.types.programmatic_buyer_service import (
    GetProgrammaticBuyerRequest,
    ListProgrammaticBuyersRequest,
    ListProgrammaticBuyersResponse,
)
from google.ads.admanager_v1.types.report_definition import ReportDefinition
from google.ads.admanager_v1.types.report_messages import (
    Report,
    ReportDataTable,
    ScheduleOptions,
)
from google.ads.admanager_v1.types.report_service import (
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
from google.ads.admanager_v1.types.report_value import ReportValue
from google.ads.admanager_v1.types.request_platform_enum import RequestPlatformEnum
from google.ads.admanager_v1.types.role_enums import RoleStatusEnum
from google.ads.admanager_v1.types.role_messages import Role
from google.ads.admanager_v1.types.role_service import (
    GetRoleRequest,
    ListRolesRequest,
    ListRolesResponse,
)
from google.ads.admanager_v1.types.site_enums import (
    SiteApprovalStatusEnum,
    SiteDisapprovalReasonEnum,
)
from google.ads.admanager_v1.types.site_messages import DisapprovalReason, Site
from google.ads.admanager_v1.types.site_service import (
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
from google.ads.admanager_v1.types.size import Size
from google.ads.admanager_v1.types.size_type_enum import SizeTypeEnum
from google.ads.admanager_v1.types.targeted_video_bumper_type_enum import (
    TargetedVideoBumperTypeEnum,
)
from google.ads.admanager_v1.types.targeting import (
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
from google.ads.admanager_v1.types.taxonomy_category_messages import TaxonomyCategory
from google.ads.admanager_v1.types.taxonomy_category_service import (
    GetTaxonomyCategoryRequest,
    ListTaxonomyCategoriesRequest,
    ListTaxonomyCategoriesResponse,
)
from google.ads.admanager_v1.types.taxonomy_type_enum import TaxonomyTypeEnum
from google.ads.admanager_v1.types.team_enums import TeamAccessTypeEnum, TeamStatusEnum
from google.ads.admanager_v1.types.team_messages import Team
from google.ads.admanager_v1.types.team_service import (
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
from google.ads.admanager_v1.types.time_unit_enum import TimeUnitEnum
from google.ads.admanager_v1.types.user_messages import User
from google.ads.admanager_v1.types.user_service import GetUserRequest
from google.ads.admanager_v1.types.video_position_enum import VideoPositionEnum
from google.ads.admanager_v1.types.web_property import WebProperty

__all__ = (
    "AdBreakServiceClient",
    "AdReviewCenterAdServiceClient",
    "AdUnitServiceClient",
    "ApplicationServiceClient",
    "AudienceSegmentServiceClient",
    "BandwidthGroupServiceClient",
    "BrowserLanguageServiceClient",
    "BrowserServiceClient",
    "CmsMetadataKeyServiceClient",
    "CmsMetadataValueServiceClient",
    "CompanyServiceClient",
    "ContactServiceClient",
    "ContentBundleServiceClient",
    "ContentLabelServiceClient",
    "ContentServiceClient",
    "CreativeTemplateServiceClient",
    "CustomFieldServiceClient",
    "CustomTargetingKeyServiceClient",
    "CustomTargetingValueServiceClient",
    "DeviceCapabilityServiceClient",
    "DeviceCategoryServiceClient",
    "DeviceManufacturerServiceClient",
    "EntitySignalsMappingServiceClient",
    "GeoTargetServiceClient",
    "LineItemServiceClient",
    "MobileCarrierServiceClient",
    "MobileDeviceServiceClient",
    "MobileDeviceSubmodelServiceClient",
    "NetworkServiceClient",
    "OperatingSystemServiceClient",
    "OperatingSystemVersionServiceClient",
    "OrderServiceClient",
    "PlacementServiceClient",
    "PrivateAuctionDealServiceClient",
    "PrivateAuctionServiceClient",
    "ProgrammaticBuyerServiceClient",
    "ReportServiceClient",
    "RoleServiceClient",
    "SiteServiceClient",
    "TaxonomyCategoryServiceClient",
    "TeamServiceClient",
    "UserServiceClient",
    "AdBreak",
    "CreateAdBreakRequest",
    "DeleteAdBreakRequest",
    "GetAdBreakRequest",
    "ListAdBreaksRequest",
    "ListAdBreaksResponse",
    "UpdateAdBreakRequest",
    "AdReviewCenterAdStatusEnum",
    "AdReviewCenterAd",
    "BatchAdReviewCenterAdsOperationMetadata",
    "BatchAllowAdReviewCenterAdsRequest",
    "BatchAllowAdReviewCenterAdsResponse",
    "BatchBlockAdReviewCenterAdsRequest",
    "BatchBlockAdReviewCenterAdsResponse",
    "SearchAdReviewCenterAdsRequest",
    "SearchAdReviewCenterAdsResponse",
    "AdUnitStatusEnum",
    "SmartSizeModeEnum",
    "TargetWindowEnum",
    "AdUnit",
    "AdUnitParent",
    "AdUnitSize",
    "LabelFrequencyCap",
    "BatchActivateAdUnitsRequest",
    "BatchActivateAdUnitsResponse",
    "BatchArchiveAdUnitsRequest",
    "BatchArchiveAdUnitsResponse",
    "BatchCreateAdUnitsRequest",
    "BatchCreateAdUnitsResponse",
    "BatchDeactivateAdUnitsRequest",
    "BatchDeactivateAdUnitsResponse",
    "BatchUpdateAdUnitsRequest",
    "BatchUpdateAdUnitsResponse",
    "CreateAdUnitRequest",
    "GetAdUnitRequest",
    "ListAdUnitSizesRequest",
    "ListAdUnitSizesResponse",
    "ListAdUnitsRequest",
    "ListAdUnitsResponse",
    "UpdateAdUnitRequest",
    "AdManagerError",
    "Application",
    "GetApplicationRequest",
    "ListApplicationsRequest",
    "ListApplicationsResponse",
    "AppliedLabel",
    "AudienceSegment",
    "GetAudienceSegmentRequest",
    "ListAudienceSegmentsRequest",
    "ListAudienceSegmentsResponse",
    "BandwidthGroup",
    "GetBandwidthGroupRequest",
    "ListBandwidthGroupsRequest",
    "ListBandwidthGroupsResponse",
    "BrowserLanguage",
    "GetBrowserLanguageRequest",
    "ListBrowserLanguagesRequest",
    "ListBrowserLanguagesResponse",
    "Browser",
    "GetBrowserRequest",
    "ListBrowsersRequest",
    "ListBrowsersResponse",
    "CmsMetadataKeyStatusEnum",
    "CmsMetadataKey",
    "GetCmsMetadataKeyRequest",
    "ListCmsMetadataKeysRequest",
    "ListCmsMetadataKeysResponse",
    "CmsMetadataValueStatusEnum",
    "CmsMetadataValue",
    "GetCmsMetadataValueRequest",
    "ListCmsMetadataValuesRequest",
    "ListCmsMetadataValuesResponse",
    "CompanyCreditStatusEnum",
    "CompanyTypeEnum",
    "Company",
    "GetCompanyRequest",
    "ListCompaniesRequest",
    "ListCompaniesResponse",
    "ContactStatusEnum",
    "Contact",
    "BatchCreateContactsRequest",
    "BatchCreateContactsResponse",
    "BatchUpdateContactsRequest",
    "BatchUpdateContactsResponse",
    "CreateContactRequest",
    "GetContactRequest",
    "ListContactsRequest",
    "ListContactsResponse",
    "UpdateContactRequest",
    "ContentBundle",
    "GetContentBundleRequest",
    "ListContentBundlesRequest",
    "ListContentBundlesResponse",
    "ContentLabel",
    "GetContentLabelRequest",
    "ListContentLabelsRequest",
    "ListContentLabelsResponse",
    "Content",
    "GetContentRequest",
    "ListContentRequest",
    "ListContentResponse",
    "CreativeTemplateStatusEnum",
    "CreativeTemplateTypeEnum",
    "CreativeTemplate",
    "CreativeTemplateVariable",
    "GetCreativeTemplateRequest",
    "ListCreativeTemplatesRequest",
    "ListCreativeTemplatesResponse",
    "CreativeTemplateVariableUrlTypeEnum",
    "CustomFieldDataTypeEnum",
    "CustomFieldEntityTypeEnum",
    "CustomFieldStatusEnum",
    "CustomFieldVisibilityEnum",
    "CustomField",
    "CustomFieldOption",
    "BatchActivateCustomFieldsRequest",
    "BatchActivateCustomFieldsResponse",
    "BatchCreateCustomFieldsRequest",
    "BatchCreateCustomFieldsResponse",
    "BatchDeactivateCustomFieldsRequest",
    "BatchDeactivateCustomFieldsResponse",
    "BatchUpdateCustomFieldsRequest",
    "BatchUpdateCustomFieldsResponse",
    "CreateCustomFieldRequest",
    "GetCustomFieldRequest",
    "ListCustomFieldsRequest",
    "ListCustomFieldsResponse",
    "UpdateCustomFieldRequest",
    "CustomFieldValue",
    "CustomTargetingKeyReportableTypeEnum",
    "CustomTargetingKeyStatusEnum",
    "CustomTargetingKeyTypeEnum",
    "CustomTargetingKey",
    "BatchActivateCustomTargetingKeysRequest",
    "BatchActivateCustomTargetingKeysResponse",
    "BatchCreateCustomTargetingKeysRequest",
    "BatchCreateCustomTargetingKeysResponse",
    "BatchDeactivateCustomTargetingKeysRequest",
    "BatchDeactivateCustomTargetingKeysResponse",
    "BatchUpdateCustomTargetingKeysRequest",
    "BatchUpdateCustomTargetingKeysResponse",
    "CreateCustomTargetingKeyRequest",
    "GetCustomTargetingKeyRequest",
    "ListCustomTargetingKeysRequest",
    "ListCustomTargetingKeysResponse",
    "UpdateCustomTargetingKeyRequest",
    "CustomTargetingValueMatchTypeEnum",
    "CustomTargetingValueStatusEnum",
    "CustomTargetingValue",
    "GetCustomTargetingValueRequest",
    "ListCustomTargetingValuesRequest",
    "ListCustomTargetingValuesResponse",
    "DealBuyerPermissionTypeEnum",
    "DeviceCapability",
    "GetDeviceCapabilityRequest",
    "ListDeviceCapabilitiesRequest",
    "ListDeviceCapabilitiesResponse",
    "DeviceCategory",
    "GetDeviceCategoryRequest",
    "ListDeviceCategoriesRequest",
    "ListDeviceCategoriesResponse",
    "DeviceManufacturer",
    "GetDeviceManufacturerRequest",
    "ListDeviceManufacturersRequest",
    "ListDeviceManufacturersResponse",
    "AdBreakStateEnum",
    "EntitySignalsMapping",
    "BatchCreateEntitySignalsMappingsRequest",
    "BatchCreateEntitySignalsMappingsResponse",
    "BatchUpdateEntitySignalsMappingsRequest",
    "BatchUpdateEntitySignalsMappingsResponse",
    "CreateEntitySignalsMappingRequest",
    "GetEntitySignalsMappingRequest",
    "ListEntitySignalsMappingsRequest",
    "ListEntitySignalsMappingsResponse",
    "UpdateEntitySignalsMappingRequest",
    "EnvironmentTypeEnum",
    "ExchangeSyndicationProductEnum",
    "FrequencyCap",
    "GeoTarget",
    "GetGeoTargetRequest",
    "ListGeoTargetsRequest",
    "ListGeoTargetsResponse",
    "Goal",
    "GoalTypeEnum",
    "UnitTypeEnum",
    "Label",
    "LineItemTypeEnum",
    "LineItem",
    "GetLineItemRequest",
    "ListLineItemsRequest",
    "ListLineItemsResponse",
    "LiveStreamEvent",
    "MobileCarrier",
    "GetMobileCarrierRequest",
    "ListMobileCarriersRequest",
    "ListMobileCarriersResponse",
    "MobileDevice",
    "GetMobileDeviceRequest",
    "ListMobileDevicesRequest",
    "ListMobileDevicesResponse",
    "MobileDeviceSubmodel",
    "GetMobileDeviceSubmodelRequest",
    "ListMobileDeviceSubmodelsRequest",
    "ListMobileDeviceSubmodelsResponse",
    "Network",
    "GetNetworkRequest",
    "ListNetworksRequest",
    "ListNetworksResponse",
    "OperatingSystem",
    "GetOperatingSystemRequest",
    "ListOperatingSystemsRequest",
    "ListOperatingSystemsResponse",
    "OperatingSystemVersion",
    "GetOperatingSystemVersionRequest",
    "ListOperatingSystemVersionsRequest",
    "ListOperatingSystemVersionsResponse",
    "OrderStatusEnum",
    "Order",
    "GetOrderRequest",
    "ListOrdersRequest",
    "ListOrdersResponse",
    "PlacementStatusEnum",
    "Placement",
    "BatchActivatePlacementsRequest",
    "BatchActivatePlacementsResponse",
    "BatchArchivePlacementsRequest",
    "BatchArchivePlacementsResponse",
    "BatchCreatePlacementsRequest",
    "BatchCreatePlacementsResponse",
    "BatchDeactivatePlacementsRequest",
    "BatchDeactivatePlacementsResponse",
    "BatchUpdatePlacementsRequest",
    "BatchUpdatePlacementsResponse",
    "CreatePlacementRequest",
    "GetPlacementRequest",
    "ListPlacementsRequest",
    "ListPlacementsResponse",
    "UpdatePlacementRequest",
    "PrivateAuctionDeal",
    "CreatePrivateAuctionDealRequest",
    "GetPrivateAuctionDealRequest",
    "ListPrivateAuctionDealsRequest",
    "ListPrivateAuctionDealsResponse",
    "UpdatePrivateAuctionDealRequest",
    "PrivateAuction",
    "CreatePrivateAuctionRequest",
    "GetPrivateAuctionRequest",
    "ListPrivateAuctionsRequest",
    "ListPrivateAuctionsResponse",
    "UpdatePrivateAuctionRequest",
    "PrivateMarketplaceDealStatusEnum",
    "ProgrammaticBuyer",
    "GetProgrammaticBuyerRequest",
    "ListProgrammaticBuyersRequest",
    "ListProgrammaticBuyersResponse",
    "ReportDefinition",
    "Report",
    "ReportDataTable",
    "ScheduleOptions",
    "CreateReportRequest",
    "FetchReportResultRowsRequest",
    "FetchReportResultRowsResponse",
    "GetReportRequest",
    "ListReportsRequest",
    "ListReportsResponse",
    "RunReportMetadata",
    "RunReportRequest",
    "RunReportResponse",
    "UpdateReportRequest",
    "ReportValue",
    "RequestPlatformEnum",
    "RoleStatusEnum",
    "Role",
    "GetRoleRequest",
    "ListRolesRequest",
    "ListRolesResponse",
    "SiteApprovalStatusEnum",
    "SiteDisapprovalReasonEnum",
    "DisapprovalReason",
    "Site",
    "BatchCreateSitesRequest",
    "BatchCreateSitesResponse",
    "BatchDeactivateSitesRequest",
    "BatchDeactivateSitesResponse",
    "BatchSubmitSitesForApprovalRequest",
    "BatchSubmitSitesForApprovalResponse",
    "BatchUpdateSitesRequest",
    "BatchUpdateSitesResponse",
    "CreateSiteRequest",
    "GetSiteRequest",
    "ListSitesRequest",
    "ListSitesResponse",
    "UpdateSiteRequest",
    "Size",
    "SizeTypeEnum",
    "TargetedVideoBumperTypeEnum",
    "AdUnitTargeting",
    "AudienceSegmentTargeting",
    "BandwidthTargeting",
    "BrowserLanguageTargeting",
    "BrowserTargeting",
    "CmsMetadataTargeting",
    "ContentTargeting",
    "CustomTargeting",
    "CustomTargetingClause",
    "CustomTargetingLiteral",
    "DataSegmentTargeting",
    "DeviceCapabilityTargeting",
    "DeviceCategoryTargeting",
    "DeviceManufacturerTargeting",
    "FirstPartyMobileApplicationTargeting",
    "GeoTargeting",
    "InventoryTargeting",
    "MobileApplicationTargeting",
    "MobileCarrierTargeting",
    "OperatingSystemTargeting",
    "RequestPlatformTargeting",
    "Targeting",
    "TechnologyTargeting",
    "UserDomainTargeting",
    "VideoPosition",
    "VideoPositionTargeting",
    "TaxonomyCategory",
    "GetTaxonomyCategoryRequest",
    "ListTaxonomyCategoriesRequest",
    "ListTaxonomyCategoriesResponse",
    "TaxonomyTypeEnum",
    "TeamAccessTypeEnum",
    "TeamStatusEnum",
    "Team",
    "BatchActivateTeamsRequest",
    "BatchActivateTeamsResponse",
    "BatchCreateTeamsRequest",
    "BatchCreateTeamsResponse",
    "BatchDeactivateTeamsRequest",
    "BatchDeactivateTeamsResponse",
    "BatchUpdateTeamsRequest",
    "BatchUpdateTeamsResponse",
    "CreateTeamRequest",
    "GetTeamRequest",
    "ListTeamsRequest",
    "ListTeamsResponse",
    "UpdateTeamRequest",
    "TimeUnitEnum",
    "User",
    "GetUserRequest",
    "VideoPositionEnum",
    "WebProperty",
)
