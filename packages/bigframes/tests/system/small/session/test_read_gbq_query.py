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

import datetime

import pytest

import bigframes
import bigframes.core.nodes as nodes


def test_read_gbq_query_w_allow_large_results(session: bigframes.Session):
    if not hasattr(session.bqclient, "default_job_creation_mode"):
        pytest.skip("Jobless query only available on newer google-cloud-bigquery.")

    query = "SELECT 1"

    # Make sure we don't get a cached table.
    configuration = {"query": {"useQueryCache": False}}

    # Very small results should wrap a local node.
    df_false = session.read_gbq(
        query,
        configuration=configuration,
        allow_large_results=False,
    )
    assert df_false.shape == (1, 1)
    nodes_false = df_false._get_block().expr.node.unique_nodes()
    assert any(isinstance(node, nodes.ReadLocalNode) for node in nodes_false)
    assert not any(isinstance(node, nodes.ReadTableNode) for node in nodes_false)

    # Large results allowed should wrap a table.
    df_true = session.read_gbq(
        query,
        configuration=configuration,
        allow_large_results=True,
    )
    assert df_true.shape == (1, 1)
    nodes_true = df_true._get_block().expr.node.unique_nodes()
    assert any(isinstance(node, nodes.ReadTableNode) for node in nodes_true)


def test_read_gbq_query_w_columns(session: bigframes.Session):
    query = """
    SELECT 1 as int_col,
    'a' as str_col,
    TIMESTAMP('2025-08-21 10:41:32.123456') as timestamp_col
    """

    result = session.read_gbq(
        query,
        columns=["timestamp_col", "int_col"],
    )
    assert list(result.columns) == ["timestamp_col", "int_col"]
    assert result.to_dict(orient="records") == [
        {
            "timestamp_col": datetime.datetime(
                2025, 8, 21, 10, 41, 32, 123456, tzinfo=datetime.timezone.utc
            ),
            "int_col": 1,
        }
    ]


@pytest.mark.parametrize(
    ("index_col", "expected_index_names"),
    (
        pytest.param(
            "my_custom_index",
            ("my_custom_index",),
            id="string",
        ),
        pytest.param(
            ("my_custom_index",),
            ("my_custom_index",),
            id="iterable",
        ),
        pytest.param(
            ("my_custom_index", "int_col"),
            ("my_custom_index", "int_col"),
            id="multiindex",
        ),
    ),
)
def test_read_gbq_query_w_index_col(
    session: bigframes.Session, index_col, expected_index_names
):
    query = """
    SELECT 1 as int_col,
    'a' as str_col,
    0 as my_custom_index,
    TIMESTAMP('2025-08-21 10:41:32.123456') as timestamp_col
    """

    result = session.read_gbq(
        query,
        index_col=index_col,
    )
    assert tuple(result.index.names) == expected_index_names
    assert frozenset(result.columns) == frozenset(
        {"int_col", "str_col", "my_custom_index", "timestamp_col"}
    ) - frozenset(expected_index_names)
