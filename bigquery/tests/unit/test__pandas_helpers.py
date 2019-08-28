# Copyright 2019 Google LLC
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

import collections
import datetime
import decimal
import functools
import warnings

import mock

try:
    import pandas
    import pandas.api.types
    import pandas.testing
except ImportError:  # pragma: NO COVER
    pandas = None
try:
    import pyarrow
    import pyarrow.types
except ImportError:  # pragma: NO COVER
    pyarrow = None
import pytest
import pytz

from google.cloud.bigquery import schema


@pytest.fixture
def module_under_test():
    from google.cloud.bigquery import _pandas_helpers

    return _pandas_helpers


def is_none(value):
    return value is None


def is_datetime(type_):
    # See: https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#datetime-type
    return all_(
        pyarrow.types.is_timestamp,
        lambda type_: type_.unit == "us",
        lambda type_: type_.tz is None,
    )(type_)


def is_numeric(type_):
    # See: https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#numeric-type
    return all_(
        pyarrow.types.is_decimal,
        lambda type_: type_.precision == 38,
        lambda type_: type_.scale == 9,
    )(type_)


def is_timestamp(type_):
    # See: https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#timestamp-type
    return all_(
        pyarrow.types.is_timestamp,
        lambda type_: type_.unit == "us",
        lambda type_: type_.tz == "UTC",
    )(type_)


def do_all(functions, value):
    return all((func(value) for func in functions))


def all_(*functions):
    return functools.partial(do_all, functions)


@pytest.mark.skipif(pyarrow is None, reason="Requires `pyarrow`")
def test_is_datetime():
    assert is_datetime(pyarrow.timestamp("us", tz=None))
    assert not is_datetime(pyarrow.timestamp("ms", tz=None))
    assert not is_datetime(pyarrow.timestamp("us", tz="UTC"))
    assert not is_datetime(pyarrow.string())


def test_do_all():
    assert do_all((lambda _: True, lambda _: True), None)
    assert not do_all((lambda _: True, lambda _: False), None)
    assert not do_all((lambda _: False,), None)


def test_all_():
    assert all_(lambda _: True, lambda _: True)(None)
    assert not all_(lambda _: True, lambda _: False)(None)


