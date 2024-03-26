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
from google.ads.admanager_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.ad_partner_service import AdPartnerServiceClient
from .services.ad_unit_service import AdUnitServiceClient
from .services.company_service import CompanyServiceClient
from .services.contact_service import ContactServiceClient
from .services.creative_service import CreativeServiceClient
from .services.custom_field_service import CustomFieldServiceClient
from .services.custom_targeting_key_service import CustomTargetingKeyServiceClient
from .services.custom_targeting_value_service import CustomTargetingValueServiceClient
from .services.label_service import LabelServiceClient
from .services.line_item_service import LineItemServiceClient
from .services.network_service import NetworkServiceClient
from .services.order_service import OrderServiceClient
from .services.placement_service import PlacementServiceClient
from .services.report_service import ReportServiceClient
from .services.role_service import RoleServiceClient
from .services.team_service import TeamServiceClient
from .services.user_service import UserServiceClient
from .types.ad_partner_declaration import AdPartnerDeclaration, DeclarationTypeEnum
from .types.ad_partner_service import (
    AdPartner,
    GetAdPartnerRequest,
    ListAdPartnersRequest,
    ListAdPartnersResponse,
)
from .types.ad_unit_enums import AppliedAdsenseEnabledEnum
from .types.ad_unit_service import (
    AdUnit,
    AdUnitParent,
    GetAdUnitRequest,
    LabelFrequencyCap,
    ListAdUnitsRequest,
    ListAdUnitsResponse,
    SmartSizeModeEnum,
    TargetWindowEnum,
)
from .types.ad_unit_size import AdUnitSize
from .types.admanager_error import AdManagerError
from .types.applied_label import AppliedLabel
from .types.company_credit_status_enum import CompanyCreditStatusEnum
from .types.company_service import (
    Company,
    GetCompanyRequest,
    ListCompaniesRequest,
    ListCompaniesResponse,
)
from .types.company_type_enum import CompanyTypeEnum
from .types.computed_status_enum import ComputedStatusEnum
from .types.contact_service import (
    Contact,
    GetContactRequest,
    ListContactsRequest,
    ListContactsResponse,
)
from .types.creative_placeholder import CreativePlaceholder
from .types.creative_service import (
    Creative,
    GetCreativeRequest,
    ListCreativesRequest,
    ListCreativesResponse,
)
from .types.custom_field_enums import (
    CustomFieldDataTypeEnum,
    CustomFieldEntityTypeEnum,
    CustomFieldStatusEnum,
    CustomFieldVisibilityEnum,
)
from .types.custom_field_service import (
    CustomField,
    CustomFieldOption,
    GetCustomFieldRequest,
    ListCustomFieldsRequest,
    ListCustomFieldsResponse,
)
from .types.custom_targeting_key_enums import (
    CustomTargetingKeyReportableTypeEnum,
    CustomTargetingKeyStatusEnum,
    CustomTargetingKeyTypeEnum,
)
from .types.custom_targeting_key_service import (
    CustomTargetingKey,
    GetCustomTargetingKeyRequest,
    ListCustomTargetingKeysRequest,
    ListCustomTargetingKeysResponse,
)
from .types.custom_targeting_value_enums import (
    CustomTargetingValueMatchTypeEnum,
    CustomTargetingValueStatusEnum,
)
from .types.custom_targeting_value_service import (
    CustomTargetingValue,
    GetCustomTargetingValueRequest,
    ListCustomTargetingValuesRequest,
    ListCustomTargetingValuesResponse,
)
from .types.environment_type_enum import EnvironmentTypeEnum
from .types.frequency_cap import FrequencyCap, TimeUnitEnum
from .types.goal import Goal, GoalTypeEnum, UnitTypeEnum
from .types.label_service import (
    GetLabelRequest,
    Label,
    ListLabelsRequest,
    ListLabelsResponse,
)
from .types.line_item_enums import (
    CreativeRotationTypeEnum,
    DeliveryRateTypeEnum,
    LineItemCostTypeEnum,
    LineItemDiscountTypeEnum,
    LineItemTypeEnum,
    ReservationStatusEnum,
)
from .types.line_item_service import (
    GetLineItemRequest,
    LineItem,
    ListLineItemsRequest,
    ListLineItemsResponse,
)
from .types.network_service import GetNetworkRequest, Network
from .types.order_service import (
    GetOrderRequest,
    ListOrdersRequest,
    ListOrdersResponse,
    Order,
)
from .types.placement_enums import PlacementStatusEnum
from .types.placement_service import (
    GetPlacementRequest,
    ListPlacementsRequest,
    ListPlacementsResponse,
    Placement,
)
from .types.report_service import (
    ExportSavedReportMetadata,
    ExportSavedReportRequest,
    ExportSavedReportResponse,
    Report,
)
from .types.role_service import (
    GetRoleRequest,
    ListRolesRequest,
    ListRolesResponse,
    Role,
)
from .types.size import Size, SizeTypeEnum
from .types.team_service import (
    GetTeamRequest,
    ListTeamsRequest,
    ListTeamsResponse,
    Team,
)
from .types.user_service import (
    GetUserRequest,
    ListUsersRequest,
    ListUsersResponse,
    User,
)

