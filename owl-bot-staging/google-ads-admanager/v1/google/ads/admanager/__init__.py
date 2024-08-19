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
from google.ads.admanager import gapic_version as package_version

__version__ = package_version.__version__


from google.ads.admanager_v1.services.ad_partner_service.client import AdPartnerServiceClient
from google.ads.admanager_v1.services.ad_unit_service.client import AdUnitServiceClient
from google.ads.admanager_v1.services.company_service.client import CompanyServiceClient
from google.ads.admanager_v1.services.contact_service.client import ContactServiceClient
from google.ads.admanager_v1.services.creative_service.client import CreativeServiceClient
from google.ads.admanager_v1.services.custom_field_service.client import CustomFieldServiceClient
from google.ads.admanager_v1.services.custom_targeting_key_service.client import CustomTargetingKeyServiceClient
from google.ads.admanager_v1.services.custom_targeting_value_service.client import CustomTargetingValueServiceClient
from google.ads.admanager_v1.services.label_service.client import LabelServiceClient
from google.ads.admanager_v1.services.line_item_service.client import LineItemServiceClient
from google.ads.admanager_v1.services.network_service.client import NetworkServiceClient
from google.ads.admanager_v1.services.order_service.client import OrderServiceClient
from google.ads.admanager_v1.services.placement_service.client import PlacementServiceClient
from google.ads.admanager_v1.services.report_service.client import ReportServiceClient
from google.ads.admanager_v1.services.role_service.client import RoleServiceClient
from google.ads.admanager_v1.services.team_service.client import TeamServiceClient
from google.ads.admanager_v1.services.user_service.client import UserServiceClient

