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

AndOp = base_ops.create_binary_op(name="and", type_signature=op_typing.LOGICAL)
and_op = AndOp()

OrOp = base_ops.create_binary_op(name="or", type_signature=op_typing.LOGICAL)
or_op = OrOp()

XorOp = base_ops.create_binary_op(name="xor", type_signature=op_typing.LOGICAL)
xor_op = XorOp()
