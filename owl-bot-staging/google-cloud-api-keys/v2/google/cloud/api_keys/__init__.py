# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from google.cloud.api_keys import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.api_keys_v2.services.api_keys.client import ApiKeysClient
from google.cloud.api_keys_v2.services.api_keys.async_client import ApiKeysAsyncClient

from google.cloud.api_keys_v2.types.apikeys import CreateKeyRequest
from google.cloud.api_keys_v2.types.apikeys import DeleteKeyRequest
from google.cloud.api_keys_v2.types.apikeys import GetKeyRequest
from google.cloud.api_keys_v2.types.apikeys import GetKeyStringRequest
from google.cloud.api_keys_v2.types.apikeys import GetKeyStringResponse
from google.cloud.api_keys_v2.types.apikeys import ListKeysRequest
from google.cloud.api_keys_v2.types.apikeys import ListKeysResponse
from google.cloud.api_keys_v2.types.apikeys import LookupKeyRequest
from google.cloud.api_keys_v2.types.apikeys import LookupKeyResponse
from google.cloud.api_keys_v2.types.apikeys import UndeleteKeyRequest
from google.cloud.api_keys_v2.types.apikeys import UpdateKeyRequest
from google.cloud.api_keys_v2.types.resources import AndroidApplication
from google.cloud.api_keys_v2.types.resources import AndroidKeyRestrictions
from google.cloud.api_keys_v2.types.resources import ApiTarget
from google.cloud.api_keys_v2.types.resources import BrowserKeyRestrictions
from google.cloud.api_keys_v2.types.resources import IosKeyRestrictions
from google.cloud.api_keys_v2.types.resources import Key
from google.cloud.api_keys_v2.types.resources import Restrictions
from google.cloud.api_keys_v2.types.resources import ServerKeyRestrictions

__all__ = ('ApiKeysClient',
    'ApiKeysAsyncClient',
    'CreateKeyRequest',
    'DeleteKeyRequest',
    'GetKeyRequest',
    'GetKeyStringRequest',
    'GetKeyStringResponse',
    'ListKeysRequest',
    'ListKeysResponse',
    'LookupKeyRequest',
    'LookupKeyResponse',
    'UndeleteKeyRequest',
    'UpdateKeyRequest',
    'AndroidApplication',
    'AndroidKeyRestrictions',
    'ApiTarget',
    'BrowserKeyRestrictions',
    'IosKeyRestrictions',
    'Key',
    'Restrictions',
    'ServerKeyRestrictions',
)
