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
from google.ads.admanager_v1.services.ad_unit_service.client import AdUnitServiceClient
from google.ads.admanager_v1.services.bandwidth_group_service.client import (
    BandwidthGroupServiceClient,
)
from google.ads.admanager_v1.services.company_service.client import CompanyServiceClient
from google.ads.admanager_v1.services.custom_field_service.client import (
    CustomFieldServiceClient,
)
from google.ads.admanager_v1.services.custom_targeting_key_service.client import (
    CustomTargetingKeyServiceClient,
)
from google.ads.admanager_v1.services.custom_targeting_value_service.client import (
    CustomTargetingValueServiceClient,
)
from google.ads.admanager_v1.services.device_category_service.client import (
    DeviceCategoryServiceClient,
)
from google.ads.admanager_v1.services.entity_signals_mapping_service.client import (
    EntitySignalsMappingServiceClient,
)
from google.ads.admanager_v1.services.geo_target_service.client import (
    GeoTargetServiceClient,
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
from google.ads.admanager_v1.services.taxonomy_category_service.client import (
    TaxonomyCategoryServiceClient,
)
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
    GetAdUnitRequest,
    ListAdUnitSizesRequest,
    ListAdUnitSizesResponse,
    ListAdUnitsRequest,
    ListAdUnitsResponse,
)
from google.ads.admanager_v1.types.admanager_error import AdManagerError
from google.ads.admanager_v1.types.applied_label import AppliedLabel
from google.ads.admanager_v1.types.bandwidth_group_messages import BandwidthGroup
from google.ads.admanager_v1.types.bandwidth_group_service import (
    GetBandwidthGroupRequest,
    ListBandwidthGroupsRequest,
    ListBandwidthGroupsResponse,
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
from google.ads.admanager_v1.types.contact_messages import Contact
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
    GetCustomFieldRequest,
    ListCustomFieldsRequest,
    ListCustomFieldsResponse,
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
    GetCustomTargetingKeyRequest,
    ListCustomTargetingKeysRequest,
    ListCustomTargetingKeysResponse,
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
from google.ads.admanager_v1.types.device_category_messages import DeviceCategory
from google.ads.admanager_v1.types.device_category_service import (
    GetDeviceCategoryRequest,
    ListDeviceCategoriesRequest,
    ListDeviceCategoriesResponse,
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
from google.ads.admanager_v1.types.frequency_cap import FrequencyCap
from google.ads.admanager_v1.types.geo_target_messages import GeoTarget
from google.ads.admanager_v1.types.geo_target_service import (
    GetGeoTargetRequest,
    ListGeoTargetsRequest,
    ListGeoTargetsResponse,
)
from google.ads.admanager_v1.types.label_messages import Label
from google.ads.admanager_v1.types.live_stream_event_messages import LiveStreamEvent
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
    GetPlacementRequest,
    ListPlacementsRequest,
    ListPlacementsResponse,
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
from google.ads.admanager_v1.types.report_messages import (
    Report,
    ReportDefinition,
    Schedule,
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
from google.ads.admanager_v1.types.request_platform_enum import RequestPlatformEnum
from google.ads.admanager_v1.types.role_enums import RoleStatusEnum
from google.ads.admanager_v1.types.role_messages import Role
from google.ads.admanager_v1.types.role_service import (
    GetRoleRequest,
    ListRolesRequest,
    ListRolesResponse,
)
from google.ads.admanager_v1.types.size import Size
from google.ads.admanager_v1.types.size_type_enum import SizeTypeEnum
from google.ads.admanager_v1.types.targeted_video_bumper_type_enum import (
    TargetedVideoBumperTypeEnum,
)
from google.ads.admanager_v1.types.targeting import (
    AdUnitTargeting,
    BandwidthTargeting,
    CustomTargeting,
    CustomTargetingClause,
    CustomTargetingLiteral,
    DataSegmentTargeting,
    DeviceCategoryTargeting,
    GeoTargeting,
    InventoryTargeting,
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
from google.ads.admanager_v1.types.team_messages import Team
from google.ads.admanager_v1.types.time_unit_enum import TimeUnitEnum
from google.ads.admanager_v1.types.user_messages import User
from google.ads.admanager_v1.types.user_service import GetUserRequest
from google.ads.admanager_v1.types.video_position_enum import VideoPositionEnum

__all__ = (
    "AdBreakServiceClient",
    "AdUnitServiceClient",
    "BandwidthGroupServiceClient",
    "CompanyServiceClient",
    "CustomFieldServiceClient",
    "CustomTargetingKeyServiceClient",
    "CustomTargetingValueServiceClient",
    "DeviceCategoryServiceClient",
    "EntitySignalsMappingServiceClient",
    "GeoTargetServiceClient",
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
    "TaxonomyCategoryServiceClient",
    "UserServiceClient",
    "AdBreak",
    "CreateAdBreakRequest",
    "DeleteAdBreakRequest",
    "GetAdBreakRequest",
    "ListAdBreaksRequest",
    "ListAdBreaksResponse",
    "UpdateAdBreakRequest",
    "AdUnitStatusEnum",
    "SmartSizeModeEnum",
    "TargetWindowEnum",
    "AdUnit",
    "AdUnitParent",
    "AdUnitSize",
    "LabelFrequencyCap",
    "GetAdUnitRequest",
    "ListAdUnitSizesRequest",
    "ListAdUnitSizesResponse",
    "ListAdUnitsRequest",
    "ListAdUnitsResponse",
    "AdManagerError",
    "AppliedLabel",
    "BandwidthGroup",
    "GetBandwidthGroupRequest",
    "ListBandwidthGroupsRequest",
    "ListBandwidthGroupsResponse",
    "CompanyCreditStatusEnum",
    "CompanyTypeEnum",
    "Company",
    "GetCompanyRequest",
    "ListCompaniesRequest",
    "ListCompaniesResponse",
    "Contact",
    "CustomFieldDataTypeEnum",
    "CustomFieldEntityTypeEnum",
    "CustomFieldStatusEnum",
    "CustomFieldVisibilityEnum",
    "CustomField",
    "CustomFieldOption",
    "GetCustomFieldRequest",
    "ListCustomFieldsRequest",
    "ListCustomFieldsResponse",
    "CustomFieldValue",
    "CustomTargetingKeyReportableTypeEnum",
    "CustomTargetingKeyStatusEnum",
    "CustomTargetingKeyTypeEnum",
    "CustomTargetingKey",
    "GetCustomTargetingKeyRequest",
    "ListCustomTargetingKeysRequest",
    "ListCustomTargetingKeysResponse",
    "CustomTargetingValueMatchTypeEnum",
    "CustomTargetingValueStatusEnum",
    "CustomTargetingValue",
    "GetCustomTargetingValueRequest",
    "ListCustomTargetingValuesRequest",
    "ListCustomTargetingValuesResponse",
    "DealBuyerPermissionTypeEnum",
    "DeviceCategory",
    "GetDeviceCategoryRequest",
    "ListDeviceCategoriesRequest",
    "ListDeviceCategoriesResponse",
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
    "FrequencyCap",
    "GeoTarget",
    "GetGeoTargetRequest",
    "ListGeoTargetsRequest",
    "ListGeoTargetsResponse",
    "Label",
    "LiveStreamEvent",
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
    "GetPlacementRequest",
    "ListPlacementsRequest",
    "ListPlacementsResponse",
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
    "Report",
    "ReportDefinition",
    "Schedule",
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
    "RequestPlatformEnum",
    "RoleStatusEnum",
    "Role",
    "GetRoleRequest",
    "ListRolesRequest",
    "ListRolesResponse",
    "Size",
    "SizeTypeEnum",
    "TargetedVideoBumperTypeEnum",
    "AdUnitTargeting",
    "BandwidthTargeting",
    "CustomTargeting",
    "CustomTargetingClause",
    "CustomTargetingLiteral",
    "DataSegmentTargeting",
    "DeviceCategoryTargeting",
    "GeoTargeting",
    "InventoryTargeting",
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
    "Team",
    "TimeUnitEnum",
    "User",
    "GetUserRequest",
    "VideoPositionEnum",
)
