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
import re

import pytest
import shapely.geometry  # type: ignore

from bigframes.core import sql


@pytest.mark.parametrize(
    ("value", "expected_pattern"),
    (
        # Try to have some literals for each scalar data type:
        # https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types
        (None, "NULL"),
        # TODO: support ARRAY type (possibly another method?)
        (True, "True"),
        (False, "False"),
        (
            b"\x01\x02\x03ABC",
            re.escape(r"b'\x01\x02\x03ABC'"),
        ),
        (
            datetime.date(2025, 1, 1),
            re.escape("DATE('2025-01-01')"),
        ),
        (
            datetime.datetime(2025, 1, 2, 3, 45, 6, 789123),
            re.escape("DATETIME('2025-01-02T03:45:06.789123')"),
        ),
        (
            shapely.geometry.Point(0, 1),
            r"ST_GEOGFROMTEXT\('POINT \(0[.]?0* 1[.]?0*\)'\)",
        ),
        # TODO: INTERVAL type (e.g. from dateutil.relativedelta)
        # TODO: JSON type (TBD what Python object that would correspond to)
        (123, re.escape("123")),
        (decimal.Decimal("123.75"), re.escape("CAST('123.75' AS NUMERIC)")),
        # TODO: support BIGNUMERIC by looking at precision/scale of the DECIMAL
        (123.75, re.escape("123.75")),
        # TODO: support RANGE type
        ("abc", re.escape("'abc'")),
        # TODO: support STRUCT type (possibly another method?)
        (
            datetime.time(12, 34, 56, 789123),
            re.escape("TIME(DATETIME('1970-01-01 12:34:56.789123'))"),
        ),
        (
            datetime.datetime(
                2025, 1, 2, 3, 45, 6, 789123, tzinfo=datetime.timezone.utc
            ),
            re.escape("TIMESTAMP('2025-01-02T03:45:06.789123+00:00')"),
        ),
    ),
)
def test_simple_literal(value, expected_pattern):
    got = sql.simple_literal(value)
    assert re.match(expected_pattern, got) is not None


@pytest.mark.parametrize(
    ("value", "expected_pattern"),
    (
        # Try to have some list of literals for each scalar data type:
        # https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types
        ([None, None], re.escape("[NULL, NULL]")),
        ([True, False], re.escape("[True, False]")),
        (
            [b"\x01\x02\x03ABC", b"\x01\x02\x03ABC"],
            re.escape("[b'\\x01\\x02\\x03ABC', b'\\x01\\x02\\x03ABC']"),
        ),
        (
            [datetime.date(2025, 1, 1), datetime.date(2025, 1, 1)],
            re.escape("[DATE('2025-01-01'), DATE('2025-01-01')]"),
        ),
        (
            [datetime.datetime(2025, 1, 2, 3, 45, 6, 789123)],
            re.escape("[DATETIME('2025-01-02T03:45:06.789123')]"),
        ),
        (
            [shapely.geometry.Point(0, 1), shapely.geometry.Point(0, 2)],
            r"\[ST_GEOGFROMTEXT\('POINT \(0[.]?0* 1[.]?0*\)'\), ST_GEOGFROMTEXT\('POINT \(0[.]?0* 2[.]?0*\)'\)\]",
        ),
        # TODO: INTERVAL type (e.g. from dateutil.relativedelta)
        # TODO: JSON type (TBD what Python object that would correspond to)
        ([123, 456], re.escape("[123, 456]")),
        (
            [decimal.Decimal("123.75"), decimal.Decimal("456.78")],
            re.escape("[CAST('123.75' AS NUMERIC), CAST('456.78' AS NUMERIC)]"),
        ),
        # TODO: support BIGNUMERIC by looking at precision/scale of the DECIMAL
        ([123.75, 456.78], re.escape("[123.75, 456.78]")),
        # TODO: support RANGE type
        (["abc", "def"], re.escape("['abc', 'def']")),
        # TODO: support STRUCT type (possibly another method?)
        (
            [datetime.time(12, 34, 56, 789123), datetime.time(11, 25, 56, 789123)],
            re.escape(
                "[TIME(DATETIME('1970-01-01 12:34:56.789123')), TIME(DATETIME('1970-01-01 11:25:56.789123'))]"
            ),
        ),
        (
            [
                datetime.datetime(
                    2025, 1, 2, 3, 45, 6, 789123, tzinfo=datetime.timezone.utc
                ),
                datetime.datetime(
                    2025, 2, 1, 4, 45, 6, 789123, tzinfo=datetime.timezone.utc
                ),
            ],
            re.escape(
                "[TIMESTAMP('2025-01-02T03:45:06.789123+00:00'), TIMESTAMP('2025-02-01T04:45:06.789123+00:00')]"
            ),
        ),
    ),
)
def test_simple_literal_w_list(value: list, expected_pattern: str):
    got = sql.simple_literal(value)
    assert re.match(expected_pattern, got) is not None


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
