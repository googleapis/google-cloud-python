# Copyright 2015 Google Inc. All rights reserved.
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

"""Datastore shim to emulate v1beta3 module structure.

This module intended to pair with query.proto.
"""

from gcloud.datastore import _datastore_v1_pb2


EntityResult = _datastore_v1_pb2.EntityResult
Query = _datastore_v1_pb2.Query
KindExpression = _datastore_v1_pb2.KindExpression
PropertyReference = _datastore_v1_pb2.PropertyReference
PropertyOrder = _datastore_v1_pb2.PropertyOrder
Filter = _datastore_v1_pb2.Filter
CompositeFilter = _datastore_v1_pb2.CompositeFilter
PropertyFilter = _datastore_v1_pb2.PropertyFilter
GqlQuery = _datastore_v1_pb2.GqlQuery
GqlQueryArg = _datastore_v1_pb2.GqlQueryArg
QueryResultBatch = _datastore_v1_pb2.QueryResultBatch
