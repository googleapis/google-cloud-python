# Copyright 2023 Google LLC
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

import inspect
from typing import Union

import bigframes_vendored.sklearn.metrics.pairwise as vendored_metrics_pairwise

from bigframes.ml import utils
import bigframes.operations as ops
import bigframes.pandas as bpd


def paired_cosine_distances(
    X: Union[bpd.DataFrame, bpd.Series], Y: Union[bpd.DataFrame, bpd.Series]
) -> bpd.DataFrame:
    X, Y = utils.batch_convert_to_series(X, Y)
    joined_block, _ = X._block.join(Y._block, how="outer")

    result_block, _ = joined_block.project_expr(
        ops.cosine_distance_op.as_expr(
            joined_block.value_columns[0], joined_block.value_columns[1]
        ),
        label="cosine_distance",
    )
    return bpd.DataFrame(result_block)


paired_cosine_distances.__doc__ = inspect.getdoc(
    vendored_metrics_pairwise.paired_cosine_distances
)


def paired_manhattan_distance(
    X: Union[bpd.DataFrame, bpd.Series], Y: Union[bpd.DataFrame, bpd.Series]
) -> bpd.DataFrame:
    X, Y = utils.batch_convert_to_series(X, Y)
    joined_block, _ = X._block.join(Y._block, how="outer")

    result_block, _ = joined_block.project_expr(
        ops.manhattan_distance_op.as_expr(
            joined_block.value_columns[0], joined_block.value_columns[1]
        ),
        label="manhattan_distance",
    )
    return bpd.DataFrame(result_block)


paired_manhattan_distance.__doc__ = inspect.getdoc(
    vendored_metrics_pairwise.paired_manhattan_distance
)


def paired_euclidean_distances(
    X: Union[bpd.DataFrame, bpd.Series], Y: Union[bpd.DataFrame, bpd.Series]
) -> bpd.DataFrame:
    X, Y = utils.batch_convert_to_series(X, Y)
    joined_block, _ = X._block.join(Y._block, how="outer")

    result_block, _ = joined_block.project_expr(
        ops.euclidean_distance_op.as_expr(
            joined_block.value_columns[0], joined_block.value_columns[1]
        ),
        label="euclidean_distance",
    )
    return bpd.DataFrame(result_block)


paired_euclidean_distances.__doc__ = inspect.getdoc(
    vendored_metrics_pairwise.paired_euclidean_distances
)
