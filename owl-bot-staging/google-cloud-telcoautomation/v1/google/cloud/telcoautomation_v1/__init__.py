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
from google.cloud.telcoautomation_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.telco_automation import TelcoAutomationClient
from .services.telco_automation import TelcoAutomationAsyncClient

from .types.telcoautomation import ApplyDeploymentRequest
from .types.telcoautomation import ApplyHydratedDeploymentRequest
from .types.telcoautomation import ApproveBlueprintRequest
from .types.telcoautomation import Blueprint
from .types.telcoautomation import ComputeDeploymentStatusRequest
from .types.telcoautomation import ComputeDeploymentStatusResponse
from .types.telcoautomation import CreateBlueprintRequest
from .types.telcoautomation import CreateDeploymentRequest
from .types.telcoautomation import CreateEdgeSlmRequest
from .types.telcoautomation import CreateOrchestrationClusterRequest
from .types.telcoautomation import DeleteBlueprintRequest
from .types.telcoautomation import DeleteEdgeSlmRequest
from .types.telcoautomation import DeleteOrchestrationClusterRequest
from .types.telcoautomation import Deployment
from .types.telcoautomation import DiscardBlueprintChangesRequest
from .types.telcoautomation import DiscardBlueprintChangesResponse
from .types.telcoautomation import DiscardDeploymentChangesRequest
from .types.telcoautomation import DiscardDeploymentChangesResponse
from .types.telcoautomation import EdgeSlm
from .types.telcoautomation import File
from .types.telcoautomation import FullManagementConfig
from .types.telcoautomation import GetBlueprintRequest
from .types.telcoautomation import GetDeploymentRequest
from .types.telcoautomation import GetEdgeSlmRequest
from .types.telcoautomation import GetHydratedDeploymentRequest
from .types.telcoautomation import GetOrchestrationClusterRequest
from .types.telcoautomation import GetPublicBlueprintRequest
from .types.telcoautomation import HydratedDeployment
from .types.telcoautomation import HydrationStatus
from .types.telcoautomation import ListBlueprintRevisionsRequest
from .types.telcoautomation import ListBlueprintRevisionsResponse
from .types.telcoautomation import ListBlueprintsRequest
from .types.telcoautomation import ListBlueprintsResponse
from .types.telcoautomation import ListDeploymentRevisionsRequest
from .types.telcoautomation import ListDeploymentRevisionsResponse
from .types.telcoautomation import ListDeploymentsRequest
from .types.telcoautomation import ListDeploymentsResponse
from .types.telcoautomation import ListEdgeSlmsRequest
from .types.telcoautomation import ListEdgeSlmsResponse
from .types.telcoautomation import ListHydratedDeploymentsRequest
from .types.telcoautomation import ListHydratedDeploymentsResponse
from .types.telcoautomation import ListOrchestrationClustersRequest
from .types.telcoautomation import ListOrchestrationClustersResponse
from .types.telcoautomation import ListPublicBlueprintsRequest
from .types.telcoautomation import ListPublicBlueprintsResponse
from .types.telcoautomation import ManagementConfig
from .types.telcoautomation import MasterAuthorizedNetworksConfig
from .types.telcoautomation import NFDeploySiteStatus
from .types.telcoautomation import NFDeployStatus
from .types.telcoautomation import OperationMetadata
from .types.telcoautomation import OrchestrationCluster
from .types.telcoautomation import ProposeBlueprintRequest
from .types.telcoautomation import PublicBlueprint
from .types.telcoautomation import RejectBlueprintRequest
from .types.telcoautomation import RemoveDeploymentRequest
from .types.telcoautomation import ResourceStatus
from .types.telcoautomation import RollbackDeploymentRequest
from .types.telcoautomation import SearchBlueprintRevisionsRequest
from .types.telcoautomation import SearchBlueprintRevisionsResponse
from .types.telcoautomation import SearchDeploymentRevisionsRequest
from .types.telcoautomation import SearchDeploymentRevisionsResponse
from .types.telcoautomation import SiteVersion
from .types.telcoautomation import StandardManagementConfig
from .types.telcoautomation import UpdateBlueprintRequest
from .types.telcoautomation import UpdateDeploymentRequest
from .types.telcoautomation import UpdateHydratedDeploymentRequest
from .types.telcoautomation import WorkloadStatus
from .types.telcoautomation import BlueprintView
from .types.telcoautomation import DeploymentLevel
from .types.telcoautomation import DeploymentView
from .types.telcoautomation import ResourceType
from .types.telcoautomation import Status

__all__ = (
    'TelcoAutomationAsyncClient',
'ApplyDeploymentRequest',
'ApplyHydratedDeploymentRequest',
'ApproveBlueprintRequest',
'Blueprint',
'BlueprintView',
'ComputeDeploymentStatusRequest',
'ComputeDeploymentStatusResponse',
'CreateBlueprintRequest',
'CreateDeploymentRequest',
'CreateEdgeSlmRequest',
'CreateOrchestrationClusterRequest',
'DeleteBlueprintRequest',
'DeleteEdgeSlmRequest',
'DeleteOrchestrationClusterRequest',
'Deployment',
'DeploymentLevel',
'DeploymentView',
'DiscardBlueprintChangesRequest',
'DiscardBlueprintChangesResponse',
'DiscardDeploymentChangesRequest',
'DiscardDeploymentChangesResponse',
'EdgeSlm',
'File',
'FullManagementConfig',
'GetBlueprintRequest',
'GetDeploymentRequest',
'GetEdgeSlmRequest',
'GetHydratedDeploymentRequest',
'GetOrchestrationClusterRequest',
'GetPublicBlueprintRequest',
'HydratedDeployment',
'HydrationStatus',
'ListBlueprintRevisionsRequest',
'ListBlueprintRevisionsResponse',
'ListBlueprintsRequest',
'ListBlueprintsResponse',
'ListDeploymentRevisionsRequest',
'ListDeploymentRevisionsResponse',
'ListDeploymentsRequest',
'ListDeploymentsResponse',
'ListEdgeSlmsRequest',
'ListEdgeSlmsResponse',
'ListHydratedDeploymentsRequest',
'ListHydratedDeploymentsResponse',
'ListOrchestrationClustersRequest',
'ListOrchestrationClustersResponse',
'ListPublicBlueprintsRequest',
'ListPublicBlueprintsResponse',
'ManagementConfig',
'MasterAuthorizedNetworksConfig',
'NFDeploySiteStatus',
'NFDeployStatus',
'OperationMetadata',
'OrchestrationCluster',
'ProposeBlueprintRequest',
'PublicBlueprint',
'RejectBlueprintRequest',
'RemoveDeploymentRequest',
'ResourceStatus',
'ResourceType',
'RollbackDeploymentRequest',
'SearchBlueprintRevisionsRequest',
'SearchBlueprintRevisionsResponse',
'SearchDeploymentRevisionsRequest',
'SearchDeploymentRevisionsResponse',
'SiteVersion',
'StandardManagementConfig',
'Status',
'TelcoAutomationClient',
'UpdateBlueprintRequest',
'UpdateDeploymentRequest',
'UpdateHydratedDeploymentRequest',
'WorkloadStatus',
)
