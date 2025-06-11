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

import random
from typing import Any, cast, Dict, Iterable

import google.cloud.bigquery
import numpy as np
import pandas as pd
import pyarrow
import pytest

import bigframes.bigquery as bbq
import bigframes.pandas as bpd
from bigframes.testing.utils import assert_pandas_df_equal

# Need at least 5,000 rows to create a vector index.
VECTOR_DF = pd.DataFrame(
    {
        "rowid": np.arange(9_999),
        # 3D values, clustered around the three unit vector axes.
        "my_embedding": pd.Series(
            [
                [
                    1 + (random.random() - 0.5) if (row % 3) == 0 else 0,
                    1 + (random.random() - 0.5) if (row % 3) == 1 else 0,
                    1 + (random.random() - 0.5) if (row % 3) == 2 else 0,
                ]
                for row in range(9_999)
            ],
            dtype=pd.ArrowDtype(pyarrow.list_(pyarrow.float64())),
        ),
        # Three groups of animal, vegetable, and mineral, corresponding to
        # the embeddings above.
        "mystery_word": [
            "aarvark",
            "broccoli",
            "calcium",
            "dog",
            "eggplant",
            "ferrite",
            "gopher",
            "huckleberry",
            "ice",
        ]
        * 1_111,
    },
)


@pytest.fixture
def vector_table_id(
    bigquery_client: google.cloud.bigquery.Client,
    # Use non-US location to ensure location autodetection works.
    table_id_not_created: str,
):
    table = google.cloud.bigquery.Table(
        table_id_not_created,
        [
            {"name": "rowid", "type": "INT64"},
            {"name": "my_embedding", "type": "FLOAT64", "mode": "REPEATED"},
            {"name": "mystery_word", "type": "STRING"},
        ],
    )
    bigquery_client.create_table(table)
    bigquery_client.load_table_from_json(
        cast(Iterable[Dict[str, Any]], VECTOR_DF.to_dict(orient="records")),
        table_id_not_created,
    ).result()
    yield table_id_not_created
    bigquery_client.delete_table(table_id_not_created, not_found_ok=True)


def test_create_vector_index_ivf(
    session, vector_table_id: str, bigquery_client: google.cloud.bigquery.Client
):
    bbq.create_vector_index(
        vector_table_id,
        "my_embedding",
        distance_type="cosine",
        stored_column_names=["mystery_word"],
        index_type="ivf",
        ivf_options={"num_lists": 3},
        session=session,
    )

    # Check that the index was created successfully.
    project_id, dataset_id, table_name = vector_table_id.split(".")
    indexes = bigquery_client.query_and_wait(
        f"""
        SELECT index_catalog, index_schema, table_name, index_name, index_column_name
        FROM `{project_id}`.`{dataset_id}`.INFORMATION_SCHEMA.VECTOR_INDEX_COLUMNS
        WHERE table_name = '{table_name}';
        """
    ).to_dataframe()

    # There should only be one vector index.
    assert len(indexes.index) == 1
    assert indexes["index_catalog"].iloc[0] == project_id
    assert indexes["index_schema"].iloc[0] == dataset_id
    assert indexes["table_name"].iloc[0] == table_name
    assert indexes["index_column_name"].iloc[0] == "my_embedding"

    # If no name is specified, use the table name as the index name
    assert indexes["index_name"].iloc[0] == table_name


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
    assert_pandas_df_equal(
        expected.sort_values("id"),
        vector_search_result.sort_values("id"),
        check_dtype=False,
        rtol=0.1,
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
