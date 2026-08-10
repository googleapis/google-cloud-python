# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for the pyformat feature."""

# TODO(tswast): consolidate with pandas-gbq and bigquery-magics. See:
# https://github.com/googleapis/python-bigquery-magics/blob/main/tests/unit/bigquery/test_pyformat.py

from __future__ import annotations

import datetime
import decimal
from typing import Any, Dict, List

import db_dtypes  # type: ignore
import geopandas  # type: ignore
import google.cloud.bigquery
import google.cloud.bigquery.table
import numpy
import pandas
import pyarrow
import pytest
import shapely.geometry  # type: ignore

from bigframes.core import pyformat
from bigframes.testing import mocks


@pytest.fixture
def session():
    return mocks.create_bigquery_session()


@pytest.mark.parametrize(
    ("sql_template", "expected"),
    (
        (
            "{my_project}.{my_dataset}.{my_table}",
            ["my_project", "my_dataset", "my_table"],
        ),
        (
            "{{not a format variable}}",
            [],
        ),
    ),
)
def test_parse_fields(sql_template: str, expected: List[str]):
    fields = pyformat._parse_fields(sql_template)
    fields.sort()
    expected.sort()
    assert fields == expected


def test_get_error_context_at_pos_invalid_pos():
    assert pyformat.get_error_context_at_pos("SELECT 1", -1) == ""
    assert pyformat.get_error_context_at_pos("SELECT 1", 100) == ""


def test_get_error_context_at_pos_single_line():
    sql = "SELECT {foo}"
    # pos of '{' is 7
    context = pyformat.get_error_context_at_pos(sql, 7)
    expected = "   1: SELECT {foo}\n             ^"
    assert context == expected


def test_get_error_context_at_pos_multi_line():
    sql = "SELECT 1\nFROM my_table\nWHERE col = {foo}\nAND active = True\nLIMIT 10"
    # Lines:
    # 1: SELECT 1 (len 9 including \n)
    # 2: FROM my_table (len 14 including \n) -> total 23
    # 3: WHERE col = {foo} -> '{' is at 23 + 12 = 35

    context = pyformat.get_error_context_at_pos(sql, 35)
    expected = (
        "   1: SELECT 1\n"
        "   2: FROM my_table\n"
        "   3: WHERE col = {foo}\n"
        "                  ^\n"
        "   4: AND active = True\n"
        "   5: LIMIT 10"
    )
    assert context == expected


def test_get_error_context_at_pos_multi_line_limits():
    # Test that it only shows at most 2 lines before and 2 lines after
    sql = (
        "LINE 1\n"
        "LINE 2\n"
        "LINE 3\n"
        "LINE 4\n"
        "LINE 5\n"
        "TARGET {foo}\n"
        "LINE 7\n"
        "LINE 8\n"
        "LINE 9\n"
        "LINE 10"
    )
    # Line lengths:
    # LINE 1\n (7)
    # LINE 2\n (7) -> 14
    # LINE 3\n (7) -> 21
    # LINE 4\n (7) -> 28
    # LINE 5\n (7) -> 35
    # TARGET {foo}\n -> '{' is at 35 + 7 = 42

    context = pyformat.get_error_context_at_pos(sql, 42)
    expected = (
        "   4: LINE 4\n"
        "   5: LINE 5\n"
        "   6: TARGET {foo}\n"
        "             ^\n"
        "   7: LINE 7\n"
        "   8: LINE 8"
    )
    assert context == expected


def test_pyformat_with_unsupported_type_raises_typeerror(session):
    pyformat_args = {"my_object": object()}
    sql = "SELECT {my_object}"

    with pytest.raises(TypeError, match="my_object has unsupported type: "):
        pyformat.pyformat(sql, pyformat_args=pyformat_args, session=session)


def test_pyformat_with_missing_variable_raises_valueerror(session):
    pyformat_args: Dict[str, Any] = {}
    sql = "SELECT {my_object}"

    with pytest.raises(ValueError) as exc_info:
        pyformat.pyformat(sql, pyformat_args=pyformat_args, session=session)

    err_msg = str(exc_info.value)
    assert "Undetected variable 'my_object' in SQL template" in err_msg
    assert "Did you mean to escape '{' and '}'" in err_msg
    assert "   1: SELECT {my_object}" in err_msg
    assert "             ^" in err_msg


