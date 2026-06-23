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
# This file was generated from: scripts/data/sql-functions/global_namespace/conversion.yaml
# by the script: scripts/generate_bigframes_bigquery.py

import bigframes.bigquery as bbq
import bigframes.core.col
import bigframes.core.expression as ex
import bigframes.operations.googlesql.global_namespace.conversion as conversion_op
import bigframes.pandas as bpd


def test_bool__expression():
    # Call the function with col() expressions
    result = bbq.bool_(
        bpd.col("json_string_expression"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == conversion_op._BOOL_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 1
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "json_string_expression"


def test_double_expression():
    # Call the function with col() expressions
    result = bbq.double(
        bpd.col("json_string_expression"),
        bpd.col("wide_number_mode"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == conversion_op._DOUBLE_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 2
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "json_string_expression"
    assert isinstance(expr.inputs[1], ex.UnboundVariableExpression)
    assert expr.inputs[1].id == "wide_number_mode"


def test_float64_expression():
    # Call the function with col() expressions
    result = bbq.float64(
        bpd.col("json_string_expression"),
        bpd.col("wide_number_mode"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == conversion_op._FLOAT64_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 2
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "json_string_expression"
    assert isinstance(expr.inputs[1], ex.UnboundVariableExpression)
    assert expr.inputs[1].id == "wide_number_mode"


def test_int64_expression():
    # Call the function with col() expressions
    result = bbq.int64(
        bpd.col("json_string_expression"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == conversion_op._INT64_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 1
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "json_string_expression"


def test_parse_bignumeric_expression():
    # Call the function with col() expressions
    result = bbq.parse_bignumeric(
        bpd.col("string_expression"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == conversion_op._PARSE_BIGNUMERIC_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 1
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "string_expression"


def test_parse_numeric_expression():
    # Call the function with col() expressions
    result = bbq.parse_numeric(
        bpd.col("string_expression"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == conversion_op._PARSE_NUMERIC_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 1
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "string_expression"


def test_string_expression():
    # Call the function with col() expressions
    result = bbq.string(
        bpd.col("expression"),
        bpd.col("timezone"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == conversion_op._STRING_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 2
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "expression"
    assert isinstance(expr.inputs[1], ex.UnboundVariableExpression)
    assert expr.inputs[1].id == "timezone"
