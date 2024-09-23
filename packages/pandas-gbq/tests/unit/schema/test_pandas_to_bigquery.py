# Copyright (c) 2019 pandas-gbq Authors All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import collections
import datetime
import operator

from google.cloud.bigquery import schema
import pandas
import pytest


@pytest.fixture
def module_under_test():
    from pandas_gbq.schema import pandas_to_bigquery

    return pandas_to_bigquery


def test_dataframe_to_bigquery_fields_w_named_index(module_under_test):
    df_data = collections.OrderedDict(
        [
            ("str_column", ["hello", "world"]),
            ("int_column", [42, 8]),
            ("bool_column", [True, False]),
        ]
    )
    index = pandas.Index(["a", "b"], name="str_index")
    dataframe = pandas.DataFrame(df_data, index=index)

    returned_schema = module_under_test.dataframe_to_bigquery_fields(
        dataframe, [], index=True
    )

    expected_schema = (
        schema.SchemaField("str_index", "STRING", "NULLABLE"),
        schema.SchemaField("str_column", "STRING", "NULLABLE"),
        schema.SchemaField("int_column", "INTEGER", "NULLABLE"),
        schema.SchemaField("bool_column", "BOOLEAN", "NULLABLE"),
    )
    assert returned_schema == expected_schema


def test_dataframe_to_bigquery_fields_w_multiindex(module_under_test):
    df_data = collections.OrderedDict(
        [
            ("str_column", ["hello", "world"]),
            ("int_column", [42, 8]),
            ("bool_column", [True, False]),
        ]
    )
    index = pandas.MultiIndex.from_tuples(
        [
            ("a", 0, datetime.datetime(1999, 12, 31, 23, 59, 59, 999999)),
            ("a", 0, datetime.datetime(2000, 1, 1, 0, 0, 0)),
        ],
        names=["str_index", "int_index", "dt_index"],
    )
    dataframe = pandas.DataFrame(df_data, index=index)

    returned_schema = module_under_test.dataframe_to_bigquery_fields(
        dataframe, [], index=True
    )

    expected_schema = (
        schema.SchemaField("str_index", "STRING", "NULLABLE"),
        schema.SchemaField("int_index", "INTEGER", "NULLABLE"),
        schema.SchemaField("dt_index", "DATETIME", "NULLABLE"),
        schema.SchemaField("str_column", "STRING", "NULLABLE"),
        schema.SchemaField("int_column", "INTEGER", "NULLABLE"),
        schema.SchemaField("bool_column", "BOOLEAN", "NULLABLE"),
    )
    assert returned_schema == expected_schema


def test_dataframe_to_bigquery_fields_w_bq_schema(module_under_test):
    df_data = collections.OrderedDict(
        [
            ("str_column", ["hello", "world"]),
            ("int_column", [42, 8]),
            ("bool_column", [True, False]),
        ]
    )
    dataframe = pandas.DataFrame(df_data)

    dict_schema = [
        {"name": "str_column", "type": "STRING", "mode": "NULLABLE"},
        {"name": "bool_column", "type": "BOOL", "mode": "REQUIRED"},
    ]

    returned_schema = module_under_test.dataframe_to_bigquery_fields(
        dataframe, dict_schema
    )

    expected_schema = (
        schema.SchemaField("str_column", "STRING", "NULLABLE"),
        schema.SchemaField("int_column", "INTEGER", "NULLABLE"),
        schema.SchemaField("bool_column", "BOOL", "REQUIRED"),
    )
    assert returned_schema == expected_schema


def test_dataframe_to_bigquery_fields_fallback_needed_w_pyarrow(module_under_test):
    dataframe = pandas.DataFrame(
        data=[
            {"id": 10, "status": "FOO", "created_at": datetime.date(2019, 5, 10)},
            {"id": 20, "status": "BAR", "created_at": datetime.date(2018, 9, 12)},
        ]
    )

    detected_schema = module_under_test.dataframe_to_bigquery_fields(
        dataframe, override_bigquery_fields=[]
    )
    expected_schema = (
        schema.SchemaField("id", "INTEGER", mode="NULLABLE"),
        schema.SchemaField("status", "STRING", mode="NULLABLE"),
        schema.SchemaField("created_at", "DATE", mode="NULLABLE"),
    )
    by_name = operator.attrgetter("name")
    assert sorted(detected_schema, key=by_name) == sorted(expected_schema, key=by_name)


def test_dataframe_to_bigquery_fields_w_extra_fields(module_under_test):
    with pytest.raises(ValueError) as exc_context:
        module_under_test.dataframe_to_bigquery_fields(
            pandas.DataFrame(),
            override_bigquery_fields=(schema.SchemaField("not_in_df", "STRING"),),
        )
    message = str(exc_context.value)
    assert (
        "Provided BigQuery fields contain field(s) not present in DataFrame:" in message
    )
    assert "not_in_df" in message


def test_dataframe_to_bigquery_fields_geography(module_under_test):
    geopandas = pytest.importorskip("geopandas")
    from shapely import wkt

    df = geopandas.GeoDataFrame(
        pandas.DataFrame(
            dict(
                name=["foo", "bar"],
                geo1=[None, None],
                geo2=[None, wkt.loads("Point(1 1)")],
            )
        ),
        geometry="geo1",
    )
    bq_schema = module_under_test.dataframe_to_bigquery_fields(df, [])
    assert bq_schema == (
        schema.SchemaField("name", "STRING"),
        schema.SchemaField("geo1", "GEOGRAPHY"),
        schema.SchemaField("geo2", "GEOGRAPHY"),
    )
