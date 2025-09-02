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
from google.cloud.storagebatchoperations_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.storage_batch_operations import StorageBatchOperationsClient
from .services.storage_batch_operations import StorageBatchOperationsAsyncClient

from .types.storage_batch_operations import CancelJobRequest
from .types.storage_batch_operations import CancelJobResponse
from .types.storage_batch_operations import CreateJobRequest
from .types.storage_batch_operations import DeleteJobRequest
from .types.storage_batch_operations import GetJobRequest
from .types.storage_batch_operations import ListJobsRequest
from .types.storage_batch_operations import ListJobsResponse
from .types.storage_batch_operations import OperationMetadata
from .types.storage_batch_operations_types import BucketList
from .types.storage_batch_operations_types import Counters
from .types.storage_batch_operations_types import DeleteObject
from .types.storage_batch_operations_types import ErrorLogEntry
from .types.storage_batch_operations_types import ErrorSummary
from .types.storage_batch_operations_types import Job
from .types.storage_batch_operations_types import LoggingConfig
from .types.storage_batch_operations_types import Manifest
from .types.storage_batch_operations_types import PrefixList
from .types.storage_batch_operations_types import PutMetadata
from .types.storage_batch_operations_types import PutObjectHold
from .types.storage_batch_operations_types import RewriteObject

__all__ = (
    'StorageBatchOperationsAsyncClient',
'BucketList',
'CancelJobRequest',
'CancelJobResponse',
'Counters',
'CreateJobRequest',
'DeleteJobRequest',
'DeleteObject',
'ErrorLogEntry',
'ErrorSummary',
'GetJobRequest',
'Job',
'ListJobsRequest',
'ListJobsResponse',
'LoggingConfig',
'Manifest',
'OperationMetadata',
'PrefixList',
'PutMetadata',
'PutObjectHold',
'RewriteObject',
'StorageBatchOperationsClient',
)
