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
"""Python idiomatic client for Google Cloud Firestore."""

from google.cloud.firestore_v1 import gapic_version as package_version

__version__ = package_version.__version__

from typing import List

from google.cloud.firestore_v1 import (
    DELETE_FIELD,
    SERVER_TIMESTAMP,
    And,
    ArrayRemove,
    ArrayUnion,
    AsyncClient,
    AsyncCollectionReference,
    AsyncDocumentReference,
    AsyncQuery,
    AsyncTransaction,
    AsyncWriteBatch,
    Client,
    CollectionGroup,
    CollectionReference,
    CountAggregation,
    DocumentReference,
    DocumentSnapshot,
    DocumentTransform,
    ExistsOption,
    ExplainOptions,
    FieldFilter,
    GeoPoint,
    Increment,
    LastUpdateOption,
    Maximum,
    Minimum,
    Or,
    Query,
    ReadAfterWriteError,
    Transaction,
    Watch,
    WriteBatch,
    WriteOption,
    async_transactional,
    transactional,
    types,
)

__all__: List[str] = [
    "__version__",
    "And",
    "ArrayRemove",
    "ArrayUnion",
    "AsyncClient",
    "AsyncCollectionReference",
    "AsyncDocumentReference",
    "AsyncQuery",
    "async_transactional",
    "AsyncTransaction",
    "AsyncWriteBatch",
    "Client",
    "CountAggregation",
    "CollectionGroup",
    "CollectionReference",
    "DELETE_FIELD",
    "DocumentReference",
    "DocumentSnapshot",
    "DocumentTransform",
    "ExistsOption",
    "ExplainOptions",
    "FieldFilter",
    "GeoPoint",
    "Increment",
    "LastUpdateOption",
    "Maximum",
    "Minimum",
    "Or",
    "Query",
    "ReadAfterWriteError",
    "SERVER_TIMESTAMP",
    "Transaction",
    "transactional",
    "types",
    "Watch",
    "WriteBatch",
    "WriteOption",
]