@pytest.mark.parametrize(
    "bq_type,bq_mode,is_correct_type",
    [
        ("STRING", "NULLABLE", pyarrow.types.is_string),
        ("STRING", None, pyarrow.types.is_string),
        ("string", "NULLABLE", pyarrow.types.is_string),
        ("StRiNg", "NULLABLE", pyarrow.types.is_string),
        ("BYTES", "NULLABLE", pyarrow.types.is_binary),
        ("INTEGER", "NULLABLE", pyarrow.types.is_int64),
        ("INT64", "NULLABLE", pyarrow.types.is_int64),
        ("FLOAT", "NULLABLE", pyarrow.types.is_float64),
        ("FLOAT64", "NULLABLE", pyarrow.types.is_float64),
        ("NUMERIC", "NULLABLE", is_numeric),
        ("BOOLEAN", "NULLABLE", pyarrow.types.is_boolean),
        ("BOOL", "NULLABLE", pyarrow.types.is_boolean),
        ("TIMESTAMP", "NULLABLE", is_timestamp),
        ("DATE", "NULLABLE", pyarrow.types.is_date32),
        ("TIME", "NULLABLE", pyarrow.types.is_time64),
        ("DATETIME", "NULLABLE", is_datetime),
        ("GEOGRAPHY", "NULLABLE", pyarrow.types.is_string),
        ("UNKNOWN_TYPE", "NULLABLE", is_none),
        # Use pyarrow.list_(item_type) for repeated (array) fields.
        (
            "STRING",
            "REPEATED",
            all_(
                pyarrow.types.is_list,
                lambda type_: pyarrow.types.is_string(type_.value_type),
            ),
        ),
        (
            "STRING",
            "repeated",
            all_(
                pyarrow.types.is_list,
                lambda type_: pyarrow.types.is_string(type_.value_type),
            ),
        ),
        (
            "STRING",
            "RePeAtEd",
            all_(
                pyarrow.types.is_list,
                lambda type_: pyarrow.types.is_string(type_.value_type),
            ),
        ),
        (
            "BYTES",
            "REPEATED",
            all_(
                pyarrow.types.is_list,
                lambda type_: pyarrow.types.is_binary(type_.value_type),
            ),
        ),
        (
            "INTEGER",
            "REPEATED",
            all_(
                pyarrow.types.is_list,
                lambda type_: pyarrow.types.is_int64(type_.value_type),
            ),
        ),
        (
            "INT64",
            "REPEATED",
            all_(
                pyarrow.types.is_list,
                lambda type_: pyarrow.types.is_int64(type_.value_type),
            ),
        ),
        (
            "FLOAT",
            "REPEATED",
            all_(
                pyarrow.types.is_list,
                lambda type_: pyarrow.types.is_float64(type_.value_type),
            ),
        ),
        (
            "FLOAT64",
            "REPEATED",
            all_(
                pyarrow.types.is_list,
                lambda type_: pyarrow.types.is_float64(type_.value_type),
            ),
        ),
        (
            "NUMERIC",
            "REPEATED",
            all_(pyarrow.types.is_list, lambda type_: is_numeric(type_.value_type)),
        ),
        (
            "BOOLEAN",
            "REPEATED",
            all_(
                pyarrow.types.is_list,
                lambda type_: pyarrow.types.is_boolean(type_.value_type),
            ),
        ),
        (
            "BOOL",
            "REPEATED",
            all_(
                pyarrow.types.is_list,
                lambda type_: pyarrow.types.is_boolean(type_.value_type),
            ),
        ),
        (
            "TIMESTAMP",
            "REPEATED",
            all_(pyarrow.types.is_list, lambda type_: is_timestamp(type_.value_type)),
        ),
        (
            "DATE",
            "REPEATED",
            all_(
                pyarrow.types.is_list,
                lambda type_: pyarrow.types.is_date32(type_.value_type),
            ),
        ),
        (
            "TIME",
            "REPEATED",
            all_(
                pyarrow.types.is_list,
                lambda type_: pyarrow.types.is_time64(type_.value_type),
            ),
        ),
        (
            "DATETIME",
            "REPEATED",
            all_(pyarrow.types.is_list, lambda type_: is_datetime(type_.value_type)),
        ),
        (
            "GEOGRAPHY",
            "REPEATED",
            all_(
                pyarrow.types.is_list,
                lambda type_: pyarrow.types.is_string(type_.value_type),
            ),
        ),
        ("RECORD", "REPEATED", is_none),
        ("UNKNOWN_TYPE", "REPEATED", is_none),
    ],
)
@pytest.mark.skipif(pyarrow is None, reason="Requires `pyarrow`")
def test_bq_to_arrow_data_type(module_under_test, bq_type, bq_mode, is_correct_type):
    field = schema.SchemaField("ignored_name", bq_type, mode=bq_mode)
    actual = module_under_test.bq_to_arrow_data_type(field)
    assert is_correct_type(actual)


@pytest.mark.parametrize("bq_type", ["RECORD", "record", "STRUCT", "struct"])
@pytest.mark.skipif(pyarrow is None, reason="Requires `pyarrow`")
def test_bq_to_arrow_data_type_w_struct(module_under_test, bq_type):
    fields = (
        schema.SchemaField("field01", "STRING"),
        schema.SchemaField("field02", "BYTES"),
        schema.SchemaField("field03", "INTEGER"),
        schema.SchemaField("field04", "INT64"),
        schema.SchemaField("field05", "FLOAT"),
        schema.SchemaField("field06", "FLOAT64"),
        schema.SchemaField("field07", "NUMERIC"),
        schema.SchemaField("field08", "BOOLEAN"),
        schema.SchemaField("field09", "BOOL"),
        schema.SchemaField("field10", "TIMESTAMP"),
        schema.SchemaField("field11", "DATE"),
        schema.SchemaField("field12", "TIME"),
        schema.SchemaField("field13", "DATETIME"),
        schema.SchemaField("field14", "GEOGRAPHY"),
    )
    field = schema.SchemaField("ignored_name", bq_type, mode="NULLABLE", fields=fields)
    actual = module_under_test.bq_to_arrow_data_type(field)
    expected = pyarrow.struct(
        (
            pyarrow.field("field01", pyarrow.string()),
            pyarrow.field("field02", pyarrow.binary()),
            pyarrow.field("field03", pyarrow.int64()),
            pyarrow.field("field04", pyarrow.int64()),
            pyarrow.field("field05", pyarrow.float64()),
            pyarrow.field("field06", pyarrow.float64()),
            pyarrow.field("field07", module_under_test.pyarrow_numeric()),
            pyarrow.field("field08", pyarrow.bool_()),
            pyarrow.field("field09", pyarrow.bool_()),
            pyarrow.field("field10", module_under_test.pyarrow_timestamp()),
            pyarrow.field("field11", pyarrow.date32()),
            pyarrow.field("field12", module_under_test.pyarrow_time()),
            pyarrow.field("field13", module_under_test.pyarrow_datetime()),
            pyarrow.field("field14", pyarrow.string()),
        )
    )
    assert pyarrow.types.is_struct(actual)
    assert actual.num_children == len(fields)
    assert actual.equals(expected)


