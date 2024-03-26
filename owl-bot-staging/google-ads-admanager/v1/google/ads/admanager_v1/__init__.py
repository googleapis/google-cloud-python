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

from .types.ad_partner_declaration import AdPartnerDeclaration
from .types.ad_partner_declaration import DeclarationTypeEnum
from .types.ad_partner_service import AdPartner
from .types.ad_partner_service import GetAdPartnerRequest
from .types.ad_partner_service import ListAdPartnersRequest
from .types.ad_partner_service import ListAdPartnersResponse
from .types.ad_unit_enums import AppliedAdsenseEnabledEnum
from .types.ad_unit_service import AdUnit
from .types.ad_unit_service import AdUnitParent
from .types.ad_unit_service import GetAdUnitRequest
from .types.ad_unit_service import LabelFrequencyCap
from .types.ad_unit_service import ListAdUnitsRequest
from .types.ad_unit_service import ListAdUnitsResponse
from .types.ad_unit_service import SmartSizeModeEnum
from .types.ad_unit_service import TargetWindowEnum
from .types.ad_unit_size import AdUnitSize
from .types.admanager_error import AdManagerError
from .types.applied_label import AppliedLabel
from .types.company_credit_status_enum import CompanyCreditStatusEnum
from .types.company_service import Company
from .types.company_service import GetCompanyRequest
from .types.company_service import ListCompaniesRequest
from .types.company_service import ListCompaniesResponse
from .types.company_type_enum import CompanyTypeEnum
from .types.computed_status_enum import ComputedStatusEnum
from .types.contact_service import Contact
from .types.contact_service import GetContactRequest
from .types.contact_service import ListContactsRequest
from .types.contact_service import ListContactsResponse
from .types.creative_placeholder import CreativePlaceholder
from .types.creative_service import Creative
from .types.creative_service import GetCreativeRequest
from .types.creative_service import ListCreativesRequest
from .types.creative_service import ListCreativesResponse
from .types.custom_field_enums import CustomFieldDataTypeEnum
from .types.custom_field_enums import CustomFieldEntityTypeEnum
from .types.custom_field_enums import CustomFieldStatusEnum
from .types.custom_field_enums import CustomFieldVisibilityEnum
from .types.custom_field_service import CustomField
from .types.custom_field_service import CustomFieldOption
from .types.custom_field_service import GetCustomFieldRequest
from .types.custom_field_service import ListCustomFieldsRequest
from .types.custom_field_service import ListCustomFieldsResponse
from .types.custom_targeting_key_enums import CustomTargetingKeyReportableTypeEnum
from .types.custom_targeting_key_enums import CustomTargetingKeyStatusEnum
from .types.custom_targeting_key_enums import CustomTargetingKeyTypeEnum
from .types.custom_targeting_key_service import CustomTargetingKey
from .types.custom_targeting_key_service import GetCustomTargetingKeyRequest
from .types.custom_targeting_key_service import ListCustomTargetingKeysRequest
from .types.custom_targeting_key_service import ListCustomTargetingKeysResponse
from .types.custom_targeting_value_enums import CustomTargetingValueMatchTypeEnum
from .types.custom_targeting_value_enums import CustomTargetingValueStatusEnum
from .types.custom_targeting_value_service import CustomTargetingValue
from .types.custom_targeting_value_service import GetCustomTargetingValueRequest
from .types.custom_targeting_value_service import ListCustomTargetingValuesRequest
from .types.custom_targeting_value_service import ListCustomTargetingValuesResponse
from .types.environment_type_enum import EnvironmentTypeEnum
from .types.frequency_cap import FrequencyCap
from .types.frequency_cap import TimeUnitEnum
from .types.goal import Goal
from .types.goal import GoalTypeEnum
from .types.goal import UnitTypeEnum
from .types.label_service import GetLabelRequest
from .types.label_service import Label
from .types.label_service import ListLabelsRequest
from .types.label_service import ListLabelsResponse
from .types.line_item_enums import CreativeRotationTypeEnum
from .types.line_item_enums import DeliveryRateTypeEnum
from .types.line_item_enums import LineItemCostTypeEnum
from .types.line_item_enums import LineItemDiscountTypeEnum
from .types.line_item_enums import LineItemTypeEnum
from .types.line_item_enums import ReservationStatusEnum
from .types.line_item_service import GetLineItemRequest
from .types.line_item_service import LineItem
from .types.line_item_service import ListLineItemsRequest
from .types.line_item_service import ListLineItemsResponse
from .types.network_service import GetNetworkRequest
from .types.network_service import Network
from .types.order_service import GetOrderRequest
from .types.order_service import ListOrdersRequest
from .types.order_service import ListOrdersResponse
from .types.order_service import Order
from .types.placement_enums import PlacementStatusEnum
from .types.placement_service import GetPlacementRequest
from .types.placement_service import ListPlacementsRequest
from .types.placement_service import ListPlacementsResponse
from .types.placement_service import Placement
from .types.report_service import ExportSavedReportMetadata
from .types.report_service import ExportSavedReportRequest
from .types.report_service import ExportSavedReportResponse
from .types.report_service import Report
from .types.role_service import GetRoleRequest
from .types.role_service import ListRolesRequest
from .types.role_service import ListRolesResponse
from .types.role_service import Role
from .types.size import Size
from .types.size import SizeTypeEnum
from .types.team_service import GetTeamRequest
from .types.team_service import ListTeamsRequest
from .types.team_service import ListTeamsResponse
from .types.team_service import Team
from .types.user_service import GetUserRequest
from .types.user_service import ListUsersRequest
from .types.user_service import ListUsersResponse
from .types.user_service import User

