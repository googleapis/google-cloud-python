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

import math
import operator
from typing import Optional

import bigframes.operations
from bigframes.operations import (
    aggregations,
    array_ops,
    bool_ops,
    comparison_ops,
    numeric_ops,
    string_ops,
)

PYTHON_TO_BIGFRAMES = {
    ## operators
    operator.add: numeric_ops.add_op,
    operator.sub: numeric_ops.sub_op,
    operator.mul: numeric_ops.mul_op,
    operator.truediv: numeric_ops.div_op,
    operator.floordiv: numeric_ops.floordiv_op,
    operator.mod: numeric_ops.mod_op,
    operator.pow: numeric_ops.pow_op,
    operator.pos: numeric_ops.pos_op,
    operator.neg: numeric_ops.neg_op,
    operator.abs: numeric_ops.abs_op,
    operator.eq: comparison_ops.eq_op,
    operator.ne: comparison_ops.ne_op,
    operator.gt: comparison_ops.gt_op,
    operator.lt: comparison_ops.lt_op,
    operator.ge: comparison_ops.ge_op,
    operator.le: comparison_ops.le_op,
    operator.and_: bool_ops.and_op,
    operator.or_: bool_ops.or_op,
    operator.xor: bool_ops.xor_op,
    ## math
    math.log: numeric_ops.ln_op,
    math.log10: numeric_ops.log10_op,
    math.log1p: numeric_ops.log1p_op,
    math.expm1: numeric_ops.expm1_op,
    math.sin: numeric_ops.sin_op,
    math.cos: numeric_ops.cos_op,
    math.tan: numeric_ops.tan_op,
    math.sinh: numeric_ops.sinh_op,
    math.cosh: numeric_ops.cosh_op,
    math.tanh: numeric_ops.tanh_op,
    math.asin: numeric_ops.arcsin_op,
    math.acos: numeric_ops.arccos_op,
    math.atan: numeric_ops.arctan_op,
    math.floor: numeric_ops.floor_op,
    math.ceil: numeric_ops.ceil_op,
    ## str
    str.upper: string_ops.upper_op,
    str.lower: string_ops.lower_op,
    ## builtins
    len: string_ops.len_op,
    abs: numeric_ops.abs_op,
    pow: numeric_ops.pow_op,
    ### builtins -- iterable
    all: array_ops.ArrayReduceOp(aggregations.all_op),
    any: array_ops.ArrayReduceOp(aggregations.any_op),
    sum: array_ops.ArrayReduceOp(aggregations.sum_op),
    min: array_ops.ArrayReduceOp(aggregations.min_op),
    max: array_ops.ArrayReduceOp(aggregations.max_op),
}


def python_callable_to_op(obj) -> Optional[bigframes.operations.RowOp]:
    if obj in PYTHON_TO_BIGFRAMES:
        return PYTHON_TO_BIGFRAMES[obj]
    return None
