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

from __future__ import annotations

from bigframes.core import expression
from bigframes.operations import aggregations as agg_ops


def agg(input: str, op: agg_ops.AggregateOp) -> expression.Aggregation:
    if isinstance(op, agg_ops.UnaryAggregateOp):
        return expression.UnaryAggregation(op, expression.deref(input))
    else:
        assert isinstance(op, agg_ops.NullaryAggregateOp)
        return expression.NullaryAggregation(op)