__all__ = (
'AdManagerError',
'AdPartner',
'AdPartnerDeclaration',
'AdPartnerServiceClient',
'AdUnit',
'AdUnitParent',
'AdUnitServiceClient',
'AdUnitSize',
'AppliedAdsenseEnabledEnum',
'AppliedLabel',
'Company',
'CompanyCreditStatusEnum',
'CompanyServiceClient',
'CompanyTypeEnum',
'ComputedStatusEnum',
'Contact',
'ContactServiceClient',
'Creative',
'CreativePlaceholder',
'CreativeRotationTypeEnum',
'CreativeServiceClient',
'CustomField',
'CustomFieldDataTypeEnum',
'CustomFieldEntityTypeEnum',
'CustomFieldOption',
'CustomFieldServiceClient',
'CustomFieldStatusEnum',
'CustomFieldVisibilityEnum',
'CustomTargetingKey',
'CustomTargetingKeyReportableTypeEnum',
'CustomTargetingKeyServiceClient',
'CustomTargetingKeyStatusEnum',
'CustomTargetingKeyTypeEnum',
'CustomTargetingValue',
'CustomTargetingValueMatchTypeEnum',
'CustomTargetingValueServiceClient',
'CustomTargetingValueStatusEnum',
'DeclarationTypeEnum',
'DeliveryRateTypeEnum',
'EnvironmentTypeEnum',
'ExportSavedReportMetadata',
'ExportSavedReportRequest',
'ExportSavedReportResponse',
'FrequencyCap',
'GetAdPartnerRequest',
'GetAdUnitRequest',
'GetCompanyRequest',
'GetContactRequest',
'GetCreativeRequest',
'GetCustomFieldRequest',
'GetCustomTargetingKeyRequest',
'GetCustomTargetingValueRequest',
'GetLabelRequest',
'GetLineItemRequest',
'GetNetworkRequest',
'GetOrderRequest',
'GetPlacementRequest',
'GetRoleRequest',
'GetTeamRequest',
'GetUserRequest',
'Goal',
'GoalTypeEnum',
'Label',
'LabelFrequencyCap',
'LabelServiceClient',
'LineItem',
'LineItemCostTypeEnum',
'LineItemDiscountTypeEnum',
'LineItemServiceClient',
'LineItemTypeEnum',
'ListAdPartnersRequest',
'ListAdPartnersResponse',
'ListAdUnitsRequest',
'ListAdUnitsResponse',
'ListCompaniesRequest',
'ListCompaniesResponse',
'ListContactsRequest',
'ListContactsResponse',
'ListCreativesRequest',
'ListCreativesResponse',
'ListCustomFieldsRequest',
'ListCustomFieldsResponse',
'ListCustomTargetingKeysRequest',
'ListCustomTargetingKeysResponse',
'ListCustomTargetingValuesRequest',
'ListCustomTargetingValuesResponse',
'ListLabelsRequest',
'ListLabelsResponse',
'ListLineItemsRequest',
'ListLineItemsResponse',
'ListOrdersRequest',
'ListOrdersResponse',
'ListPlacementsRequest',
'ListPlacementsResponse',
'ListRolesRequest',
'ListRolesResponse',
'ListTeamsRequest',
'ListTeamsResponse',
'ListUsersRequest',
'ListUsersResponse',
'Network',
'NetworkServiceClient',
'Order',
'OrderServiceClient',
'Placement',
'PlacementServiceClient',
'PlacementStatusEnum',
'Report',
'ReportServiceClient',
'ReservationStatusEnum',
'Role',
'RoleServiceClient',
'Size',
'SizeTypeEnum',
'SmartSizeModeEnum',
'TargetWindowEnum',
'Team',
'TeamServiceClient',
'TimeUnitEnum',
'UnitTypeEnum',
'User',
'UserServiceClient',
)
