# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from google.cloud.workstations import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.workstations_v1.services.workstations.client import WorkstationsClient
from google.cloud.workstations_v1.services.workstations.async_client import WorkstationsAsyncClient

from google.cloud.workstations_v1.types.workstations import CreateWorkstationClusterRequest
from google.cloud.workstations_v1.types.workstations import CreateWorkstationConfigRequest
from google.cloud.workstations_v1.types.workstations import CreateWorkstationRequest
from google.cloud.workstations_v1.types.workstations import DeleteWorkstationClusterRequest
from google.cloud.workstations_v1.types.workstations import DeleteWorkstationConfigRequest
from google.cloud.workstations_v1.types.workstations import DeleteWorkstationRequest
from google.cloud.workstations_v1.types.workstations import GenerateAccessTokenRequest
from google.cloud.workstations_v1.types.workstations import GenerateAccessTokenResponse
from google.cloud.workstations_v1.types.workstations import GetWorkstationClusterRequest
from google.cloud.workstations_v1.types.workstations import GetWorkstationConfigRequest
from google.cloud.workstations_v1.types.workstations import GetWorkstationRequest
from google.cloud.workstations_v1.types.workstations import ListUsableWorkstationConfigsRequest
from google.cloud.workstations_v1.types.workstations import ListUsableWorkstationConfigsResponse
from google.cloud.workstations_v1.types.workstations import ListUsableWorkstationsRequest
from google.cloud.workstations_v1.types.workstations import ListUsableWorkstationsResponse
from google.cloud.workstations_v1.types.workstations import ListWorkstationClustersRequest
from google.cloud.workstations_v1.types.workstations import ListWorkstationClustersResponse
from google.cloud.workstations_v1.types.workstations import ListWorkstationConfigsRequest
from google.cloud.workstations_v1.types.workstations import ListWorkstationConfigsResponse
from google.cloud.workstations_v1.types.workstations import ListWorkstationsRequest
from google.cloud.workstations_v1.types.workstations import ListWorkstationsResponse
from google.cloud.workstations_v1.types.workstations import OperationMetadata
from google.cloud.workstations_v1.types.workstations import StartWorkstationRequest
from google.cloud.workstations_v1.types.workstations import StopWorkstationRequest
from google.cloud.workstations_v1.types.workstations import UpdateWorkstationClusterRequest
from google.cloud.workstations_v1.types.workstations import UpdateWorkstationConfigRequest
from google.cloud.workstations_v1.types.workstations import UpdateWorkstationRequest
from google.cloud.workstations_v1.types.workstations import Workstation
from google.cloud.workstations_v1.types.workstations import WorkstationCluster
from google.cloud.workstations_v1.types.workstations import WorkstationConfig

__all__ = ('WorkstationsClient',
    'WorkstationsAsyncClient',
    'CreateWorkstationClusterRequest',
    'CreateWorkstationConfigRequest',
    'CreateWorkstationRequest',
    'DeleteWorkstationClusterRequest',
    'DeleteWorkstationConfigRequest',
    'DeleteWorkstationRequest',
    'GenerateAccessTokenRequest',
    'GenerateAccessTokenResponse',
    'GetWorkstationClusterRequest',
    'GetWorkstationConfigRequest',
    'GetWorkstationRequest',
    'ListUsableWorkstationConfigsRequest',
    'ListUsableWorkstationConfigsResponse',
    'ListUsableWorkstationsRequest',
    'ListUsableWorkstationsResponse',
    'ListWorkstationClustersRequest',
    'ListWorkstationClustersResponse',
    'ListWorkstationConfigsRequest',
    'ListWorkstationConfigsResponse',
    'ListWorkstationsRequest',
    'ListWorkstationsResponse',
    'OperationMetadata',
    'StartWorkstationRequest',
    'StopWorkstationRequest',
    'UpdateWorkstationClusterRequest',
    'UpdateWorkstationConfigRequest',
    'UpdateWorkstationRequest',
    'Workstation',
    'WorkstationCluster',
    'WorkstationConfig',
)
