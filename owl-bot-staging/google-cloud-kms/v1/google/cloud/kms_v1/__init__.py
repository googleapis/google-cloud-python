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
from google.cloud.kms_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.autokey import AutokeyClient
from .services.autokey import AutokeyAsyncClient
from .services.autokey_admin import AutokeyAdminClient
from .services.autokey_admin import AutokeyAdminAsyncClient
from .services.ekm_service import EkmServiceClient
from .services.ekm_service import EkmServiceAsyncClient
from .services.key_management_service import KeyManagementServiceClient
from .services.key_management_service import KeyManagementServiceAsyncClient

from .types.autokey import CreateKeyHandleMetadata
from .types.autokey import CreateKeyHandleRequest
from .types.autokey import GetKeyHandleRequest
from .types.autokey import KeyHandle
from .types.autokey import ListKeyHandlesRequest
from .types.autokey import ListKeyHandlesResponse
from .types.autokey_admin import AutokeyConfig
from .types.autokey_admin import GetAutokeyConfigRequest
from .types.autokey_admin import ShowEffectiveAutokeyConfigRequest
from .types.autokey_admin import ShowEffectiveAutokeyConfigResponse
from .types.autokey_admin import UpdateAutokeyConfigRequest
from .types.ekm_service import Certificate
from .types.ekm_service import CreateEkmConnectionRequest
from .types.ekm_service import EkmConfig
from .types.ekm_service import EkmConnection
from .types.ekm_service import GetEkmConfigRequest
from .types.ekm_service import GetEkmConnectionRequest
from .types.ekm_service import ListEkmConnectionsRequest
from .types.ekm_service import ListEkmConnectionsResponse
from .types.ekm_service import UpdateEkmConfigRequest
from .types.ekm_service import UpdateEkmConnectionRequest
from .types.ekm_service import VerifyConnectivityRequest
from .types.ekm_service import VerifyConnectivityResponse
from .types.resources import CryptoKey
from .types.resources import CryptoKeyVersion
from .types.resources import CryptoKeyVersionTemplate
from .types.resources import ExternalProtectionLevelOptions
from .types.resources import ImportJob
from .types.resources import KeyAccessJustificationsPolicy
from .types.resources import KeyOperationAttestation
from .types.resources import KeyRing
from .types.resources import PublicKey
from .types.resources import AccessReason
from .types.resources import ProtectionLevel
from .types.service import AsymmetricDecryptRequest
from .types.service import AsymmetricDecryptResponse
from .types.service import AsymmetricSignRequest
from .types.service import AsymmetricSignResponse
from .types.service import CreateCryptoKeyRequest
from .types.service import CreateCryptoKeyVersionRequest
from .types.service import CreateImportJobRequest
from .types.service import CreateKeyRingRequest
from .types.service import DecryptRequest
from .types.service import DecryptResponse
from .types.service import DestroyCryptoKeyVersionRequest
from .types.service import Digest
from .types.service import EncryptRequest
from .types.service import EncryptResponse
from .types.service import GenerateRandomBytesRequest
from .types.service import GenerateRandomBytesResponse
from .types.service import GetCryptoKeyRequest
from .types.service import GetCryptoKeyVersionRequest
from .types.service import GetImportJobRequest
from .types.service import GetKeyRingRequest
from .types.service import GetPublicKeyRequest
from .types.service import ImportCryptoKeyVersionRequest
from .types.service import ListCryptoKeysRequest
from .types.service import ListCryptoKeysResponse
from .types.service import ListCryptoKeyVersionsRequest
from .types.service import ListCryptoKeyVersionsResponse
from .types.service import ListImportJobsRequest
from .types.service import ListImportJobsResponse
from .types.service import ListKeyRingsRequest
from .types.service import ListKeyRingsResponse
from .types.service import LocationMetadata
from .types.service import MacSignRequest
from .types.service import MacSignResponse
from .types.service import MacVerifyRequest
from .types.service import MacVerifyResponse
from .types.service import RawDecryptRequest
from .types.service import RawDecryptResponse
from .types.service import RawEncryptRequest
from .types.service import RawEncryptResponse
from .types.service import RestoreCryptoKeyVersionRequest
from .types.service import UpdateCryptoKeyPrimaryVersionRequest
from .types.service import UpdateCryptoKeyRequest
from .types.service import UpdateCryptoKeyVersionRequest

__all__ = (
    'AutokeyAdminAsyncClient',
    'AutokeyAsyncClient',
    'EkmServiceAsyncClient',
    'KeyManagementServiceAsyncClient',
'AccessReason',
'AsymmetricDecryptRequest',
'AsymmetricDecryptResponse',
'AsymmetricSignRequest',
'AsymmetricSignResponse',
'AutokeyAdminClient',
'AutokeyClient',
'AutokeyConfig',
'Certificate',
'CreateCryptoKeyRequest',
'CreateCryptoKeyVersionRequest',
'CreateEkmConnectionRequest',
'CreateImportJobRequest',
'CreateKeyHandleMetadata',
'CreateKeyHandleRequest',
'CreateKeyRingRequest',
'CryptoKey',
'CryptoKeyVersion',
'CryptoKeyVersionTemplate',
'DecryptRequest',
'DecryptResponse',
'DestroyCryptoKeyVersionRequest',
'Digest',
'EkmConfig',
'EkmConnection',
'EkmServiceClient',
'EncryptRequest',
'EncryptResponse',
'ExternalProtectionLevelOptions',
'GenerateRandomBytesRequest',
'GenerateRandomBytesResponse',
'GetAutokeyConfigRequest',
'GetCryptoKeyRequest',
'GetCryptoKeyVersionRequest',
'GetEkmConfigRequest',
'GetEkmConnectionRequest',
'GetImportJobRequest',
'GetKeyHandleRequest',
'GetKeyRingRequest',
'GetPublicKeyRequest',
'ImportCryptoKeyVersionRequest',
'ImportJob',
'KeyAccessJustificationsPolicy',
'KeyHandle',
'KeyManagementServiceClient',
'KeyOperationAttestation',
'KeyRing',
'ListCryptoKeyVersionsRequest',
'ListCryptoKeyVersionsResponse',
'ListCryptoKeysRequest',
'ListCryptoKeysResponse',
'ListEkmConnectionsRequest',
'ListEkmConnectionsResponse',
'ListImportJobsRequest',
'ListImportJobsResponse',
'ListKeyHandlesRequest',
'ListKeyHandlesResponse',
'ListKeyRingsRequest',
'ListKeyRingsResponse',
'LocationMetadata',
'MacSignRequest',
'MacSignResponse',
'MacVerifyRequest',
'MacVerifyResponse',
'ProtectionLevel',
'PublicKey',
'RawDecryptRequest',
'RawDecryptResponse',
'RawEncryptRequest',
'RawEncryptResponse',
'RestoreCryptoKeyVersionRequest',
'ShowEffectiveAutokeyConfigRequest',
'ShowEffectiveAutokeyConfigResponse',
'UpdateAutokeyConfigRequest',
'UpdateCryptoKeyPrimaryVersionRequest',
'UpdateCryptoKeyRequest',
'UpdateCryptoKeyVersionRequest',
'UpdateEkmConfigRequest',
'UpdateEkmConnectionRequest',
'VerifyConnectivityRequest',
'VerifyConnectivityResponse',
)
