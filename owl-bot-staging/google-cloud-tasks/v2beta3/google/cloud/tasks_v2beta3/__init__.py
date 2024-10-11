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
from google.cloud.tasks_v2beta3 import gapic_version as package_version

__version__ = package_version.__version__


from .services.cloud_tasks import CloudTasksClient
from .services.cloud_tasks import CloudTasksAsyncClient

from .types.cloudtasks import CreateQueueRequest
from .types.cloudtasks import CreateTaskRequest
from .types.cloudtasks import DeleteQueueRequest
from .types.cloudtasks import DeleteTaskRequest
from .types.cloudtasks import GetQueueRequest
from .types.cloudtasks import GetTaskRequest
from .types.cloudtasks import ListQueuesRequest
from .types.cloudtasks import ListQueuesResponse
from .types.cloudtasks import ListTasksRequest
from .types.cloudtasks import ListTasksResponse
from .types.cloudtasks import PauseQueueRequest
from .types.cloudtasks import PurgeQueueRequest
from .types.cloudtasks import ResumeQueueRequest
from .types.cloudtasks import RunTaskRequest
from .types.cloudtasks import UpdateQueueRequest
from .types.queue import Queue
from .types.queue import QueueStats
from .types.queue import RateLimits
from .types.queue import RetryConfig
from .types.queue import StackdriverLoggingConfig
from .types.target import AppEngineHttpQueue
from .types.target import AppEngineHttpRequest
from .types.target import AppEngineRouting
from .types.target import HttpRequest
from .types.target import HttpTarget
from .types.target import OAuthToken
from .types.target import OidcToken
from .types.target import PathOverride
from .types.target import PullMessage
from .types.target import QueryOverride
from .types.target import UriOverride
from .types.target import HttpMethod
from .types.task import Attempt
from .types.task import Task

__all__ = (
    'CloudTasksAsyncClient',
'AppEngineHttpQueue',
'AppEngineHttpRequest',
'AppEngineRouting',
'Attempt',
'CloudTasksClient',
'CreateQueueRequest',
'CreateTaskRequest',
'DeleteQueueRequest',
'DeleteTaskRequest',
'GetQueueRequest',
'GetTaskRequest',
'HttpMethod',
'HttpRequest',
'HttpTarget',
'ListQueuesRequest',
'ListQueuesResponse',
'ListTasksRequest',
'ListTasksResponse',
'OAuthToken',
'OidcToken',
'PathOverride',
'PauseQueueRequest',
'PullMessage',
'PurgeQueueRequest',
'QueryOverride',
'Queue',
'QueueStats',
'RateLimits',
'ResumeQueueRequest',
'RetryConfig',
'RunTaskRequest',
'StackdriverLoggingConfig',
'Task',
'UpdateQueueRequest',
'UriOverride',
)
