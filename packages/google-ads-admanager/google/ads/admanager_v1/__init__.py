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


from .services.ad_unit_service import AdUnitServiceClient
from .services.company_service import CompanyServiceClient
from .services.custom_field_service import CustomFieldServiceClient
from .services.custom_targeting_key_service import CustomTargetingKeyServiceClient
from .services.custom_targeting_value_service import CustomTargetingValueServiceClient
from .services.entity_signals_mapping_service import EntitySignalsMappingServiceClient
from .services.network_service import NetworkServiceClient
from .services.order_service import OrderServiceClient
from .services.placement_service import PlacementServiceClient
from .services.report_service import ReportServiceClient
from .services.role_service import RoleServiceClient
from .services.taxonomy_category_service import TaxonomyCategoryServiceClient
from .services.user_service import UserServiceClient
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
from .types.company_credit_status_enum import CompanyCreditStatusEnum
from .types.company_messages import Company
from .types.company_service import (
    GetCompanyRequest,
    ListCompaniesRequest,
    ListCompaniesResponse,
)
from .types.company_type_enum import CompanyTypeEnum
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
from .types.label_messages import Label
from .types.network_messages import Network
from .types.network_service import (
    GetNetworkRequest,
    ListNetworksRequest,
    ListNetworksResponse,
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
from .types.report_service import (
    CreateReportRequest,
    FetchReportResultRowsRequest,
    FetchReportResultRowsResponse,
    GetReportRequest,
    ListReportsRequest,
    ListReportsResponse,
    Report,
    ReportDefinition,
    RunReportMetadata,
    RunReportRequest,
    RunReportResponse,
    Schedule,
    ScheduleOptions,
    UpdateReportRequest,
)
from .types.role_enums import RoleStatusEnum
from .types.role_messages import Role
from .types.role_service import GetRoleRequest, ListRolesRequest, ListRolesResponse
from .types.size import Size
from .types.size_type_enum import SizeTypeEnum
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

__all__ = (
    "AdManagerError",
    "AdUnit",
    "AdUnitParent",
    "AdUnitServiceClient",
    "AdUnitSize",
    "AdUnitStatusEnum",
    "AppliedLabel",
    "BatchCreateEntitySignalsMappingsRequest",
    "BatchCreateEntitySignalsMappingsResponse",
    "BatchUpdateEntitySignalsMappingsRequest",
    "BatchUpdateEntitySignalsMappingsResponse",
    "Company",
    "CompanyCreditStatusEnum",
    "CompanyServiceClient",
    "CompanyTypeEnum",
    "Contact",
    "CreateEntitySignalsMappingRequest",
    "CreateReportRequest",
    "CustomField",
    "CustomFieldDataTypeEnum",
    "CustomFieldEntityTypeEnum",
    "CustomFieldOption",
    "CustomFieldServiceClient",
    "CustomFieldStatusEnum",
    "CustomFieldValue",
    "CustomFieldVisibilityEnum",
    "CustomTargetingKey",
    "CustomTargetingKeyReportableTypeEnum",
    "CustomTargetingKeyServiceClient",
    "CustomTargetingKeyStatusEnum",
    "CustomTargetingKeyTypeEnum",
    "CustomTargetingValue",
    "CustomTargetingValueMatchTypeEnum",
    "CustomTargetingValueServiceClient",
    "CustomTargetingValueStatusEnum",
    "EntitySignalsMapping",
    "EntitySignalsMappingServiceClient",
    "EnvironmentTypeEnum",
    "FetchReportResultRowsRequest",
    "FetchReportResultRowsResponse",
    "FrequencyCap",
    "GetAdUnitRequest",
    "GetCompanyRequest",
    "GetCustomFieldRequest",
    "GetCustomTargetingKeyRequest",
    "GetCustomTargetingValueRequest",
    "GetEntitySignalsMappingRequest",
    "GetNetworkRequest",
    "GetOrderRequest",
    "GetPlacementRequest",
    "GetReportRequest",
    "GetRoleRequest",
    "GetTaxonomyCategoryRequest",
    "GetUserRequest",
    "Label",
    "LabelFrequencyCap",
    "ListAdUnitSizesRequest",
    "ListAdUnitSizesResponse",
    "ListAdUnitsRequest",
    "ListAdUnitsResponse",
    "ListCompaniesRequest",
    "ListCompaniesResponse",
    "ListCustomFieldsRequest",
    "ListCustomFieldsResponse",
    "ListCustomTargetingKeysRequest",
    "ListCustomTargetingKeysResponse",
    "ListCustomTargetingValuesRequest",
    "ListCustomTargetingValuesResponse",
    "ListEntitySignalsMappingsRequest",
    "ListEntitySignalsMappingsResponse",
    "ListNetworksRequest",
    "ListNetworksResponse",
    "ListOrdersRequest",
    "ListOrdersResponse",
    "ListPlacementsRequest",
    "ListPlacementsResponse",
    "ListReportsRequest",
    "ListReportsResponse",
    "ListRolesRequest",
    "ListRolesResponse",
    "ListTaxonomyCategoriesRequest",
    "ListTaxonomyCategoriesResponse",
    "Network",
    "NetworkServiceClient",
    "Order",
    "OrderServiceClient",
    "OrderStatusEnum",
    "Placement",
    "PlacementServiceClient",
    "PlacementStatusEnum",
    "Report",
    "ReportDefinition",
    "ReportServiceClient",
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
    "TaxonomyCategory",
    "TaxonomyCategoryServiceClient",
    "TaxonomyTypeEnum",
    "Team",
    "TimeUnitEnum",
    "UpdateEntitySignalsMappingRequest",
    "UpdateReportRequest",
    "User",
    "UserServiceClient",
)