def test_pyformat_with_unescaped_braces_raises_valueerror_with_context(session):
    pyformat_args = {"active": True}
    sql = """SELECT * FROM my_table
WHERE json_col = { "generation_config": { "temperature": 0.9 } }
AND active = {active}
"""

    with pytest.raises(ValueError) as exc_info:
        pyformat.pyformat(sql, pyformat_args=pyformat_args, session=session)

    err_msg = str(exc_info.value)
    assert "Undetected variable ' \"generation_config\"' in SQL template" in err_msg
    assert "Did you mean to escape '{' and '}'" in err_msg
    # The triple quote string starts with SELECT immediately, so lines are:
    # 1: SELECT * FROM my_table
    # 2: WHERE json_col = { "generation_config": { "temperature": 0.9 } }
    # 3: AND active = {active}
    assert "   1: SELECT * FROM my_table" in err_msg
    assert (
        '   2: WHERE json_col = { "generation_config": { "temperature": 0.9 } }'
        in err_msg
    )
    assert "                       ^" in err_msg
    assert "   3: AND active = {active}" in err_msg


@pytest.mark.parametrize(
    ("sql_template", "expected_error"),
    (
        pytest.param(
            "SELECT {foo",
            "expected '}' before end of string",
            id="missing_closing_brace",
        ),
        pytest.param(
            "SELECT foo}",
            "Single '}' encountered in format string",
            id="missing_opening_brace",
        ),
    ),
)
def test_pyformat_with_malformed_template_raises_valueerror(
    session, sql_template: str, expected_error: str
):
    pyformat_args: Dict[str, Any] = {}

    # Case 1: Single '{' (unmatched)
    with pytest.raises(ValueError) as exc_info:
        pyformat.pyformat(sql_template, pyformat_args=pyformat_args, session=session)

    error_message = str(exc_info.value)
    assert "Failed to parse SQL template" in error_message
    assert "Did you mean to escape '{' and '}'" in error_message
    assert expected_error in error_message


def test_pyformat_with_no_variables(session):
    pyformat_args: Dict[str, Any] = {}
    sql = "SELECT '{{escaped curly brackets}}'"
    expected_sql = "SELECT '{escaped curly brackets}'"
    got_sql = pyformat.pyformat(sql, pyformat_args=pyformat_args, session=session)
    assert got_sql == expected_sql