from google.ads.admanager_v1.types.ad_partner_declaration import AdPartnerDeclaration
from google.ads.admanager_v1.types.ad_partner_declaration import DeclarationTypeEnum
from google.ads.admanager_v1.types.ad_partner_service import AdPartner
from google.ads.admanager_v1.types.ad_partner_service import GetAdPartnerRequest
from google.ads.admanager_v1.types.ad_partner_service import ListAdPartnersRequest
from google.ads.admanager_v1.types.ad_partner_service import ListAdPartnersResponse
from google.ads.admanager_v1.types.ad_unit_enums import AppliedAdsenseEnabledEnum
from google.ads.admanager_v1.types.ad_unit_service import AdUnit
from google.ads.admanager_v1.types.ad_unit_service import AdUnitParent
from google.ads.admanager_v1.types.ad_unit_service import GetAdUnitRequest
from google.ads.admanager_v1.types.ad_unit_service import LabelFrequencyCap
from google.ads.admanager_v1.types.ad_unit_service import ListAdUnitsRequest
from google.ads.admanager_v1.types.ad_unit_service import ListAdUnitsResponse
from google.ads.admanager_v1.types.ad_unit_service import SmartSizeModeEnum
from google.ads.admanager_v1.types.ad_unit_service import TargetWindowEnum
from google.ads.admanager_v1.types.ad_unit_size import AdUnitSize
from google.ads.admanager_v1.types.admanager_error import AdManagerError
from google.ads.admanager_v1.types.applied_label import AppliedLabel
from google.ads.admanager_v1.types.company_credit_status_enum import CompanyCreditStatusEnum
from google.ads.admanager_v1.types.company_service import Company
from google.ads.admanager_v1.types.company_service import GetCompanyRequest
from google.ads.admanager_v1.types.company_service import ListCompaniesRequest
from google.ads.admanager_v1.types.company_service import ListCompaniesResponse
from google.ads.admanager_v1.types.company_type_enum import CompanyTypeEnum
from google.ads.admanager_v1.types.computed_status_enum import ComputedStatusEnum
from google.ads.admanager_v1.types.contact_service import Contact
from google.ads.admanager_v1.types.contact_service import GetContactRequest
from google.ads.admanager_v1.types.contact_service import ListContactsRequest
from google.ads.admanager_v1.types.contact_service import ListContactsResponse
from google.ads.admanager_v1.types.creative_placeholder import CreativePlaceholder
from google.ads.admanager_v1.types.creative_service import Creative
from google.ads.admanager_v1.types.creative_service import GetCreativeRequest
from google.ads.admanager_v1.types.creative_service import ListCreativesRequest
from google.ads.admanager_v1.types.creative_service import ListCreativesResponse
from google.ads.admanager_v1.types.custom_field_enums import CustomFieldDataTypeEnum
from google.ads.admanager_v1.types.custom_field_enums import CustomFieldEntityTypeEnum
from google.ads.admanager_v1.types.custom_field_enums import CustomFieldStatusEnum
from google.ads.admanager_v1.types.custom_field_enums import CustomFieldVisibilityEnum
from google.ads.admanager_v1.types.custom_field_service import CustomField
from google.ads.admanager_v1.types.custom_field_service import CustomFieldOption
from google.ads.admanager_v1.types.custom_field_service import GetCustomFieldRequest
from google.ads.admanager_v1.types.custom_field_service import ListCustomFieldsRequest
from google.ads.admanager_v1.types.custom_field_service import ListCustomFieldsResponse
from google.ads.admanager_v1.types.custom_targeting_key_enums import CustomTargetingKeyReportableTypeEnum
from google.ads.admanager_v1.types.custom_targeting_key_enums import CustomTargetingKeyStatusEnum
from google.ads.admanager_v1.types.custom_targeting_key_enums import CustomTargetingKeyTypeEnum
from google.ads.admanager_v1.types.custom_targeting_key_service import CustomTargetingKey
from google.ads.admanager_v1.types.custom_targeting_key_service import GetCustomTargetingKeyRequest
from google.ads.admanager_v1.types.custom_targeting_key_service import ListCustomTargetingKeysRequest
from google.ads.admanager_v1.types.custom_targeting_key_service import ListCustomTargetingKeysResponse
from google.ads.admanager_v1.types.custom_targeting_value_enums import CustomTargetingValueMatchTypeEnum
from google.ads.admanager_v1.types.custom_targeting_value_enums import CustomTargetingValueStatusEnum
from google.ads.admanager_v1.types.custom_targeting_value_service import CustomTargetingValue
from google.ads.admanager_v1.types.custom_targeting_value_service import GetCustomTargetingValueRequest
from google.ads.admanager_v1.types.custom_targeting_value_service import ListCustomTargetingValuesRequest
from google.ads.admanager_v1.types.custom_targeting_value_service import ListCustomTargetingValuesResponse
from google.ads.admanager_v1.types.environment_type_enum import EnvironmentTypeEnum
from google.ads.admanager_v1.types.frequency_cap import FrequencyCap
from google.ads.admanager_v1.types.frequency_cap import TimeUnitEnum
from google.ads.admanager_v1.types.goal import Goal
from google.ads.admanager_v1.types.goal import GoalTypeEnum
from google.ads.admanager_v1.types.goal import UnitTypeEnum
from google.ads.admanager_v1.types.label_service import GetLabelRequest
from google.ads.admanager_v1.types.label_service import Label
from google.ads.admanager_v1.types.label_service import ListLabelsRequest
from google.ads.admanager_v1.types.label_service import ListLabelsResponse
from google.ads.admanager_v1.types.line_item_enums import CreativeRotationTypeEnum
from google.ads.admanager_v1.types.line_item_enums import DeliveryRateTypeEnum
from google.ads.admanager_v1.types.line_item_enums import LineItemCostTypeEnum
from google.ads.admanager_v1.types.line_item_enums import LineItemDiscountTypeEnum
from google.ads.admanager_v1.types.line_item_enums import LineItemTypeEnum
from google.ads.admanager_v1.types.line_item_enums import ReservationStatusEnum
from google.ads.admanager_v1.types.line_item_service import GetLineItemRequest
from google.ads.admanager_v1.types.line_item_service import LineItem
from google.ads.admanager_v1.types.line_item_service import ListLineItemsRequest
from google.ads.admanager_v1.types.line_item_service import ListLineItemsResponse
from google.ads.admanager_v1.types.network_service import GetNetworkRequest
from google.ads.admanager_v1.types.network_service import Network
from google.ads.admanager_v1.types.order_service import GetOrderRequest
from google.ads.admanager_v1.types.order_service import ListOrdersRequest
from google.ads.admanager_v1.types.order_service import ListOrdersResponse
from google.ads.admanager_v1.types.order_service import Order
from google.ads.admanager_v1.types.placement_enums import PlacementStatusEnum
from google.ads.admanager_v1.types.placement_service import GetPlacementRequest
from google.ads.admanager_v1.types.placement_service import ListPlacementsRequest
from google.ads.admanager_v1.types.placement_service import ListPlacementsResponse
from google.ads.admanager_v1.types.placement_service import Placement
from google.ads.admanager_v1.types.report_service import ExportSavedReportMetadata
from google.ads.admanager_v1.types.report_service import ExportSavedReportRequest
from google.ads.admanager_v1.types.report_service import ExportSavedReportResponse
from google.ads.admanager_v1.types.report_service import Report
from google.ads.admanager_v1.types.role_service import GetRoleRequest
from google.ads.admanager_v1.types.role_service import ListRolesRequest
from google.ads.admanager_v1.types.role_service import ListRolesResponse
from google.ads.admanager_v1.types.role_service import Role
from google.ads.admanager_v1.types.size import Size
from google.ads.admanager_v1.types.size import SizeTypeEnum
from google.ads.admanager_v1.types.team_service import GetTeamRequest
from google.ads.admanager_v1.types.team_service import ListTeamsRequest
from google.ads.admanager_v1.types.team_service import ListTeamsResponse
from google.ads.admanager_v1.types.team_service import Team
from google.ads.admanager_v1.types.user_service import GetUserRequest
from google.ads.admanager_v1.types.user_service import ListUsersRequest
from google.ads.admanager_v1.types.user_service import ListUsersResponse
from google.ads.admanager_v1.types.user_service import User

