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
from google.cloud.resourcesettings_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.resource_settings_service import ResourceSettingsServiceClient
from .services.resource_settings_service import ResourceSettingsServiceAsyncClient

from .types.resource_settings import GetSettingRequest
from .types.resource_settings import ListSettingsRequest
from .types.resource_settings import ListSettingsResponse
from .types.resource_settings import Setting
from .types.resource_settings import SettingMetadata
from .types.resource_settings import UpdateSettingRequest
from .types.resource_settings import Value
from .types.resource_settings import SettingView

__all__ = (
    'ResourceSettingsServiceAsyncClient',
'GetSettingRequest',
'ListSettingsRequest',
'ListSettingsResponse',
'ResourceSettingsServiceClient',
'Setting',
'SettingMetadata',
'SettingView',
'UpdateSettingRequest',
'Value',
)
