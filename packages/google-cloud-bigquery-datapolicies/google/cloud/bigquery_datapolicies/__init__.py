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
from google.cloud.bigquery_datapolicies import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.bigquery_datapolicies_v1.services.data_policy_service.async_client import (
    DataPolicyServiceAsyncClient,
)
from google.cloud.bigquery_datapolicies_v1.services.data_policy_service.client import (
    DataPolicyServiceClient,
)
from google.cloud.bigquery_datapolicies_v1.types.datapolicy import (
    CreateDataPolicyRequest,
    DataMaskingPolicy,
    DataPolicy,
    DeleteDataPolicyRequest,
    GetDataPolicyRequest,
    ListDataPoliciesRequest,
    ListDataPoliciesResponse,
    RenameDataPolicyRequest,
    UpdateDataPolicyRequest,
)

__all__ = (
    "DataPolicyServiceClient",
    "DataPolicyServiceAsyncClient",
    "CreateDataPolicyRequest",
    "DataMaskingPolicy",
    "DataPolicy",
    "DeleteDataPolicyRequest",
    "GetDataPolicyRequest",
    "ListDataPoliciesRequest",
    "ListDataPoliciesResponse",
    "RenameDataPolicyRequest",
    "UpdateDataPolicyRequest",
)
