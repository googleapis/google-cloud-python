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
from google.cloud.licensemanager import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.licensemanager_v1.services.license_manager.client import LicenseManagerClient
from google.cloud.licensemanager_v1.services.license_manager.async_client import LicenseManagerAsyncClient

from google.cloud.licensemanager_v1.types.api_entities import BillingInfo
from google.cloud.licensemanager_v1.types.api_entities import Configuration
from google.cloud.licensemanager_v1.types.api_entities import Instance
from google.cloud.licensemanager_v1.types.api_entities import Product
from google.cloud.licensemanager_v1.types.api_entities import Usage
from google.cloud.licensemanager_v1.types.api_entities import UserCountBillingInfo
from google.cloud.licensemanager_v1.types.api_entities import UserCountUsage
from google.cloud.licensemanager_v1.types.api_entities import ActivationState
from google.cloud.licensemanager_v1.types.api_entities import LicenseType
from google.cloud.licensemanager_v1.types.licensemanager import AggregateUsageRequest
from google.cloud.licensemanager_v1.types.licensemanager import AggregateUsageResponse
from google.cloud.licensemanager_v1.types.licensemanager import CreateConfigurationRequest
from google.cloud.licensemanager_v1.types.licensemanager import DeactivateConfigurationRequest
from google.cloud.licensemanager_v1.types.licensemanager import DeleteConfigurationRequest
from google.cloud.licensemanager_v1.types.licensemanager import GetConfigurationRequest
from google.cloud.licensemanager_v1.types.licensemanager import GetInstanceRequest
from google.cloud.licensemanager_v1.types.licensemanager import GetProductRequest
from google.cloud.licensemanager_v1.types.licensemanager import ListConfigurationsRequest
from google.cloud.licensemanager_v1.types.licensemanager import ListConfigurationsResponse
from google.cloud.licensemanager_v1.types.licensemanager import ListInstancesRequest
from google.cloud.licensemanager_v1.types.licensemanager import ListInstancesResponse
from google.cloud.licensemanager_v1.types.licensemanager import ListProductsRequest
from google.cloud.licensemanager_v1.types.licensemanager import ListProductsResponse
from google.cloud.licensemanager_v1.types.licensemanager import OperationMetadata
from google.cloud.licensemanager_v1.types.licensemanager import QueryConfigurationLicenseUsageRequest
from google.cloud.licensemanager_v1.types.licensemanager import QueryConfigurationLicenseUsageResponse
from google.cloud.licensemanager_v1.types.licensemanager import ReactivateConfigurationRequest
from google.cloud.licensemanager_v1.types.licensemanager import UpdateConfigurationRequest

__all__ = ('LicenseManagerClient',
    'LicenseManagerAsyncClient',
    'BillingInfo',
    'Configuration',
    'Instance',
    'Product',
    'Usage',
    'UserCountBillingInfo',
    'UserCountUsage',
    'ActivationState',
    'LicenseType',
    'AggregateUsageRequest',
    'AggregateUsageResponse',
    'CreateConfigurationRequest',
    'DeactivateConfigurationRequest',
    'DeleteConfigurationRequest',
    'GetConfigurationRequest',
    'GetInstanceRequest',
    'GetProductRequest',
    'ListConfigurationsRequest',
    'ListConfigurationsResponse',
    'ListInstancesRequest',
    'ListInstancesResponse',
    'ListProductsRequest',
    'ListProductsResponse',
    'OperationMetadata',
    'QueryConfigurationLicenseUsageRequest',
    'QueryConfigurationLicenseUsageResponse',
    'ReactivateConfigurationRequest',
    'UpdateConfigurationRequest',
)
