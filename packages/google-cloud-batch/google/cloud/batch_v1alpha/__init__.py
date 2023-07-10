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
from google.cloud.batch_v1alpha import gapic_version as package_version

__version__ = package_version.__version__


from .services.batch_service import BatchServiceAsyncClient, BatchServiceClient
from .types.batch import (
    CreateJobRequest,
    DeleteJobRequest,
    GetJobRequest,
    GetTaskRequest,
    ListJobsRequest,
    ListJobsResponse,
    ListTasksRequest,
    ListTasksResponse,
    OperationMetadata,
)
from .types.job import (
    AllocationPolicy,
    Job,
    JobDependency,
    JobNotification,
    JobStatus,
    LogsPolicy,
    ResourceUsage,
    ServiceAccount,
    TaskGroup,
)
from .types.task import (
    ComputeResource,
    Environment,
    LifecyclePolicy,
    Runnable,
    StatusEvent,
    Task,
    TaskExecution,
    TaskResourceUsage,
    TaskSpec,
    TaskStatus,
)
from .types.volume import GCS, NFS, PD, Volume

__all__ = (
    "BatchServiceAsyncClient",
    "AllocationPolicy",
    "BatchServiceClient",
    "ComputeResource",
    "CreateJobRequest",
    "DeleteJobRequest",
    "Environment",
    "GCS",
    "GetJobRequest",
    "GetTaskRequest",
    "Job",
    "JobDependency",
    "JobNotification",
    "JobStatus",
    "LifecyclePolicy",
    "ListJobsRequest",
    "ListJobsResponse",
    "ListTasksRequest",
    "ListTasksResponse",
    "LogsPolicy",
    "NFS",
    "OperationMetadata",
    "PD",
    "ResourceUsage",
    "Runnable",
    "ServiceAccount",
    "StatusEvent",
    "Task",
    "TaskExecution",
    "TaskGroup",
    "TaskResourceUsage",
    "TaskSpec",
    "TaskStatus",
    "Volume",
)
