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
from google.cloud.gkehub import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.gkehub_v1.services.gke_hub.async_client import GkeHubAsyncClient
from google.cloud.gkehub_v1.services.gke_hub.client import GkeHubClient
from google.cloud.gkehub_v1.types.feature import (
    CommonFeatureSpec,
    CommonFeatureState,
    Feature,
    FeatureResourceState,
    FeatureState,
    MembershipFeatureSpec,
    MembershipFeatureState,
)
from google.cloud.gkehub_v1.types.membership import (
    Authority,
    GkeCluster,
    KubernetesMetadata,
    KubernetesResource,
    Membership,
    MembershipEndpoint,
    MembershipState,
    MonitoringConfig,
    ResourceManifest,
    ResourceOptions,
)
from google.cloud.gkehub_v1.types.service import (
    ConnectAgentResource,
    CreateFeatureRequest,
    CreateMembershipRequest,
    DeleteFeatureRequest,
    DeleteMembershipRequest,
    GenerateConnectManifestRequest,
    GenerateConnectManifestResponse,
    GetFeatureRequest,
    GetMembershipRequest,
    ListFeaturesRequest,
    ListFeaturesResponse,
    ListMembershipsRequest,
    ListMembershipsResponse,
    OperationMetadata,
    TypeMeta,
    UpdateFeatureRequest,
    UpdateMembershipRequest,
)

__all__ = (
    "GkeHubClient",
    "GkeHubAsyncClient",
    "CommonFeatureSpec",
    "CommonFeatureState",
    "Feature",
    "FeatureResourceState",
    "FeatureState",
    "MembershipFeatureSpec",
    "MembershipFeatureState",
    "Authority",
    "GkeCluster",
    "KubernetesMetadata",
    "KubernetesResource",
    "Membership",
    "MembershipEndpoint",
    "MembershipState",
    "MonitoringConfig",
    "ResourceManifest",
    "ResourceOptions",
    "ConnectAgentResource",
    "CreateFeatureRequest",
    "CreateMembershipRequest",
    "DeleteFeatureRequest",
    "DeleteMembershipRequest",
    "GenerateConnectManifestRequest",
    "GenerateConnectManifestResponse",
    "GetFeatureRequest",
    "GetMembershipRequest",
    "ListFeaturesRequest",
    "ListFeaturesResponse",
    "ListMembershipsRequest",
    "ListMembershipsResponse",
    "OperationMetadata",
    "TypeMeta",
    "UpdateFeatureRequest",
    "UpdateMembershipRequest",
)
