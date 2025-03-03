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
from google.cloud.certificate_manager import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.certificate_manager_v1.services.certificate_manager.client import CertificateManagerClient
from google.cloud.certificate_manager_v1.services.certificate_manager.async_client import CertificateManagerAsyncClient

from google.cloud.certificate_manager_v1.types.certificate_issuance_config import CertificateIssuanceConfig
from google.cloud.certificate_manager_v1.types.certificate_issuance_config import CreateCertificateIssuanceConfigRequest
from google.cloud.certificate_manager_v1.types.certificate_issuance_config import DeleteCertificateIssuanceConfigRequest
from google.cloud.certificate_manager_v1.types.certificate_issuance_config import GetCertificateIssuanceConfigRequest
from google.cloud.certificate_manager_v1.types.certificate_issuance_config import ListCertificateIssuanceConfigsRequest
from google.cloud.certificate_manager_v1.types.certificate_issuance_config import ListCertificateIssuanceConfigsResponse
from google.cloud.certificate_manager_v1.types.certificate_manager import Certificate
from google.cloud.certificate_manager_v1.types.certificate_manager import CertificateMap
from google.cloud.certificate_manager_v1.types.certificate_manager import CertificateMapEntry
from google.cloud.certificate_manager_v1.types.certificate_manager import CreateCertificateMapEntryRequest
from google.cloud.certificate_manager_v1.types.certificate_manager import CreateCertificateMapRequest
from google.cloud.certificate_manager_v1.types.certificate_manager import CreateCertificateRequest
from google.cloud.certificate_manager_v1.types.certificate_manager import CreateDnsAuthorizationRequest
from google.cloud.certificate_manager_v1.types.certificate_manager import DeleteCertificateMapEntryRequest
from google.cloud.certificate_manager_v1.types.certificate_manager import DeleteCertificateMapRequest
from google.cloud.certificate_manager_v1.types.certificate_manager import DeleteCertificateRequest
from google.cloud.certificate_manager_v1.types.certificate_manager import DeleteDnsAuthorizationRequest
from google.cloud.certificate_manager_v1.types.certificate_manager import DnsAuthorization
from google.cloud.certificate_manager_v1.types.certificate_manager import GetCertificateMapEntryRequest
from google.cloud.certificate_manager_v1.types.certificate_manager import GetCertificateMapRequest
from google.cloud.certificate_manager_v1.types.certificate_manager import GetCertificateRequest
from google.cloud.certificate_manager_v1.types.certificate_manager import GetDnsAuthorizationRequest
from google.cloud.certificate_manager_v1.types.certificate_manager import ListCertificateMapEntriesRequest
from google.cloud.certificate_manager_v1.types.certificate_manager import ListCertificateMapEntriesResponse
from google.cloud.certificate_manager_v1.types.certificate_manager import ListCertificateMapsRequest
from google.cloud.certificate_manager_v1.types.certificate_manager import ListCertificateMapsResponse
from google.cloud.certificate_manager_v1.types.certificate_manager import ListCertificatesRequest
from google.cloud.certificate_manager_v1.types.certificate_manager import ListCertificatesResponse
from google.cloud.certificate_manager_v1.types.certificate_manager import ListDnsAuthorizationsRequest
from google.cloud.certificate_manager_v1.types.certificate_manager import ListDnsAuthorizationsResponse
from google.cloud.certificate_manager_v1.types.certificate_manager import OperationMetadata
from google.cloud.certificate_manager_v1.types.certificate_manager import UpdateCertificateMapEntryRequest
from google.cloud.certificate_manager_v1.types.certificate_manager import UpdateCertificateMapRequest
from google.cloud.certificate_manager_v1.types.certificate_manager import UpdateCertificateRequest
from google.cloud.certificate_manager_v1.types.certificate_manager import UpdateDnsAuthorizationRequest
from google.cloud.certificate_manager_v1.types.certificate_manager import ServingState
from google.cloud.certificate_manager_v1.types.trust_config import CreateTrustConfigRequest
from google.cloud.certificate_manager_v1.types.trust_config import DeleteTrustConfigRequest
from google.cloud.certificate_manager_v1.types.trust_config import GetTrustConfigRequest
from google.cloud.certificate_manager_v1.types.trust_config import ListTrustConfigsRequest
from google.cloud.certificate_manager_v1.types.trust_config import ListTrustConfigsResponse
from google.cloud.certificate_manager_v1.types.trust_config import TrustConfig
from google.cloud.certificate_manager_v1.types.trust_config import UpdateTrustConfigRequest

__all__ = ('CertificateManagerClient',
    'CertificateManagerAsyncClient',
    'CertificateIssuanceConfig',
    'CreateCertificateIssuanceConfigRequest',
    'DeleteCertificateIssuanceConfigRequest',
    'GetCertificateIssuanceConfigRequest',
    'ListCertificateIssuanceConfigsRequest',
    'ListCertificateIssuanceConfigsResponse',
    'Certificate',
    'CertificateMap',
    'CertificateMapEntry',
    'CreateCertificateMapEntryRequest',
    'CreateCertificateMapRequest',
    'CreateCertificateRequest',
    'CreateDnsAuthorizationRequest',
    'DeleteCertificateMapEntryRequest',
    'DeleteCertificateMapRequest',
    'DeleteCertificateRequest',
    'DeleteDnsAuthorizationRequest',
    'DnsAuthorization',
    'GetCertificateMapEntryRequest',
    'GetCertificateMapRequest',
    'GetCertificateRequest',
    'GetDnsAuthorizationRequest',
    'ListCertificateMapEntriesRequest',
    'ListCertificateMapEntriesResponse',
    'ListCertificateMapsRequest',
    'ListCertificateMapsResponse',
    'ListCertificatesRequest',
    'ListCertificatesResponse',
    'ListDnsAuthorizationsRequest',
    'ListDnsAuthorizationsResponse',
    'OperationMetadata',
    'UpdateCertificateMapEntryRequest',
    'UpdateCertificateMapRequest',
    'UpdateCertificateRequest',
    'UpdateDnsAuthorizationRequest',
    'ServingState',
    'CreateTrustConfigRequest',
    'DeleteTrustConfigRequest',
    'GetTrustConfigRequest',
    'ListTrustConfigsRequest',
    'ListTrustConfigsResponse',
    'TrustConfig',
    'UpdateTrustConfigRequest',
)
