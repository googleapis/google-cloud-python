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
from google.cloud.gkehub_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.gke_hub import GkeHubAsyncClient, GkeHubClient
from .types.feature import (
    CommonFeatureSpec,
    CommonFeatureState,
    Feature,
    FeatureResourceState,
    FeatureState,
    MembershipFeatureSpec,
    MembershipFeatureState,
)
from .types.membership import (
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
from .types.service import (
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
    "GkeHubAsyncClient",
    "Authority",
    "CommonFeatureSpec",
    "CommonFeatureState",
    "ConnectAgentResource",
    "CreateFeatureRequest",
    "CreateMembershipRequest",
    "DeleteFeatureRequest",
    "DeleteMembershipRequest",
    "Feature",
    "FeatureResourceState",
    "FeatureState",
    "GenerateConnectManifestRequest",
    "GenerateConnectManifestResponse",
    "GetFeatureRequest",
    "GetMembershipRequest",
    "GkeCluster",
    "GkeHubClient",
    "KubernetesMetadata",
    "KubernetesResource",
    "ListFeaturesRequest",
    "ListFeaturesResponse",
    "ListMembershipsRequest",
    "ListMembershipsResponse",
    "Membership",
    "MembershipEndpoint",
    "MembershipFeatureSpec",
    "MembershipFeatureState",
    "MembershipState",
    "MonitoringConfig",
    "OperationMetadata",
    "ResourceManifest",
    "ResourceOptions",
    "TypeMeta",
    "UpdateFeatureRequest",
    "UpdateMembershipRequest",
)
