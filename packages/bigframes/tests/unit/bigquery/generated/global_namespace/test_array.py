# Copyright 2026 Google LLC
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
# DO NOT MODIFY THIS FILE DIRECTLY.
# This file was generated from: scripts/data/sql-functions/global_namespace/array.yaml
# by the script: scripts/generate_bigframes_bigquery.py

import bigframes.bigquery as bbq
import bigframes.core.col
import bigframes.core.expression as ex
import bigframes.operations.googlesql.global_namespace.array as array_op
import bigframes.pandas as bpd


def test_array_concat_expression():
    # Call the function with col() expressions
    result = bbq.array_concat(
        bpd.col("array_expression_1"),
        bpd.col("array_expression_2"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == array_op._ARRAY_CONCAT_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 2
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "array_expression_1"
    assert isinstance(expr.inputs[1], ex.UnboundVariableExpression)
    assert expr.inputs[1].id == "array_expression_2"


def test_array_first_expression():
    # Call the function with col() expressions
    result = bbq.array_first(
        bpd.col("array_expression"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == array_op._ARRAY_FIRST_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 1
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "array_expression"


def test_array_first_n_expression():
    # Call the function with col() expressions
    result = bbq.array_first_n(
        bpd.col("input_array"),
        bpd.col("n"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == array_op._ARRAY_FIRST_N_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 2
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "input_array"
    assert isinstance(expr.inputs[1], ex.UnboundVariableExpression)
    assert expr.inputs[1].id == "n"


def test_array_includes_expression():
    # Call the function with col() expressions
    result = bbq.array_includes(
        bpd.col("array_to_search"),
        bpd.col("search_value"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == array_op._ARRAY_INCLUDES_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 2
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "array_to_search"
    assert isinstance(expr.inputs[1], ex.UnboundVariableExpression)
    assert expr.inputs[1].id == "search_value"


def test_array_includes_all_expression():
    # Call the function with col() expressions
    result = bbq.array_includes_all(
        bpd.col("array_to_search"),
        bpd.col("search_values"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == array_op._ARRAY_INCLUDES_ALL_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 2
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "array_to_search"
    assert isinstance(expr.inputs[1], ex.UnboundVariableExpression)
    assert expr.inputs[1].id == "search_values"


def test_array_includes_any_expression():
    # Call the function with col() expressions
    result = bbq.array_includes_any(
        bpd.col("array_to_search"),
        bpd.col("search_values"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == array_op._ARRAY_INCLUDES_ANY_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 2
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "array_to_search"
    assert isinstance(expr.inputs[1], ex.UnboundVariableExpression)
    assert expr.inputs[1].id == "search_values"


def test_array_is_distinct_expression():
    # Call the function with col() expressions
    result = bbq.array_is_distinct(
        bpd.col("array_expression"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == array_op._ARRAY_IS_DISTINCT_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 1
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "array_expression"


def test_array_last_expression():
    # Call the function with col() expressions
    result = bbq.array_last(
        bpd.col("array_expression"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == array_op._ARRAY_LAST_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 1
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "array_expression"


def test_array_length_expression():
    # Call the function with col() expressions
    result = bbq.array_length(
        bpd.col("series"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == array_op._ARRAY_LENGTH_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 1
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "series"


def test_array_reverse_expression():
    # Call the function with col() expressions
    result = bbq.array_reverse(
        bpd.col("value"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == array_op._ARRAY_REVERSE_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 1
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "value"


def test_array_slice_expression():
    # Call the function with col() expressions
    result = bbq.array_slice(
        bpd.col("array_to_slice"),
        bpd.col("start_offset"),
        bpd.col("end_offset"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == array_op._ARRAY_SLICE_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 3
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "array_to_slice"
    assert isinstance(expr.inputs[1], ex.UnboundVariableExpression)
    assert expr.inputs[1].id == "start_offset"
    assert isinstance(expr.inputs[2], ex.UnboundVariableExpression)
    assert expr.inputs[2].id == "end_offset"


def test_array_to_string_expression():
    # Call the function with col() expressions
    result = bbq.array_to_string(
        bpd.col("series"),
        bpd.col("delimiter"),
        bpd.col("null_text"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == array_op._ARRAY_TO_STRING_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 3
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "series"
    assert isinstance(expr.inputs[1], ex.UnboundVariableExpression)
    assert expr.inputs[1].id == "delimiter"
    assert isinstance(expr.inputs[2], ex.UnboundVariableExpression)
    assert expr.inputs[2].id == "null_text"


def test_flatten_expression():
    # Call the function with col() expressions
    result = bbq.flatten(
        bpd.col("array_to_flatten"),
        bpd.col("depth"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == array_op._FLATTEN_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 2
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "array_to_flatten"
    assert isinstance(expr.inputs[1], ex.UnboundVariableExpression)
    assert expr.inputs[1].id == "depth"


def test_generate_array_expression():
    # Call the function with col() expressions
    result = bbq.generate_array(
        bpd.col("start_expression"),
        bpd.col("end_expression"),
        bpd.col("step_expression"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == array_op._GENERATE_ARRAY_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 3
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "start_expression"
    assert isinstance(expr.inputs[1], ex.UnboundVariableExpression)
    assert expr.inputs[1].id == "end_expression"
    assert isinstance(expr.inputs[2], ex.UnboundVariableExpression)
    assert expr.inputs[2].id == "step_expression"
