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

from bigframes.ml import core, utils
import bigframes.pandas as bpd


def paired_cosine_distances(
    X: Union[bpd.DataFrame, bpd.Series], Y: Union[bpd.DataFrame, bpd.Series]
) -> bpd.DataFrame:
    X, Y = utils.convert_to_dataframe(X, Y)
    if len(X.columns) != 1 or len(Y.columns) != 1:
        raise ValueError("Inputs X and Y can only contain 1 column.")

    base_bqml = core.BaseBqml(session=X._session)
    return base_bqml.distance(X, Y, type="COSINE", name="cosine_distance")


paired_cosine_distances.__doc__ = inspect.getdoc(
    vendored_metrics_pairwise.paired_cosine_distances
)


def paired_manhattan_distance(
    X: Union[bpd.DataFrame, bpd.Series], Y: Union[bpd.DataFrame, bpd.Series]
) -> bpd.DataFrame:
    X, Y = utils.convert_to_dataframe(X, Y)
    if len(X.columns) != 1 or len(Y.columns) != 1:
        raise ValueError("Inputs X and Y can only contain 1 column.")

    base_bqml = core.BaseBqml(session=X._session)
    return base_bqml.distance(X, Y, type="MANHATTAN", name="manhattan_distance")


paired_manhattan_distance.__doc__ = inspect.getdoc(
    vendored_metrics_pairwise.paired_manhattan_distance
)


def paired_euclidean_distances(
    X: Union[bpd.DataFrame, bpd.Series], Y: Union[bpd.DataFrame, bpd.Series]
) -> bpd.DataFrame:
    X, Y = utils.convert_to_dataframe(X, Y)
    if len(X.columns) != 1 or len(Y.columns) != 1:
        raise ValueError("Inputs X and Y can only contain 1 column.")

    base_bqml = core.BaseBqml(session=X._session)
    return base_bqml.distance(X, Y, type="EUCLIDEAN", name="euclidean_distance")


paired_euclidean_distances.__doc__ = inspect.getdoc(
    vendored_metrics_pairwise.paired_euclidean_distances
)
