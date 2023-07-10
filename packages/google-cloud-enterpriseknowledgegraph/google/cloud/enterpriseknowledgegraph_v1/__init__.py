# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from google.cloud.enterpriseknowledgegraph_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.enterprise_knowledge_graph_service import (
    EnterpriseKnowledgeGraphServiceAsyncClient,
    EnterpriseKnowledgeGraphServiceClient,
)
from .types.job_state import JobState
from .types.operation_metadata import CommonOperationMetadata
from .types.service import (
    AffinityClusteringConfig,
    BigQueryInputConfig,
    CancelEntityReconciliationJobRequest,
    ConnectedComponentsConfig,
    CreateEntityReconciliationJobRequest,
    DeleteEntityReconciliationJobRequest,
    DeleteOperationMetadata,
    EntityReconciliationJob,
    GetEntityReconciliationJobRequest,
    InputConfig,
    ListEntityReconciliationJobsRequest,
    ListEntityReconciliationJobsResponse,
    LookupPublicKgRequest,
    LookupPublicKgResponse,
    LookupRequest,
    LookupResponse,
    OutputConfig,
    ReconConfig,
    SearchPublicKgRequest,
    SearchPublicKgResponse,
    SearchRequest,
    SearchResponse,
)

__all__ = (
    "EnterpriseKnowledgeGraphServiceAsyncClient",
    "AffinityClusteringConfig",
    "BigQueryInputConfig",
    "CancelEntityReconciliationJobRequest",
    "CommonOperationMetadata",
    "ConnectedComponentsConfig",
    "CreateEntityReconciliationJobRequest",
    "DeleteEntityReconciliationJobRequest",
    "DeleteOperationMetadata",
    "EnterpriseKnowledgeGraphServiceClient",
    "EntityReconciliationJob",
    "GetEntityReconciliationJobRequest",
    "InputConfig",
    "JobState",
    "ListEntityReconciliationJobsRequest",
    "ListEntityReconciliationJobsResponse",
    "LookupPublicKgRequest",
    "LookupPublicKgResponse",
    "LookupRequest",
    "LookupResponse",
    "OutputConfig",
    "ReconConfig",
    "SearchPublicKgRequest",
    "SearchPublicKgResponse",
    "SearchRequest",
    "SearchResponse",
)
