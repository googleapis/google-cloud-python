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

import pytest
from sqlglot import expressions as sge

from bigframes.core.compile.sqlglot.expressions import op_registration
from bigframes.operations import numeric_ops


def test_register_then_get():
    reg = op_registration.OpRegistration()
    input = sge.to_identifier("A")
    op = numeric_ops.add_op

    @reg.register(numeric_ops.AddOp)
    def test_func(op: numeric_ops.AddOp, input: sge.Expression) -> sge.Expression:
        return input

    assert reg[numeric_ops.add_op](op, input) == test_func(op, input)
    assert reg[numeric_ops.add_op.name](op, input) == test_func(op, input)


def test_register_function_first_argument_is_not_scalar_op_raise_error():
    reg = op_registration.OpRegistration()

    @reg.register(numeric_ops.AddOp)
    def test_func(input: sge.Expression) -> sge.Expression:
        return input

    with pytest.raises(ValueError, match=r".*first parameter must be an operator.*"):
        test_func(sge.to_identifier("A"))
