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
from google.api.cloudquotas import gapic_version as package_version

__version__ = package_version.__version__


from google.api.cloudquotas_v1beta.services.cloud_quotas.client import CloudQuotasClient
from google.api.cloudquotas_v1beta.services.cloud_quotas.async_client import CloudQuotasAsyncClient
from google.api.cloudquotas_v1beta.services.quota_adjuster_settings_manager.client import QuotaAdjusterSettingsManagerClient
from google.api.cloudquotas_v1beta.services.quota_adjuster_settings_manager.async_client import QuotaAdjusterSettingsManagerAsyncClient

from google.api.cloudquotas_v1beta.types.cloudquotas import CreateQuotaPreferenceRequest
from google.api.cloudquotas_v1beta.types.cloudquotas import GetQuotaInfoRequest
from google.api.cloudquotas_v1beta.types.cloudquotas import GetQuotaPreferenceRequest
from google.api.cloudquotas_v1beta.types.cloudquotas import ListQuotaInfosRequest
from google.api.cloudquotas_v1beta.types.cloudquotas import ListQuotaInfosResponse
from google.api.cloudquotas_v1beta.types.cloudquotas import ListQuotaPreferencesRequest
from google.api.cloudquotas_v1beta.types.cloudquotas import ListQuotaPreferencesResponse
from google.api.cloudquotas_v1beta.types.cloudquotas import UpdateQuotaPreferenceRequest
from google.api.cloudquotas_v1beta.types.quota_adjuster_settings import GetQuotaAdjusterSettingsRequest
from google.api.cloudquotas_v1beta.types.quota_adjuster_settings import QuotaAdjusterSettings
from google.api.cloudquotas_v1beta.types.quota_adjuster_settings import UpdateQuotaAdjusterSettingsRequest
from google.api.cloudquotas_v1beta.types.resources import DimensionsInfo
from google.api.cloudquotas_v1beta.types.resources import QuotaConfig
from google.api.cloudquotas_v1beta.types.resources import QuotaDetails
from google.api.cloudquotas_v1beta.types.resources import QuotaIncreaseEligibility
from google.api.cloudquotas_v1beta.types.resources import QuotaInfo
from google.api.cloudquotas_v1beta.types.resources import QuotaPreference
from google.api.cloudquotas_v1beta.types.resources import RolloutInfo
from google.api.cloudquotas_v1beta.types.resources import QuotaSafetyCheck

__all__ = ('CloudQuotasClient',
    'CloudQuotasAsyncClient',
    'QuotaAdjusterSettingsManagerClient',
    'QuotaAdjusterSettingsManagerAsyncClient',
    'CreateQuotaPreferenceRequest',
    'GetQuotaInfoRequest',
    'GetQuotaPreferenceRequest',
    'ListQuotaInfosRequest',
    'ListQuotaInfosResponse',
    'ListQuotaPreferencesRequest',
    'ListQuotaPreferencesResponse',
    'UpdateQuotaPreferenceRequest',
    'GetQuotaAdjusterSettingsRequest',
    'QuotaAdjusterSettings',
    'UpdateQuotaAdjusterSettingsRequest',
    'DimensionsInfo',
    'QuotaConfig',
    'QuotaDetails',
    'QuotaIncreaseEligibility',
    'QuotaInfo',
    'QuotaPreference',
    'RolloutInfo',
    'QuotaSafetyCheck',
)
