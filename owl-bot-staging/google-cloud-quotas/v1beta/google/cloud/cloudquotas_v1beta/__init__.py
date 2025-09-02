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
from google.cloud.cloudquotas_v1beta import gapic_version as package_version

__version__ = package_version.__version__


from .services.cloud_quotas import CloudQuotasClient
from .services.cloud_quotas import CloudQuotasAsyncClient
from .services.quota_adjuster_settings_manager import QuotaAdjusterSettingsManagerClient
from .services.quota_adjuster_settings_manager import QuotaAdjusterSettingsManagerAsyncClient

from .types.cloudquotas import CreateQuotaPreferenceRequest
from .types.cloudquotas import GetQuotaInfoRequest
from .types.cloudquotas import GetQuotaPreferenceRequest
from .types.cloudquotas import ListQuotaInfosRequest
from .types.cloudquotas import ListQuotaInfosResponse
from .types.cloudquotas import ListQuotaPreferencesRequest
from .types.cloudquotas import ListQuotaPreferencesResponse
from .types.cloudquotas import UpdateQuotaPreferenceRequest
from .types.quota_adjuster_settings import GetQuotaAdjusterSettingsRequest
from .types.quota_adjuster_settings import QuotaAdjusterSettings
from .types.quota_adjuster_settings import UpdateQuotaAdjusterSettingsRequest
from .types.resources import DimensionsInfo
from .types.resources import QuotaConfig
from .types.resources import QuotaDetails
from .types.resources import QuotaIncreaseEligibility
from .types.resources import QuotaInfo
from .types.resources import QuotaPreference
from .types.resources import RolloutInfo
from .types.resources import QuotaSafetyCheck

__all__ = (
    'CloudQuotasAsyncClient',
    'QuotaAdjusterSettingsManagerAsyncClient',
'CloudQuotasClient',
'CreateQuotaPreferenceRequest',
'DimensionsInfo',
'GetQuotaAdjusterSettingsRequest',
'GetQuotaInfoRequest',
'GetQuotaPreferenceRequest',
'ListQuotaInfosRequest',
'ListQuotaInfosResponse',
'ListQuotaPreferencesRequest',
'ListQuotaPreferencesResponse',
'QuotaAdjusterSettings',
'QuotaAdjusterSettingsManagerClient',
'QuotaConfig',
'QuotaDetails',
'QuotaIncreaseEligibility',
'QuotaInfo',
'QuotaPreference',
'QuotaSafetyCheck',
'RolloutInfo',
'UpdateQuotaAdjusterSettingsRequest',
'UpdateQuotaPreferenceRequest',
)
