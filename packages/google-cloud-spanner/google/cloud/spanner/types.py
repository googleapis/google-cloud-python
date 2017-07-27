# Copyright 2017 Google Inc. All rights reserved.
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

"""Types exported from this package."""

from google.cloud.proto.spanner.v1 import type_pb2


# Scalar paramter types
STRING_PARAM_TYPE = type_pb2.Type(code=type_pb2.STRING)
BYTES_PARAM_TYPE = type_pb2.Type(code=type_pb2.BYTES)
BOOL_PARAM_TYPE = type_pb2.Type(code=type_pb2.BOOL)
INT64_PARAM_TYPE = type_pb2.Type(code=type_pb2.INT64)
FLOAT64_PARAM_TYPE = type_pb2.Type(code=type_pb2.FLOAT64)
DATE_PARAM_TYPE = type_pb2.Type(code=type_pb2.DATE)
TIMESTAMP_PARAM_TYPE = type_pb2.Type(code=type_pb2.TIMESTAMP)