@pytest.mark.parametrize("bq_type", ["RECORD", "record", "STRUCT", "struct"])
@pytest.mark.skipif(pyarrow is None, reason="Requires `pyarrow`")
def test_bq_to_arrow_data_type_w_array_struct(module_under_test, bq_type):
    fields = (
        schema.SchemaField("field01", "STRING"),
        schema.SchemaField("field02", "BYTES"),
        schema.SchemaField("field03", "INTEGER"),
        schema.SchemaField("field04", "INT64"),
        schema.SchemaField("field05", "FLOAT"),
        schema.SchemaField("field06", "FLOAT64"),
        schema.SchemaField("field07", "NUMERIC"),
        schema.SchemaField("field08", "BOOLEAN"),
        schema.SchemaField("field09", "BOOL"),
        schema.SchemaField("field10", "TIMESTAMP"),
        schema.SchemaField("field11", "DATE"),
        schema.SchemaField("field12", "TIME"),
        schema.SchemaField("field13", "DATETIME"),
        schema.SchemaField("field14", "GEOGRAPHY"),
    )
    field = schema.SchemaField("ignored_name", bq_type, mode="REPEATED", fields=fields)
    actual = module_under_test.bq_to_arrow_data_type(field)
    expected_value_type = pyarrow.struct(
        (
            pyarrow.field("field01", pyarrow.string()),
            pyarrow.field("field02", pyarrow.binary()),
            pyarrow.field("field03", pyarrow.int64()),
            pyarrow.field("field04", pyarrow.int64()),
            pyarrow.field("field05", pyarrow.float64()),
            pyarrow.field("field06", pyarrow.float64()),
            pyarrow.field("field07", module_under_test.pyarrow_numeric()),
            pyarrow.field("field08", pyarrow.bool_()),
            pyarrow.field("field09", pyarrow.bool_()),
            pyarrow.field("field10", module_under_test.pyarrow_timestamp()),
            pyarrow.field("field11", pyarrow.date32()),
            pyarrow.field("field12", module_under_test.pyarrow_time()),
            pyarrow.field("field13", module_under_test.pyarrow_datetime()),
            pyarrow.field("field14", pyarrow.string()),
        )
    )
    assert pyarrow.types.is_list(actual)
    assert pyarrow.types.is_struct(actual.value_type)
    assert actual.value_type.num_children == len(fields)
    assert actual.value_type.equals(expected_value_type)


@pytest.mark.skipif(pyarrow is None, reason="Requires `pyarrow`")
def test_bq_to_arrow_data_type_w_struct_unknown_subfield(module_under_test):
    fields = (
        schema.SchemaField("field1", "STRING"),
        schema.SchemaField("field2", "INTEGER"),
        # Don't know what to convert UNKNOWN_TYPE to, let type inference work,
        # instead.
        schema.SchemaField("field3", "UNKNOWN_TYPE"),
    )
    field = schema.SchemaField("ignored_name", "RECORD", mode="NULLABLE", fields=fields)

    with warnings.catch_warnings(record=True) as warned:
        actual = module_under_test.bq_to_arrow_data_type(field)

    assert actual is None
    assert len(warned) == 1
    warning = warned[0]
    assert "field3" in str(warning)


