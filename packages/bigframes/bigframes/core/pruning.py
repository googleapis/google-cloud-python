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

import bigframes.core.expression as ex
import bigframes.core.schema as schemata
import bigframes.dtypes
import bigframes.operations as ops

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
    predicate: ex.Expression, schema: schemata.ArraySchema
) -> list[str]:
    """Try to determine cluster col candidates that work with given predicates."""
    # TODO: Prioritize based on predicted selectivity (eg. equality conditions are probably very selective)
    if isinstance(predicate, ex.UnboundVariableExpression):
        cols = [predicate.id]
    elif isinstance(predicate, ex.OpExpression):
        op = predicate.op
        # TODO: Support geo predicates, which support pruning if clustered (other than st_disjoint)
        # https://cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions
        if isinstance(op, COMPARISON_OP_TYPES):
            cols = cluster_cols_for_comparison(predicate.inputs[0], predicate.inputs[1])
        elif isinstance(op, (type(ops.invert_op))):
            cols = cluster_cols_for_predicate(predicate.inputs[0], schema)
        elif isinstance(op, (type(ops.and_op), type(ops.or_op))):
            left_cols = cluster_cols_for_predicate(predicate.inputs[0], schema)
            right_cols = cluster_cols_for_predicate(predicate.inputs[1], schema)
            cols = [*left_cols, *[col for col in right_cols if col not in left_cols]]
        else:
            cols = []
    else:
        # Constant
        cols = []
    return [
        col for col in cols if bigframes.dtypes.is_clusterable(schema.get_type(col))
    ]


def cluster_cols_for_comparison(
    left_ex: ex.Expression, right_ex: ex.Expression
) -> list[str]:
    # TODO: Try to normalize expressions such that one side is a single variable.
    # eg. Convert -cola>=3 to cola<-3 and colb+3 < 4 to colb < 1
    if left_ex.is_const:
        # There are some invertible ops that would also be ok
        if isinstance(right_ex, ex.UnboundVariableExpression):
            return [right_ex.id]
    elif right_ex.is_const:
        if isinstance(left_ex, ex.UnboundVariableExpression):
            return [left_ex.id]
    return []
