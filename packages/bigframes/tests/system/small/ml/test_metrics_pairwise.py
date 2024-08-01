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

import numpy as np
import pandas as pd

from bigframes.ml import metrics
import bigframes.pandas as bpd


def test_paired_cosine_distances():
    x_col = [np.array([4.1, 0.5, 1.0])]
    y_col = [np.array([3.0, 0.0, 2.5])]
    X = bpd.read_pandas(pd.DataFrame({"X": x_col}))
    Y = bpd.read_pandas(pd.DataFrame({"Y": y_col}))

    result = metrics.pairwise.paired_cosine_distances(X, Y)
    expected_pd_df = pd.DataFrame(
        {"X": x_col, "Y": y_col, "cosine_distance": [0.108199]}
    )

    pd.testing.assert_frame_equal(
        result.to_pandas(), expected_pd_df, check_dtype=False, check_index_type=False
    )


def test_paired_cosine_distances_multiindex():
    x_col = [np.array([4.1, 0.5, 1.0])]
    y_col = [np.array([3.0, 0.0, 2.5])]
    data = bpd.read_pandas(
        pd.DataFrame(
            {("DATA", "X"): x_col, ("DATA", "Y"): y_col},
        )
    )

    result = metrics.pairwise.paired_cosine_distances(
        data[("DATA", "X")], data[("DATA", "Y")]
    )
    expected_pd_df = pd.DataFrame(
        {
            ("DATA", "X"): x_col,
            ("DATA", "Y"): y_col,
            ("cosine_distance", ""): [0.108199],
        }
    )

    pd.testing.assert_frame_equal(
        result.to_pandas(), expected_pd_df, check_dtype=False, check_index_type=False
    )


def test_paired_cosine_distances_single_frame():
    x_col = [np.array([4.1, 0.5, 1.0])]
    y_col = [np.array([3.0, 0.0, 2.5])]
    input = bpd.read_pandas(pd.DataFrame({"X": x_col}))
    input["Y"] = y_col  # type: ignore

    result = metrics.pairwise.paired_cosine_distances(input.X, input.Y)
    expected_pd_df = pd.DataFrame(
        {"X": x_col, "Y": y_col, "cosine_distance": [0.108199]}
    )

    pd.testing.assert_frame_equal(
        result.to_pandas(), expected_pd_df, check_dtype=False, check_index_type=False
    )


def test_paired_manhattan_distance():
    x_col = [np.array([4.1, 0.5, 1.0])]
    y_col = [np.array([3.0, 0.0, 2.5])]
    X = bpd.read_pandas(pd.DataFrame({"X": x_col}))
    Y = bpd.read_pandas(pd.DataFrame({"Y": y_col}))

    result = metrics.pairwise.paired_manhattan_distance(X, Y)
    expected_pd_df = pd.DataFrame({"X": x_col, "Y": y_col, "manhattan_distance": [3.1]})

    pd.testing.assert_frame_equal(
        result.to_pandas(), expected_pd_df, check_dtype=False, check_index_type=False
    )


def test_paired_euclidean_distances():
    x_col = [np.array([4.1, 0.5, 1.0])]
    y_col = [np.array([3.0, 0.0, 2.5])]
    X = bpd.read_pandas(pd.DataFrame({"X": x_col}))
    Y = bpd.read_pandas(pd.DataFrame({"Y": y_col}))

    result = metrics.pairwise.paired_euclidean_distances(X, Y)
    expected_pd_df = pd.DataFrame(
        {"X": x_col, "Y": y_col, "euclidean_distance": [1.926136]}
    )

    pd.testing.assert_frame_equal(
        result.to_pandas(), expected_pd_df, check_dtype=False, check_index_type=False
    )
