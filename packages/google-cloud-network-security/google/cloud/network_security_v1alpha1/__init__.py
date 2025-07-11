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
from google.cloud.network_security_v1alpha1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.network_security import NetworkSecurityAsyncClient, NetworkSecurityClient
from .types.client_tls_policy import (
    ClientTlsPolicy,
    CreateClientTlsPolicyRequest,
    DeleteClientTlsPolicyRequest,
    GetClientTlsPolicyRequest,
    ListClientTlsPoliciesRequest,
    ListClientTlsPoliciesResponse,
    UpdateClientTlsPolicyRequest,
)
from .types.common import OperationMetadata
from .types.tls import (
    CertificateProvider,
    CertificateProviderInstance,
    GrpcEndpoint,
    ValidationCA,
)

__all__ = (
    "NetworkSecurityAsyncClient",
    "CertificateProvider",
    "CertificateProviderInstance",
    "ClientTlsPolicy",
    "CreateClientTlsPolicyRequest",
    "DeleteClientTlsPolicyRequest",
    "GetClientTlsPolicyRequest",
    "GrpcEndpoint",
    "ListClientTlsPoliciesRequest",
    "ListClientTlsPoliciesResponse",
    "NetworkSecurityClient",
    "OperationMetadata",
    "UpdateClientTlsPolicyRequest",
    "ValidationCA",
)
