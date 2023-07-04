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
from google.cloud.api_keys_v2 import gapic_version as package_version

__version__ = package_version.__version__


from .services.api_keys import ApiKeysClient
from .services.api_keys import ApiKeysAsyncClient

from .types.apikeys import CreateKeyRequest
from .types.apikeys import DeleteKeyRequest
from .types.apikeys import GetKeyRequest
from .types.apikeys import GetKeyStringRequest
from .types.apikeys import GetKeyStringResponse
from .types.apikeys import ListKeysRequest
from .types.apikeys import ListKeysResponse
from .types.apikeys import LookupKeyRequest
from .types.apikeys import LookupKeyResponse
from .types.apikeys import UndeleteKeyRequest
from .types.apikeys import UpdateKeyRequest
from .types.resources import AndroidApplication
from .types.resources import AndroidKeyRestrictions
from .types.resources import ApiTarget
from .types.resources import BrowserKeyRestrictions
from .types.resources import IosKeyRestrictions
from .types.resources import Key
from .types.resources import Restrictions
from .types.resources import ServerKeyRestrictions

__all__ = (
    'ApiKeysAsyncClient',
'AndroidApplication',
'AndroidKeyRestrictions',
'ApiKeysClient',
'ApiTarget',
'BrowserKeyRestrictions',
'CreateKeyRequest',
'DeleteKeyRequest',
'GetKeyRequest',
'GetKeyStringRequest',
'GetKeyStringResponse',
'IosKeyRestrictions',
'Key',
'ListKeysRequest',
'ListKeysResponse',
'LookupKeyRequest',
'LookupKeyResponse',
'Restrictions',
'ServerKeyRestrictions',
'UndeleteKeyRequest',
'UpdateKeyRequest',
)