__all__ = ('AdPartnerServiceClient',
    'AdUnitServiceClient',
    'CompanyServiceClient',
    'ContactServiceClient',
    'CreativeServiceClient',
    'CustomFieldServiceClient',
    'CustomTargetingKeyServiceClient',
    'CustomTargetingValueServiceClient',
    'LabelServiceClient',
    'LineItemServiceClient',
    'NetworkServiceClient',
    'OrderServiceClient',
    'PlacementServiceClient',
    'ReportServiceClient',
    'RoleServiceClient',
    'TeamServiceClient',
    'UserServiceClient',
    'AdPartnerDeclaration',
    'DeclarationTypeEnum',
    'AdPartner',
    'GetAdPartnerRequest',
    'ListAdPartnersRequest',
    'ListAdPartnersResponse',
    'AppliedAdsenseEnabledEnum',
    'AdUnit',
    'AdUnitParent',
    'GetAdUnitRequest',
    'LabelFrequencyCap',
    'ListAdUnitsRequest',
    'ListAdUnitsResponse',
    'SmartSizeModeEnum',
    'TargetWindowEnum',
    'AdUnitSize',
    'AdManagerError',
    'AppliedLabel',
    'CompanyCreditStatusEnum',
    'Company',
    'GetCompanyRequest',
    'ListCompaniesRequest',
    'ListCompaniesResponse',
    'CompanyTypeEnum',
    'ComputedStatusEnum',
    'Contact',
    'GetContactRequest',
    'ListContactsRequest',
    'ListContactsResponse',
    'CreativePlaceholder',
    'Creative',
    'GetCreativeRequest',
    'ListCreativesRequest',
    'ListCreativesResponse',
    'CustomFieldDataTypeEnum',
    'CustomFieldEntityTypeEnum',
    'CustomFieldStatusEnum',
    'CustomFieldVisibilityEnum',
    'CustomField',
    'CustomFieldOption',
    'GetCustomFieldRequest',
    'ListCustomFieldsRequest',
    'ListCustomFieldsResponse',
    'CustomTargetingKeyReportableTypeEnum',
    'CustomTargetingKeyStatusEnum',
    'CustomTargetingKeyTypeEnum',
    'CustomTargetingKey',
    'GetCustomTargetingKeyRequest',
    'ListCustomTargetingKeysRequest',
    'ListCustomTargetingKeysResponse',
    'CustomTargetingValueMatchTypeEnum',
    'CustomTargetingValueStatusEnum',
    'CustomTargetingValue',
    'GetCustomTargetingValueRequest',
    'ListCustomTargetingValuesRequest',
    'ListCustomTargetingValuesResponse',
    'EnvironmentTypeEnum',
    'FrequencyCap',
    'TimeUnitEnum',
    'Goal',
    'GoalTypeEnum',
    'UnitTypeEnum',
    'GetLabelRequest',
    'Label',
    'ListLabelsRequest',
    'ListLabelsResponse',
    'CreativeRotationTypeEnum',
    'DeliveryRateTypeEnum',
    'LineItemCostTypeEnum',
    'LineItemDiscountTypeEnum',
    'LineItemTypeEnum',
    'ReservationStatusEnum',
    'GetLineItemRequest',
    'LineItem',
    'ListLineItemsRequest',
    'ListLineItemsResponse',
    'GetNetworkRequest',
    'Network',
    'GetOrderRequest',
    'ListOrdersRequest',
    'ListOrdersResponse',
    'Order',
    'PlacementStatusEnum',
    'GetPlacementRequest',
    'ListPlacementsRequest',
    'ListPlacementsResponse',
    'Placement',
    'ExportSavedReportMetadata',
    'ExportSavedReportRequest',
    'ExportSavedReportResponse',
    'Report',
    'GetRoleRequest',
    'ListRolesRequest',
    'ListRolesResponse',
    'Role',
    'Size',
    'SizeTypeEnum',
    'GetTeamRequest',
    'ListTeamsRequest',
    'ListTeamsResponse',
    'Team',
    'GetUserRequest',
    'ListUsersRequest',
    'ListUsersResponse',
    'User',
)
