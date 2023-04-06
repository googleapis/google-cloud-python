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
from google.cloud.workstations_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.workstations import WorkstationsClient
from .services.workstations import WorkstationsAsyncClient

from .types.workstations import CreateWorkstationClusterRequest
from .types.workstations import CreateWorkstationConfigRequest
from .types.workstations import CreateWorkstationRequest
from .types.workstations import DeleteWorkstationClusterRequest
from .types.workstations import DeleteWorkstationConfigRequest
from .types.workstations import DeleteWorkstationRequest
from .types.workstations import GenerateAccessTokenRequest
from .types.workstations import GenerateAccessTokenResponse
from .types.workstations import GetWorkstationClusterRequest
from .types.workstations import GetWorkstationConfigRequest
from .types.workstations import GetWorkstationRequest
from .types.workstations import ListUsableWorkstationConfigsRequest
from .types.workstations import ListUsableWorkstationConfigsResponse
from .types.workstations import ListUsableWorkstationsRequest
from .types.workstations import ListUsableWorkstationsResponse
from .types.workstations import ListWorkstationClustersRequest
from .types.workstations import ListWorkstationClustersResponse
from .types.workstations import ListWorkstationConfigsRequest
from .types.workstations import ListWorkstationConfigsResponse
from .types.workstations import ListWorkstationsRequest
from .types.workstations import ListWorkstationsResponse
from .types.workstations import OperationMetadata
from .types.workstations import StartWorkstationRequest
from .types.workstations import StopWorkstationRequest
from .types.workstations import UpdateWorkstationClusterRequest
from .types.workstations import UpdateWorkstationConfigRequest
from .types.workstations import UpdateWorkstationRequest
from .types.workstations import Workstation
from .types.workstations import WorkstationCluster
from .types.workstations import WorkstationConfig

__all__ = (
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
'WorkstationsClient',
)
