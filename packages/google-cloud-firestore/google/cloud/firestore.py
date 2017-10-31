# Copyright 2017 Google LLC All rights reserved.
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

"""Python idiomatic client for Google Cloud Firestore."""


from google.cloud.firestore_v1beta1 import __version__
from google.cloud.firestore_v1beta1 import AdminClient
from google.cloud.firestore_v1beta1 import Client
from google.cloud.firestore_v1beta1 import CollectionReference
from google.cloud.firestore_v1beta1 import CreateIfMissingOption
from google.cloud.firestore_v1beta1 import DELETE_FIELD
from google.cloud.firestore_v1beta1 import DocumentReference
from google.cloud.firestore_v1beta1 import DocumentSnapshot
from google.cloud.firestore_v1beta1 import enums
from google.cloud.firestore_v1beta1 import ExistsOption
from google.cloud.firestore_v1beta1 import GeoPoint
from google.cloud.firestore_v1beta1 import LastUpdateOption
from google.cloud.firestore_v1beta1 import Query
from google.cloud.firestore_v1beta1 import ReadAfterWriteError
from google.cloud.firestore_v1beta1 import SERVER_TIMESTAMP
from google.cloud.firestore_v1beta1 import Transaction
from google.cloud.firestore_v1beta1 import transactional
from google.cloud.firestore_v1beta1 import types
from google.cloud.firestore_v1beta1 import WriteBatch
from google.cloud.firestore_v1beta1 import WriteOption


__all__ = [
    '__version__',
    'AdminClient',
    'Client',
    'CollectionReference',
    'CreateIfMissingOption',
    'DELETE_FIELD',
    'DocumentReference',
    'DocumentSnapshot',
    'enums',
    'ExistsOption',
    'GeoPoint',
    'LastUpdateOption',
    'Query',
    'ReadAfterWriteError',
    'SERVER_TIMESTAMP',
    'Transaction',
    'transactional',
    'types',
    'WriteBatch',
    'WriteOption',
]
