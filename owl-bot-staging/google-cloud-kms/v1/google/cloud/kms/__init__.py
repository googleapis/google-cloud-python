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
from google.cloud.kms import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.kms_v1.services.autokey.client import AutokeyClient
from google.cloud.kms_v1.services.autokey.async_client import AutokeyAsyncClient
from google.cloud.kms_v1.services.autokey_admin.client import AutokeyAdminClient
from google.cloud.kms_v1.services.autokey_admin.async_client import AutokeyAdminAsyncClient
from google.cloud.kms_v1.services.ekm_service.client import EkmServiceClient
from google.cloud.kms_v1.services.ekm_service.async_client import EkmServiceAsyncClient
from google.cloud.kms_v1.services.key_management_service.client import KeyManagementServiceClient
from google.cloud.kms_v1.services.key_management_service.async_client import KeyManagementServiceAsyncClient

from google.cloud.kms_v1.types.autokey import CreateKeyHandleMetadata
from google.cloud.kms_v1.types.autokey import CreateKeyHandleRequest
from google.cloud.kms_v1.types.autokey import GetKeyHandleRequest
from google.cloud.kms_v1.types.autokey import KeyHandle
from google.cloud.kms_v1.types.autokey import ListKeyHandlesRequest
from google.cloud.kms_v1.types.autokey import ListKeyHandlesResponse
from google.cloud.kms_v1.types.autokey_admin import AutokeyConfig
from google.cloud.kms_v1.types.autokey_admin import GetAutokeyConfigRequest
from google.cloud.kms_v1.types.autokey_admin import ShowEffectiveAutokeyConfigRequest
from google.cloud.kms_v1.types.autokey_admin import ShowEffectiveAutokeyConfigResponse
from google.cloud.kms_v1.types.autokey_admin import UpdateAutokeyConfigRequest
from google.cloud.kms_v1.types.ekm_service import Certificate
from google.cloud.kms_v1.types.ekm_service import CreateEkmConnectionRequest
from google.cloud.kms_v1.types.ekm_service import EkmConfig
from google.cloud.kms_v1.types.ekm_service import EkmConnection
from google.cloud.kms_v1.types.ekm_service import GetEkmConfigRequest
from google.cloud.kms_v1.types.ekm_service import GetEkmConnectionRequest
from google.cloud.kms_v1.types.ekm_service import ListEkmConnectionsRequest
from google.cloud.kms_v1.types.ekm_service import ListEkmConnectionsResponse
from google.cloud.kms_v1.types.ekm_service import UpdateEkmConfigRequest
from google.cloud.kms_v1.types.ekm_service import UpdateEkmConnectionRequest
from google.cloud.kms_v1.types.ekm_service import VerifyConnectivityRequest
from google.cloud.kms_v1.types.ekm_service import VerifyConnectivityResponse
from google.cloud.kms_v1.types.resources import CryptoKey
from google.cloud.kms_v1.types.resources import CryptoKeyVersion
from google.cloud.kms_v1.types.resources import CryptoKeyVersionTemplate
from google.cloud.kms_v1.types.resources import ExternalProtectionLevelOptions
from google.cloud.kms_v1.types.resources import ImportJob
from google.cloud.kms_v1.types.resources import KeyAccessJustificationsPolicy
from google.cloud.kms_v1.types.resources import KeyOperationAttestation
from google.cloud.kms_v1.types.resources import KeyRing
from google.cloud.kms_v1.types.resources import PublicKey
from google.cloud.kms_v1.types.resources import AccessReason
from google.cloud.kms_v1.types.resources import ProtectionLevel
from google.cloud.kms_v1.types.service import AsymmetricDecryptRequest
from google.cloud.kms_v1.types.service import AsymmetricDecryptResponse
from google.cloud.kms_v1.types.service import AsymmetricSignRequest
from google.cloud.kms_v1.types.service import AsymmetricSignResponse
from google.cloud.kms_v1.types.service import CreateCryptoKeyRequest
from google.cloud.kms_v1.types.service import CreateCryptoKeyVersionRequest
from google.cloud.kms_v1.types.service import CreateImportJobRequest
from google.cloud.kms_v1.types.service import CreateKeyRingRequest
from google.cloud.kms_v1.types.service import DecryptRequest
from google.cloud.kms_v1.types.service import DecryptResponse
from google.cloud.kms_v1.types.service import DestroyCryptoKeyVersionRequest
from google.cloud.kms_v1.types.service import Digest
from google.cloud.kms_v1.types.service import EncryptRequest
from google.cloud.kms_v1.types.service import EncryptResponse
from google.cloud.kms_v1.types.service import GenerateRandomBytesRequest
from google.cloud.kms_v1.types.service import GenerateRandomBytesResponse
from google.cloud.kms_v1.types.service import GetCryptoKeyRequest
from google.cloud.kms_v1.types.service import GetCryptoKeyVersionRequest
from google.cloud.kms_v1.types.service import GetImportJobRequest
from google.cloud.kms_v1.types.service import GetKeyRingRequest
from google.cloud.kms_v1.types.service import GetPublicKeyRequest
from google.cloud.kms_v1.types.service import ImportCryptoKeyVersionRequest
from google.cloud.kms_v1.types.service import ListCryptoKeysRequest
from google.cloud.kms_v1.types.service import ListCryptoKeysResponse
from google.cloud.kms_v1.types.service import ListCryptoKeyVersionsRequest
from google.cloud.kms_v1.types.service import ListCryptoKeyVersionsResponse
from google.cloud.kms_v1.types.service import ListImportJobsRequest
from google.cloud.kms_v1.types.service import ListImportJobsResponse
from google.cloud.kms_v1.types.service import ListKeyRingsRequest
from google.cloud.kms_v1.types.service import ListKeyRingsResponse
from google.cloud.kms_v1.types.service import LocationMetadata
from google.cloud.kms_v1.types.service import MacSignRequest
from google.cloud.kms_v1.types.service import MacSignResponse
from google.cloud.kms_v1.types.service import MacVerifyRequest
from google.cloud.kms_v1.types.service import MacVerifyResponse
from google.cloud.kms_v1.types.service import RawDecryptRequest
from google.cloud.kms_v1.types.service import RawDecryptResponse
from google.cloud.kms_v1.types.service import RawEncryptRequest
from google.cloud.kms_v1.types.service import RawEncryptResponse
from google.cloud.kms_v1.types.service import RestoreCryptoKeyVersionRequest
from google.cloud.kms_v1.types.service import UpdateCryptoKeyPrimaryVersionRequest
from google.cloud.kms_v1.types.service import UpdateCryptoKeyRequest
from google.cloud.kms_v1.types.service import UpdateCryptoKeyVersionRequest

