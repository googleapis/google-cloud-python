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
from google.cloud.telcoautomation import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.telcoautomation_v1alpha1.services.telco_automation.client import TelcoAutomationClient
from google.cloud.telcoautomation_v1alpha1.services.telco_automation.async_client import TelcoAutomationAsyncClient

from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import ApplyDeploymentRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import ApplyHydratedDeploymentRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import ApproveBlueprintRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import Blueprint
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import ComputeDeploymentStatusRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import ComputeDeploymentStatusResponse
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import CreateBlueprintRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import CreateDeploymentRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import CreateEdgeSlmRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import CreateOrchestrationClusterRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import DeleteBlueprintRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import DeleteBlueprintRevisionRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import DeleteDeploymentRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import DeleteDeploymentRevisionRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import DeleteEdgeSlmRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import DeleteOrchestrationClusterRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import Deployment
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import DiscardBlueprintChangesRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import DiscardBlueprintChangesResponse
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import DiscardDeploymentChangesRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import DiscardDeploymentChangesResponse
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import EdgeSlm
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import File
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import FullManagementConfig
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import GetBlueprintRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import GetDeploymentRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import GetEdgeSlmRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import GetHydratedDeploymentRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import GetOrchestrationClusterRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import GetPublicBlueprintRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import HydratedDeployment
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import ListBlueprintRevisionsRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import ListBlueprintRevisionsResponse
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import ListBlueprintsRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import ListBlueprintsResponse
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import ListDeploymentRevisionsRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import ListDeploymentRevisionsResponse
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import ListDeploymentsRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import ListDeploymentsResponse
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import ListEdgeSlmsRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import ListEdgeSlmsResponse
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import ListHydratedDeploymentsRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import ListHydratedDeploymentsResponse
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import ListOrchestrationClustersRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import ListOrchestrationClustersResponse
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import ListPublicBlueprintsRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import ListPublicBlueprintsResponse
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import ManagementConfig
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import MasterAuthorizedNetworksConfig
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import OperationMetadata
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import OrchestrationCluster
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import ProposeBlueprintRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import PublicBlueprint
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import RejectBlueprintRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import RemoveDeploymentRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import ResourceStatus
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import RollbackDeploymentRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import SearchBlueprintRevisionsRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import SearchBlueprintRevisionsResponse
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import SearchDeploymentRevisionsRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import SearchDeploymentRevisionsResponse
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import StandardManagementConfig
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import UpdateBlueprintRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import UpdateDeploymentRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import UpdateHydratedDeploymentRequest
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import BlueprintView
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import DeploymentView
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import ResourceType
from google.cloud.telcoautomation_v1alpha1.types.telcoautomation import Status

__all__ = ('TelcoAutomationClient',
    'TelcoAutomationAsyncClient',
    'ApplyDeploymentRequest',
    'ApplyHydratedDeploymentRequest',
    'ApproveBlueprintRequest',
    'Blueprint',
    'ComputeDeploymentStatusRequest',
    'ComputeDeploymentStatusResponse',
    'CreateBlueprintRequest',
    'CreateDeploymentRequest',
    'CreateEdgeSlmRequest',
    'CreateOrchestrationClusterRequest',
    'DeleteBlueprintRequest',
    'DeleteBlueprintRevisionRequest',
    'DeleteDeploymentRequest',
    'DeleteDeploymentRevisionRequest',
    'DeleteEdgeSlmRequest',
    'DeleteOrchestrationClusterRequest',
    'Deployment',
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
    'OperationMetadata',
    'OrchestrationCluster',
    'ProposeBlueprintRequest',
    'PublicBlueprint',
    'RejectBlueprintRequest',
    'RemoveDeploymentRequest',
    'ResourceStatus',
    'RollbackDeploymentRequest',
    'SearchBlueprintRevisionsRequest',
    'SearchBlueprintRevisionsResponse',
    'SearchDeploymentRevisionsRequest',
    'SearchDeploymentRevisionsResponse',
    'StandardManagementConfig',
    'UpdateBlueprintRequest',
    'UpdateDeploymentRequest',
    'UpdateHydratedDeploymentRequest',
    'BlueprintView',
    'DeploymentView',
    'ResourceType',
    'Status',
)
