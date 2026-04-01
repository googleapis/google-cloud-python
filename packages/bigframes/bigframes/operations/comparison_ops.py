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

EqOp = base_ops.create_binary_op(name="eq", type_signature=op_typing.COMPARISON)
eq_op = EqOp()

EqNullsMatchOp = base_ops.create_binary_op(
    name="eq_nulls_match", type_signature=op_typing.COMPARISON
)
eq_null_match_op = EqNullsMatchOp()

NeOp = base_ops.create_binary_op(name="ne", type_signature=op_typing.COMPARISON)
ne_op = NeOp()

LtOp = base_ops.create_binary_op(name="lt", type_signature=op_typing.COMPARISON)
lt_op = LtOp()

GtOp = base_ops.create_binary_op(name="gt", type_signature=op_typing.COMPARISON)
gt_op = GtOp()

LeOp = base_ops.create_binary_op(name="le", type_signature=op_typing.COMPARISON)
le_op = LeOp()

GeOp = base_ops.create_binary_op(name="ge", type_signature=op_typing.COMPARISON)
ge_op = GeOp()
