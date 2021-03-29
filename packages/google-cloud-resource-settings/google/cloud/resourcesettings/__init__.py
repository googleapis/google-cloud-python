# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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

from google.cloud.resourcesettings_v1.services.resource_settings_service.async_client import (
    ResourceSettingsServiceAsyncClient,
)
from google.cloud.resourcesettings_v1.services.resource_settings_service.client import (
    ResourceSettingsServiceClient,
)
from google.cloud.resourcesettings_v1.types.resource_settings import (
    CreateSettingValueRequest,
)
from google.cloud.resourcesettings_v1.types.resource_settings import (
    DeleteSettingValueRequest,
)
from google.cloud.resourcesettings_v1.types.resource_settings import (
    GetSettingValueRequest,
)
from google.cloud.resourcesettings_v1.types.resource_settings import ListSettingsRequest
from google.cloud.resourcesettings_v1.types.resource_settings import (
    ListSettingsResponse,
)
from google.cloud.resourcesettings_v1.types.resource_settings import (
    LookupEffectiveSettingValueRequest,
)
from google.cloud.resourcesettings_v1.types.resource_settings import (
    SearchSettingValuesRequest,
)
from google.cloud.resourcesettings_v1.types.resource_settings import (
    SearchSettingValuesResponse,
)
from google.cloud.resourcesettings_v1.types.resource_settings import Setting
from google.cloud.resourcesettings_v1.types.resource_settings import SettingValue
from google.cloud.resourcesettings_v1.types.resource_settings import (
    UpdateSettingValueRequest,
)
from google.cloud.resourcesettings_v1.types.resource_settings import Value

__all__ = (
    "CreateSettingValueRequest",
    "DeleteSettingValueRequest",
    "GetSettingValueRequest",
    "ListSettingsRequest",
    "ListSettingsResponse",
    "LookupEffectiveSettingValueRequest",
    "ResourceSettingsServiceAsyncClient",
    "ResourceSettingsServiceClient",
    "SearchSettingValuesRequest",
    "SearchSettingValuesResponse",
    "Setting",
    "SettingValue",
    "UpdateSettingValueRequest",
    "Value",
)
