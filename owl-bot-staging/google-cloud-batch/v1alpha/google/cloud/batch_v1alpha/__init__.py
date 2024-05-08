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
from google.cloud.batch_v1alpha import gapic_version as package_version

__version__ = package_version.__version__


from .services.batch_service import BatchServiceClient
from .services.batch_service import BatchServiceAsyncClient

from .types.batch import CreateJobRequest
from .types.batch import CreateResourceAllowanceRequest
from .types.batch import DeleteJobRequest
from .types.batch import DeleteResourceAllowanceRequest
from .types.batch import GetJobRequest
from .types.batch import GetResourceAllowanceRequest
from .types.batch import GetTaskRequest
from .types.batch import ListJobsRequest
from .types.batch import ListJobsResponse
from .types.batch import ListResourceAllowancesRequest
from .types.batch import ListResourceAllowancesResponse
from .types.batch import ListTasksRequest
from .types.batch import ListTasksResponse
from .types.batch import OperationMetadata
from .types.batch import UpdateJobRequest
from .types.batch import UpdateResourceAllowanceRequest
from .types.job import AllocationPolicy
from .types.job import Job
from .types.job import JobDependency
from .types.job import JobNotification
from .types.job import JobStatus
from .types.job import LogsPolicy
from .types.job import ResourceUsage
from .types.job import ServiceAccount
from .types.job import TaskGroup
from .types.notification import Notification
from .types.resource_allowance import ResourceAllowance
from .types.resource_allowance import UsageResourceAllowance
from .types.resource_allowance import UsageResourceAllowanceSpec
from .types.resource_allowance import UsageResourceAllowanceStatus
from .types.resource_allowance import CalendarPeriod
from .types.resource_allowance import ResourceAllowanceState
from .types.task import ComputeResource
from .types.task import Environment
from .types.task import LifecyclePolicy
from .types.task import Runnable
from .types.task import StatusEvent
from .types.task import Task
from .types.task import TaskExecution
from .types.task import TaskResourceUsage
from .types.task import TaskSpec
from .types.task import TaskStatus
from .types.volume import GCS
from .types.volume import NFS
from .types.volume import PD
from .types.volume import Volume

__all__ = (
    'BatchServiceAsyncClient',
'AllocationPolicy',
'BatchServiceClient',
'CalendarPeriod',
'ComputeResource',
'CreateJobRequest',
'CreateResourceAllowanceRequest',
'DeleteJobRequest',
'DeleteResourceAllowanceRequest',
'Environment',
'GCS',
'GetJobRequest',
'GetResourceAllowanceRequest',
'GetTaskRequest',
'Job',
'JobDependency',
'JobNotification',
'JobStatus',
'LifecyclePolicy',
'ListJobsRequest',
'ListJobsResponse',
'ListResourceAllowancesRequest',
'ListResourceAllowancesResponse',
'ListTasksRequest',
'ListTasksResponse',
'LogsPolicy',
'NFS',
'Notification',
'OperationMetadata',
'PD',
'ResourceAllowance',
'ResourceAllowanceState',
'ResourceUsage',
'Runnable',
'ServiceAccount',
'StatusEvent',
'Task',
'TaskExecution',
'TaskGroup',
'TaskResourceUsage',
'TaskSpec',
'TaskStatus',
'UpdateJobRequest',
'UpdateResourceAllowanceRequest',
'UsageResourceAllowance',
'UsageResourceAllowanceSpec',
'UsageResourceAllowanceStatus',
'Volume',
)
