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

This module intended to pair with datastore.proto.
"""

from gcloud.datastore import _datastore_v1_pb2


LookupRequest = _datastore_v1_pb2.LookupRequest
LookupResponse = _datastore_v1_pb2.LookupResponse
RunQueryRequest = _datastore_v1_pb2.RunQueryRequest
RunQueryResponse = _datastore_v1_pb2.RunQueryResponse
BeginTransactionRequest = _datastore_v1_pb2.BeginTransactionRequest
BeginTransactionResponse = _datastore_v1_pb2.BeginTransactionResponse
RollbackRequest = _datastore_v1_pb2.RollbackRequest
RollbackResponse = _datastore_v1_pb2.RollbackResponse
CommitRequest = _datastore_v1_pb2.CommitRequest
CommitResponse = _datastore_v1_pb2.CommitResponse
AllocateIdsRequest = _datastore_v1_pb2.AllocateIdsRequest
AllocateIdsResponse = _datastore_v1_pb2.AllocateIdsResponse
Mutation = _datastore_v1_pb2.Mutation
MutationResult = _datastore_v1_pb2.MutationResult
ReadOptions = _datastore_v1_pb2.ReadOptions
