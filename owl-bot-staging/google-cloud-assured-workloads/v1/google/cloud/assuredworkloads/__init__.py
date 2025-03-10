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
from google.cloud.assuredworkloads import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.assuredworkloads_v1.services.assured_workloads_service.client import AssuredWorkloadsServiceClient
from google.cloud.assuredworkloads_v1.services.assured_workloads_service.async_client import AssuredWorkloadsServiceAsyncClient

from google.cloud.assuredworkloads_v1.types.assuredworkloads import AcknowledgeViolationRequest
from google.cloud.assuredworkloads_v1.types.assuredworkloads import AcknowledgeViolationResponse
from google.cloud.assuredworkloads_v1.types.assuredworkloads import CreateWorkloadOperationMetadata
from google.cloud.assuredworkloads_v1.types.assuredworkloads import CreateWorkloadRequest
from google.cloud.assuredworkloads_v1.types.assuredworkloads import DeleteWorkloadRequest
from google.cloud.assuredworkloads_v1.types.assuredworkloads import GetViolationRequest
from google.cloud.assuredworkloads_v1.types.assuredworkloads import GetWorkloadRequest
from google.cloud.assuredworkloads_v1.types.assuredworkloads import ListViolationsRequest
from google.cloud.assuredworkloads_v1.types.assuredworkloads import ListViolationsResponse
from google.cloud.assuredworkloads_v1.types.assuredworkloads import ListWorkloadsRequest
from google.cloud.assuredworkloads_v1.types.assuredworkloads import ListWorkloadsResponse
from google.cloud.assuredworkloads_v1.types.assuredworkloads import RestrictAllowedResourcesRequest
from google.cloud.assuredworkloads_v1.types.assuredworkloads import RestrictAllowedResourcesResponse
from google.cloud.assuredworkloads_v1.types.assuredworkloads import TimeWindow
from google.cloud.assuredworkloads_v1.types.assuredworkloads import UpdateWorkloadRequest
from google.cloud.assuredworkloads_v1.types.assuredworkloads import Violation
from google.cloud.assuredworkloads_v1.types.assuredworkloads import Workload

__all__ = ('AssuredWorkloadsServiceClient',
    'AssuredWorkloadsServiceAsyncClient',
    'AcknowledgeViolationRequest',
    'AcknowledgeViolationResponse',
    'CreateWorkloadOperationMetadata',
    'CreateWorkloadRequest',
    'DeleteWorkloadRequest',
    'GetViolationRequest',
    'GetWorkloadRequest',
    'ListViolationsRequest',
    'ListViolationsResponse',
    'ListWorkloadsRequest',
    'ListWorkloadsResponse',
    'RestrictAllowedResourcesRequest',
    'RestrictAllowedResourcesResponse',
    'TimeWindow',
    'UpdateWorkloadRequest',
    'Violation',
    'Workload',
)
