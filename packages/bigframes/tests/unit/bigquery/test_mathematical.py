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

import bigframes.bigquery as bbq
import bigframes.core.col as col
import bigframes.core.expression as ex
import bigframes.dtypes as dtypes
import bigframes.operations as ops


def test_rand_returns_expression():
    expr = bbq.rand()

    assert isinstance(expr, col.Expression)
    node = expr._value
    assert isinstance(node, ex.OpExpression)
    op = node.op
    assert isinstance(op, ops.SqlScalarOp)
    assert op.sql_template == "RAND()"
    assert op._output_type == dtypes.FLOAT_DTYPE
    assert not op.is_deterministic
    assert len(node.inputs) == 0
