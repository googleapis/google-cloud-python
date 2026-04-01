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

import typing

import pytest

from bigframes.core import field
import bigframes.core.expression as ex
import bigframes.core.identifiers as ids
import bigframes.dtypes as dtypes
import bigframes.operations as ops


def test_simple_expression_dtype():
    expression = ops.add_op.as_expr("a", "b")
    field_bindings = _create_field_bindings(
        {"a": dtypes.INT_DTYPE, "b": dtypes.INT_DTYPE}
    )

    result = ex.bind_schema_fields(expression, field_bindings)

    _assert_output_type(result, dtypes.INT_DTYPE)


def test_nested_expression_dtype():
    expression = ops.add_op.as_expr(
        "a", ops.abs_op.as_expr(ops.sub_op.as_expr("b", ex.const(3.14)))
    )
    field_bindings = _create_field_bindings(
        {"a": dtypes.INT_DTYPE, "b": dtypes.INT_DTYPE}
    )

    result = ex.bind_schema_fields(expression, field_bindings)

    _assert_output_type(result, dtypes.FLOAT_DTYPE)


def test_where_op_dtype():
    expression = ops.where_op.as_expr(ex.const(3), ex.const(True), ex.const(None))

    _assert_output_type(expression, dtypes.INT_DTYPE)


def test_astype_op_dtype():
    expression = ops.AsTypeOp(dtypes.INT_DTYPE).as_expr(ex.const(3.14159))

    _assert_output_type(expression, dtypes.INT_DTYPE)


def test_deref_op_dtype_unavailable():
    expression = ex.deref("mycol")

    assert not expression.is_resolved
    with pytest.raises(ValueError):
        expression.output_type


def test_deref_op_dtype_resolution():
    expression = ex.deref("mycol")
    field_bindings = _create_field_bindings({"mycol": dtypes.STRING_DTYPE})

    result = ex.bind_schema_fields(expression, field_bindings)

    _assert_output_type(result, dtypes.STRING_DTYPE)


def test_field_ref_expr_dtype_resolution_short_circuit():
    expression = ex.ResolvedDerefOp(
        id=ids.ColumnId("mycol"), dtype=dtypes.INT_DTYPE, is_nullable=True
    )
    field_bindings = _create_field_bindings({"anotherCol": dtypes.STRING_DTYPE})

    result = ex.bind_schema_fields(expression, field_bindings)

    _assert_output_type(result, dtypes.INT_DTYPE)


def test_nested_expression_dtypes_are_cached():
    expression = ops.add_op.as_expr(ex.deref("left_col"), ex.deref("right_col"))
    field_bindings = _create_field_bindings(
        {
            "right_col": dtypes.INT_DTYPE,
            "left_col": dtypes.FLOAT_DTYPE,
        }
    )

    result = ex.bind_schema_fields(expression, field_bindings)

    _assert_output_type(result, dtypes.FLOAT_DTYPE)
    assert isinstance(result, ex.OpExpression)
    _assert_output_type(result.inputs[0], dtypes.FLOAT_DTYPE)
    _assert_output_type(result.inputs[1], dtypes.INT_DTYPE)


def _create_field_bindings(
    col_dtypes: typing.Dict[str, dtypes.Dtype]
) -> typing.Dict[ids.ColumnId, field.Field]:
    return {
        ids.ColumnId(col): field.Field(ids.ColumnId(col), dtype)
        for col, dtype in col_dtypes.items()
    }


def _assert_output_type(expr: ex.Expression, dtype: dtypes.Dtype):
    assert expr.is_resolved
    assert expr.output_type == dtype
