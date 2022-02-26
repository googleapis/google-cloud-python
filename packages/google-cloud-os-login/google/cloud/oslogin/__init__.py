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

from google.cloud.oslogin_v1.services.os_login_service.client import (
    OsLoginServiceClient,
)
from google.cloud.oslogin_v1.services.os_login_service.async_client import (
    OsLoginServiceAsyncClient,
)

from google.cloud.oslogin_v1.types.oslogin import DeletePosixAccountRequest
from google.cloud.oslogin_v1.types.oslogin import DeleteSshPublicKeyRequest
from google.cloud.oslogin_v1.types.oslogin import GetLoginProfileRequest
from google.cloud.oslogin_v1.types.oslogin import GetSshPublicKeyRequest
from google.cloud.oslogin_v1.types.oslogin import ImportSshPublicKeyRequest
from google.cloud.oslogin_v1.types.oslogin import ImportSshPublicKeyResponse
from google.cloud.oslogin_v1.types.oslogin import LoginProfile
from google.cloud.oslogin_v1.types.oslogin import UpdateSshPublicKeyRequest

__all__ = (
    "OsLoginServiceClient",
    "OsLoginServiceAsyncClient",
    "DeletePosixAccountRequest",
    "DeleteSshPublicKeyRequest",
    "GetLoginProfileRequest",
    "GetSshPublicKeyRequest",
    "ImportSshPublicKeyRequest",
    "ImportSshPublicKeyResponse",
    "LoginProfile",
    "UpdateSshPublicKeyRequest",
)