__all__ = (
    "AdManagerError",
    "AdPartner",
    "AdPartnerDeclaration",
    "AdPartnerServiceClient",
    "AdUnit",
    "AdUnitParent",
    "AdUnitServiceClient",
    "AdUnitSize",
    "AppliedAdsenseEnabledEnum",
    "AppliedLabel",
    "Company",
    "CompanyCreditStatusEnum",
    "CompanyServiceClient",
    "CompanyTypeEnum",
    "ComputedStatusEnum",
    "Contact",
    "ContactServiceClient",
    "Creative",
    "CreativePlaceholder",
    "CreativeRotationTypeEnum",
    "CreativeServiceClient",
    "CustomField",
    "CustomFieldDataTypeEnum",
    "CustomFieldEntityTypeEnum",
    "CustomFieldOption",
    "CustomFieldServiceClient",
    "CustomFieldStatusEnum",
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
    "DeclarationTypeEnum",
    "DeliveryRateTypeEnum",
    "EnvironmentTypeEnum",
    "ExportSavedReportMetadata",
    "ExportSavedReportRequest",
    "ExportSavedReportResponse",
    "FrequencyCap",
    "GetAdPartnerRequest",
    "GetAdUnitRequest",
    "GetCompanyRequest",
    "GetContactRequest",
    "GetCreativeRequest",
    "GetCustomFieldRequest",
    "GetCustomTargetingKeyRequest",
    "GetCustomTargetingValueRequest",
    "GetLabelRequest",
    "GetLineItemRequest",
    "GetNetworkRequest",
    "GetOrderRequest",
    "GetPlacementRequest",
    "GetRoleRequest",
    "GetTeamRequest",
    "GetUserRequest",
    "Goal",
    "GoalTypeEnum",
    "Label",
    "LabelFrequencyCap",
    "LabelServiceClient",
    "LineItem",
    "LineItemCostTypeEnum",
    "LineItemDiscountTypeEnum",
    "LineItemServiceClient",
    "LineItemTypeEnum",
    "ListAdPartnersRequest",
    "ListAdPartnersResponse",
    "ListAdUnitsRequest",
    "ListAdUnitsResponse",
    "ListCompaniesRequest",
    "ListCompaniesResponse",
    "ListContactsRequest",
    "ListContactsResponse",
    "ListCreativesRequest",
    "ListCreativesResponse",
    "ListCustomFieldsRequest",
    "ListCustomFieldsResponse",
    "ListCustomTargetingKeysRequest",
    "ListCustomTargetingKeysResponse",
    "ListCustomTargetingValuesRequest",
    "ListCustomTargetingValuesResponse",
    "ListLabelsRequest",
    "ListLabelsResponse",
    "ListLineItemsRequest",
    "ListLineItemsResponse",
    "ListOrdersRequest",
    "ListOrdersResponse",
    "ListPlacementsRequest",
    "ListPlacementsResponse",
    "ListRolesRequest",
    "ListRolesResponse",
    "ListTeamsRequest",
    "ListTeamsResponse",
    "ListUsersRequest",
    "ListUsersResponse",
    "Network",
    "NetworkServiceClient",
    "Order",
    "OrderServiceClient",
    "Placement",
    "PlacementServiceClient",
    "PlacementStatusEnum",
    "Report",
    "ReportServiceClient",
    "ReservationStatusEnum",
    "Role",
    "RoleServiceClient",
    "Size",
    "SizeTypeEnum",
    "SmartSizeModeEnum",
    "TargetWindowEnum",
    "Team",
    "TeamServiceClient",
    "TimeUnitEnum",
    "UnitTypeEnum",
    "User",
    "UserServiceClient",
)
