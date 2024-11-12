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
from google.cloud.cloudquotas import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.cloudquotas_v1.services.cloud_quotas.client import CloudQuotasClient
from google.cloud.cloudquotas_v1.services.cloud_quotas.async_client import CloudQuotasAsyncClient

from google.cloud.cloudquotas_v1.types.cloudquotas import CreateQuotaPreferenceRequest
from google.cloud.cloudquotas_v1.types.cloudquotas import GetQuotaInfoRequest
from google.cloud.cloudquotas_v1.types.cloudquotas import GetQuotaPreferenceRequest
from google.cloud.cloudquotas_v1.types.cloudquotas import ListQuotaInfosRequest
from google.cloud.cloudquotas_v1.types.cloudquotas import ListQuotaInfosResponse
from google.cloud.cloudquotas_v1.types.cloudquotas import ListQuotaPreferencesRequest
from google.cloud.cloudquotas_v1.types.cloudquotas import ListQuotaPreferencesResponse
from google.cloud.cloudquotas_v1.types.cloudquotas import UpdateQuotaPreferenceRequest
from google.cloud.cloudquotas_v1.types.resources import DimensionsInfo
from google.cloud.cloudquotas_v1.types.resources import QuotaConfig
from google.cloud.cloudquotas_v1.types.resources import QuotaDetails
from google.cloud.cloudquotas_v1.types.resources import QuotaIncreaseEligibility
from google.cloud.cloudquotas_v1.types.resources import QuotaInfo
from google.cloud.cloudquotas_v1.types.resources import QuotaPreference
from google.cloud.cloudquotas_v1.types.resources import RolloutInfo
from google.cloud.cloudquotas_v1.types.resources import QuotaSafetyCheck

__all__ = ('CloudQuotasClient',
    'CloudQuotasAsyncClient',
    'CreateQuotaPreferenceRequest',
    'GetQuotaInfoRequest',
    'GetQuotaPreferenceRequest',
    'ListQuotaInfosRequest',
    'ListQuotaInfosResponse',
    'ListQuotaPreferencesRequest',
    'ListQuotaPreferencesResponse',
    'UpdateQuotaPreferenceRequest',
    'DimensionsInfo',
    'QuotaConfig',
    'QuotaDetails',
    'QuotaIncreaseEligibility',
    'QuotaInfo',
    'QuotaPreference',
    'RolloutInfo',
    'QuotaSafetyCheck',
)
