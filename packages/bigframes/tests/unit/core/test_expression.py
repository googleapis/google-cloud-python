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

import bigframes.core.expression as ex
import bigframes.dtypes as dtypes
import bigframes.operations as ops


def test_expression_dtype_simple():
    expression = ops.add_op.as_expr("a", "b")
    result = expression.output_type({"a": dtypes.INT_DTYPE, "b": dtypes.INT_DTYPE})
    assert result == dtypes.INT_DTYPE


def test_expression_dtype_nested():
    expression = ops.add_op.as_expr(
        "a", ops.abs_op.as_expr(ops.sub_op.as_expr("b", ex.const(3.14)))
    )

    result = expression.output_type({"a": dtypes.INT_DTYPE, "b": dtypes.INT_DTYPE})

    assert result == dtypes.FLOAT_DTYPE


def test_expression_dtype_where():
    expression = ops.where_op.as_expr(ex.const(3), ex.const(True), ex.const(None))

    result = expression.output_type({})

    assert result == dtypes.INT_DTYPE


def test_expression_dtype_astype():
    expression = ops.AsTypeOp("Int64").as_expr(ex.const(3.14159))

    result = expression.output_type({})

    assert result == dtypes.INT_DTYPE
