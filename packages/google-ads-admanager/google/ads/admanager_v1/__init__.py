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
from google.ads.admanager_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.ad_break_service import AdBreakServiceClient
from .services.ad_unit_service import AdUnitServiceClient
from .services.bandwidth_group_service import BandwidthGroupServiceClient
from .services.company_service import CompanyServiceClient
from .services.custom_field_service import CustomFieldServiceClient
from .services.custom_targeting_key_service import CustomTargetingKeyServiceClient
from .services.custom_targeting_value_service import CustomTargetingValueServiceClient
from .services.device_category_service import DeviceCategoryServiceClient
from .services.entity_signals_mapping_service import EntitySignalsMappingServiceClient
from .services.geo_target_service import GeoTargetServiceClient
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
from .services.taxonomy_category_service import TaxonomyCategoryServiceClient
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
from .types.ad_unit_enums import AdUnitStatusEnum, SmartSizeModeEnum, TargetWindowEnum
from .types.ad_unit_messages import AdUnit, AdUnitParent, AdUnitSize, LabelFrequencyCap
from .types.ad_unit_service import (
    GetAdUnitRequest,
    ListAdUnitSizesRequest,
    ListAdUnitSizesResponse,
    ListAdUnitsRequest,
    ListAdUnitsResponse,
)
from .types.admanager_error import AdManagerError
from .types.applied_label import AppliedLabel
from .types.bandwidth_group_messages import BandwidthGroup
from .types.bandwidth_group_service import (
    GetBandwidthGroupRequest,
    ListBandwidthGroupsRequest,
    ListBandwidthGroupsResponse,
)
from .types.company_enums import CompanyCreditStatusEnum, CompanyTypeEnum
from .types.company_messages import Company
from .types.company_service import (
    GetCompanyRequest,
    ListCompaniesRequest,
    ListCompaniesResponse,
)
from .types.contact_messages import Contact
from .types.custom_field_enums import (
    CustomFieldDataTypeEnum,
    CustomFieldEntityTypeEnum,
    CustomFieldStatusEnum,
    CustomFieldVisibilityEnum,
)
from .types.custom_field_messages import CustomField, CustomFieldOption
from .types.custom_field_service import (
    GetCustomFieldRequest,
    ListCustomFieldsRequest,
    ListCustomFieldsResponse,
)
from .types.custom_field_value import CustomFieldValue
from .types.custom_targeting_key_enums import (
    CustomTargetingKeyReportableTypeEnum,
    CustomTargetingKeyStatusEnum,
    CustomTargetingKeyTypeEnum,
)
from .types.custom_targeting_key_messages import CustomTargetingKey
from .types.custom_targeting_key_service import (
    GetCustomTargetingKeyRequest,
    ListCustomTargetingKeysRequest,
    ListCustomTargetingKeysResponse,
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
from .types.device_category_messages import DeviceCategory
from .types.device_category_service import (
    GetDeviceCategoryRequest,
    ListDeviceCategoriesRequest,
    ListDeviceCategoriesResponse,
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
from .types.frequency_cap import FrequencyCap
from .types.geo_target_messages import GeoTarget
from .types.geo_target_service import (
    GetGeoTargetRequest,
    ListGeoTargetsRequest,
    ListGeoTargetsResponse,
)
from .types.label_messages import Label
from .types.live_stream_event_messages import LiveStreamEvent
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
    GetPlacementRequest,
    ListPlacementsRequest,
    ListPlacementsResponse,
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
from .types.report_messages import Report, ReportDefinition, Schedule, ScheduleOptions
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
from .types.request_platform_enum import RequestPlatformEnum
from .types.role_enums import RoleStatusEnum
from .types.role_messages import Role
from .types.role_service import GetRoleRequest, ListRolesRequest, ListRolesResponse
from .types.size import Size
from .types.size_type_enum import SizeTypeEnum
from .types.targeted_video_bumper_type_enum import TargetedVideoBumperTypeEnum
from .types.targeting import (
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
from .types.taxonomy_category_messages import TaxonomyCategory
from .types.taxonomy_category_service import (
    GetTaxonomyCategoryRequest,
    ListTaxonomyCategoriesRequest,
    ListTaxonomyCategoriesResponse,
)
from .types.taxonomy_type_enum import TaxonomyTypeEnum
from .types.team_messages import Team
from .types.time_unit_enum import TimeUnitEnum
from .types.user_messages import User
from .types.user_service import GetUserRequest
from .types.video_position_enum import VideoPositionEnum

__all__ = (
    "AdBreak",
    "AdBreakServiceClient",
    "AdBreakStateEnum",
    "AdManagerError",
    "AdUnit",
    "AdUnitParent",
    "AdUnitServiceClient",
    "AdUnitSize",
    "AdUnitStatusEnum",
    "AdUnitTargeting",
    "AppliedLabel",
    "BandwidthGroup",
    "BandwidthGroupServiceClient",
    "BandwidthTargeting",
    "BatchCreateEntitySignalsMappingsRequest",
    "BatchCreateEntitySignalsMappingsResponse",
    "BatchUpdateEntitySignalsMappingsRequest",
    "BatchUpdateEntitySignalsMappingsResponse",
    "Company",
    "CompanyCreditStatusEnum",
    "CompanyServiceClient",
    "CompanyTypeEnum",
    "Contact",
    "CreateAdBreakRequest",
    "CreateEntitySignalsMappingRequest",
    "CreatePrivateAuctionDealRequest",
    "CreatePrivateAuctionRequest",
    "CreateReportRequest",
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
    "DeviceCategory",
    "DeviceCategoryServiceClient",
    "DeviceCategoryTargeting",
    "EntitySignalsMapping",
    "EntitySignalsMappingServiceClient",
    "EnvironmentTypeEnum",
    "FetchReportResultRowsRequest",
    "FetchReportResultRowsResponse",
    "FrequencyCap",
    "GeoTarget",
    "GeoTargetServiceClient",
    "GeoTargeting",
    "GetAdBreakRequest",
    "GetAdUnitRequest",
    "GetBandwidthGroupRequest",
    "GetCompanyRequest",
    "GetCustomFieldRequest",
    "GetCustomTargetingKeyRequest",
    "GetCustomTargetingValueRequest",
    "GetDeviceCategoryRequest",
    "GetEntitySignalsMappingRequest",
    "GetGeoTargetRequest",
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
    "GetTaxonomyCategoryRequest",
    "GetUserRequest",
    "InventoryTargeting",
    "Label",
    "LabelFrequencyCap",
    "ListAdBreaksRequest",
    "ListAdBreaksResponse",
    "ListAdUnitSizesRequest",
    "ListAdUnitSizesResponse",
    "ListAdUnitsRequest",
    "ListAdUnitsResponse",
    "ListBandwidthGroupsRequest",
    "ListBandwidthGroupsResponse",
    "ListCompaniesRequest",
    "ListCompaniesResponse",
    "ListCustomFieldsRequest",
    "ListCustomFieldsResponse",
    "ListCustomTargetingKeysRequest",
    "ListCustomTargetingKeysResponse",
    "ListCustomTargetingValuesRequest",
    "ListCustomTargetingValuesResponse",
    "ListDeviceCategoriesRequest",
    "ListDeviceCategoriesResponse",
    "ListEntitySignalsMappingsRequest",
    "ListEntitySignalsMappingsResponse",
    "ListGeoTargetsRequest",
    "ListGeoTargetsResponse",
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
    "ListTaxonomyCategoriesRequest",
    "ListTaxonomyCategoriesResponse",
    "LiveStreamEvent",
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
    "ReportDefinition",
    "ReportServiceClient",
    "RequestPlatformEnum",
    "RequestPlatformTargeting",
    "Role",
    "RoleServiceClient",
    "RoleStatusEnum",
    "RunReportMetadata",
    "RunReportRequest",
    "RunReportResponse",
    "Schedule",
    "ScheduleOptions",
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
    "TechnologyTargeting",
    "TimeUnitEnum",
    "UpdateAdBreakRequest",
    "UpdateEntitySignalsMappingRequest",
    "UpdatePrivateAuctionDealRequest",
    "UpdatePrivateAuctionRequest",
    "UpdateReportRequest",
    "User",
    "UserDomainTargeting",
    "UserServiceClient",
    "VideoPosition",
    "VideoPositionEnum",
    "VideoPositionTargeting",
)