@pytest.mark.parametrize(
    "bq_type,rows",
    [
        ("STRING", ["abc", None, "def", None]),
        ("BYTES", [b"abc", None, b"def", None]),
        ("INTEGER", [123, None, 456, None]),
        ("INT64", [-9223372036854775808, None, 9223372036854775807, 123]),
        ("FLOAT", [1.25, None, 3.5, None]),
        (
            "NUMERIC",
            [
                decimal.Decimal("-99999999999999999999999999999.999999999"),
                None,
                decimal.Decimal("99999999999999999999999999999.999999999"),
                decimal.Decimal("999.123456789"),
            ],
        ),
        ("BOOLEAN", [True, None, False, None]),
        ("BOOL", [False, None, True, None]),
        # TODO: Once https://issues.apache.org/jira/browse/ARROW-5450 is
        # resolved, test with TIMESTAMP column. Conversion from pyarrow
        # TimestampArray to list of Python objects fails with OverflowError:
        # Python int too large to convert to C long.
        #
        # (
        #     "TIMESTAMP",
        #     [
        #         datetime.datetime(1, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
        #         None,
        #         datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=pytz.utc),
        #         datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
        #     ],
        # ),
        (
            "DATE",
            [
                datetime.date(1, 1, 1),
                None,
                datetime.date(9999, 12, 31),
                datetime.date(1970, 1, 1),
            ],
        ),
        (
            "TIME",
            [
                datetime.time(0, 0, 0),
                None,
                datetime.time(23, 59, 59, 999999),
                datetime.time(12, 0, 0),
            ],
        ),
        # TODO: Once https://issues.apache.org/jira/browse/ARROW-5450 is
        # resolved, test with DATETIME column. Conversion from pyarrow
        # TimestampArray to list of Python objects fails with OverflowError:
        # Python int too large to convert to C long.
        #
        # (
        #     "DATETIME",
        #     [
        #         datetime.datetime(1, 1, 1, 0, 0, 0),
        #         None,
        #         datetime.datetime(9999, 12, 31, 23, 59, 59, 999999),
        #         datetime.datetime(1970, 1, 1, 0, 0, 0),
        #     ],
        # ),
        (
            "GEOGRAPHY",
            [
                "POINT(30 10)",
                None,
                "LINESTRING (30 10, 10 30, 40 40)",
                "POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))",
            ],
        ),
    ],
)
@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
@pytest.mark.skipif(pyarrow is None, reason="Requires `pyarrow`")
def test_bq_to_arrow_array_w_nullable_scalars(module_under_test, bq_type, rows):
    series = pandas.Series(rows, dtype="object")
    bq_field = schema.SchemaField("field_name", bq_type)
    arrow_array = module_under_test.bq_to_arrow_array(series, bq_field)
    roundtrip = arrow_array.to_pylist()
    assert rows == roundtrip


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
@pytest.mark.skipif(pyarrow is None, reason="Requires `pyarrow`")
def test_bq_to_arrow_array_w_arrays(module_under_test):
    rows = [[1, 2, 3], [], [4, 5, 6]]
    series = pandas.Series(rows, dtype="object")
    bq_field = schema.SchemaField("field_name", "INTEGER", mode="REPEATED")
    arrow_array = module_under_test.bq_to_arrow_array(series, bq_field)
    roundtrip = arrow_array.to_pylist()
    assert rows == roundtrip


@pytest.mark.parametrize("bq_type", ["RECORD", "record", "STRUCT", "struct"])
@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
@pytest.mark.skipif(pyarrow is None, reason="Requires `pyarrow`")
def test_bq_to_arrow_array_w_structs(module_under_test, bq_type):
    rows = [
        {"int_col": 123, "string_col": "abc"},
        None,
        {"int_col": 456, "string_col": "def"},
    ]
    series = pandas.Series(rows, dtype="object")
    bq_field = schema.SchemaField(
        "field_name",
        bq_type,
        fields=(
            schema.SchemaField("int_col", "INTEGER"),
            schema.SchemaField("string_col", "STRING"),
        ),
    )
    arrow_array = module_under_test.bq_to_arrow_array(series, bq_field)
    roundtrip = arrow_array.to_pylist()
    assert rows == roundtrip


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
@pytest.mark.skipif(pyarrow is None, reason="Requires `pyarrow`")
def test_bq_to_arrow_array_w_special_floats(module_under_test):
    bq_field = schema.SchemaField("field_name", "FLOAT64")
    rows = [float("-inf"), float("nan"), float("inf"), None]
    series = pandas.Series(rows, dtype="object")
    arrow_array = module_under_test.bq_to_arrow_array(series, bq_field)
    roundtrip = arrow_array.to_pylist()
    assert len(rows) == len(roundtrip)
    assert roundtrip[0] == float("-inf")
    # Since we are converting from pandas, NaN is treated as NULL in pyarrow
    # due to pandas conventions.
    # https://arrow.apache.org/docs/python/data.html#none-values-and-nan-handling
    assert roundtrip[1] is None
    assert roundtrip[2] == float("inf")
    assert roundtrip[3] is None


