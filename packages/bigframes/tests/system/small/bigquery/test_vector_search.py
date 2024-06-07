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

import numpy as np
import pandas as pd

import bigframes.bigquery as bbq
import bigframes.pandas as bpd


def test_vector_search_basic_params_with_df():
    search_query = bpd.DataFrame(
        {
            "query_id": ["dog", "cat"],
            "embedding": [[1.0, 2.0], [3.0, 5.2]],
        }
    )
    vector_search_result = bbq.vector_search(
        base_table="bigframes-dev.bigframes_tests_sys.base_table",
        column_to_search="my_embedding",
        query=search_query,
        top_k=2,
    ).to_pandas()  # type:ignore
    expected = pd.DataFrame(
        {
            "query_id": ["cat", "dog", "dog", "cat"],
            "embedding": [
                np.array([3.0, 5.2]),
                np.array([1.0, 2.0]),
                np.array([1.0, 2.0]),
                np.array([3.0, 5.2]),
            ],
            "id": [5, 1, 4, 2],
            "my_embedding": [
                np.array([5.0, 5.4]),
                np.array([1.0, 2.0]),
                np.array([1.0, 3.2]),
                np.array([2.0, 4.0]),
            ],
            "distance": [2.009975, 0.0, 1.2, 1.56205],
        },
        index=pd.Index([1, 0, 0, 1], dtype="Int64"),
    )
    pd.testing.assert_frame_equal(
        vector_search_result, expected, check_dtype=False, rtol=0.1
    )


def test_vector_search_different_params_with_query():
    search_query = bpd.Series([[1.0, 2.0], [3.0, 5.2]])
    vector_search_result = bbq.vector_search(
        base_table="bigframes-dev.bigframes_tests_sys.base_table",
        column_to_search="my_embedding",
        query=search_query,
        distance_type="cosine",
        top_k=2,
    ).to_pandas()  # type:ignore
    expected = pd.DataFrame(
        {
            "0": [
                np.array([1.0, 2.0]),
                np.array([1.0, 2.0]),
                np.array([3.0, 5.2]),
                np.array([3.0, 5.2]),
            ],
            "id": [2, 1, 1, 2],
            "my_embedding": [
                np.array([2.0, 4.0]),
                np.array([1.0, 2.0]),
                np.array([1.0, 2.0]),
                np.array([2.0, 4.0]),
            ],
            "distance": [0.0, 0.0, 0.001777, 0.001777],
        },
        index=pd.Index([0, 0, 1, 1], dtype="Int64"),
    )
    pd.testing.assert_frame_equal(
        vector_search_result, expected, check_dtype=False, rtol=0.1
    )


def test_vector_search_df_with_query_column_to_search():
    search_query = bpd.DataFrame(
        {
            "query_id": ["dog", "cat"],
            "embedding": [[1.0, 2.0], [3.0, 5.2]],
            "another_embedding": [[1.0, 2.5], [3.3, 5.2]],
        }
    )
    vector_search_result = bbq.vector_search(
        base_table="bigframes-dev.bigframes_tests_sys.base_table",
        column_to_search="my_embedding",
        query=search_query,
        query_column_to_search="another_embedding",
        top_k=2,
    ).to_pandas()  # type:ignore
    expected = pd.DataFrame(
        {
            "query_id": ["dog", "dog", "cat", "cat"],
            "embedding": [
                np.array([1.0, 2.0]),
                np.array([1.0, 2.0]),
                np.array([3.0, 5.2]),
                np.array([3.0, 5.2]),
            ],
            "another_embedding": [
                np.array([1.0, 2.5]),
                np.array([1.0, 2.5]),
                np.array([3.3, 5.2]),
                np.array([3.3, 5.2]),
            ],
            "id": [1, 4, 2, 5],
            "my_embedding": [
                np.array([1.0, 2.0]),
                np.array([1.0, 3.2]),
                np.array([2.0, 4.0]),
                np.array([5.0, 5.4]),
            ],
            "distance": [0.5, 0.7, 1.769181, 1.711724],
        },
        index=pd.Index([0, 0, 1, 1], dtype="Int64"),
    )
    pd.testing.assert_frame_equal(
        vector_search_result, expected, check_dtype=False, rtol=0.1
    )
