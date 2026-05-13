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
import sys

import google.api_core as api_core

from google.cloud.spanner_admin_instance_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.instance_admin import InstanceAdminAsyncClient, InstanceAdminClient
from .types.common import FulfillmentPeriod, OperationProgress, ReplicaSelection
from .types.spanner_instance_admin import (
    AutoscalingConfig,
    CreateInstanceConfigMetadata,
    CreateInstanceConfigRequest,
    CreateInstanceMetadata,
    CreateInstancePartitionMetadata,
    CreateInstancePartitionRequest,
    CreateInstanceRequest,
    DeleteInstanceConfigRequest,
    DeleteInstancePartitionRequest,
    DeleteInstanceRequest,
    FreeInstanceMetadata,
    GetInstanceConfigRequest,
    GetInstancePartitionRequest,
    GetInstanceRequest,
    Instance,
    InstanceConfig,
    InstancePartition,
    ListInstanceConfigOperationsRequest,
    ListInstanceConfigOperationsResponse,
    ListInstanceConfigsRequest,
    ListInstanceConfigsResponse,
    ListInstancePartitionOperationsRequest,
    ListInstancePartitionOperationsResponse,
    ListInstancePartitionsRequest,
    ListInstancePartitionsResponse,
    ListInstancesRequest,
    ListInstancesResponse,
    MoveInstanceMetadata,
    MoveInstanceRequest,
    MoveInstanceResponse,
    ReplicaComputeCapacity,
    ReplicaInfo,
    UpdateInstanceConfigMetadata,
    UpdateInstanceConfigRequest,
    UpdateInstanceMetadata,
    UpdateInstancePartitionMetadata,
    UpdateInstancePartitionRequest,
    UpdateInstanceRequest,
)

if hasattr(api_core, "check_python_version") and hasattr(
    api_core, "check_dependency_versions"
):  # pragma: NO COVER
    api_core.check_python_version("google.cloud.spanner_admin_instance_v1")  # type: ignore
    api_core.check_dependency_versions("google.cloud.spanner_admin_instance_v1")  # type: ignore
else:  # pragma: NO COVER
    import warnings

    _py_version_str = sys.version.split()[0]
    # version-scanner: ignore-next-line
    if sys.version_info < (3, 10):
        warnings.warn(
            "You are using a non-supported Python version "
            + f"({_py_version_str}).  Google will not post any further "
            + "updates to google.cloud.spanner_admin_instance_v1 supporting this Python version. "
            + "Please upgrade to the latest Python version, or at "
            + "least to Python 3.10, and then update google.cloud.spanner_admin_instance_v1.",
            FutureWarning,
        )

__all__ = (
    "InstanceAdminAsyncClient",
    "AutoscalingConfig",
    "CreateInstanceConfigMetadata",
    "CreateInstanceConfigRequest",
    "CreateInstanceMetadata",
    "CreateInstancePartitionMetadata",
    "CreateInstancePartitionRequest",
    "CreateInstanceRequest",
    "DeleteInstanceConfigRequest",
    "DeleteInstancePartitionRequest",
    "DeleteInstanceRequest",
    "FreeInstanceMetadata",
    "FulfillmentPeriod",
    "GetInstanceConfigRequest",
    "GetInstancePartitionRequest",
    "GetInstanceRequest",
    "Instance",
    "InstanceAdminClient",
    "InstanceConfig",
    "InstancePartition",
    "ListInstanceConfigOperationsRequest",
    "ListInstanceConfigOperationsResponse",
    "ListInstanceConfigsRequest",
    "ListInstanceConfigsResponse",
    "ListInstancePartitionOperationsRequest",
    "ListInstancePartitionOperationsResponse",
    "ListInstancePartitionsRequest",
    "ListInstancePartitionsResponse",
    "ListInstancesRequest",
    "ListInstancesResponse",
    "MoveInstanceMetadata",
    "MoveInstanceRequest",
    "MoveInstanceResponse",
    "OperationProgress",
    "ReplicaComputeCapacity",
    "ReplicaInfo",
    "ReplicaSelection",
    "UpdateInstanceConfigMetadata",
    "UpdateInstanceConfigRequest",
    "UpdateInstanceMetadata",
    "UpdateInstancePartitionMetadata",
    "UpdateInstancePartitionRequest",
    "UpdateInstanceRequest",
)
