# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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


from .services.api_keys import ApiKeysAsyncClient, ApiKeysClient
from .types.apikeys import (
    CreateKeyRequest,
    DeleteKeyRequest,
    GetKeyRequest,
    GetKeyStringRequest,
    GetKeyStringResponse,
    ListKeysRequest,
    ListKeysResponse,
    LookupKeyRequest,
    LookupKeyResponse,
    UndeleteKeyRequest,
    UpdateKeyRequest,
)
from .types.resources import (
    AndroidApplication,
    AndroidKeyRestrictions,
    ApiTarget,
    BrowserKeyRestrictions,
    IosKeyRestrictions,
    Key,
    Restrictions,
    ServerKeyRestrictions,
)

__all__ = (
    "ApiKeysAsyncClient",
    "AndroidApplication",
    "AndroidKeyRestrictions",
    "ApiKeysClient",
    "ApiTarget",
    "BrowserKeyRestrictions",
    "CreateKeyRequest",
    "DeleteKeyRequest",
    "GetKeyRequest",
    "GetKeyStringRequest",
    "GetKeyStringResponse",
    "IosKeyRestrictions",
    "Key",
    "ListKeysRequest",
    "ListKeysResponse",
    "LookupKeyRequest",
    "LookupKeyResponse",
    "Restrictions",
    "ServerKeyRestrictions",
    "UndeleteKeyRequest",
    "UpdateKeyRequest",
)
