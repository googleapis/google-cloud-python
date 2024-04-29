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
from google.cloud.parallelstore_v1beta import gapic_version as package_version

__version__ = package_version.__version__


from .services.parallelstore import ParallelstoreClient
from .services.parallelstore import ParallelstoreAsyncClient

from .types.parallelstore import CreateInstanceRequest
from .types.parallelstore import DeleteInstanceRequest
from .types.parallelstore import ExportDataMetadata
from .types.parallelstore import ExportDataRequest
from .types.parallelstore import ExportDataResponse
from .types.parallelstore import GetInstanceRequest
from .types.parallelstore import ImportDataMetadata
from .types.parallelstore import ImportDataRequest
from .types.parallelstore import ImportDataResponse
from .types.parallelstore import Instance
from .types.parallelstore import ListInstancesRequest
from .types.parallelstore import ListInstancesResponse
from .types.parallelstore import OperationMetadata
from .types.parallelstore import TransferCounters
from .types.parallelstore import TransferOperationMetadata
from .types.parallelstore import UpdateInstanceRequest
from .types.parallelstore import TransferType

__all__ = (
    'ParallelstoreAsyncClient',
'CreateInstanceRequest',
'DeleteInstanceRequest',
'ExportDataMetadata',
'ExportDataRequest',
'ExportDataResponse',
'GetInstanceRequest',
'ImportDataMetadata',
'ImportDataRequest',
'ImportDataResponse',
'Instance',
'ListInstancesRequest',
'ListInstancesResponse',
'OperationMetadata',
'ParallelstoreClient',
'TransferCounters',
'TransferOperationMetadata',
'TransferType',
'UpdateInstanceRequest',
)
