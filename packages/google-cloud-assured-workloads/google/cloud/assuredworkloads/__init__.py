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

from google.cloud.assuredworkloads_v1beta1.services.assured_workloads_service.client import (
    AssuredWorkloadsServiceClient,
)
from google.cloud.assuredworkloads_v1beta1.services.assured_workloads_service.async_client import (
    AssuredWorkloadsServiceAsyncClient,
)

from google.cloud.assuredworkloads_v1beta1.types.assuredworkloads_v1beta1 import (
    CreateWorkloadOperationMetadata,
)
from google.cloud.assuredworkloads_v1beta1.types.assuredworkloads_v1beta1 import (
    CreateWorkloadRequest,
)
from google.cloud.assuredworkloads_v1beta1.types.assuredworkloads_v1beta1 import (
    DeleteWorkloadRequest,
)
from google.cloud.assuredworkloads_v1beta1.types.assuredworkloads_v1beta1 import (
    GetWorkloadRequest,
)
from google.cloud.assuredworkloads_v1beta1.types.assuredworkloads_v1beta1 import (
    ListWorkloadsRequest,
)
from google.cloud.assuredworkloads_v1beta1.types.assuredworkloads_v1beta1 import (
    ListWorkloadsResponse,
)
from google.cloud.assuredworkloads_v1beta1.types.assuredworkloads_v1beta1 import (
    UpdateWorkloadRequest,
)
from google.cloud.assuredworkloads_v1beta1.types.assuredworkloads_v1beta1 import (
    Workload,
)

__all__ = (
    "AssuredWorkloadsServiceClient",
    "AssuredWorkloadsServiceAsyncClient",
    "CreateWorkloadOperationMetadata",
    "CreateWorkloadRequest",
    "DeleteWorkloadRequest",
    "GetWorkloadRequest",
    "ListWorkloadsRequest",
    "ListWorkloadsResponse",
    "UpdateWorkloadRequest",
    "Workload",
)
