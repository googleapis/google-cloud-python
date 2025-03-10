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


from google.ads.admanager_v1.services.ad_unit_service.client import AdUnitServiceClient
from google.ads.admanager_v1.services.company_service.client import CompanyServiceClient
from google.ads.admanager_v1.services.custom_field_service.client import CustomFieldServiceClient
from google.ads.admanager_v1.services.custom_targeting_key_service.client import CustomTargetingKeyServiceClient
from google.ads.admanager_v1.services.custom_targeting_value_service.client import CustomTargetingValueServiceClient
from google.ads.admanager_v1.services.entity_signals_mapping_service.client import EntitySignalsMappingServiceClient
from google.ads.admanager_v1.services.network_service.client import NetworkServiceClient
from google.ads.admanager_v1.services.order_service.client import OrderServiceClient
from google.ads.admanager_v1.services.placement_service.client import PlacementServiceClient
from google.ads.admanager_v1.services.report_service.client import ReportServiceClient
from google.ads.admanager_v1.services.role_service.client import RoleServiceClient
from google.ads.admanager_v1.services.taxonomy_category_service.client import TaxonomyCategoryServiceClient
from google.ads.admanager_v1.services.user_service.client import UserServiceClient

from google.ads.admanager_v1.types.ad_unit_enums import AdUnitStatusEnum
from google.ads.admanager_v1.types.ad_unit_enums import SmartSizeModeEnum
from google.ads.admanager_v1.types.ad_unit_enums import TargetWindowEnum
from google.ads.admanager_v1.types.ad_unit_messages import AdUnit
from google.ads.admanager_v1.types.ad_unit_messages import AdUnitParent
from google.ads.admanager_v1.types.ad_unit_messages import AdUnitSize
from google.ads.admanager_v1.types.ad_unit_messages import LabelFrequencyCap
from google.ads.admanager_v1.types.ad_unit_service import GetAdUnitRequest
from google.ads.admanager_v1.types.ad_unit_service import ListAdUnitSizesRequest
from google.ads.admanager_v1.types.ad_unit_service import ListAdUnitSizesResponse
from google.ads.admanager_v1.types.ad_unit_service import ListAdUnitsRequest
from google.ads.admanager_v1.types.ad_unit_service import ListAdUnitsResponse
from google.ads.admanager_v1.types.admanager_error import AdManagerError
from google.ads.admanager_v1.types.applied_label import AppliedLabel
from google.ads.admanager_v1.types.company_credit_status_enum import CompanyCreditStatusEnum
from google.ads.admanager_v1.types.company_messages import Company
from google.ads.admanager_v1.types.company_service import GetCompanyRequest
from google.ads.admanager_v1.types.company_service import ListCompaniesRequest
from google.ads.admanager_v1.types.company_service import ListCompaniesResponse
from google.ads.admanager_v1.types.company_type_enum import CompanyTypeEnum
from google.ads.admanager_v1.types.contact_messages import Contact
from google.ads.admanager_v1.types.custom_field_enums import CustomFieldDataTypeEnum
from google.ads.admanager_v1.types.custom_field_enums import CustomFieldEntityTypeEnum
from google.ads.admanager_v1.types.custom_field_enums import CustomFieldStatusEnum
from google.ads.admanager_v1.types.custom_field_enums import CustomFieldVisibilityEnum
from google.ads.admanager_v1.types.custom_field_messages import CustomField
from google.ads.admanager_v1.types.custom_field_messages import CustomFieldOption
from google.ads.admanager_v1.types.custom_field_service import GetCustomFieldRequest
from google.ads.admanager_v1.types.custom_field_service import ListCustomFieldsRequest
from google.ads.admanager_v1.types.custom_field_service import ListCustomFieldsResponse
from google.ads.admanager_v1.types.custom_field_value import CustomFieldValue
from google.ads.admanager_v1.types.custom_targeting_key_enums import CustomTargetingKeyReportableTypeEnum
from google.ads.admanager_v1.types.custom_targeting_key_enums import CustomTargetingKeyStatusEnum
from google.ads.admanager_v1.types.custom_targeting_key_enums import CustomTargetingKeyTypeEnum
from google.ads.admanager_v1.types.custom_targeting_key_messages import CustomTargetingKey
from google.ads.admanager_v1.types.custom_targeting_key_service import GetCustomTargetingKeyRequest
from google.ads.admanager_v1.types.custom_targeting_key_service import ListCustomTargetingKeysRequest
from google.ads.admanager_v1.types.custom_targeting_key_service import ListCustomTargetingKeysResponse
from google.ads.admanager_v1.types.custom_targeting_value_enums import CustomTargetingValueMatchTypeEnum
from google.ads.admanager_v1.types.custom_targeting_value_enums import CustomTargetingValueStatusEnum
from google.ads.admanager_v1.types.custom_targeting_value_messages import CustomTargetingValue
from google.ads.admanager_v1.types.custom_targeting_value_service import GetCustomTargetingValueRequest
from google.ads.admanager_v1.types.custom_targeting_value_service import ListCustomTargetingValuesRequest
from google.ads.admanager_v1.types.custom_targeting_value_service import ListCustomTargetingValuesResponse
from google.ads.admanager_v1.types.entity_signals_mapping_messages import EntitySignalsMapping
from google.ads.admanager_v1.types.entity_signals_mapping_service import BatchCreateEntitySignalsMappingsRequest
from google.ads.admanager_v1.types.entity_signals_mapping_service import BatchCreateEntitySignalsMappingsResponse
from google.ads.admanager_v1.types.entity_signals_mapping_service import BatchUpdateEntitySignalsMappingsRequest
from google.ads.admanager_v1.types.entity_signals_mapping_service import BatchUpdateEntitySignalsMappingsResponse
from google.ads.admanager_v1.types.entity_signals_mapping_service import CreateEntitySignalsMappingRequest
from google.ads.admanager_v1.types.entity_signals_mapping_service import GetEntitySignalsMappingRequest
from google.ads.admanager_v1.types.entity_signals_mapping_service import ListEntitySignalsMappingsRequest
from google.ads.admanager_v1.types.entity_signals_mapping_service import ListEntitySignalsMappingsResponse
from google.ads.admanager_v1.types.entity_signals_mapping_service import UpdateEntitySignalsMappingRequest
from google.ads.admanager_v1.types.environment_type_enum import EnvironmentTypeEnum
from google.ads.admanager_v1.types.frequency_cap import FrequencyCap
from google.ads.admanager_v1.types.label_messages import Label
from google.ads.admanager_v1.types.network_messages import Network
from google.ads.admanager_v1.types.network_service import GetNetworkRequest
from google.ads.admanager_v1.types.network_service import ListNetworksRequest
from google.ads.admanager_v1.types.network_service import ListNetworksResponse
from google.ads.admanager_v1.types.order_enums import OrderStatusEnum
from google.ads.admanager_v1.types.order_messages import Order
from google.ads.admanager_v1.types.order_service import GetOrderRequest
from google.ads.admanager_v1.types.order_service import ListOrdersRequest
from google.ads.admanager_v1.types.order_service import ListOrdersResponse
from google.ads.admanager_v1.types.placement_enums import PlacementStatusEnum
from google.ads.admanager_v1.types.placement_messages import Placement
from google.ads.admanager_v1.types.placement_service import GetPlacementRequest
from google.ads.admanager_v1.types.placement_service import ListPlacementsRequest
from google.ads.admanager_v1.types.placement_service import ListPlacementsResponse
from google.ads.admanager_v1.types.report_service import CreateReportRequest
from google.ads.admanager_v1.types.report_service import FetchReportResultRowsRequest
from google.ads.admanager_v1.types.report_service import FetchReportResultRowsResponse
from google.ads.admanager_v1.types.report_service import GetReportRequest
from google.ads.admanager_v1.types.report_service import ListReportsRequest
from google.ads.admanager_v1.types.report_service import ListReportsResponse
from google.ads.admanager_v1.types.report_service import Report
from google.ads.admanager_v1.types.report_service import ReportDefinition
from google.ads.admanager_v1.types.report_service import RunReportMetadata
from google.ads.admanager_v1.types.report_service import RunReportRequest
from google.ads.admanager_v1.types.report_service import RunReportResponse
from google.ads.admanager_v1.types.report_service import Schedule
from google.ads.admanager_v1.types.report_service import ScheduleOptions
from google.ads.admanager_v1.types.report_service import UpdateReportRequest
from google.ads.admanager_v1.types.role_enums import RoleStatusEnum
from google.ads.admanager_v1.types.role_messages import Role
from google.ads.admanager_v1.types.role_service import GetRoleRequest
from google.ads.admanager_v1.types.role_service import ListRolesRequest
from google.ads.admanager_v1.types.role_service import ListRolesResponse
from google.ads.admanager_v1.types.size import Size
from google.ads.admanager_v1.types.size_type_enum import SizeTypeEnum
from google.ads.admanager_v1.types.taxonomy_category_messages import TaxonomyCategory
from google.ads.admanager_v1.types.taxonomy_category_service import GetTaxonomyCategoryRequest
from google.ads.admanager_v1.types.taxonomy_category_service import ListTaxonomyCategoriesRequest
from google.ads.admanager_v1.types.taxonomy_category_service import ListTaxonomyCategoriesResponse
from google.ads.admanager_v1.types.taxonomy_type_enum import TaxonomyTypeEnum
from google.ads.admanager_v1.types.team_messages import Team
from google.ads.admanager_v1.types.time_unit_enum import TimeUnitEnum
from google.ads.admanager_v1.types.user_messages import User
from google.ads.admanager_v1.types.user_service import GetUserRequest

