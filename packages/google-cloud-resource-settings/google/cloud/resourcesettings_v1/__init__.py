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

from .services.resource_settings_service import ResourceSettingsServiceClient
from .types.resource_settings import CreateSettingValueRequest
from .types.resource_settings import DeleteSettingValueRequest
from .types.resource_settings import GetSettingValueRequest
from .types.resource_settings import ListSettingsRequest
from .types.resource_settings import ListSettingsResponse
from .types.resource_settings import LookupEffectiveSettingValueRequest
from .types.resource_settings import SearchSettingValuesRequest
from .types.resource_settings import SearchSettingValuesResponse
from .types.resource_settings import Setting
from .types.resource_settings import SettingValue
from .types.resource_settings import UpdateSettingValueRequest
from .types.resource_settings import Value


__all__ = (
    "CreateSettingValueRequest",
    "DeleteSettingValueRequest",
    "GetSettingValueRequest",
    "ListSettingsRequest",
    "ListSettingsResponse",
    "LookupEffectiveSettingValueRequest",
    "SearchSettingValuesRequest",
    "SearchSettingValuesResponse",
    "Setting",
    "SettingValue",
    "UpdateSettingValueRequest",
    "Value",
    "ResourceSettingsServiceClient",
)