__all__ = ('AutokeyClient',
    'AutokeyAsyncClient',
    'AutokeyAdminClient',
    'AutokeyAdminAsyncClient',
    'EkmServiceClient',
    'EkmServiceAsyncClient',
    'KeyManagementServiceClient',
    'KeyManagementServiceAsyncClient',
    'CreateKeyHandleMetadata',
    'CreateKeyHandleRequest',
    'GetKeyHandleRequest',
    'KeyHandle',
    'ListKeyHandlesRequest',
    'ListKeyHandlesResponse',
    'AutokeyConfig',
    'GetAutokeyConfigRequest',
    'ShowEffectiveAutokeyConfigRequest',
    'ShowEffectiveAutokeyConfigResponse',
    'UpdateAutokeyConfigRequest',
    'Certificate',
    'CreateEkmConnectionRequest',
    'EkmConfig',
    'EkmConnection',
    'GetEkmConfigRequest',
    'GetEkmConnectionRequest',
    'ListEkmConnectionsRequest',
    'ListEkmConnectionsResponse',
    'UpdateEkmConfigRequest',
    'UpdateEkmConnectionRequest',
    'VerifyConnectivityRequest',
    'VerifyConnectivityResponse',
    'CryptoKey',
    'CryptoKeyVersion',
    'CryptoKeyVersionTemplate',
    'ExternalProtectionLevelOptions',
    'ImportJob',
    'KeyAccessJustificationsPolicy',
    'KeyOperationAttestation',
    'KeyRing',
    'PublicKey',
    'AccessReason',
    'ProtectionLevel',
    'AsymmetricDecryptRequest',
    'AsymmetricDecryptResponse',
    'AsymmetricSignRequest',
    'AsymmetricSignResponse',
    'CreateCryptoKeyRequest',
    'CreateCryptoKeyVersionRequest',
    'CreateImportJobRequest',
    'CreateKeyRingRequest',
    'DecryptRequest',
    'DecryptResponse',
    'DestroyCryptoKeyVersionRequest',
    'Digest',
    'EncryptRequest',
    'EncryptResponse',
    'GenerateRandomBytesRequest',
    'GenerateRandomBytesResponse',
    'GetCryptoKeyRequest',
    'GetCryptoKeyVersionRequest',
    'GetImportJobRequest',
    'GetKeyRingRequest',
    'GetPublicKeyRequest',
    'ImportCryptoKeyVersionRequest',
    'ListCryptoKeysRequest',
    'ListCryptoKeysResponse',
    'ListCryptoKeyVersionsRequest',
    'ListCryptoKeyVersionsResponse',
    'ListImportJobsRequest',
    'ListImportJobsResponse',
    'ListKeyRingsRequest',
    'ListKeyRingsResponse',
    'LocationMetadata',
    'MacSignRequest',
    'MacSignResponse',
    'MacVerifyRequest',
    'MacVerifyResponse',
    'RawDecryptRequest',
    'RawDecryptResponse',
    'RawEncryptRequest',
    'RawEncryptResponse',
    'RestoreCryptoKeyVersionRequest',
    'UpdateCryptoKeyPrimaryVersionRequest',
    'UpdateCryptoKeyRequest',
    'UpdateCryptoKeyVersionRequest',
)
