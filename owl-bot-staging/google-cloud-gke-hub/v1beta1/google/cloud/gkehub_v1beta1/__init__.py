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
from google.cloud.gkehub_v1beta1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.gke_hub_membership_service import GkeHubMembershipServiceClient
from .services.gke_hub_membership_service import GkeHubMembershipServiceAsyncClient

from .types.membership import ApplianceCluster
from .types.membership import Authority
from .types.membership import ConnectAgent
from .types.membership import ConnectAgentResource
from .types.membership import CreateMembershipRequest
from .types.membership import DeleteMembershipRequest
from .types.membership import EdgeCluster
from .types.membership import GenerateConnectManifestRequest
from .types.membership import GenerateConnectManifestResponse
from .types.membership import GenerateExclusivityManifestRequest
from .types.membership import GenerateExclusivityManifestResponse
from .types.membership import GetMembershipRequest
from .types.membership import GkeCluster
from .types.membership import KubernetesMetadata
from .types.membership import KubernetesResource
from .types.membership import ListMembershipsRequest
from .types.membership import ListMembershipsResponse
from .types.membership import Membership
from .types.membership import MembershipEndpoint
from .types.membership import MembershipState
from .types.membership import MonitoringConfig
from .types.membership import MultiCloudCluster
from .types.membership import OnPremCluster
from .types.membership import OperationMetadata
from .types.membership import ResourceManifest
from .types.membership import ResourceOptions
from .types.membership import TypeMeta
from .types.membership import UpdateMembershipRequest
from .types.membership import ValidateExclusivityRequest
from .types.membership import ValidateExclusivityResponse

__all__ = (
    'GkeHubMembershipServiceAsyncClient',
'ApplianceCluster',
'Authority',
'ConnectAgent',
'ConnectAgentResource',
'CreateMembershipRequest',
'DeleteMembershipRequest',
'EdgeCluster',
'GenerateConnectManifestRequest',
'GenerateConnectManifestResponse',
'GenerateExclusivityManifestRequest',
'GenerateExclusivityManifestResponse',
'GetMembershipRequest',
'GkeCluster',
'GkeHubMembershipServiceClient',
'KubernetesMetadata',
'KubernetesResource',
'ListMembershipsRequest',
'ListMembershipsResponse',
'Membership',
'MembershipEndpoint',
'MembershipState',
'MonitoringConfig',
'MultiCloudCluster',
'OnPremCluster',
'OperationMetadata',
'ResourceManifest',
'ResourceOptions',
'TypeMeta',
'UpdateMembershipRequest',
'ValidateExclusivityRequest',
'ValidateExclusivityResponse',
)
