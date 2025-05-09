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

from typing import Any, Dict, List

import google.cloud.bigquery
import google.cloud.bigquery.table
import pytest

import bigframes.core.pyformat as pyformat


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


def test_pyformat_with_unsupported_type_raises_typeerror():
    pyformat_args = {"my_object": object()}
    sql = "SELECT {my_object}"

    with pytest.raises(TypeError, match="my_object has unsupported type: "):
        pyformat.pyformat(sql, pyformat_args=pyformat_args)


def test_pyformat_with_missing_variable_raises_keyerror():
    pyformat_args: Dict[str, Any] = {}
    sql = "SELECT {my_object}"

    with pytest.raises(KeyError, match="my_object"):
        pyformat.pyformat(sql, pyformat_args=pyformat_args)


def test_pyformat_with_no_variables():
    pyformat_args: Dict[str, Any] = {}
    sql = "SELECT '{{escaped curly brackets}}'"
    expected_sql = "SELECT '{escaped curly brackets}'"
    got_sql = pyformat.pyformat(sql, pyformat_args=pyformat_args)
    assert got_sql == expected_sql


def test_pyformat_with_query_string_replaces_variables():
    pyformat_args = {
        "my_string": "some string value",
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
    {my_string} AS my_string,
    {null_value} AS null_value,
    FROM my_dataset.my_table
    WHERE height < {max_value}
    """.strip()

    expected_sql = """
    SELECT 2025 - year  AS age,
    @myparam AS myparam,
    '{my_string}' AS escaped_string,
    'some string value' AS my_string,
    NULL AS null_value,
    FROM my_dataset.my_table
    WHERE height < 2.25
    """.strip()

    got_sql = pyformat.pyformat(sql, pyformat_args=pyformat_args)
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
    ),
)
def test_pyformat_with_table_replaces_variables(table, expected_sql):
    pyformat_args = {
        "table": table,
        # Unreferenced values of unsupported type shouldn't cause issues.
        "my_object": object(),
    }
    sql = "SELECT * FROM {table}"
    got_sql = pyformat.pyformat(sql, pyformat_args=pyformat_args)
    assert got_sql == expected_sql
