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
from google.cloud.tasks import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.tasks_v2beta2.services.cloud_tasks.client import CloudTasksClient
from google.cloud.tasks_v2beta2.services.cloud_tasks.async_client import CloudTasksAsyncClient

from google.cloud.tasks_v2beta2.types.cloudtasks import AcknowledgeTaskRequest
from google.cloud.tasks_v2beta2.types.cloudtasks import BufferTaskRequest
from google.cloud.tasks_v2beta2.types.cloudtasks import BufferTaskResponse
from google.cloud.tasks_v2beta2.types.cloudtasks import CancelLeaseRequest
from google.cloud.tasks_v2beta2.types.cloudtasks import CreateQueueRequest
from google.cloud.tasks_v2beta2.types.cloudtasks import CreateTaskRequest
from google.cloud.tasks_v2beta2.types.cloudtasks import DeleteQueueRequest
from google.cloud.tasks_v2beta2.types.cloudtasks import DeleteTaskRequest
from google.cloud.tasks_v2beta2.types.cloudtasks import GetQueueRequest
from google.cloud.tasks_v2beta2.types.cloudtasks import GetTaskRequest
from google.cloud.tasks_v2beta2.types.cloudtasks import LeaseTasksRequest
from google.cloud.tasks_v2beta2.types.cloudtasks import LeaseTasksResponse
from google.cloud.tasks_v2beta2.types.cloudtasks import ListQueuesRequest
from google.cloud.tasks_v2beta2.types.cloudtasks import ListQueuesResponse
from google.cloud.tasks_v2beta2.types.cloudtasks import ListTasksRequest
from google.cloud.tasks_v2beta2.types.cloudtasks import ListTasksResponse
from google.cloud.tasks_v2beta2.types.cloudtasks import PauseQueueRequest
from google.cloud.tasks_v2beta2.types.cloudtasks import PurgeQueueRequest
from google.cloud.tasks_v2beta2.types.cloudtasks import RenewLeaseRequest
from google.cloud.tasks_v2beta2.types.cloudtasks import ResumeQueueRequest
from google.cloud.tasks_v2beta2.types.cloudtasks import RunTaskRequest
from google.cloud.tasks_v2beta2.types.cloudtasks import UpdateQueueRequest
from google.cloud.tasks_v2beta2.types.cloudtasks import UploadQueueYamlRequest
from google.cloud.tasks_v2beta2.types.queue import Queue
from google.cloud.tasks_v2beta2.types.queue import QueueStats
from google.cloud.tasks_v2beta2.types.queue import RateLimits
from google.cloud.tasks_v2beta2.types.queue import RetryConfig
from google.cloud.tasks_v2beta2.types.target import AppEngineHttpRequest
from google.cloud.tasks_v2beta2.types.target import AppEngineHttpTarget
from google.cloud.tasks_v2beta2.types.target import AppEngineRouting
from google.cloud.tasks_v2beta2.types.target import HttpRequest
from google.cloud.tasks_v2beta2.types.target import HttpTarget
from google.cloud.tasks_v2beta2.types.target import OAuthToken
from google.cloud.tasks_v2beta2.types.target import OidcToken
from google.cloud.tasks_v2beta2.types.target import PathOverride
from google.cloud.tasks_v2beta2.types.target import PullMessage
from google.cloud.tasks_v2beta2.types.target import PullTarget
from google.cloud.tasks_v2beta2.types.target import QueryOverride
from google.cloud.tasks_v2beta2.types.target import UriOverride
from google.cloud.tasks_v2beta2.types.target import HttpMethod
from google.cloud.tasks_v2beta2.types.task import AttemptStatus
from google.cloud.tasks_v2beta2.types.task import Task
from google.cloud.tasks_v2beta2.types.task import TaskStatus

__all__ = ('CloudTasksClient',
    'CloudTasksAsyncClient',
    'AcknowledgeTaskRequest',
    'BufferTaskRequest',
    'BufferTaskResponse',
    'CancelLeaseRequest',
    'CreateQueueRequest',
    'CreateTaskRequest',
    'DeleteQueueRequest',
    'DeleteTaskRequest',
    'GetQueueRequest',
    'GetTaskRequest',
    'LeaseTasksRequest',
    'LeaseTasksResponse',
    'ListQueuesRequest',
    'ListQueuesResponse',
    'ListTasksRequest',
    'ListTasksResponse',
    'PauseQueueRequest',
    'PurgeQueueRequest',
    'RenewLeaseRequest',
    'ResumeQueueRequest',
    'RunTaskRequest',
    'UpdateQueueRequest',
    'UploadQueueYamlRequest',
    'Queue',
    'QueueStats',
    'RateLimits',
    'RetryConfig',
    'AppEngineHttpRequest',
    'AppEngineHttpTarget',
    'AppEngineRouting',
    'HttpRequest',
    'HttpTarget',
    'OAuthToken',
    'OidcToken',
    'PathOverride',
    'PullMessage',
    'PullTarget',
    'QueryOverride',
    'UriOverride',
    'HttpMethod',
    'AttemptStatus',
    'Task',
    'TaskStatus',
)
