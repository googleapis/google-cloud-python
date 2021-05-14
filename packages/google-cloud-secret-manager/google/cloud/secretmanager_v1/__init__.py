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

from .services.secret_manager_service import SecretManagerServiceClient
from .services.secret_manager_service import SecretManagerServiceAsyncClient

from .types.resources import CustomerManagedEncryption
from .types.resources import CustomerManagedEncryptionStatus
from .types.resources import Replication
from .types.resources import ReplicationStatus
from .types.resources import Rotation
from .types.resources import Secret
from .types.resources import SecretPayload
from .types.resources import SecretVersion
from .types.resources import Topic
from .types.service import AccessSecretVersionRequest
from .types.service import AccessSecretVersionResponse
from .types.service import AddSecretVersionRequest
from .types.service import CreateSecretRequest
from .types.service import DeleteSecretRequest
from .types.service import DestroySecretVersionRequest
from .types.service import DisableSecretVersionRequest
from .types.service import EnableSecretVersionRequest
from .types.service import GetSecretRequest
from .types.service import GetSecretVersionRequest
from .types.service import ListSecretsRequest
from .types.service import ListSecretsResponse
from .types.service import ListSecretVersionsRequest
from .types.service import ListSecretVersionsResponse
from .types.service import UpdateSecretRequest

__all__ = (
    "SecretManagerServiceAsyncClient",
    "AccessSecretVersionRequest",
    "AccessSecretVersionResponse",
    "AddSecretVersionRequest",
    "CreateSecretRequest",
    "CustomerManagedEncryption",
    "CustomerManagedEncryptionStatus",
    "DeleteSecretRequest",
    "DestroySecretVersionRequest",
    "DisableSecretVersionRequest",
    "EnableSecretVersionRequest",
    "GetSecretRequest",
    "GetSecretVersionRequest",
    "ListSecretVersionsRequest",
    "ListSecretVersionsResponse",
    "ListSecretsRequest",
    "ListSecretsResponse",
    "Replication",
    "ReplicationStatus",
    "Rotation",
    "Secret",
    "SecretManagerServiceClient",
    "SecretPayload",
    "SecretVersion",
    "Topic",
    "UpdateSecretRequest",
)
