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


"""Python idiomatic client for Google Cloud Firestore."""

from pkg_resources import get_distribution

__version__ = get_distribution("google-cloud-firestore").version

from google.cloud.firestore_v1beta1 import types
from google.cloud.firestore_v1beta1._helpers import GeoPoint
from google.cloud.firestore_v1beta1._helpers import ExistsOption
from google.cloud.firestore_v1beta1._helpers import LastUpdateOption
from google.cloud.firestore_v1beta1._helpers import ReadAfterWriteError
from google.cloud.firestore_v1beta1._helpers import WriteOption
from google.cloud.firestore_v1beta1.batch import WriteBatch
from google.cloud.firestore_v1beta1.client import Client
from google.cloud.firestore_v1beta1.collection import CollectionReference
from google.cloud.firestore_v1beta1.transforms import ArrayRemove
from google.cloud.firestore_v1beta1.transforms import ArrayUnion
from google.cloud.firestore_v1beta1.transforms import DELETE_FIELD
from google.cloud.firestore_v1beta1.transforms import SERVER_TIMESTAMP
from google.cloud.firestore_v1beta1.document import DocumentReference
from google.cloud.firestore_v1beta1.document import DocumentSnapshot
from google.cloud.firestore_v1beta1.query import Query
from google.cloud.firestore_v1beta1.transaction import Transaction
from google.cloud.firestore_v1beta1.transaction import transactional
from google.cloud.firestore_v1beta1.watch import Watch


from .services.firestore import FirestoreClient
from .types.common import DocumentMask
from .types.common import Precondition
from .types.common import TransactionOptions
from .types.document import ArrayValue
from .types.document import Document
from .types.document import MapValue
from .types.document import Value
from .types.firestore import BatchGetDocumentsRequest
from .types.firestore import BatchGetDocumentsResponse
from .types.firestore import BeginTransactionRequest
from .types.firestore import BeginTransactionResponse
from .types.firestore import CommitRequest
from .types.firestore import CommitResponse
from .types.firestore import CreateDocumentRequest
from .types.firestore import DeleteDocumentRequest
from .types.firestore import GetDocumentRequest
from .types.firestore import ListCollectionIdsRequest
from .types.firestore import ListCollectionIdsResponse
from .types.firestore import ListDocumentsRequest
from .types.firestore import ListDocumentsResponse
from .types.firestore import ListenRequest
from .types.firestore import ListenResponse
from .types.firestore import RollbackRequest
from .types.firestore import RunQueryRequest
from .types.firestore import RunQueryResponse
from .types.firestore import Target
from .types.firestore import TargetChange
from .types.firestore import UpdateDocumentRequest
from .types.firestore import WriteRequest
from .types.firestore import WriteResponse
from .types.query import Cursor
from .types.query import StructuredQuery
from .types.write import DocumentChange
from .types.write import DocumentDelete
from .types.write import DocumentRemove
from .types.write import DocumentTransform
from .types.write import ExistenceFilter
from .types.write import Write
from .types.write import WriteResult


__all__ = (
    "ArrayValue",
    "BatchGetDocumentsRequest",
    "BatchGetDocumentsResponse",
    "BeginTransactionRequest",
    "BeginTransactionResponse",
    "CommitRequest",
    "CommitResponse",
    "CreateDocumentRequest",
    "Cursor",
    "DeleteDocumentRequest",
    "Document",
    "DocumentChange",
    "DocumentDelete",
    "DocumentMask",
    "DocumentRemove",
    "DocumentTransform",
    "ExistenceFilter",
    "GetDocumentRequest",
    "ListCollectionIdsRequest",
    "ListCollectionIdsResponse",
    "ListDocumentsRequest",
    "ListDocumentsResponse",
    "ListenRequest",
    "ListenResponse",
    "MapValue",
    "Precondition",
    "RollbackRequest",
    "RunQueryRequest",
    "RunQueryResponse",
    "StructuredQuery",
    "Target",
    "TargetChange",
    "TransactionOptions",
    "UpdateDocumentRequest",
    "Value",
    "Write",
    "WriteRequest",
    "WriteResponse",
    "WriteResult",
    "FirestoreClient",
    "__version__",
    "ArrayRemove",
    "ArrayUnion",
    "Client",
    "CollectionReference",
    "DELETE_FIELD",
    "DocumentReference",
    "DocumentSnapshot",
    "ExistsOption",
    "GeoPoint",
    "LastUpdateOption",
    "Query",
    "ReadAfterWriteError",
    "SERVER_TIMESTAMP",
    "Transaction",
    "transactional",
    "types",
    "Watch",
    "WriteBatch",
    "WriteOption",
)
