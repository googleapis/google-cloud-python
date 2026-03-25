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


from bigframes.operations import base_ops
import bigframes.operations.type as op_typing

CosineDistanceOp = base_ops.create_binary_op(
    name="ml_cosine_distance", type_signature=op_typing.VECTOR_METRIC
)
cosine_distance_op = CosineDistanceOp()

ManhattanDistanceOp = base_ops.create_binary_op(
    name="ml_manhattan_distance", type_signature=op_typing.VECTOR_METRIC
)
manhattan_distance_op = ManhattanDistanceOp()

EuclidDistanceOp = base_ops.create_binary_op(
    name="ml_euclidean_distance", type_signature=op_typing.VECTOR_METRIC
)
euclidean_distance_op = EuclidDistanceOp()
