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

import datetime
import decimal

import pytest
import shapely  # type: ignore

from bigframes.core import sql


@pytest.mark.parametrize(
    ("value", "expected"),
    (
        # Try to have some literals for each scalar data type:
        # https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types
        (None, "NULL"),
        # TODO: support ARRAY type (possibly another method?)
        (True, "True"),
        (False, "False"),
        (
            b"\x01\x02\x03ABC",
            r"b'\x01\x02\x03ABC'",
        ),
        (
            datetime.date(2025, 1, 1),
            "DATE('2025-01-01')",
        ),
        (
            datetime.datetime(2025, 1, 2, 3, 45, 6, 789123),
            "DATETIME('2025-01-02T03:45:06.789123')",
        ),
        (
            shapely.Point(0, 1),
            "ST_GEOGFROMTEXT('POINT (0 1)')",
        ),
        # TODO: INTERVAL type (e.g. from dateutil.relativedelta)
        # TODO: JSON type (TBD what Python object that would correspond to)
        (123, "123"),
        (decimal.Decimal("123.75"), "CAST('123.75' AS NUMERIC)"),
        # TODO: support BIGNUMERIC by looking at precision/scale of the DECIMAL
        (123.75, "123.75"),
        # TODO: support RANGE type
        ("abc", "'abc'"),
        # TODO: support STRUCT type (possibly another method?)
        (
            datetime.time(12, 34, 56, 789123),
            "TIME(DATETIME('1970-01-01 12:34:56.789123'))",
        ),
        (
            datetime.datetime(
                2025, 1, 2, 3, 45, 6, 789123, tzinfo=datetime.timezone.utc
            ),
            "TIMESTAMP('2025-01-02T03:45:06.789123+00:00')",
        ),
    ),
)
def test_simple_literal(value, expected):
    got = sql.simple_literal(value)
    assert got == expected


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