@pytest.mark.parametrize(
    ("df_pd", "expected_struct"),
    (
        pytest.param(
            pandas.DataFrame(),
            "STRUCT<>",
            id="empty",
        ),
        pytest.param(
            # Empty columns default to floating point, just like pandas.
            pandas.DataFrame({"empty column": []}),
            "STRUCT<`empty column` FLOAT64>",
            id="empty column",
        ),
        # Regression tests for b/428190014.
        #
        # Test every BigQuery type we support, especially those where the legacy
        # SQL type name differs from the GoogleSQL type name.
        #
        # See:
        # https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types
        # and compare to the legacy types at
        # https://cloud.google.com/bigquery/docs/data-types
        #
        # Test these against the real BigQuery dry run API in
        # tests/system/small/pandas/io/api/test_read_gbq_colab.py
        pytest.param(
            pandas.DataFrame(
                {
                    "ints": pandas.Series(
                        [[1], [2], [3]],
                        dtype=pandas.ArrowDtype(pyarrow.list_(pyarrow.int64())),
                    ),
                    "floats": pandas.Series(
                        [[1.0], [2.0], [3.0]],
                        dtype=pandas.ArrowDtype(pyarrow.list_(pyarrow.float64())),
                    ),
                }
            ),
            "STRUCT<`ints` ARRAY<INT64>, `floats` ARRAY<FLOAT64>>",
            id="arrays",
        ),
        pytest.param(
            pandas.DataFrame(
                {
                    "bool": pandas.Series([True, False, True], dtype="bool"),
                    "boolean": pandas.Series([True, None, True], dtype="boolean"),
                    "object": pandas.Series([True, None, True], dtype="object"),
                    "arrow": pandas.Series(
                        [True, None, True], dtype=pandas.ArrowDtype(pyarrow.bool_())
                    ),
                }
            ),
            "STRUCT<`bool` BOOL, `boolean` BOOL, `object` BOOL, `arrow` BOOL>",
            id="bools",
        ),
        pytest.param(
            pandas.DataFrame(
                {
                    "bytes": pandas.Series([b"a", b"b", b"c"], dtype=numpy.bytes_),
                    "object": pandas.Series([b"a", None, b"c"], dtype="object"),
                    "arrow": pandas.Series(
                        [b"a", None, b"c"], dtype=pandas.ArrowDtype(pyarrow.binary())
                    ),
                }
            ),
            "STRUCT<`bytes` BYTES, `object` BYTES, `arrow` BYTES>",
            id="bytes",
        ),
        pytest.param(
            pandas.DataFrame(
                {
                    "object": pandas.Series(
                        [
                            datetime.date(2023, 11, 23),
                            None,
                            datetime.date(1970, 1, 1),
                        ],
                        dtype="object",
                    ),
                    "arrow": pandas.Series(
                        [
                            datetime.date(2023, 11, 23),
                            None,
                            datetime.date(1970, 1, 1),
                        ],
                        dtype=pandas.ArrowDtype(pyarrow.date32()),
                    ),
                }
            ),
            "STRUCT<`object` DATE, `arrow` DATE>",
            id="dates",
        ),
        pytest.param(
            pandas.DataFrame(
                {
                    "object": pandas.Series(
                        [
                            datetime.datetime(2023, 11, 23, 13, 14, 15),
                            None,
                            datetime.datetime(1970, 1, 1, 0, 0, 0),
                        ],
                        dtype="object",
                    ),
                    "datetime64": pandas.Series(
                        [
                            datetime.datetime(2023, 11, 23, 13, 14, 15),
                            None,
                            datetime.datetime(1970, 1, 1, 0, 0, 0),
                        ],
                        dtype="datetime64[us]",
                    ),
                    "arrow": pandas.Series(
                        [
                            datetime.datetime(2023, 11, 23, 13, 14, 15),
                            None,
                            datetime.datetime(1970, 1, 1, 0, 0, 0),
                        ],
                        dtype=pandas.ArrowDtype(pyarrow.timestamp("us")),
                    ),
                }
            ),
            "STRUCT<`object` DATETIME, `datetime64` DATETIME, `arrow` DATETIME>",
            id="datetimes",
        ),
        pytest.param(
            pandas.DataFrame(
                {
                    "object": pandas.Series(
                        [
                            shapely.geometry.Point(145.0, -37.8),
                            None,
                            shapely.geometry.Point(-122.3, 47.6),
                        ],
                        dtype="object",
                    ),
                    "geopandas": geopandas.GeoSeries(
                        [
                            shapely.geometry.Point(145.0, -37.8),
                            None,
                            shapely.geometry.Point(-122.3, 47.6),
                        ]
                    ),
                }
            ),
            "STRUCT<`object` GEOGRAPHY, `geopandas` GEOGRAPHY>",
            id="geographys",
        ),
        # TODO(tswast): Add INTERVAL once BigFrames supports it.
        pytest.param(
            pandas.DataFrame(
                {
                    # TODO(tswast): Is there an equivalent object type we can use here?
                    # TODO(tswast): Add built-in Arrow extension type
                    "db_dtypes": pandas.Series(
                        ["{}", None, "123"],
                        dtype=pandas.ArrowDtype(db_dtypes.JSONArrowType()),
                    ),
                }
            ),
            "STRUCT<`db_dtypes` JSON>",
            id="jsons",
        ),
        pytest.param(
            pandas.DataFrame(
                {
                    "int64": pandas.Series([1, 2, 3], dtype="int64"),
                    "Int64": pandas.Series([1, None, 3], dtype="Int64"),
                    "object": pandas.Series([1, None, 3], dtype="object"),
                    "arrow": pandas.Series(
                        [1, None, 3], dtype=pandas.ArrowDtype(pyarrow.int64())
                    ),
                }
            ),
            "STRUCT<`int64` INT64, `Int64` INT64, `object` INT64, `arrow` INT64>",
            id="ints",
        ),
        pytest.param(
            pandas.DataFrame(
                {
                    "object": pandas.Series(
                        [decimal.Decimal("1.23"), None, decimal.Decimal("4.56")],
                        dtype="object",
                    ),
                    "arrow": pandas.Series(
                        [decimal.Decimal("1.23"), None, decimal.Decimal("4.56")],
                        dtype=pandas.ArrowDtype(pyarrow.decimal128(38, 9)),
                    ),
                }
            ),
            "STRUCT<`object` NUMERIC, `arrow` NUMERIC>",
            id="numerics",
        ),
        pytest.param(
            pandas.DataFrame(
                {
                    # TODO(tswast): Add object type for BIGNUMERIC. Can bigframes disambiguate?
                    "arrow": pandas.Series(
                        [decimal.Decimal("1.23"), None, decimal.Decimal("4.56")],
                        dtype=pandas.ArrowDtype(pyarrow.decimal256(76, 38)),
                    ),
                }
            ),
            "STRUCT<`arrow` BIGNUMERIC>",
            id="bignumerics",
        ),
        pytest.param(
            pandas.DataFrame(
                {
                    "float64": pandas.Series([1.23, None, 4.56], dtype="float64"),
                    "Float64": pandas.Series([1.23, None, 4.56], dtype="Float64"),
                    "object": pandas.Series([1.23, None, 4.56], dtype="object"),
                    "arrow": pandas.Series(
                        [1.23, None, 4.56], dtype=pandas.ArrowDtype(pyarrow.float64())
                    ),
                }
            ),
            "STRUCT<`float64` FLOAT64, `Float64` FLOAT64, `object` FLOAT64, `arrow` FLOAT64>",
            id="floats",
        ),
        # TODO(tswast): Add RANGE once BigFrames supports it.
        pytest.param(
            pandas.DataFrame(
                {
                    "string": pandas.Series(["a", "b", "c"], dtype="string[python]"),
                    "object": pandas.Series(["a", None, "c"], dtype="object"),
                    "arrow": pandas.Series(["a", None, "c"], dtype="string[pyarrow]"),
                }
            ),
            "STRUCT<`string` STRING, `object` STRING, `arrow` STRING>",
            id="strings",
        ),
        pytest.param(
            pandas.DataFrame(
                {
                    # TODO(tswast): Add object type for STRUCT? How to tell apart from JSON?
                    "arrow": pandas.Series(
                        [{"a": 1, "b": 1.0, "c": "c"}],
                        dtype=pandas.ArrowDtype(
                            pyarrow.struct(
                                [
                                    ("a", pyarrow.int64()),
                                    ("b", pyarrow.float64()),
                                    ("c", pyarrow.string()),
                                ]
                            )
                        ),
                    ),
                }
            ),
            "STRUCT<`arrow` STRUCT<`a` INT64, `b` FLOAT64, `c` STRING>>",
            id="structs",
        ),
        pytest.param(
            pandas.DataFrame(
                {
                    "object": pandas.Series(
                        [
                            datetime.time(0, 0, 0),
                            None,
                            datetime.time(13, 7, 11),
                        ],
                        dtype="object",
                    ),
                    "arrow": pandas.Series(
                        [
                            datetime.time(0, 0, 0),
                            None,
                            datetime.time(13, 7, 11),
                        ],
                        dtype=pandas.ArrowDtype(pyarrow.time64("us")),
                    ),
                }
            ),
            "STRUCT<`object` TIME, `arrow` TIME>",
            id="times",
        ),
        pytest.param(
            pandas.DataFrame(
                {
                    "object": pandas.Series(
                        [
                            datetime.datetime(
                                2023, 11, 23, 13, 14, 15, tzinfo=datetime.timezone.utc
                            ),
                            None,
                            datetime.datetime(
                                1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc
                            ),
                        ],
                        dtype="object",
                    ),
                    "datetime64": pandas.Series(
                        [
                            datetime.datetime(2023, 11, 23, 13, 14, 15),
                            None,
                            datetime.datetime(1970, 1, 1, 0, 0, 0),
                        ],
                        dtype="datetime64[us]",
                    ).dt.tz_localize("UTC"),
                    "arrow": pandas.Series(
                        [
                            datetime.datetime(
                                2023, 11, 23, 13, 14, 15, tzinfo=datetime.timezone.utc
                            ),
                            None,
                            datetime.datetime(
                                1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc
                            ),
                        ],
                        dtype=pandas.ArrowDtype(pyarrow.timestamp("us", "UTC")),
                    ),
                }
            ),
            "STRUCT<`object` TIMESTAMP, `datetime64` TIMESTAMP, `arrow` TIMESTAMP>",
            id="timestamps",
        ),
        # More complicated edge cases:
        pytest.param(
            pandas.DataFrame(
                {
                    "array of struct col": [
                        [{"subfield": {"subsubfield": 1}, "subfield2": 2}],
                    ],
                }
            ),
            "STRUCT<`array of struct col` ARRAY<STRUCT<`subfield` STRUCT<`subsubfield` INT64>, `subfield2` INT64>>>",
            id="array_of_structs",
        ),
        pytest.param(
            pandas.DataFrame({"c1": [1, 2, 3], "c2": ["a", "b", "c"]}).rename(
                columns={"c1": "c", "c2": "c"}
            ),
            "STRUCT<`c` INT64, `c_1` STRING>",
            id="duplicate_column_names",
        ),
    ),
)
def test_pyformat_with_pandas_dataframe_dry_run_no_session(df_pd, expected_struct):
    pyformat_args: Dict[str, Any] = {"my_pandas_df": df_pd}
    sql = "SELECT * FROM {my_pandas_df}"
    expected_sql = f"SELECT * FROM UNNEST(ARRAY<{expected_struct}>[])"
    got_sql = pyformat.pyformat(
        sql, pyformat_args=pyformat_args, dry_run=True, session=None
    )
    assert got_sql == expected_sql


