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
from google.cloud.licensemanager_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.license_manager import LicenseManagerClient
from .services.license_manager import LicenseManagerAsyncClient

from .types.api_entities import BillingInfo
from .types.api_entities import Configuration
from .types.api_entities import Instance
from .types.api_entities import Product
from .types.api_entities import Usage
from .types.api_entities import UserCountBillingInfo
from .types.api_entities import UserCountUsage
from .types.api_entities import ActivationState
from .types.api_entities import LicenseType
from .types.licensemanager import AggregateUsageRequest
from .types.licensemanager import AggregateUsageResponse
from .types.licensemanager import CreateConfigurationRequest
from .types.licensemanager import DeactivateConfigurationRequest
from .types.licensemanager import DeleteConfigurationRequest
from .types.licensemanager import GetConfigurationRequest
from .types.licensemanager import GetInstanceRequest
from .types.licensemanager import GetProductRequest
from .types.licensemanager import ListConfigurationsRequest
from .types.licensemanager import ListConfigurationsResponse
from .types.licensemanager import ListInstancesRequest
from .types.licensemanager import ListInstancesResponse
from .types.licensemanager import ListProductsRequest
from .types.licensemanager import ListProductsResponse
from .types.licensemanager import OperationMetadata
from .types.licensemanager import QueryConfigurationLicenseUsageRequest
from .types.licensemanager import QueryConfigurationLicenseUsageResponse
from .types.licensemanager import ReactivateConfigurationRequest
from .types.licensemanager import UpdateConfigurationRequest

__all__ = (
    'LicenseManagerAsyncClient',
'ActivationState',
'AggregateUsageRequest',
'AggregateUsageResponse',
'BillingInfo',
'Configuration',
'CreateConfigurationRequest',
'DeactivateConfigurationRequest',
'DeleteConfigurationRequest',
'GetConfigurationRequest',
'GetInstanceRequest',
'GetProductRequest',
'Instance',
'LicenseManagerClient',
'LicenseType',
'ListConfigurationsRequest',
'ListConfigurationsResponse',
'ListInstancesRequest',
'ListInstancesResponse',
'ListProductsRequest',
'ListProductsResponse',
'OperationMetadata',
'Product',
'QueryConfigurationLicenseUsageRequest',
'QueryConfigurationLicenseUsageResponse',
'ReactivateConfigurationRequest',
'UpdateConfigurationRequest',
'Usage',
'UserCountBillingInfo',
'UserCountUsage',
)
