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
from google.cloud.networksecurity import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.networksecurity_v1alpha1.services.network_security.async_client import (
    NetworkSecurityAsyncClient,
)
from google.cloud.networksecurity_v1alpha1.services.network_security.client import (
    NetworkSecurityClient,
)
from google.cloud.networksecurity_v1alpha1.types.client_tls_policy import (
    ClientTlsPolicy,
    CreateClientTlsPolicyRequest,
    DeleteClientTlsPolicyRequest,
    GetClientTlsPolicyRequest,
    ListClientTlsPoliciesRequest,
    ListClientTlsPoliciesResponse,
    UpdateClientTlsPolicyRequest,
)
from google.cloud.networksecurity_v1alpha1.types.common import OperationMetadata
from google.cloud.networksecurity_v1alpha1.types.tls import (
    CertificateProvider,
    CertificateProviderInstance,
    GrpcEndpoint,
    ValidationCA,
)

__all__ = (
    "NetworkSecurityClient",
    "NetworkSecurityAsyncClient",
    "ClientTlsPolicy",
    "CreateClientTlsPolicyRequest",
    "DeleteClientTlsPolicyRequest",
    "GetClientTlsPolicyRequest",
    "ListClientTlsPoliciesRequest",
    "ListClientTlsPoliciesResponse",
    "UpdateClientTlsPolicyRequest",
    "OperationMetadata",
    "CertificateProvider",
    "CertificateProviderInstance",
    "GrpcEndpoint",
    "ValidationCA",
)
