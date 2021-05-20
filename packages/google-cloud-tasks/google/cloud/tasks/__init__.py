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

from google.cloud.tasks_v2.services.cloud_tasks.client import CloudTasksClient
from google.cloud.tasks_v2.services.cloud_tasks.async_client import (
    CloudTasksAsyncClient,
)

from google.cloud.tasks_v2.types.cloudtasks import CreateQueueRequest
from google.cloud.tasks_v2.types.cloudtasks import CreateTaskRequest
from google.cloud.tasks_v2.types.cloudtasks import DeleteQueueRequest
from google.cloud.tasks_v2.types.cloudtasks import DeleteTaskRequest
from google.cloud.tasks_v2.types.cloudtasks import GetQueueRequest
from google.cloud.tasks_v2.types.cloudtasks import GetTaskRequest
from google.cloud.tasks_v2.types.cloudtasks import ListQueuesRequest
from google.cloud.tasks_v2.types.cloudtasks import ListQueuesResponse
from google.cloud.tasks_v2.types.cloudtasks import ListTasksRequest
from google.cloud.tasks_v2.types.cloudtasks import ListTasksResponse
from google.cloud.tasks_v2.types.cloudtasks import PauseQueueRequest
from google.cloud.tasks_v2.types.cloudtasks import PurgeQueueRequest
from google.cloud.tasks_v2.types.cloudtasks import ResumeQueueRequest
from google.cloud.tasks_v2.types.cloudtasks import RunTaskRequest
from google.cloud.tasks_v2.types.cloudtasks import UpdateQueueRequest
from google.cloud.tasks_v2.types.queue import Queue
from google.cloud.tasks_v2.types.queue import RateLimits
from google.cloud.tasks_v2.types.queue import RetryConfig
from google.cloud.tasks_v2.types.queue import StackdriverLoggingConfig
from google.cloud.tasks_v2.types.target import AppEngineHttpRequest
from google.cloud.tasks_v2.types.target import AppEngineRouting
from google.cloud.tasks_v2.types.target import HttpRequest
from google.cloud.tasks_v2.types.target import OAuthToken
from google.cloud.tasks_v2.types.target import OidcToken
from google.cloud.tasks_v2.types.target import HttpMethod
from google.cloud.tasks_v2.types.task import Attempt
from google.cloud.tasks_v2.types.task import Task

__all__ = (
    "CloudTasksClient",
    "CloudTasksAsyncClient",
    "CreateQueueRequest",
    "CreateTaskRequest",
    "DeleteQueueRequest",
    "DeleteTaskRequest",
    "GetQueueRequest",
    "GetTaskRequest",
    "ListQueuesRequest",
    "ListQueuesResponse",
    "ListTasksRequest",
    "ListTasksResponse",
    "PauseQueueRequest",
    "PurgeQueueRequest",
    "ResumeQueueRequest",
    "RunTaskRequest",
    "UpdateQueueRequest",
    "Queue",
    "RateLimits",
    "RetryConfig",
    "StackdriverLoggingConfig",
    "AppEngineHttpRequest",
    "AppEngineRouting",
    "HttpRequest",
    "OAuthToken",
    "OidcToken",
    "HttpMethod",
    "Attempt",
    "Task",
)
