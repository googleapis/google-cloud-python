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
# This file was generated from: scripts/data/sql-functions/global_namespace/date.yaml
# by the script: scripts/generate_bigframes_bigquery.py

import bigframes.bigquery as bbq
import bigframes.core.col
import bigframes.core.expression as ex
import bigframes.operations.googlesql.global_namespace.date as date_op
import bigframes.pandas as bpd


def test_current_date_expression():
    # Call the function with col() expressions
    result = bbq.current_date(
        bpd.col("time_zone_expression"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == date_op._CURRENT_DATE_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 1
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "time_zone_expression"


def test_date_expression():
    # Call the function with col() expressions
    result = bbq.date(
        bpd.col("expression"),
        bpd.col("time_zone_expression"),
        bpd.col("year"),
        bpd.col("month"),
        bpd.col("day"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == date_op._DATE_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 5
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "expression"
    assert isinstance(expr.inputs[1], ex.UnboundVariableExpression)
    assert expr.inputs[1].id == "time_zone_expression"
    assert isinstance(expr.inputs[2], ex.UnboundVariableExpression)
    assert expr.inputs[2].id == "year"
    assert isinstance(expr.inputs[3], ex.UnboundVariableExpression)
    assert expr.inputs[3].id == "month"
    assert isinstance(expr.inputs[4], ex.UnboundVariableExpression)
    assert expr.inputs[4].id == "day"


def test_date_add_expression():
    # Call the function with col() expressions
    result = bbq.date_add(
        bpd.col("date_expression"),
        bpd.col("int64_expression"),
        bpd.col("date_part"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == date_op._DATE_ADD_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 3
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "date_expression"
    assert isinstance(expr.inputs[1], ex.UnboundVariableExpression)
    assert expr.inputs[1].id == "int64_expression"
    assert isinstance(expr.inputs[2], ex.UnboundVariableExpression)
    assert expr.inputs[2].id == "date_part"


def test_date_diff_expression():
    # Call the function with col() expressions
    result = bbq.date_diff(
        bpd.col("end_date"),
        bpd.col("start_date"),
        bpd.col("granularity"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == date_op._DATE_DIFF_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 3
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "end_date"
    assert isinstance(expr.inputs[1], ex.UnboundVariableExpression)
    assert expr.inputs[1].id == "start_date"
    assert isinstance(expr.inputs[2], ex.UnboundVariableExpression)
    assert expr.inputs[2].id == "granularity"


def test_date_from_unix_date_expression():
    # Call the function with col() expressions
    result = bbq.date_from_unix_date(
        bpd.col("int64_expression"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == date_op._DATE_FROM_UNIX_DATE_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 1
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "int64_expression"


def test_date_sub_expression():
    # Call the function with col() expressions
    result = bbq.date_sub(
        bpd.col("date_expression"),
        bpd.col("int64_expression"),
        bpd.col("date_part"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == date_op._DATE_SUB_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 3
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "date_expression"
    assert isinstance(expr.inputs[1], ex.UnboundVariableExpression)
    assert expr.inputs[1].id == "int64_expression"
    assert isinstance(expr.inputs[2], ex.UnboundVariableExpression)
    assert expr.inputs[2].id == "date_part"


def test_date_trunc_expression():
    # Call the function with col() expressions
    result = bbq.date_trunc(
        bpd.col("date_value"),
        bpd.col("granularity"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == date_op._DATE_TRUNC_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 2
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "date_value"
    assert isinstance(expr.inputs[1], ex.UnboundVariableExpression)
    assert expr.inputs[1].id == "granularity"


def test_extract_expression():
    # Call the function with col() expressions
    result = bbq.extract(
        bpd.col("date_expression"),
        bpd.col("part"),
        bpd.col("time_zone"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == date_op._EXTRACT_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 3
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "date_expression"
    assert isinstance(expr.inputs[1], ex.UnboundVariableExpression)
    assert expr.inputs[1].id == "part"
    assert isinstance(expr.inputs[2], ex.UnboundVariableExpression)
    assert expr.inputs[2].id == "time_zone"


def test_format_date_expression():
    # Call the function with col() expressions
    result = bbq.format_date(
        bpd.col("format_string"),
        bpd.col("date_expr"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == date_op._FORMAT_DATE_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 2
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "format_string"
    assert isinstance(expr.inputs[1], ex.UnboundVariableExpression)
    assert expr.inputs[1].id == "date_expr"


def test_generate_date_array_expression():
    # Call the function with col() expressions
    result = bbq.generate_date_array(
        bpd.col("start_date"),
        bpd.col("end_date"),
        bpd.col("int64_expression"),
        bpd.col("date_part"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == date_op._GENERATE_DATE_ARRAY_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 4
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "start_date"
    assert isinstance(expr.inputs[1], ex.UnboundVariableExpression)
    assert expr.inputs[1].id == "end_date"
    assert isinstance(expr.inputs[2], ex.UnboundVariableExpression)
    assert expr.inputs[2].id == "int64_expression"
    assert isinstance(expr.inputs[3], ex.UnboundVariableExpression)
    assert expr.inputs[3].id == "date_part"


def test_last_day_expression():
    # Call the function with col() expressions
    result = bbq.last_day(
        bpd.col("date_expression"),
        bpd.col("date_part"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == date_op._LAST_DAY_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 2
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "date_expression"
    assert isinstance(expr.inputs[1], ex.UnboundVariableExpression)
    assert expr.inputs[1].id == "date_part"


def test_parse_date_expression():
    # Call the function with col() expressions
    result = bbq.parse_date(
        bpd.col("format_string"),
        bpd.col("date_string"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == date_op._PARSE_DATE_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 2
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "format_string"
    assert isinstance(expr.inputs[1], ex.UnboundVariableExpression)
    assert expr.inputs[1].id == "date_string"


def test_unix_date_expression():
    # Call the function with col() expressions
    result = bbq.unix_date(
        bpd.col("date_expression"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == date_op._UNIX_DATE_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 1
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "date_expression"
