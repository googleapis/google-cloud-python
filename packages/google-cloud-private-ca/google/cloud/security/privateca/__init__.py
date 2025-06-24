# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from google.cloud.security.privateca import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.security.privateca_v1.services.certificate_authority_service.async_client import (
    CertificateAuthorityServiceAsyncClient,
)
from google.cloud.security.privateca_v1.services.certificate_authority_service.client import (
    CertificateAuthorityServiceClient,
)
from google.cloud.security.privateca_v1.types.resources import (
    CaPool,
    Certificate,
    CertificateAuthority,
    CertificateConfig,
    CertificateDescription,
    CertificateExtensionConstraints,
    CertificateIdentityConstraints,
    CertificateRevocationList,
    CertificateTemplate,
    KeyUsage,
    ObjectId,
    PublicKey,
    RevocationReason,
    Subject,
    SubjectAltNames,
    SubjectRequestMode,
    SubordinateConfig,
    X509Extension,
    X509Parameters,
)
from google.cloud.security.privateca_v1.types.service import (
    ActivateCertificateAuthorityRequest,
    CreateCaPoolRequest,
    CreateCertificateAuthorityRequest,
    CreateCertificateRequest,
    CreateCertificateTemplateRequest,
    DeleteCaPoolRequest,
    DeleteCertificateAuthorityRequest,
    DeleteCertificateTemplateRequest,
    DisableCertificateAuthorityRequest,
    EnableCertificateAuthorityRequest,
    FetchCaCertsRequest,
    FetchCaCertsResponse,
    FetchCertificateAuthorityCsrRequest,
    FetchCertificateAuthorityCsrResponse,
    GetCaPoolRequest,
    GetCertificateAuthorityRequest,
    GetCertificateRequest,
    GetCertificateRevocationListRequest,
    GetCertificateTemplateRequest,
    ListCaPoolsRequest,
    ListCaPoolsResponse,
    ListCertificateAuthoritiesRequest,
    ListCertificateAuthoritiesResponse,
    ListCertificateRevocationListsRequest,
    ListCertificateRevocationListsResponse,
    ListCertificatesRequest,
    ListCertificatesResponse,
    ListCertificateTemplatesRequest,
    ListCertificateTemplatesResponse,
    OperationMetadata,
    RevokeCertificateRequest,
    UndeleteCertificateAuthorityRequest,
    UpdateCaPoolRequest,
    UpdateCertificateAuthorityRequest,
    UpdateCertificateRequest,
    UpdateCertificateRevocationListRequest,
    UpdateCertificateTemplateRequest,
)

__all__ = (
    "CertificateAuthorityServiceClient",
    "CertificateAuthorityServiceAsyncClient",
    "CaPool",
    "Certificate",
    "CertificateAuthority",
    "CertificateConfig",
    "CertificateDescription",
    "CertificateExtensionConstraints",
    "CertificateIdentityConstraints",
    "CertificateRevocationList",
    "CertificateTemplate",
    "KeyUsage",
    "ObjectId",
    "PublicKey",
    "Subject",
    "SubjectAltNames",
    "SubordinateConfig",
    "X509Extension",
    "X509Parameters",
    "RevocationReason",
    "SubjectRequestMode",
    "ActivateCertificateAuthorityRequest",
    "CreateCaPoolRequest",
    "CreateCertificateAuthorityRequest",
    "CreateCertificateRequest",
    "CreateCertificateTemplateRequest",
    "DeleteCaPoolRequest",
    "DeleteCertificateAuthorityRequest",
    "DeleteCertificateTemplateRequest",
    "DisableCertificateAuthorityRequest",
    "EnableCertificateAuthorityRequest",
    "FetchCaCertsRequest",
    "FetchCaCertsResponse",
    "FetchCertificateAuthorityCsrRequest",
    "FetchCertificateAuthorityCsrResponse",
    "GetCaPoolRequest",
    "GetCertificateAuthorityRequest",
    "GetCertificateRequest",
    "GetCertificateRevocationListRequest",
    "GetCertificateTemplateRequest",
    "ListCaPoolsRequest",
    "ListCaPoolsResponse",
    "ListCertificateAuthoritiesRequest",
    "ListCertificateAuthoritiesResponse",
    "ListCertificateRevocationListsRequest",
    "ListCertificateRevocationListsResponse",
    "ListCertificatesRequest",
    "ListCertificatesResponse",
    "ListCertificateTemplatesRequest",
    "ListCertificateTemplatesResponse",
    "OperationMetadata",
    "RevokeCertificateRequest",
    "UndeleteCertificateAuthorityRequest",
    "UpdateCaPoolRequest",
    "UpdateCertificateAuthorityRequest",
    "UpdateCertificateRequest",
    "UpdateCertificateRevocationListRequest",
    "UpdateCertificateTemplateRequest",
)
