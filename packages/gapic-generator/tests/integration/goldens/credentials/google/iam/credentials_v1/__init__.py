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

from .services.iam_credentials import IAMCredentialsClient
from .services.iam_credentials import IAMCredentialsAsyncClient

from .types.common import GenerateAccessTokenRequest
from .types.common import GenerateAccessTokenResponse
from .types.common import GenerateIdTokenRequest
from .types.common import GenerateIdTokenResponse
from .types.common import SignBlobRequest
from .types.common import SignBlobResponse
from .types.common import SignJwtRequest
from .types.common import SignJwtResponse

__all__ = (
    'IAMCredentialsAsyncClient',
'GenerateAccessTokenRequest',
'GenerateAccessTokenResponse',
'GenerateIdTokenRequest',
'GenerateIdTokenResponse',
'IAMCredentialsClient',
'SignBlobRequest',
'SignBlobResponse',
'SignJwtRequest',
'SignJwtResponse',
)
