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

from google.cloud.secretmanager_v1.services.secret_manager_service.client import (
    SecretManagerServiceClient,
)
from google.cloud.secretmanager_v1.services.secret_manager_service.async_client import (
    SecretManagerServiceAsyncClient,
)

from google.cloud.secretmanager_v1.types.resources import CustomerManagedEncryption
from google.cloud.secretmanager_v1.types.resources import (
    CustomerManagedEncryptionStatus,
)
from google.cloud.secretmanager_v1.types.resources import Replication
from google.cloud.secretmanager_v1.types.resources import ReplicationStatus
from google.cloud.secretmanager_v1.types.resources import Rotation
from google.cloud.secretmanager_v1.types.resources import Secret
from google.cloud.secretmanager_v1.types.resources import SecretPayload
from google.cloud.secretmanager_v1.types.resources import SecretVersion
from google.cloud.secretmanager_v1.types.resources import Topic
from google.cloud.secretmanager_v1.types.service import AccessSecretVersionRequest
from google.cloud.secretmanager_v1.types.service import AccessSecretVersionResponse
from google.cloud.secretmanager_v1.types.service import AddSecretVersionRequest
from google.cloud.secretmanager_v1.types.service import CreateSecretRequest
from google.cloud.secretmanager_v1.types.service import DeleteSecretRequest
from google.cloud.secretmanager_v1.types.service import DestroySecretVersionRequest
from google.cloud.secretmanager_v1.types.service import DisableSecretVersionRequest
from google.cloud.secretmanager_v1.types.service import EnableSecretVersionRequest
from google.cloud.secretmanager_v1.types.service import GetSecretRequest
from google.cloud.secretmanager_v1.types.service import GetSecretVersionRequest
from google.cloud.secretmanager_v1.types.service import ListSecretsRequest
from google.cloud.secretmanager_v1.types.service import ListSecretsResponse
from google.cloud.secretmanager_v1.types.service import ListSecretVersionsRequest
from google.cloud.secretmanager_v1.types.service import ListSecretVersionsResponse
from google.cloud.secretmanager_v1.types.service import UpdateSecretRequest

__all__ = (
    "SecretManagerServiceClient",
    "SecretManagerServiceAsyncClient",
    "CustomerManagedEncryption",
    "CustomerManagedEncryptionStatus",
    "Replication",
    "ReplicationStatus",
    "Rotation",
    "Secret",
    "SecretPayload",
    "SecretVersion",
    "Topic",
    "AccessSecretVersionRequest",
    "AccessSecretVersionResponse",
    "AddSecretVersionRequest",
    "CreateSecretRequest",
    "DeleteSecretRequest",
    "DestroySecretVersionRequest",
    "DisableSecretVersionRequest",
    "EnableSecretVersionRequest",
    "GetSecretRequest",
    "GetSecretVersionRequest",
    "ListSecretsRequest",
    "ListSecretsResponse",
    "ListSecretVersionsRequest",
    "ListSecretVersionsResponse",
    "UpdateSecretRequest",
)
