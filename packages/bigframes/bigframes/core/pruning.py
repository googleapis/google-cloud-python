# Copyright 2024 Google LLC
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

from typing import Set, TYPE_CHECKING

import bigframes.core.expression as ex
import bigframes.core.identifiers as ids
import bigframes.core.nodes
import bigframes.dtypes
import bigframes.operations as ops

if TYPE_CHECKING:
    import bigframes.core.nodes


LOW_CARDINALITY_TYPES = [bigframes.dtypes.BOOL_DTYPE]

COMPARISON_OP_TYPES = tuple(
    type(i)
    for i in (
        ops.eq_op,
        ops.eq_null_match_op,
        ops.ne_op,
        ops.gt_op,
        ops.ge_op,
        ops.lt_op,
        ops.le_op,
    )
)


def cluster_cols_for_predicate(
    predicate: ex.Expression, clusterable_cols: Set[ids.ColumnId]
) -> list[ids.ColumnId]:
    """Try to determine cluster col candidates that work with given predicates."""
    # TODO: Prioritize based on predicted selectivity (eg. equality conditions are probably very selective)
    if isinstance(predicate, ex.DerefOp):
        cols = [predicate.id]
    elif isinstance(predicate, ex.OpExpression):
        op = predicate.op
        # TODO: Support geo predicates, which support pruning if clustered (other than st_disjoint)
        # https://cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions
        if isinstance(op, COMPARISON_OP_TYPES):
            cols = cluster_cols_for_comparison(predicate.inputs[0], predicate.inputs[1])
        elif isinstance(op, (type(ops.invert_op))):
            cols = cluster_cols_for_predicate(predicate.inputs[0], clusterable_cols)
        elif isinstance(op, (type(ops.and_op), type(ops.or_op))):
            left_cols = cluster_cols_for_predicate(
                predicate.inputs[0], clusterable_cols
            )
            right_cols = cluster_cols_for_predicate(
                predicate.inputs[1], clusterable_cols
            )
            cols = [*left_cols, *[col for col in right_cols if col not in left_cols]]
        else:
            cols = []
    else:
        # Constant
        cols = []
    return [col for col in cols if col in clusterable_cols]


def cluster_cols_for_comparison(
    left_ex: ex.Expression, right_ex: ex.Expression
) -> list[ids.ColumnId]:
    # TODO: Try to normalize expressions such that one side is a single variable.
    # eg. Convert -cola>=3 to cola<-3 and colb+3 < 4 to colb < 1
    if left_ex.is_const:
        # There are some invertible ops that would also be ok
        if isinstance(right_ex, ex.DerefOp):
            return [right_ex.id]
    elif right_ex.is_const:
        if isinstance(left_ex, ex.DerefOp):
            return [left_ex.id]
    return []
