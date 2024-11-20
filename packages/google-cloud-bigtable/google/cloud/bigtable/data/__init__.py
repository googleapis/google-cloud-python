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
from google.cloud.bigtable import gapic_version as package_version

from google.cloud.bigtable.data._async.client import BigtableDataClientAsync
from google.cloud.bigtable.data._async.client import TableAsync

from google.cloud.bigtable.data._async.mutations_batcher import MutationsBatcherAsync

from google.cloud.bigtable.data.read_rows_query import ReadRowsQuery
from google.cloud.bigtable.data.read_rows_query import RowRange
from google.cloud.bigtable.data.row import Row
from google.cloud.bigtable.data.row import Cell

from google.cloud.bigtable.data.mutations import Mutation
from google.cloud.bigtable.data.mutations import RowMutationEntry
from google.cloud.bigtable.data.mutations import SetCell
from google.cloud.bigtable.data.mutations import DeleteRangeFromColumn
from google.cloud.bigtable.data.mutations import DeleteAllFromFamily
from google.cloud.bigtable.data.mutations import DeleteAllFromRow

from google.cloud.bigtable.data.exceptions import InvalidChunk
from google.cloud.bigtable.data.exceptions import FailedMutationEntryError
from google.cloud.bigtable.data.exceptions import FailedQueryShardError

from google.cloud.bigtable.data.exceptions import RetryExceptionGroup
from google.cloud.bigtable.data.exceptions import MutationsExceptionGroup
from google.cloud.bigtable.data.exceptions import ShardedReadRowsExceptionGroup
from google.cloud.bigtable.data.exceptions import ParameterTypeInferenceFailed

from google.cloud.bigtable.data._helpers import TABLE_DEFAULT
from google.cloud.bigtable.data._helpers import RowKeySamples
from google.cloud.bigtable.data._helpers import ShardedQuery

# setup custom CrossSync mappings for library
from google.cloud.bigtable_v2.services.bigtable.async_client import (
    BigtableAsyncClient,
)
from google.cloud.bigtable.data._async._read_rows import _ReadRowsOperationAsync
from google.cloud.bigtable.data._async._mutate_rows import _MutateRowsOperationAsync

from google.cloud.bigtable.data._cross_sync import CrossSync

CrossSync.add_mapping("GapicClient", BigtableAsyncClient)
CrossSync.add_mapping("_ReadRowsOperation", _ReadRowsOperationAsync)
CrossSync.add_mapping("_MutateRowsOperation", _MutateRowsOperationAsync)
CrossSync.add_mapping("MutationsBatcher", MutationsBatcherAsync)


__version__: str = package_version.__version__

__all__ = (
    "BigtableDataClientAsync",
    "TableAsync",
    "MutationsBatcherAsync",
    "RowKeySamples",
    "ReadRowsQuery",
    "RowRange",
    "Mutation",
    "RowMutationEntry",
    "SetCell",
    "DeleteRangeFromColumn",
    "DeleteAllFromFamily",
    "DeleteAllFromRow",
    "Row",
    "Cell",
    "InvalidChunk",
    "FailedMutationEntryError",
    "FailedQueryShardError",
    "RetryExceptionGroup",
    "MutationsExceptionGroup",
    "ShardedReadRowsExceptionGroup",
    "ParameterTypeInferenceFailed",
    "ShardedQuery",
    "TABLE_DEFAULT",
)