@pytest.mark.skipif(pyarrow is None, reason="Requires `pyarrow`")
def test_bq_to_arrow_schema_w_unknown_type(module_under_test):
    fields = (
        schema.SchemaField("field1", "STRING"),
        schema.SchemaField("field2", "INTEGER"),
        # Don't know what to convert UNKNOWN_TYPE to, let type inference work,
        # instead.
        schema.SchemaField("field3", "UNKNOWN_TYPE"),
    )
    actual = module_under_test.bq_to_arrow_schema(fields)
    assert actual is None


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
def test_get_column_or_index_not_found(module_under_test):
    dataframe = pandas.DataFrame({"not_the_column_youre_looking_for": [1, 2, 3]})
    with pytest.raises(ValueError, match="col_is_missing"):
        module_under_test.get_column_or_index(dataframe, "col_is_missing")


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
def test_get_column_or_index_with_multiindex_not_found(module_under_test):
    dataframe = pandas.DataFrame(
        {"column_name": [1, 2, 3, 4, 5, 6]},
        index=pandas.MultiIndex.from_tuples(
            [("a", 0), ("a", 1), ("b", 0), ("b", 1), ("c", 0), ("c", 1)]
        ),
    )
    with pytest.raises(ValueError, match="not_in_df"):
        module_under_test.get_column_or_index(dataframe, "not_in_df")


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
def test_get_column_or_index_with_both_prefers_column(module_under_test):
    dataframe = pandas.DataFrame(
        {"some_name": [1, 2, 3]}, index=pandas.Index([0, 1, 2], name="some_name")
    )
    series = module_under_test.get_column_or_index(dataframe, "some_name")
    expected = pandas.Series([1, 2, 3], name="some_name")
    pandas.testing.assert_series_equal(series, expected)


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
def test_get_column_or_index_with_column(module_under_test):
    dataframe = pandas.DataFrame({"column_name": [1, 2, 3], "other_column": [4, 5, 6]})
    series = module_under_test.get_column_or_index(dataframe, "column_name")
    expected = pandas.Series([1, 2, 3], name="column_name")
    pandas.testing.assert_series_equal(series, expected)


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
def test_get_column_or_index_with_named_index(module_under_test):
    dataframe = pandas.DataFrame(
        {"column_name": [1, 2, 3]}, index=pandas.Index([4, 5, 6], name="index_name")
    )
    series = module_under_test.get_column_or_index(dataframe, "index_name")
    expected = pandas.Series([4, 5, 6], name="index_name")
    pandas.testing.assert_series_equal(series, expected)


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
def test_get_column_or_index_with_datetimeindex(module_under_test):
    datetimes = [
        datetime.datetime(2000, 1, 2, 3, 4, 5, 101),
        datetime.datetime(2006, 7, 8, 9, 10, 11, 202),
        datetime.datetime(2012, 1, 14, 15, 16, 17, 303),
    ]
    dataframe = pandas.DataFrame(
        {"column_name": [1, 2, 3]},
        index=pandas.DatetimeIndex(datetimes, name="index_name"),
    )
    series = module_under_test.get_column_or_index(dataframe, "index_name")
    expected = pandas.Series(datetimes, name="index_name")
    pandas.testing.assert_series_equal(series, expected)


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
def test_get_column_or_index_with_multiindex(module_under_test):
    dataframe = pandas.DataFrame(
        {"column_name": [1, 2, 3, 4, 5, 6]},
        index=pandas.MultiIndex.from_tuples(
            [("a", 0), ("a", 1), ("b", 0), ("b", 1), ("c", 0), ("c", 1)],
            names=["letters", "numbers"],
        ),
    )

    series = module_under_test.get_column_or_index(dataframe, "letters")
    expected = pandas.Series(["a", "a", "b", "b", "c", "c"], name="letters")
    pandas.testing.assert_series_equal(series, expected)

    series = module_under_test.get_column_or_index(dataframe, "numbers")
    expected = pandas.Series([0, 1, 0, 1, 0, 1], name="numbers")
    pandas.testing.assert_series_equal(series, expected)


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
def test_list_columns_and_indexes_without_named_index(module_under_test):
    df_data = collections.OrderedDict(
        [
            ("a_series", [1, 2, 3, 4]),
            ("b_series", [0.1, 0.2, 0.3, 0.4]),
            ("c_series", ["a", "b", "c", "d"]),
        ]
    )
    dataframe = pandas.DataFrame(df_data)

    columns_and_indexes = module_under_test.list_columns_and_indexes(dataframe)
    expected = [
        ("a_series", pandas.api.types.pandas_dtype("int64")),
        ("b_series", pandas.api.types.pandas_dtype("float64")),
        ("c_series", pandas.api.types.pandas_dtype("object")),
    ]
    assert columns_and_indexes == expected


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
def test_list_columns_and_indexes_with_named_index_same_as_column_name(
    module_under_test
):
    df_data = collections.OrderedDict(
        [
            ("a_series", [1, 2, 3, 4]),
            ("b_series", [0.1, 0.2, 0.3, 0.4]),
            ("c_series", ["a", "b", "c", "d"]),
        ]
    )
    dataframe = pandas.DataFrame(
        df_data,
        # Use same name as an integer column but a different datatype so that
        # we can verify that the column is listed but the index isn't.
        index=pandas.Index([0.1, 0.2, 0.3, 0.4], name="a_series"),
    )

    columns_and_indexes = module_under_test.list_columns_and_indexes(dataframe)
    expected = [
        ("a_series", pandas.api.types.pandas_dtype("int64")),
        ("b_series", pandas.api.types.pandas_dtype("float64")),
        ("c_series", pandas.api.types.pandas_dtype("object")),
    ]
    assert columns_and_indexes == expected


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
def test_list_columns_and_indexes_with_named_index(module_under_test):
    df_data = collections.OrderedDict(
        [
            ("a_series", [1, 2, 3, 4]),
            ("b_series", [0.1, 0.2, 0.3, 0.4]),
            ("c_series", ["a", "b", "c", "d"]),
        ]
    )
    dataframe = pandas.DataFrame(
        df_data, index=pandas.Index([4, 5, 6, 7], name="a_index")
    )

    columns_and_indexes = module_under_test.list_columns_and_indexes(dataframe)
    expected = [
        ("a_index", pandas.api.types.pandas_dtype("int64")),
        ("a_series", pandas.api.types.pandas_dtype("int64")),
        ("b_series", pandas.api.types.pandas_dtype("float64")),
        ("c_series", pandas.api.types.pandas_dtype("object")),
    ]
    assert columns_and_indexes == expected


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
def test_list_columns_and_indexes_with_multiindex(module_under_test):
    df_data = collections.OrderedDict(
        [
            ("a_series", [1, 2, 3, 4]),
            ("b_series", [0.1, 0.2, 0.3, 0.4]),
            ("c_series", ["a", "b", "c", "d"]),
        ]
    )
    dataframe = pandas.DataFrame(
        df_data,
        index=pandas.MultiIndex.from_tuples(
            [(0, 0, 41), (0, 0, 42), (1, 0, 41), (1, 1, 41)],
            names=[
                "a_index",
                # Use same name as column, but different dtype so we can verify
                # the column type is included.
                "b_series",
                "c_index",
            ],
        ),
    )

    columns_and_indexes = module_under_test.list_columns_and_indexes(dataframe)
    expected = [
        ("a_index", pandas.api.types.pandas_dtype("int64")),
        ("c_index", pandas.api.types.pandas_dtype("int64")),
        ("a_series", pandas.api.types.pandas_dtype("int64")),
        ("b_series", pandas.api.types.pandas_dtype("float64")),
        ("c_series", pandas.api.types.pandas_dtype("object")),
    ]
    assert columns_and_indexes == expected


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
@pytest.mark.skipif(pyarrow is None, reason="Requires `pyarrow`")
def test_dataframe_to_arrow_with_multiindex(module_under_test):
    bq_schema = (
        schema.SchemaField("str_index", "STRING"),
        # int_index is intentionally omitted, to verify that it's okay to be
        # missing indexes from the schema.
        schema.SchemaField("dt_index", "DATETIME"),
        schema.SchemaField("int_col", "INTEGER"),
        schema.SchemaField("nullable_int_col", "INTEGER"),
        schema.SchemaField("str_col", "STRING"),
    )
    df_data = collections.OrderedDict(
        [
            ("int_col", [1, 2, 3, 4, 5, 6]),
            ("nullable_int_col", [6.0, float("nan"), 7.0, float("nan"), 8.0, 9.0]),
            ("str_col", ["apple", "banana", "cherry", "durian", "etrog", "fig"]),
        ]
    )
    df_index = pandas.MultiIndex.from_tuples(
        [
            ("a", 0, datetime.datetime(1999, 12, 31, 23, 59, 59, 999999)),
            ("a", 0, datetime.datetime(2000, 1, 1, 0, 0, 0)),
            ("a", 1, datetime.datetime(1999, 12, 31, 23, 59, 59, 999999)),
            ("b", 1, datetime.datetime(2000, 1, 1, 0, 0, 0)),
            ("b", 0, datetime.datetime(1999, 12, 31, 23, 59, 59, 999999)),
            ("b", 0, datetime.datetime(2000, 1, 1, 0, 0, 0)),
        ],
        names=["str_index", "int_index", "dt_index"],
    )
    dataframe = pandas.DataFrame(df_data, index=df_index)

    arrow_table = module_under_test.dataframe_to_arrow(dataframe, bq_schema)

    assert arrow_table.schema.names == [
        "str_index",
        "dt_index",
        "int_col",
        "nullable_int_col",
        "str_col",
    ]
    arrow_data = arrow_table.to_pydict()
    assert arrow_data["str_index"] == ["a", "a", "a", "b", "b", "b"]
    expected_dt_index = [
        pandas.Timestamp(dt)
        for dt in (
            datetime.datetime(1999, 12, 31, 23, 59, 59, 999999),
            datetime.datetime(2000, 1, 1, 0, 0, 0),
            datetime.datetime(1999, 12, 31, 23, 59, 59, 999999),
            datetime.datetime(2000, 1, 1, 0, 0, 0),
            datetime.datetime(1999, 12, 31, 23, 59, 59, 999999),
            datetime.datetime(2000, 1, 1, 0, 0, 0),
        )
    ]
    assert arrow_data["dt_index"] == expected_dt_index
    assert arrow_data["int_col"] == [1, 2, 3, 4, 5, 6]
    assert arrow_data["nullable_int_col"] == [6, None, 7, None, 8, 9]
    assert arrow_data["str_col"] == [
        "apple",
        "banana",
        "cherry",
        "durian",
        "etrog",
        "fig",
    ]


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
@pytest.mark.skipif(pyarrow is None, reason="Requires `pyarrow`")
def test_dataframe_to_arrow_with_required_fields(module_under_test):
    bq_schema = (
        schema.SchemaField("field01", "STRING", mode="REQUIRED"),
        schema.SchemaField("field02", "BYTES", mode="REQUIRED"),
        schema.SchemaField("field03", "INTEGER", mode="REQUIRED"),
        schema.SchemaField("field04", "INT64", mode="REQUIRED"),
        schema.SchemaField("field05", "FLOAT", mode="REQUIRED"),
        schema.SchemaField("field06", "FLOAT64", mode="REQUIRED"),
        schema.SchemaField("field07", "NUMERIC", mode="REQUIRED"),
        schema.SchemaField("field08", "BOOLEAN", mode="REQUIRED"),
        schema.SchemaField("field09", "BOOL", mode="REQUIRED"),
        schema.SchemaField("field10", "TIMESTAMP", mode="REQUIRED"),
        schema.SchemaField("field11", "DATE", mode="REQUIRED"),
        schema.SchemaField("field12", "TIME", mode="REQUIRED"),
        schema.SchemaField("field13", "DATETIME", mode="REQUIRED"),
        schema.SchemaField("field14", "GEOGRAPHY", mode="REQUIRED"),
    )
    dataframe = pandas.DataFrame(
        {
            "field01": ["hello", "world"],
            "field02": [b"abd", b"efg"],
            "field03": [1, 2],
            "field04": [3, 4],
            "field05": [1.25, 9.75],
            "field06": [-1.75, -3.5],
            "field07": [decimal.Decimal("1.2345"), decimal.Decimal("6.7891")],
            "field08": [True, False],
            "field09": [False, True],
            "field10": [
                datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
                datetime.datetime(2012, 12, 21, 9, 7, 42, tzinfo=pytz.utc),
            ],
            "field11": [datetime.date(9999, 12, 31), datetime.date(1970, 1, 1)],
            "field12": [datetime.time(23, 59, 59, 999999), datetime.time(12, 0, 0)],
            "field13": [
                datetime.datetime(1970, 1, 1, 0, 0, 0),
                datetime.datetime(2012, 12, 21, 9, 7, 42),
            ],
            "field14": [
                "POINT(30 10)",
                "POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))",
            ],
        }
    )

    arrow_table = module_under_test.dataframe_to_arrow(dataframe, bq_schema)
    arrow_schema = arrow_table.schema

    assert len(arrow_schema) == len(bq_schema)
    for arrow_field in arrow_schema:
        assert not arrow_field.nullable


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
@pytest.mark.skipif(pyarrow is None, reason="Requires `pyarrow`")
def test_dataframe_to_arrow_with_unknown_type(module_under_test):
    bq_schema = (
        schema.SchemaField("field00", "UNKNOWN_TYPE"),
        schema.SchemaField("field01", "STRING"),
        schema.SchemaField("field02", "BYTES"),
        schema.SchemaField("field03", "INTEGER"),
    )
    dataframe = pandas.DataFrame(
        {
            "field00": ["whoami", "whatami"],
            "field01": ["hello", "world"],
            "field02": [b"abd", b"efg"],
            "field03": [1, 2],
        }
    )

    with warnings.catch_warnings(record=True) as warned:
        arrow_table = module_under_test.dataframe_to_arrow(dataframe, bq_schema)
    arrow_schema = arrow_table.schema

    assert len(warned) == 1
    warning = warned[0]
    assert "field00" in str(warning)

    assert len(arrow_schema) == len(bq_schema)
    assert arrow_schema[0].name == "field00"
    assert arrow_schema[1].name == "field01"
    assert arrow_schema[2].name == "field02"
    assert arrow_schema[3].name == "field03"


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
def test_dataframe_to_parquet_without_pyarrow(module_under_test, monkeypatch):
    monkeypatch.setattr(module_under_test, "pyarrow", None)
    with pytest.raises(ValueError) as exc_context:
        module_under_test.dataframe_to_parquet(pandas.DataFrame(), (), None)
    assert "pyarrow is required" in str(exc_context.value)


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
@pytest.mark.skipif(pyarrow is None, reason="Requires `pyarrow`")
def test_dataframe_to_parquet_w_extra_fields(module_under_test, monkeypatch):
    with pytest.raises(ValueError) as exc_context:
        module_under_test.dataframe_to_parquet(
            pandas.DataFrame(), (schema.SchemaField("not_in_df", "STRING"),), None
        )
    message = str(exc_context.value)
    assert "bq_schema contains fields not present in dataframe" in message
    assert "not_in_df" in message


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
@pytest.mark.skipif(pyarrow is None, reason="Requires `pyarrow`")
def test_dataframe_to_parquet_w_missing_fields(module_under_test, monkeypatch):
    with pytest.raises(ValueError) as exc_context:
        module_under_test.dataframe_to_parquet(
            pandas.DataFrame({"not_in_bq": [1, 2, 3]}), (), None
        )
    message = str(exc_context.value)
    assert "bq_schema is missing fields from dataframe" in message
    assert "not_in_bq" in message


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
@pytest.mark.skipif(pyarrow is None, reason="Requires `pyarrow`")
def test_dataframe_to_parquet_compression_method(module_under_test):
    bq_schema = (schema.SchemaField("field00", "STRING"),)
    dataframe = pandas.DataFrame({"field00": ["foo", "bar"]})

    write_table_patch = mock.patch.object(
        module_under_test.pyarrow.parquet, "write_table", autospec=True
    )

    with write_table_patch as fake_write_table:
        module_under_test.dataframe_to_parquet(
            dataframe, bq_schema, None, parquet_compression="ZSTD"
        )

    call_args = fake_write_table.call_args
    assert call_args is not None
    assert call_args.kwargs.get("compression") == "ZSTD"