def test_pyformat_with_pandas_dataframe_not_dry_run_no_session_raises_valueerror():
    pyformat_args: Dict[str, Any] = {"my_pandas_df": pandas.DataFrame()}
    sql = "SELECT * FROM {my_pandas_df}"

    with pytest.raises(ValueError, match="my_pandas_df"):
        pyformat.pyformat(sql, pyformat_args=pyformat_args)


def test_pyformat_with_query_string_replaces_variables(session):
    pyformat_args = {
        "my_string": "`my_table`",
        "max_value": 2.25,
        "year": 2025,
        "null_value": None,
        # Unreferenced values of unsupported type shouldn't cause issues.
        "my_object": object(),
    }

    sql = """
    SELECT {year} - year  AS age,
    @myparam AS myparam,
    '{{my_string}}' AS escaped_string,
    *
    FROM {my_string}
    WHERE height < {max_value}
    """.strip()

    expected_sql = """
    SELECT 2025 - year  AS age,
    @myparam AS myparam,
    '{my_string}' AS escaped_string,
    *
    FROM `my_table`
    WHERE height < 2.25
    """.strip()

    got_sql = pyformat.pyformat(sql, pyformat_args=pyformat_args, session=session)
    assert got_sql == expected_sql


@pytest.mark.parametrize(
    ("table", "expected_sql"),
    (
        (
            google.cloud.bigquery.Table("my-project.my_dataset.my_table"),
            "SELECT * FROM `my-project`.`my_dataset`.`my_table`",
        ),
        (
            google.cloud.bigquery.TableReference(
                google.cloud.bigquery.DatasetReference("some-project", "some_dataset"),
                "some_table",
            ),
            "SELECT * FROM `some-project`.`some_dataset`.`some_table`",
        ),
        (
            google.cloud.bigquery.table.TableListItem(
                {
                    "tableReference": {
                        "projectId": "ListedProject",
                        "datasetId": "ListedDataset",
                        "tableId": "ListedTable",
                    }
                }
            ),
            "SELECT * FROM `ListedProject`.`ListedDataset`.`ListedTable`",
        ),
        (
            google.cloud.bigquery.TableReference(
                google.cloud.bigquery.DatasetReference(
                    "my-project", "my-catalog.my-namespace"
                ),
                "my-table",
            ),
            "SELECT * FROM `my-project`.`my-catalog`.`my-namespace`.`my-table`",
        ),
    ),
)
def test_pyformat_with_table_replaces_variables(table, expected_sql, session=session):
    pyformat_args = {
        "table": table,
        # Unreferenced values of unsupported type shouldn't cause issues.
        "my_object": object(),
    }
    sql = "SELECT * FROM {table}"
    got_sql = pyformat.pyformat(sql, pyformat_args=pyformat_args, session=session)
    assert got_sql == expected_sql


