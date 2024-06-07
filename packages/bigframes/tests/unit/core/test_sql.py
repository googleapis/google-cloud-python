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


from bigframes.core import sql


def test_create_vector_search_sql_simple():
    sql_string = "SELECT embedding FROM my_embeddings_table WHERE id = 1"
    options = {
        "base_table": "my_base_table",
        "column_to_search": "my_embedding_column",
        "distance_type": "COSINE",
        "top_k": 10,
        "use_brute_force": False,
    }

    expected_query = f"""
    SELECT
        query.*,
        base.*,
        distance,
    FROM VECTOR_SEARCH(
        TABLE `my_base_table`,
        'my_embedding_column',
        ({sql_string}),
        distance_type => 'COSINE',
        top_k => 10
    )
    """

    result_query = sql.create_vector_search_sql(
        sql_string, options  # type:ignore
    )
    assert result_query == expected_query


def test_create_vector_search_sql_query_column_to_search():
    sql_string = "SELECT embedding FROM my_embeddings_table WHERE id = 1"
    options = {
        "base_table": "my_base_table",
        "column_to_search": "my_embedding_column",
        "distance_type": "COSINE",
        "top_k": 10,
        "query_column_to_search": "new_embedding_column",
        "use_brute_force": False,
    }

    expected_query = f"""
    SELECT
        query.*,
        base.*,
        distance,
    FROM VECTOR_SEARCH(
        TABLE `my_base_table`,
        'my_embedding_column',
        ({sql_string}),
        'new_embedding_column',
        distance_type => 'COSINE',
        top_k => 10
    )
    """

    result_query = sql.create_vector_search_sql(
        sql_string, options  # type:ignore
    )
    assert result_query == expected_query
