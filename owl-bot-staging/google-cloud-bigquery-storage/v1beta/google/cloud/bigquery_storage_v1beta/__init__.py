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
from google.cloud.bigquery_storage_v1beta import gapic_version as package_version

__version__ = package_version.__version__


from .services.metastore_partition_service import MetastorePartitionServiceClient
from .services.metastore_partition_service import MetastorePartitionServiceAsyncClient

from .types.metastore_partition import BatchCreateMetastorePartitionsRequest
from .types.metastore_partition import BatchCreateMetastorePartitionsResponse
from .types.metastore_partition import BatchDeleteMetastorePartitionsRequest
from .types.metastore_partition import BatchSizeTooLargeError
from .types.metastore_partition import BatchUpdateMetastorePartitionsRequest
from .types.metastore_partition import BatchUpdateMetastorePartitionsResponse
from .types.metastore_partition import CreateMetastorePartitionRequest
from .types.metastore_partition import ListMetastorePartitionsRequest
from .types.metastore_partition import ListMetastorePartitionsResponse
from .types.metastore_partition import StreamMetastorePartitionsRequest
from .types.metastore_partition import StreamMetastorePartitionsResponse
from .types.metastore_partition import UpdateMetastorePartitionRequest
from .types.partition import FieldSchema
from .types.partition import MetastorePartition
from .types.partition import MetastorePartitionList
from .types.partition import MetastorePartitionValues
from .types.partition import ReadStream
from .types.partition import SerDeInfo
from .types.partition import StorageDescriptor
from .types.partition import StreamList

__all__ = (
    'MetastorePartitionServiceAsyncClient',
'BatchCreateMetastorePartitionsRequest',
'BatchCreateMetastorePartitionsResponse',
'BatchDeleteMetastorePartitionsRequest',
'BatchSizeTooLargeError',
'BatchUpdateMetastorePartitionsRequest',
'BatchUpdateMetastorePartitionsResponse',
'CreateMetastorePartitionRequest',
'FieldSchema',
'ListMetastorePartitionsRequest',
'ListMetastorePartitionsResponse',
'MetastorePartition',
'MetastorePartitionList',
'MetastorePartitionServiceClient',
'MetastorePartitionValues',
'ReadStream',
'SerDeInfo',
'StorageDescriptor',
'StreamList',
'StreamMetastorePartitionsRequest',
'StreamMetastorePartitionsResponse',
'UpdateMetastorePartitionRequest',
)
