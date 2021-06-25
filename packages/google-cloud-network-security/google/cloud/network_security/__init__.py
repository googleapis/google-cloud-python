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

from google.cloud.network_security_v1beta1.services.network_security.client import (
    NetworkSecurityClient,
)
from google.cloud.network_security_v1beta1.services.network_security.async_client import (
    NetworkSecurityAsyncClient,
)

from google.cloud.network_security_v1beta1.types.authorization_policy import (
    AuthorizationPolicy,
)
from google.cloud.network_security_v1beta1.types.authorization_policy import (
    CreateAuthorizationPolicyRequest,
)
from google.cloud.network_security_v1beta1.types.authorization_policy import (
    DeleteAuthorizationPolicyRequest,
)
from google.cloud.network_security_v1beta1.types.authorization_policy import (
    GetAuthorizationPolicyRequest,
)
from google.cloud.network_security_v1beta1.types.authorization_policy import (
    ListAuthorizationPoliciesRequest,
)
from google.cloud.network_security_v1beta1.types.authorization_policy import (
    ListAuthorizationPoliciesResponse,
)
from google.cloud.network_security_v1beta1.types.authorization_policy import (
    UpdateAuthorizationPolicyRequest,
)
from google.cloud.network_security_v1beta1.types.client_tls_policy import (
    ClientTlsPolicy,
)
from google.cloud.network_security_v1beta1.types.client_tls_policy import (
    CreateClientTlsPolicyRequest,
)
from google.cloud.network_security_v1beta1.types.client_tls_policy import (
    DeleteClientTlsPolicyRequest,
)
from google.cloud.network_security_v1beta1.types.client_tls_policy import (
    GetClientTlsPolicyRequest,
)
from google.cloud.network_security_v1beta1.types.client_tls_policy import (
    ListClientTlsPoliciesRequest,
)
from google.cloud.network_security_v1beta1.types.client_tls_policy import (
    ListClientTlsPoliciesResponse,
)
from google.cloud.network_security_v1beta1.types.client_tls_policy import (
    UpdateClientTlsPolicyRequest,
)
from google.cloud.network_security_v1beta1.types.common import OperationMetadata
from google.cloud.network_security_v1beta1.types.server_tls_policy import (
    CreateServerTlsPolicyRequest,
)
from google.cloud.network_security_v1beta1.types.server_tls_policy import (
    DeleteServerTlsPolicyRequest,
)
from google.cloud.network_security_v1beta1.types.server_tls_policy import (
    GetServerTlsPolicyRequest,
)
from google.cloud.network_security_v1beta1.types.server_tls_policy import (
    ListServerTlsPoliciesRequest,
)
from google.cloud.network_security_v1beta1.types.server_tls_policy import (
    ListServerTlsPoliciesResponse,
)
from google.cloud.network_security_v1beta1.types.server_tls_policy import (
    ServerTlsPolicy,
)
from google.cloud.network_security_v1beta1.types.server_tls_policy import (
    UpdateServerTlsPolicyRequest,
)
from google.cloud.network_security_v1beta1.types.tls import CertificateProvider
from google.cloud.network_security_v1beta1.types.tls import CertificateProviderInstance
from google.cloud.network_security_v1beta1.types.tls import GrpcEndpoint
from google.cloud.network_security_v1beta1.types.tls import ValidationCA

__all__ = (
    "NetworkSecurityClient",
    "NetworkSecurityAsyncClient",
    "AuthorizationPolicy",
    "CreateAuthorizationPolicyRequest",
    "DeleteAuthorizationPolicyRequest",
    "GetAuthorizationPolicyRequest",
    "ListAuthorizationPoliciesRequest",
    "ListAuthorizationPoliciesResponse",
    "UpdateAuthorizationPolicyRequest",
    "ClientTlsPolicy",
    "CreateClientTlsPolicyRequest",
    "DeleteClientTlsPolicyRequest",
    "GetClientTlsPolicyRequest",
    "ListClientTlsPoliciesRequest",
    "ListClientTlsPoliciesResponse",
    "UpdateClientTlsPolicyRequest",
    "OperationMetadata",
    "CreateServerTlsPolicyRequest",
    "DeleteServerTlsPolicyRequest",
    "GetServerTlsPolicyRequest",
    "ListServerTlsPoliciesRequest",
    "ListServerTlsPoliciesResponse",
    "ServerTlsPolicy",
    "UpdateServerTlsPolicyRequest",
    "CertificateProvider",
    "CertificateProviderInstance",
    "GrpcEndpoint",
    "ValidationCA",
)