__all__ = ('AdUnitServiceClient',
    'CompanyServiceClient',
    'CustomFieldServiceClient',
    'CustomTargetingKeyServiceClient',
    'CustomTargetingValueServiceClient',
    'EntitySignalsMappingServiceClient',
    'NetworkServiceClient',
    'OrderServiceClient',
    'PlacementServiceClient',
    'ReportServiceClient',
    'RoleServiceClient',
    'TaxonomyCategoryServiceClient',
    'UserServiceClient',
    'AdUnitStatusEnum',
    'SmartSizeModeEnum',
    'TargetWindowEnum',
    'AdUnit',
    'AdUnitParent',
    'AdUnitSize',
    'LabelFrequencyCap',
    'GetAdUnitRequest',
    'ListAdUnitSizesRequest',
    'ListAdUnitSizesResponse',
    'ListAdUnitsRequest',
    'ListAdUnitsResponse',
    'AdManagerError',
    'AppliedLabel',
    'CompanyCreditStatusEnum',
    'Company',
    'GetCompanyRequest',
    'ListCompaniesRequest',
    'ListCompaniesResponse',
    'CompanyTypeEnum',
    'Contact',
    'CustomFieldDataTypeEnum',
    'CustomFieldEntityTypeEnum',
    'CustomFieldStatusEnum',
    'CustomFieldVisibilityEnum',
    'CustomField',
    'CustomFieldOption',
    'GetCustomFieldRequest',
    'ListCustomFieldsRequest',
    'ListCustomFieldsResponse',
    'CustomFieldValue',
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
    'EntitySignalsMapping',
    'BatchCreateEntitySignalsMappingsRequest',
    'BatchCreateEntitySignalsMappingsResponse',
    'BatchUpdateEntitySignalsMappingsRequest',
    'BatchUpdateEntitySignalsMappingsResponse',
    'CreateEntitySignalsMappingRequest',
    'GetEntitySignalsMappingRequest',
    'ListEntitySignalsMappingsRequest',
    'ListEntitySignalsMappingsResponse',
    'UpdateEntitySignalsMappingRequest',
    'EnvironmentTypeEnum',
    'FrequencyCap',
    'Label',
    'Network',
    'GetNetworkRequest',
    'ListNetworksRequest',
    'ListNetworksResponse',
    'OrderStatusEnum',
    'Order',
    'GetOrderRequest',
    'ListOrdersRequest',
    'ListOrdersResponse',
    'PlacementStatusEnum',
    'Placement',
    'GetPlacementRequest',
    'ListPlacementsRequest',
    'ListPlacementsResponse',
    'CreateReportRequest',
    'FetchReportResultRowsRequest',
    'FetchReportResultRowsResponse',
    'GetReportRequest',
    'ListReportsRequest',
    'ListReportsResponse',
    'Report',
    'ReportDefinition',
    'RunReportMetadata',
    'RunReportRequest',
    'RunReportResponse',
    'Schedule',
    'ScheduleOptions',
    'UpdateReportRequest',
    'RoleStatusEnum',
    'Role',
    'GetRoleRequest',
    'ListRolesRequest',
    'ListRolesResponse',
    'Size',
    'SizeTypeEnum',
    'TaxonomyCategory',
    'GetTaxonomyCategoryRequest',
    'ListTaxonomyCategoriesRequest',
    'ListTaxonomyCategoriesResponse',
    'TaxonomyTypeEnum',
    'Team',
    'TimeUnitEnum',
    'User',
    'GetUserRequest',
)
