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
# This file was generated from: scripts/data/sql-functions/global_namespace/bit.yaml
# by the script: scripts/generate_bigframes_bigquery.py

import bigframes.bigquery as bbq
import bigframes.core.col
import bigframes.core.expression as ex
import bigframes.operations.googlesql.global_namespace.bit as bit_op
import bigframes.pandas as bpd


def test_bit_count_expression():
    # Call the function with col() expressions
    result = bbq.bit_count(
        bpd.col("expression"),
    )

    # Verify result is a col Expression
    assert isinstance(result, bigframes.core.col.Expression)

    # Verify the internal expression structure
    expr = result._value
    assert isinstance(expr, ex.OpExpression)
    assert expr.op == bit_op._BIT_COUNT_OP

    # Verify arguments are free variables matching the names
    assert len(expr.inputs) == 1
    assert isinstance(expr.inputs[0], ex.UnboundVariableExpression)
    assert expr.inputs[0].id == "expression"