def test_pyformat_with_bigframes_dataframe_biglake_table(session):
    # Create a real BigFrames DataFrame that points to a BigLake table.
    import bigframes.core.array_value as array_value
    import bigframes.core.blocks as blocks
    import bigframes.core.bq_data as bq_data
    import bigframes.dataframe

    # Define the BigLake table
    project_id = "my-project"
    catalog_id = "my-catalog"
    namespace_id = "my-namespace"
    table_id = "my-table"
    schema = (google.cloud.bigquery.SchemaField("col", "INTEGER"),)

    biglake_table = bq_data.BiglakeIcebergTable(
        project_id=project_id,
        catalog_id=catalog_id,
        namespace_id=namespace_id,
        table_id=table_id,
        physical_schema=schema,
        cluster_cols=(),
        metadata=bq_data.TableMetadata(
            location=bq_data.BigQueryRegion("us-central1"),
            type="TABLE",
        ),
    )

    # ArrayValue.from_table is what read_gbq uses.
    av = array_value.ArrayValue.from_table(biglake_table, session)
    block = blocks.Block(av, index_columns=[], column_labels=["col"])
    df = bigframes.dataframe.DataFrame(block)

    pyformat_args = {"df": df}
    sql = "SELECT * FROM {df}"

    got_sql = pyformat.pyformat(sql, pyformat_args=pyformat_args, session=session)

    # For BigLake, we now expect a SUBQUERY, not a view reference.
    # The subquery should have correctly quoted 4-part ID.
    assert "SELECT" in got_sql
    assert project_id in got_sql
    assert catalog_id in got_sql
    assert namespace_id in got_sql
    assert table_id in got_sql
    assert got_sql.startswith("SELECT * FROM (SELECT")
    assert got_sql.endswith(")")
