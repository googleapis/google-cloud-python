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
from google.cloud.policysimulator_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.org_policy_violations_preview_service import (
    OrgPolicyViolationsPreviewServiceAsyncClient,
    OrgPolicyViolationsPreviewServiceClient,
)
from .services.simulator import SimulatorAsyncClient, SimulatorClient
from .types.explanations import (
    AccessState,
    AccessTuple,
    BindingExplanation,
    ExplainedPolicy,
    HeuristicRelevance,
)
from .types.orgpolicy import (
    CreateOrgPolicyViolationsPreviewOperationMetadata,
    CreateOrgPolicyViolationsPreviewRequest,
    GetOrgPolicyViolationsPreviewRequest,
    ListOrgPolicyViolationsPreviewsRequest,
    ListOrgPolicyViolationsPreviewsResponse,
    ListOrgPolicyViolationsRequest,
    ListOrgPolicyViolationsResponse,
    OrgPolicyOverlay,
    OrgPolicyViolation,
    OrgPolicyViolationsPreview,
    PreviewState,
    ResourceContext,
)
from .types.simulator import (
    AccessStateDiff,
    CreateReplayRequest,
    ExplainedAccess,
    GetReplayRequest,
    ListReplayResultsRequest,
    ListReplayResultsResponse,
    Replay,
    ReplayConfig,
    ReplayDiff,
    ReplayOperationMetadata,
    ReplayResult,
)

__all__ = (
    "OrgPolicyViolationsPreviewServiceAsyncClient",
    "SimulatorAsyncClient",
    "AccessState",
    "AccessStateDiff",
    "AccessTuple",
    "BindingExplanation",
    "CreateOrgPolicyViolationsPreviewOperationMetadata",
    "CreateOrgPolicyViolationsPreviewRequest",
    "CreateReplayRequest",
    "ExplainedAccess",
    "ExplainedPolicy",
    "GetOrgPolicyViolationsPreviewRequest",
    "GetReplayRequest",
    "HeuristicRelevance",
    "ListOrgPolicyViolationsPreviewsRequest",
    "ListOrgPolicyViolationsPreviewsResponse",
    "ListOrgPolicyViolationsRequest",
    "ListOrgPolicyViolationsResponse",
    "ListReplayResultsRequest",
    "ListReplayResultsResponse",
    "OrgPolicyOverlay",
    "OrgPolicyViolation",
    "OrgPolicyViolationsPreview",
    "OrgPolicyViolationsPreviewServiceClient",
    "PreviewState",
    "Replay",
    "ReplayConfig",
    "ReplayDiff",
    "ReplayOperationMetadata",
    "ReplayResult",
    "ResourceContext",
    "SimulatorClient",
)
