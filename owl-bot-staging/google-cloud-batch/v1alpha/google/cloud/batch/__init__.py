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
from google.cloud.batch import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.batch_v1alpha.services.batch_service.client import BatchServiceClient
from google.cloud.batch_v1alpha.services.batch_service.async_client import BatchServiceAsyncClient

from google.cloud.batch_v1alpha.types.batch import CreateJobRequest
from google.cloud.batch_v1alpha.types.batch import CreateResourceAllowanceRequest
from google.cloud.batch_v1alpha.types.batch import DeleteJobRequest
from google.cloud.batch_v1alpha.types.batch import DeleteResourceAllowanceRequest
from google.cloud.batch_v1alpha.types.batch import GetJobRequest
from google.cloud.batch_v1alpha.types.batch import GetResourceAllowanceRequest
from google.cloud.batch_v1alpha.types.batch import GetTaskRequest
from google.cloud.batch_v1alpha.types.batch import ListJobsRequest
from google.cloud.batch_v1alpha.types.batch import ListJobsResponse
from google.cloud.batch_v1alpha.types.batch import ListResourceAllowancesRequest
from google.cloud.batch_v1alpha.types.batch import ListResourceAllowancesResponse
from google.cloud.batch_v1alpha.types.batch import ListTasksRequest
from google.cloud.batch_v1alpha.types.batch import ListTasksResponse
from google.cloud.batch_v1alpha.types.batch import OperationMetadata
from google.cloud.batch_v1alpha.types.batch import UpdateResourceAllowanceRequest
from google.cloud.batch_v1alpha.types.job import AllocationPolicy
from google.cloud.batch_v1alpha.types.job import Job
from google.cloud.batch_v1alpha.types.job import JobDependency
from google.cloud.batch_v1alpha.types.job import JobNotification
from google.cloud.batch_v1alpha.types.job import JobStatus
from google.cloud.batch_v1alpha.types.job import LogsPolicy
from google.cloud.batch_v1alpha.types.job import ResourceUsage
from google.cloud.batch_v1alpha.types.job import ServiceAccount
from google.cloud.batch_v1alpha.types.job import TaskGroup
from google.cloud.batch_v1alpha.types.notification import Notification
from google.cloud.batch_v1alpha.types.resource_allowance import ResourceAllowance
from google.cloud.batch_v1alpha.types.resource_allowance import UsageResourceAllowance
from google.cloud.batch_v1alpha.types.resource_allowance import UsageResourceAllowanceSpec
from google.cloud.batch_v1alpha.types.resource_allowance import UsageResourceAllowanceStatus
from google.cloud.batch_v1alpha.types.resource_allowance import CalendarPeriod
from google.cloud.batch_v1alpha.types.resource_allowance import ResourceAllowanceState
from google.cloud.batch_v1alpha.types.task import ComputeResource
from google.cloud.batch_v1alpha.types.task import Environment
from google.cloud.batch_v1alpha.types.task import LifecyclePolicy
from google.cloud.batch_v1alpha.types.task import Runnable
from google.cloud.batch_v1alpha.types.task import StatusEvent
from google.cloud.batch_v1alpha.types.task import Task
from google.cloud.batch_v1alpha.types.task import TaskExecution
from google.cloud.batch_v1alpha.types.task import TaskResourceUsage
from google.cloud.batch_v1alpha.types.task import TaskSpec
from google.cloud.batch_v1alpha.types.task import TaskStatus
from google.cloud.batch_v1alpha.types.volume import GCS
from google.cloud.batch_v1alpha.types.volume import NFS
from google.cloud.batch_v1alpha.types.volume import PD
from google.cloud.batch_v1alpha.types.volume import Volume

__all__ = ('BatchServiceClient',
    'BatchServiceAsyncClient',
    'CreateJobRequest',
    'CreateResourceAllowanceRequest',
    'DeleteJobRequest',
    'DeleteResourceAllowanceRequest',
    'GetJobRequest',
    'GetResourceAllowanceRequest',
    'GetTaskRequest',
    'ListJobsRequest',
    'ListJobsResponse',
    'ListResourceAllowancesRequest',
    'ListResourceAllowancesResponse',
    'ListTasksRequest',
    'ListTasksResponse',
    'OperationMetadata',
    'UpdateResourceAllowanceRequest',
    'AllocationPolicy',
    'Job',
    'JobDependency',
    'JobNotification',
    'JobStatus',
    'LogsPolicy',
    'ResourceUsage',
    'ServiceAccount',
    'TaskGroup',
    'Notification',
    'ResourceAllowance',
    'UsageResourceAllowance',
    'UsageResourceAllowanceSpec',
    'UsageResourceAllowanceStatus',
    'CalendarPeriod',
    'ResourceAllowanceState',
    'ComputeResource',
    'Environment',
    'LifecyclePolicy',
    'Runnable',
    'StatusEvent',
    'Task',
    'TaskExecution',
    'TaskResourceUsage',
    'TaskSpec',
    'TaskStatus',
    'GCS',
    'NFS',
    'PD',
    'Volume',
)
