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
from google.iam_v1beta import gapic_version as package_version

__version__ = package_version.__version__


from .services.workload_identity_pools import WorkloadIdentityPoolsClient
from .services.workload_identity_pools import WorkloadIdentityPoolsAsyncClient

from .types.workload_identity_pool import CreateWorkloadIdentityPoolProviderRequest
from .types.workload_identity_pool import CreateWorkloadIdentityPoolRequest
from .types.workload_identity_pool import DeleteWorkloadIdentityPoolProviderRequest
from .types.workload_identity_pool import DeleteWorkloadIdentityPoolRequest
from .types.workload_identity_pool import GetWorkloadIdentityPoolProviderRequest
from .types.workload_identity_pool import GetWorkloadIdentityPoolRequest
from .types.workload_identity_pool import ListWorkloadIdentityPoolProvidersRequest
from .types.workload_identity_pool import ListWorkloadIdentityPoolProvidersResponse
from .types.workload_identity_pool import ListWorkloadIdentityPoolsRequest
from .types.workload_identity_pool import ListWorkloadIdentityPoolsResponse
from .types.workload_identity_pool import UndeleteWorkloadIdentityPoolProviderRequest
from .types.workload_identity_pool import UndeleteWorkloadIdentityPoolRequest
from .types.workload_identity_pool import UpdateWorkloadIdentityPoolProviderRequest
from .types.workload_identity_pool import UpdateWorkloadIdentityPoolRequest
from .types.workload_identity_pool import WorkloadIdentityPool
from .types.workload_identity_pool import WorkloadIdentityPoolOperationMetadata
from .types.workload_identity_pool import WorkloadIdentityPoolProvider
from .types.workload_identity_pool import WorkloadIdentityPoolProviderOperationMetadata

__all__ = (
    'WorkloadIdentityPoolsAsyncClient',
'CreateWorkloadIdentityPoolProviderRequest',
'CreateWorkloadIdentityPoolRequest',
'DeleteWorkloadIdentityPoolProviderRequest',
'DeleteWorkloadIdentityPoolRequest',
'GetWorkloadIdentityPoolProviderRequest',
'GetWorkloadIdentityPoolRequest',
'ListWorkloadIdentityPoolProvidersRequest',
'ListWorkloadIdentityPoolProvidersResponse',
'ListWorkloadIdentityPoolsRequest',
'ListWorkloadIdentityPoolsResponse',
'UndeleteWorkloadIdentityPoolProviderRequest',
'UndeleteWorkloadIdentityPoolRequest',
'UpdateWorkloadIdentityPoolProviderRequest',
'UpdateWorkloadIdentityPoolRequest',
'WorkloadIdentityPool',
'WorkloadIdentityPoolOperationMetadata',
'WorkloadIdentityPoolProvider',
'WorkloadIdentityPoolProviderOperationMetadata',
'WorkloadIdentityPoolsClient',
)
