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
    result_query = sql.create_vector_search_sql(
        sql_string="SELECT embedding FROM my_embeddings_table WHERE id = 1",
        base_table="my_base_table",
        column_to_search="my_embedding_column",
    )
    assert (
        result_query
        == """
    SELECT
        query.*,
        base.*,
        distance,
    FROM VECTOR_SEARCH(TABLE `my_base_table`,
'my_embedding_column',
(SELECT embedding FROM my_embeddings_table WHERE id = 1))
    """
    )


def test_create_vector_search_sql_all_named_parameters():
    result_query = sql.create_vector_search_sql(
        sql_string="SELECT embedding FROM my_embeddings_table WHERE id = 1",
        base_table="my_base_table",
        column_to_search="my_embedding_column",
        query_column_to_search="another_embedding_column",
        top_k=10,
        distance_type="cosine",
        options={
            "fraction_lists_to_search": 0.1,
            "use_brute_force": False,
        },
    )
    assert (
        result_query
        == """
    SELECT
        query.*,
        base.*,
        distance,
    FROM VECTOR_SEARCH(TABLE `my_base_table`,
'my_embedding_column',
(SELECT embedding FROM my_embeddings_table WHERE id = 1),
query_column_to_search => 'another_embedding_column',
top_k=> 10,
distance_type => 'cosine',
options => '{\\"fraction_lists_to_search\\": 0.1, \\"use_brute_force\\": false}')
    """
    )
