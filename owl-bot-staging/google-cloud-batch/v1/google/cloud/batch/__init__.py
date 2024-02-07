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
from google.cloud.batch import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.batch_v1.services.batch_service.client import BatchServiceClient
from google.cloud.batch_v1.services.batch_service.async_client import BatchServiceAsyncClient

from google.cloud.batch_v1.types.batch import CreateJobRequest
from google.cloud.batch_v1.types.batch import DeleteJobRequest
from google.cloud.batch_v1.types.batch import GetJobRequest
from google.cloud.batch_v1.types.batch import GetTaskRequest
from google.cloud.batch_v1.types.batch import ListJobsRequest
from google.cloud.batch_v1.types.batch import ListJobsResponse
from google.cloud.batch_v1.types.batch import ListTasksRequest
from google.cloud.batch_v1.types.batch import ListTasksResponse
from google.cloud.batch_v1.types.batch import OperationMetadata
from google.cloud.batch_v1.types.job import AllocationPolicy
from google.cloud.batch_v1.types.job import Job
from google.cloud.batch_v1.types.job import JobNotification
from google.cloud.batch_v1.types.job import JobStatus
from google.cloud.batch_v1.types.job import LogsPolicy
from google.cloud.batch_v1.types.job import ServiceAccount
from google.cloud.batch_v1.types.job import TaskGroup
from google.cloud.batch_v1.types.task import ComputeResource
from google.cloud.batch_v1.types.task import Environment
from google.cloud.batch_v1.types.task import LifecyclePolicy
from google.cloud.batch_v1.types.task import Runnable
from google.cloud.batch_v1.types.task import StatusEvent
from google.cloud.batch_v1.types.task import Task
from google.cloud.batch_v1.types.task import TaskExecution
from google.cloud.batch_v1.types.task import TaskSpec
from google.cloud.batch_v1.types.task import TaskStatus
from google.cloud.batch_v1.types.volume import GCS
from google.cloud.batch_v1.types.volume import NFS
from google.cloud.batch_v1.types.volume import Volume

__all__ = ('BatchServiceClient',
    'BatchServiceAsyncClient',
    'CreateJobRequest',
    'DeleteJobRequest',
    'GetJobRequest',
    'GetTaskRequest',
    'ListJobsRequest',
    'ListJobsResponse',
    'ListTasksRequest',
    'ListTasksResponse',
    'OperationMetadata',
    'AllocationPolicy',
    'Job',
    'JobNotification',
    'JobStatus',
    'LogsPolicy',
    'ServiceAccount',
    'TaskGroup',
    'ComputeResource',
    'Environment',
    'LifecyclePolicy',
    'Runnable',
    'StatusEvent',
    'Task',
    'TaskExecution',
    'TaskSpec',
    'TaskStatus',
    'GCS',
    'NFS',
    'Volume',
)
