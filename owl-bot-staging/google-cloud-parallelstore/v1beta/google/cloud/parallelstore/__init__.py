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
from google.cloud.parallelstore import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.parallelstore_v1beta.services.parallelstore.client import ParallelstoreClient
from google.cloud.parallelstore_v1beta.services.parallelstore.async_client import ParallelstoreAsyncClient

from google.cloud.parallelstore_v1beta.types.parallelstore import CreateInstanceRequest
from google.cloud.parallelstore_v1beta.types.parallelstore import DeleteInstanceRequest
from google.cloud.parallelstore_v1beta.types.parallelstore import DestinationGcsBucket
from google.cloud.parallelstore_v1beta.types.parallelstore import DestinationParallelstore
from google.cloud.parallelstore_v1beta.types.parallelstore import ExportDataMetadata
from google.cloud.parallelstore_v1beta.types.parallelstore import ExportDataRequest
from google.cloud.parallelstore_v1beta.types.parallelstore import ExportDataResponse
from google.cloud.parallelstore_v1beta.types.parallelstore import GetInstanceRequest
from google.cloud.parallelstore_v1beta.types.parallelstore import ImportDataMetadata
from google.cloud.parallelstore_v1beta.types.parallelstore import ImportDataRequest
from google.cloud.parallelstore_v1beta.types.parallelstore import ImportDataResponse
from google.cloud.parallelstore_v1beta.types.parallelstore import Instance
from google.cloud.parallelstore_v1beta.types.parallelstore import ListInstancesRequest
from google.cloud.parallelstore_v1beta.types.parallelstore import ListInstancesResponse
from google.cloud.parallelstore_v1beta.types.parallelstore import OperationMetadata
from google.cloud.parallelstore_v1beta.types.parallelstore import SourceGcsBucket
from google.cloud.parallelstore_v1beta.types.parallelstore import SourceParallelstore
from google.cloud.parallelstore_v1beta.types.parallelstore import TransferCounters
from google.cloud.parallelstore_v1beta.types.parallelstore import TransferOperationMetadata
from google.cloud.parallelstore_v1beta.types.parallelstore import UpdateInstanceRequest
from google.cloud.parallelstore_v1beta.types.parallelstore import DirectoryStripeLevel
from google.cloud.parallelstore_v1beta.types.parallelstore import FileStripeLevel
from google.cloud.parallelstore_v1beta.types.parallelstore import TransferType

__all__ = ('ParallelstoreClient',
    'ParallelstoreAsyncClient',
    'CreateInstanceRequest',
    'DeleteInstanceRequest',
    'DestinationGcsBucket',
    'DestinationParallelstore',
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
    'SourceGcsBucket',
    'SourceParallelstore',
    'TransferCounters',
    'TransferOperationMetadata',
    'UpdateInstanceRequest',
    'DirectoryStripeLevel',
    'FileStripeLevel',
    'TransferType',
)
