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
from google.cloud.bigquery_storage import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.bigquery_storage_v1alpha.services.metastore_partition_service.client import MetastorePartitionServiceClient
from google.cloud.bigquery_storage_v1alpha.services.metastore_partition_service.async_client import MetastorePartitionServiceAsyncClient

from google.cloud.bigquery_storage_v1alpha.types.metastore_partition import BatchCreateMetastorePartitionsRequest
from google.cloud.bigquery_storage_v1alpha.types.metastore_partition import BatchCreateMetastorePartitionsResponse
from google.cloud.bigquery_storage_v1alpha.types.metastore_partition import BatchDeleteMetastorePartitionsRequest
from google.cloud.bigquery_storage_v1alpha.types.metastore_partition import BatchSizeTooLargeError
from google.cloud.bigquery_storage_v1alpha.types.metastore_partition import BatchUpdateMetastorePartitionsRequest
from google.cloud.bigquery_storage_v1alpha.types.metastore_partition import BatchUpdateMetastorePartitionsResponse
from google.cloud.bigquery_storage_v1alpha.types.metastore_partition import CreateMetastorePartitionRequest
from google.cloud.bigquery_storage_v1alpha.types.metastore_partition import ListMetastorePartitionsRequest
from google.cloud.bigquery_storage_v1alpha.types.metastore_partition import ListMetastorePartitionsResponse
from google.cloud.bigquery_storage_v1alpha.types.metastore_partition import StreamMetastorePartitionsRequest
from google.cloud.bigquery_storage_v1alpha.types.metastore_partition import StreamMetastorePartitionsResponse
from google.cloud.bigquery_storage_v1alpha.types.metastore_partition import UpdateMetastorePartitionRequest
from google.cloud.bigquery_storage_v1alpha.types.partition import FieldSchema
from google.cloud.bigquery_storage_v1alpha.types.partition import MetastorePartition
from google.cloud.bigquery_storage_v1alpha.types.partition import MetastorePartitionList
from google.cloud.bigquery_storage_v1alpha.types.partition import MetastorePartitionValues
from google.cloud.bigquery_storage_v1alpha.types.partition import ReadStream
from google.cloud.bigquery_storage_v1alpha.types.partition import SerDeInfo
from google.cloud.bigquery_storage_v1alpha.types.partition import StorageDescriptor
from google.cloud.bigquery_storage_v1alpha.types.partition import StreamList

__all__ = ('MetastorePartitionServiceClient',
    'MetastorePartitionServiceAsyncClient',
    'BatchCreateMetastorePartitionsRequest',
    'BatchCreateMetastorePartitionsResponse',
    'BatchDeleteMetastorePartitionsRequest',
    'BatchSizeTooLargeError',
    'BatchUpdateMetastorePartitionsRequest',
    'BatchUpdateMetastorePartitionsResponse',
    'CreateMetastorePartitionRequest',
    'ListMetastorePartitionsRequest',
    'ListMetastorePartitionsResponse',
    'StreamMetastorePartitionsRequest',
    'StreamMetastorePartitionsResponse',
    'UpdateMetastorePartitionRequest',
    'FieldSchema',
    'MetastorePartition',
    'MetastorePartitionList',
    'MetastorePartitionValues',
    'ReadStream',
    'SerDeInfo',
    'StorageDescriptor',
    'StreamList',
)
