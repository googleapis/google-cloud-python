# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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

from .services.assured_workloads_service import AssuredWorkloadsServiceClient
from .services.assured_workloads_service import AssuredWorkloadsServiceAsyncClient

from .types.assuredworkloads_v1beta1 import CreateWorkloadOperationMetadata
from .types.assuredworkloads_v1beta1 import CreateWorkloadRequest
from .types.assuredworkloads_v1beta1 import DeleteWorkloadRequest
from .types.assuredworkloads_v1beta1 import GetWorkloadRequest
from .types.assuredworkloads_v1beta1 import ListWorkloadsRequest
from .types.assuredworkloads_v1beta1 import ListWorkloadsResponse
from .types.assuredworkloads_v1beta1 import UpdateWorkloadRequest
from .types.assuredworkloads_v1beta1 import Workload

__all__ = (
    "AssuredWorkloadsServiceAsyncClient",
    "AssuredWorkloadsServiceClient",
    "CreateWorkloadOperationMetadata",
    "CreateWorkloadRequest",
    "DeleteWorkloadRequest",
    "GetWorkloadRequest",
    "ListWorkloadsRequest",
    "ListWorkloadsResponse",
    "UpdateWorkloadRequest",
    "Workload",
)
