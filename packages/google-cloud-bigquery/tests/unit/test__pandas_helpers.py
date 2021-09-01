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
import operator
import queue
import warnings
import pkg_resources

import mock

try:
    import pandas
    import pandas.api.types
    import pandas.testing
except ImportError:  # pragma: NO COVER
    pandas = None
try:
    import geopandas
except ImportError:  # pragma: NO COVER
    geopandas = None

import pytest

from google import api_core
from google.cloud.bigquery import exceptions
from google.cloud.bigquery import _helpers
from google.cloud.bigquery import schema


pyarrow = _helpers.PYARROW_VERSIONS.try_import()
if pyarrow:
    import pyarrow.types
else:  # pragma: NO COVER
    # Mock out pyarrow when missing, because methods from pyarrow.types are
    # used in test parameterization.
    pyarrow = mock.Mock()

try:
    from google.cloud import bigquery_storage

    _helpers.BQ_STORAGE_VERSIONS.verify_version()
except ImportError:  # pragma: NO COVER
    bigquery_storage = None

PANDAS_MINIUM_VERSION = pkg_resources.parse_version("1.0.0")

if pandas is not None:
    PANDAS_INSTALLED_VERSION = pkg_resources.get_distribution("pandas").parsed_version
else:
    # Set to less than MIN version.
    PANDAS_INSTALLED_VERSION = pkg_resources.parse_version("0.0.0")


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


def is_bignumeric(type_):
    # See: https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#numeric-type
    return all_(
        pyarrow.types.is_decimal,
        lambda type_: type_.precision == 76,
        lambda type_: type_.scale == 38,
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


@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
def test_is_datetime():
    assert is_datetime(pyarrow.timestamp("us", tz=None))
    assert not is_datetime(pyarrow.timestamp("ms", tz=None))
    assert not is_datetime(pyarrow.timestamp("us", tz="UTC"))
    assert not is_datetime(pyarrow.timestamp("ns", tz="UTC"))
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
        ("BIGNUMERIC", "NULLABLE", is_bignumeric),
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
            "BIGNUMERIC",
            "REPEATED",
            all_(pyarrow.types.is_list, lambda type_: is_bignumeric(type_.value_type)),
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
@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
def test_bq_to_arrow_data_type(module_under_test, bq_type, bq_mode, is_correct_type):
    field = schema.SchemaField("ignored_name", bq_type, mode=bq_mode)
    actual = module_under_test.bq_to_arrow_data_type(field)
    assert is_correct_type(actual)


@pytest.mark.parametrize("bq_type", ["RECORD", "record", "STRUCT", "struct"])
@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
def test_bq_to_arrow_data_type_w_struct(module_under_test, bq_type):
    fields = (
        schema.SchemaField("field01", "STRING"),
        schema.SchemaField("field02", "BYTES"),
        schema.SchemaField("field03", "INTEGER"),
        schema.SchemaField("field04", "INT64"),
        schema.SchemaField("field05", "FLOAT"),
        schema.SchemaField("field06", "FLOAT64"),
        schema.SchemaField("field07", "NUMERIC"),
        schema.SchemaField("field08", "BIGNUMERIC"),
        schema.SchemaField("field09", "BOOLEAN"),
        schema.SchemaField("field10", "BOOL"),
        schema.SchemaField("field11", "TIMESTAMP"),
        schema.SchemaField("field12", "DATE"),
        schema.SchemaField("field13", "TIME"),
        schema.SchemaField("field14", "DATETIME"),
        schema.SchemaField("field15", "GEOGRAPHY"),
    )

    field = schema.SchemaField("ignored_name", bq_type, mode="NULLABLE", fields=fields)
    actual = module_under_test.bq_to_arrow_data_type(field)

    expected = (
        pyarrow.field("field01", pyarrow.string()),
        pyarrow.field("field02", pyarrow.binary()),
        pyarrow.field("field03", pyarrow.int64()),
        pyarrow.field("field04", pyarrow.int64()),
        pyarrow.field("field05", pyarrow.float64()),
        pyarrow.field("field06", pyarrow.float64()),
        pyarrow.field("field07", module_under_test.pyarrow_numeric()),
        pyarrow.field("field08", module_under_test.pyarrow_bignumeric()),
        pyarrow.field("field09", pyarrow.bool_()),
        pyarrow.field("field10", pyarrow.bool_()),
        pyarrow.field("field11", module_under_test.pyarrow_timestamp()),
        pyarrow.field("field12", pyarrow.date32()),
        pyarrow.field("field13", module_under_test.pyarrow_time()),
        pyarrow.field("field14", module_under_test.pyarrow_datetime()),
        pyarrow.field("field15", pyarrow.string()),
    )
    expected = pyarrow.struct(expected)

    assert pyarrow.types.is_struct(actual)
    assert actual.num_fields == len(fields)
    assert actual.equals(expected)


@pytest.mark.parametrize("bq_type", ["RECORD", "record", "STRUCT", "struct"])
@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
def test_bq_to_arrow_data_type_w_array_struct(module_under_test, bq_type):
    fields = (
        schema.SchemaField("field01", "STRING"),
        schema.SchemaField("field02", "BYTES"),
        schema.SchemaField("field03", "INTEGER"),
        schema.SchemaField("field04", "INT64"),
        schema.SchemaField("field05", "FLOAT"),
        schema.SchemaField("field06", "FLOAT64"),
        schema.SchemaField("field07", "NUMERIC"),
        schema.SchemaField("field08", "BIGNUMERIC"),
        schema.SchemaField("field09", "BOOLEAN"),
        schema.SchemaField("field10", "BOOL"),
        schema.SchemaField("field11", "TIMESTAMP"),
        schema.SchemaField("field12", "DATE"),
        schema.SchemaField("field13", "TIME"),
        schema.SchemaField("field14", "DATETIME"),
        schema.SchemaField("field15", "GEOGRAPHY"),
    )

    field = schema.SchemaField("ignored_name", bq_type, mode="REPEATED", fields=fields)
    actual = module_under_test.bq_to_arrow_data_type(field)

    expected = (
        pyarrow.field("field01", pyarrow.string()),
        pyarrow.field("field02", pyarrow.binary()),
        pyarrow.field("field03", pyarrow.int64()),
        pyarrow.field("field04", pyarrow.int64()),
        pyarrow.field("field05", pyarrow.float64()),
        pyarrow.field("field06", pyarrow.float64()),
        pyarrow.field("field07", module_under_test.pyarrow_numeric()),
        pyarrow.field("field08", module_under_test.pyarrow_bignumeric()),
        pyarrow.field("field09", pyarrow.bool_()),
        pyarrow.field("field10", pyarrow.bool_()),
        pyarrow.field("field11", module_under_test.pyarrow_timestamp()),
        pyarrow.field("field12", pyarrow.date32()),
        pyarrow.field("field13", module_under_test.pyarrow_time()),
        pyarrow.field("field14", module_under_test.pyarrow_datetime()),
        pyarrow.field("field15", pyarrow.string()),
    )
    expected_value_type = pyarrow.struct(expected)

    assert pyarrow.types.is_list(actual)
    assert pyarrow.types.is_struct(actual.value_type)
    assert actual.value_type.num_fields == len(fields)
    assert actual.value_type.equals(expected_value_type)


@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
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
        (
            "BIGNUMERIC",
            [
                decimal.Decimal("-{d38}.{d38}".format(d38="9" * 38)),
                None,
                decimal.Decimal("{d38}.{d38}".format(d38="9" * 38)),
                decimal.Decimal("3.141592653589793238462643383279"),
            ],
        ),
        ("BOOLEAN", [True, None, False, None]),
        ("BOOL", [False, None, True, None]),
        (
            "TIMESTAMP",
            [
                datetime.datetime(1, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc),
                None,
                datetime.datetime(
                    9999, 12, 31, 23, 59, 59, 999999, tzinfo=datetime.timezone.utc
                ),
                datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc),
            ],
        ),
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
        (
            "DATETIME",
            [
                datetime.datetime(1, 1, 1, 0, 0, 0),
                datetime.datetime(9999, 12, 31, 23, 59, 59, 999999),
                None,
                datetime.datetime(1970, 1, 1, 0, 0, 0),
                datetime.datetime(1999, 3, 14, 15, 9, 26, 535898),
            ],
        ),
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
@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
def test_bq_to_arrow_array_w_nullable_scalars(module_under_test, bq_type, rows):
    series = pandas.Series(rows, dtype="object")
    bq_field = schema.SchemaField("field_name", bq_type)
    arrow_array = module_under_test.bq_to_arrow_array(series, bq_field)
    roundtrip = arrow_array.to_pylist()
    assert rows == roundtrip


@pytest.mark.parametrize(
    "bq_type,rows",
    [
        (
            "TIMESTAMP",
            [
                "1971-09-28T23:59:07+00:00",
                "1975-04-09T23:59:02+00:00",
                "1979-08-17T23:59:05+00:00",
                "NaT",
                "1983-05-09T13:00:00+00:00",
            ],
        ),
        (
            "DATETIME",
            [
                "1971-09-28T23:59:07",
                "1975-04-09T23:59:02",
                "1979-08-17T23:59:05",
                "NaT",
                "1983-05-09T13:00:00",
            ],
        ),
    ],
)
@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
def test_bq_to_arrow_array_w_pandas_timestamp(module_under_test, bq_type, rows):
    rows = [pandas.Timestamp(row) for row in rows]
    series = pandas.Series(rows)
    bq_field = schema.SchemaField("field_name", bq_type)
    arrow_array = module_under_test.bq_to_arrow_array(series, bq_field)
    roundtrip = arrow_array.to_pandas()
    assert series.equals(roundtrip)


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
def test_bq_to_arrow_array_w_arrays(module_under_test):
    rows = [[1, 2, 3], [], [4, 5, 6]]
    series = pandas.Series(rows, dtype="object")
    bq_field = schema.SchemaField("field_name", "INTEGER", mode="REPEATED")
    arrow_array = module_under_test.bq_to_arrow_array(series, bq_field)
    roundtrip = arrow_array.to_pylist()
    assert rows == roundtrip


@pytest.mark.parametrize("bq_type", ["RECORD", "record", "STRUCT", "struct"])
@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
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
@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
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


@pytest.mark.skipif(geopandas is None, reason="Requires `geopandas`")
@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
def test_bq_to_arrow_array_w_geography_dtype(module_under_test):
    from shapely import wkb, wkt

    bq_field = schema.SchemaField("field_name", "GEOGRAPHY")

    series = geopandas.GeoSeries([None, wkt.loads("point(0 0)")])
    array = module_under_test.bq_to_arrow_array(series, bq_field)
    # The result is binary, because we use wkb format
    assert array.type == pyarrow.binary()
    assert array.to_pylist() == [None, wkb.dumps(series[1])]

    # All na:
    series = geopandas.GeoSeries([None, None])
    array = module_under_test.bq_to_arrow_array(series, bq_field)
    assert array.type == pyarrow.string()
    assert array.to_pylist() == list(series)


@pytest.mark.skipif(geopandas is None, reason="Requires `geopandas`")
@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
def test_bq_to_arrow_array_w_geography_type_shapely_data(module_under_test):
    from shapely import wkb, wkt

    bq_field = schema.SchemaField("field_name", "GEOGRAPHY")

    series = pandas.Series([None, wkt.loads("point(0 0)")])
    array = module_under_test.bq_to_arrow_array(series, bq_field)
    # The result is binary, because we use wkb format
    assert array.type == pyarrow.binary()
    assert array.to_pylist() == [None, wkb.dumps(series[1])]

    # All na:
    series = pandas.Series([None, None])
    array = module_under_test.bq_to_arrow_array(series, bq_field)
    assert array.type == pyarrow.string()
    assert array.to_pylist() == list(series)


@pytest.mark.skipif(geopandas is None, reason="Requires `geopandas`")
@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
def test_bq_to_arrow_array_w_geography_type_wkb_data(module_under_test):
    from shapely import wkb, wkt

    bq_field = schema.SchemaField("field_name", "GEOGRAPHY")

    series = pandas.Series([None, wkb.dumps(wkt.loads("point(0 0)"))])
    array = module_under_test.bq_to_arrow_array(series, bq_field)
    # The result is binary, because we use wkb format
    assert array.type == pyarrow.binary()
    assert array.to_pylist() == list(series)


@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
def test_bq_to_arrow_schema_w_unknown_type(module_under_test):
    fields = (
        schema.SchemaField("field1", "STRING"),
        schema.SchemaField("field2", "INTEGER"),
        # Don't know what to convert UNKNOWN_TYPE to, let type inference work,
        # instead.
        schema.SchemaField("field3", "UNKNOWN_TYPE"),
    )
    with warnings.catch_warnings(record=True) as warned:
        actual = module_under_test.bq_to_arrow_schema(fields)
    assert actual is None

    assert len(warned) == 1
    warning = warned[0]
    assert "field3" in str(warning)


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
    module_under_test,
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


@pytest.mark.skipif(
    pandas is None or PANDAS_INSTALLED_VERSION < PANDAS_MINIUM_VERSION,
    reason="Requires `pandas version >= 1.0.0` which introduces pandas.NA",
)
def test_dataframe_to_json_generator(module_under_test):
    utcnow = datetime.datetime.utcnow()
    df_data = collections.OrderedDict(
        [
            ("a_series", [pandas.NA, 2, 3, 4]),
            ("b_series", [0.1, float("NaN"), 0.3, 0.4]),
            ("c_series", ["a", "b", pandas.NA, "d"]),
            ("d_series", [utcnow, utcnow, utcnow, pandas.NaT]),
            ("e_series", [True, False, True, None]),
        ]
    )
    dataframe = pandas.DataFrame(
        df_data, index=pandas.Index([4, 5, 6, 7], name="a_index")
    )

    dataframe = dataframe.astype({"a_series": pandas.Int64Dtype()})

    rows = module_under_test.dataframe_to_json_generator(dataframe)
    expected = [
        {"b_series": 0.1, "c_series": "a", "d_series": utcnow, "e_series": True},
        {"a_series": 2, "c_series": "b", "d_series": utcnow, "e_series": False},
        {"a_series": 3, "b_series": 0.3, "d_series": utcnow, "e_series": True},
        {"a_series": 4, "b_series": 0.4, "c_series": "d"},
    ]
    assert list(rows) == expected


def test_dataframe_to_json_generator_repeated_field(module_under_test):
    pytest.importorskip(
        "pandas",
        minversion=str(PANDAS_MINIUM_VERSION),
        reason=(
            f"Requires `pandas version >= {PANDAS_MINIUM_VERSION}` "
            "which introduces pandas.NA"
        ),
    )

    df_data = [
        collections.OrderedDict(
            [("repeated_col", [pandas.NA, 2, None, 4]), ("not_repeated_col", "first")]
        ),
        collections.OrderedDict(
            [
                ("repeated_col", ["a", "b", mock.sentinel.foo, "d"]),
                ("not_repeated_col", "second"),
            ]
        ),
    ]
    dataframe = pandas.DataFrame(df_data)

    rows = module_under_test.dataframe_to_json_generator(dataframe)

    expected = [
        {"repeated_col": [pandas.NA, 2, None, 4], "not_repeated_col": "first"},
        {
            "repeated_col": ["a", "b", mock.sentinel.foo, "d"],
            "not_repeated_col": "second",
        },
    ]
    assert list(rows) == expected


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
def test_dataframe_to_bq_schema_dict_sequence(module_under_test):
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

    returned_schema = module_under_test.dataframe_to_bq_schema(dataframe, dict_schema)

    expected_schema = (
        schema.SchemaField("str_column", "STRING", "NULLABLE"),
        schema.SchemaField("int_column", "INTEGER", "NULLABLE"),
        schema.SchemaField("bool_column", "BOOL", "REQUIRED"),
    )
    assert returned_schema == expected_schema


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
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
@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
def test_dataframe_to_arrow_with_required_fields(module_under_test):
    bq_schema = (
        schema.SchemaField("field01", "STRING", mode="REQUIRED"),
        schema.SchemaField("field02", "BYTES", mode="REQUIRED"),
        schema.SchemaField("field03", "INTEGER", mode="REQUIRED"),
        schema.SchemaField("field04", "INT64", mode="REQUIRED"),
        schema.SchemaField("field05", "FLOAT", mode="REQUIRED"),
        schema.SchemaField("field06", "FLOAT64", mode="REQUIRED"),
        schema.SchemaField("field07", "NUMERIC", mode="REQUIRED"),
        schema.SchemaField("field08", "BIGNUMERIC", mode="REQUIRED"),
        schema.SchemaField("field09", "BOOLEAN", mode="REQUIRED"),
        schema.SchemaField("field10", "BOOL", mode="REQUIRED"),
        schema.SchemaField("field11", "TIMESTAMP", mode="REQUIRED"),
        schema.SchemaField("field12", "DATE", mode="REQUIRED"),
        schema.SchemaField("field13", "TIME", mode="REQUIRED"),
        schema.SchemaField("field14", "DATETIME", mode="REQUIRED"),
        schema.SchemaField("field15", "GEOGRAPHY", mode="REQUIRED"),
    )

    data = {
        "field01": ["hello", "world"],
        "field02": [b"abd", b"efg"],
        "field03": [1, 2],
        "field04": [3, 4],
        "field05": [1.25, 9.75],
        "field06": [-1.75, -3.5],
        "field07": [decimal.Decimal("1.2345"), decimal.Decimal("6.7891")],
        "field08": [
            decimal.Decimal("-{d38}.{d38}".format(d38="9" * 38)),
            decimal.Decimal("{d38}.{d38}".format(d38="9" * 38)),
        ],
        "field09": [True, False],
        "field10": [False, True],
        "field11": [
            datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc),
            datetime.datetime(2012, 12, 21, 9, 7, 42, tzinfo=datetime.timezone.utc),
        ],
        "field12": [datetime.date(9999, 12, 31), datetime.date(1970, 1, 1)],
        "field13": [datetime.time(23, 59, 59, 999999), datetime.time(12, 0, 0)],
        "field14": [
            datetime.datetime(1970, 1, 1, 0, 0, 0),
            datetime.datetime(2012, 12, 21, 9, 7, 42),
        ],
        "field15": ["POINT(30 10)", "POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))"],
    }
    dataframe = pandas.DataFrame(data)

    arrow_table = module_under_test.dataframe_to_arrow(dataframe, bq_schema)
    arrow_schema = arrow_table.schema

    assert len(arrow_schema) == len(bq_schema)
    for arrow_field in arrow_schema:
        assert not arrow_field.nullable


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
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
@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
def test_dataframe_to_arrow_dict_sequence_schema(module_under_test):
    dict_schema = [
        {"name": "field01", "type": "STRING", "mode": "REQUIRED"},
        {"name": "field02", "type": "BOOL", "mode": "NULLABLE"},
    ]

    dataframe = pandas.DataFrame(
        {"field01": ["hello", "world"], "field02": [True, False]}
    )

    arrow_table = module_under_test.dataframe_to_arrow(dataframe, dict_schema)
    arrow_schema = arrow_table.schema

    expected_fields = [
        pyarrow.field("field01", "string", nullable=False),
        pyarrow.field("field02", "bool", nullable=True),
    ]
    assert list(arrow_schema) == expected_fields


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
def test_dataframe_to_parquet_without_pyarrow(module_under_test, monkeypatch):
    mock_pyarrow_import = mock.Mock()
    mock_pyarrow_import.side_effect = exceptions.LegacyPyarrowError(
        "pyarrow not installed"
    )
    monkeypatch.setattr(_helpers.PYARROW_VERSIONS, "try_import", mock_pyarrow_import)

    with pytest.raises(exceptions.LegacyPyarrowError):
        module_under_test.dataframe_to_parquet(pandas.DataFrame(), (), None)


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
def test_dataframe_to_parquet_w_extra_fields(module_under_test):
    with pytest.raises(ValueError) as exc_context:
        module_under_test.dataframe_to_parquet(
            pandas.DataFrame(), (schema.SchemaField("not_in_df", "STRING"),), None
        )
    message = str(exc_context.value)
    assert "bq_schema contains fields not present in dataframe" in message
    assert "not_in_df" in message


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
def test_dataframe_to_parquet_w_missing_fields(module_under_test, monkeypatch):
    with pytest.raises(ValueError) as exc_context:
        module_under_test.dataframe_to_parquet(
            pandas.DataFrame({"not_in_bq": [1, 2, 3]}), (), None
        )
    message = str(exc_context.value)
    assert "bq_schema is missing fields from dataframe" in message
    assert "not_in_bq" in message


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
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


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
def test_dataframe_to_bq_schema_fallback_needed_wo_pyarrow(module_under_test):
    dataframe = pandas.DataFrame(
        data=[
            {"id": 10, "status": "FOO", "execution_date": datetime.date(2019, 5, 10)},
            {"id": 20, "status": "BAR", "created_at": datetime.date(2018, 9, 12)},
        ]
    )

    no_pyarrow_patch = mock.patch(module_under_test.__name__ + ".pyarrow", None)

    with no_pyarrow_patch, warnings.catch_warnings(record=True) as warned:
        detected_schema = module_under_test.dataframe_to_bq_schema(
            dataframe, bq_schema=[]
        )

    assert detected_schema is None

    # a warning should also be issued
    expected_warnings = [
        warning for warning in warned if "could not determine" in str(warning).lower()
    ]
    assert len(expected_warnings) == 1
    msg = str(expected_warnings[0])
    assert "execution_date" in msg and "created_at" in msg


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
def test_dataframe_to_bq_schema_fallback_needed_w_pyarrow(module_under_test):
    dataframe = pandas.DataFrame(
        data=[
            {"id": 10, "status": "FOO", "created_at": datetime.date(2019, 5, 10)},
            {"id": 20, "status": "BAR", "created_at": datetime.date(2018, 9, 12)},
        ]
    )

    with warnings.catch_warnings(record=True) as warned:
        detected_schema = module_under_test.dataframe_to_bq_schema(
            dataframe, bq_schema=[]
        )

    expected_schema = (
        schema.SchemaField("id", "INTEGER", mode="NULLABLE"),
        schema.SchemaField("status", "STRING", mode="NULLABLE"),
        schema.SchemaField("created_at", "DATE", mode="NULLABLE"),
    )
    by_name = operator.attrgetter("name")
    assert sorted(detected_schema, key=by_name) == sorted(expected_schema, key=by_name)

    # there should be no relevant warnings
    unwanted_warnings = [
        warning for warning in warned if "could not determine" in str(warning).lower()
    ]
    assert not unwanted_warnings


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
def test_dataframe_to_bq_schema_pyarrow_fallback_fails(module_under_test):
    dataframe = pandas.DataFrame(
        data=[
            {"struct_field": {"one": 2}, "status": "FOO"},
            {"struct_field": {"two": "222"}, "status": "BAR"},
        ]
    )

    with warnings.catch_warnings(record=True) as warned:
        detected_schema = module_under_test.dataframe_to_bq_schema(
            dataframe, bq_schema=[]
        )

    assert detected_schema is None

    # a warning should also be issued
    expected_warnings = [
        warning for warning in warned if "could not determine" in str(warning).lower()
    ]
    assert len(expected_warnings) == 1
    assert "struct_field" in str(expected_warnings[0])


@pytest.mark.skipif(geopandas is None, reason="Requires `geopandas`")
def test_dataframe_to_bq_schema_geography(module_under_test):
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
    bq_schema = module_under_test.dataframe_to_bq_schema(df, [])
    assert bq_schema == (
        schema.SchemaField("name", "STRING"),
        schema.SchemaField("geo1", "GEOGRAPHY"),
        schema.SchemaField("geo2", "GEOGRAPHY"),
    )


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
def test_augment_schema_type_detection_succeeds(module_under_test):
    dataframe = pandas.DataFrame(
        data=[
            {
                "bool_field": False,
                "int_field": 123,
                "float_field": 3.141592,
                "time_field": datetime.time(17, 59, 47),
                "timestamp_field": datetime.datetime(2005, 5, 31, 14, 25, 55),
                "date_field": datetime.date(2005, 5, 31),
                "bytes_field": b"some bytes",
                "string_field": "some characters",
                "numeric_field": decimal.Decimal("123.456"),
                "bignumeric_field": decimal.Decimal("{d38}.{d38}".format(d38="9" * 38)),
            }
        ]
    )

    # NOTE: In Pandas dataframe, the dtype of Python's datetime instances is
    # set to "datetime64[ns]", and pyarrow converts that to pyarrow.TimestampArray.
    # We thus cannot expect to get a DATETIME date when converting back to the
    # BigQuery type.

    current_schema = (
        schema.SchemaField("bool_field", field_type=None, mode="NULLABLE"),
        schema.SchemaField("int_field", field_type=None, mode="NULLABLE"),
        schema.SchemaField("float_field", field_type=None, mode="NULLABLE"),
        schema.SchemaField("time_field", field_type=None, mode="NULLABLE"),
        schema.SchemaField("timestamp_field", field_type=None, mode="NULLABLE"),
        schema.SchemaField("date_field", field_type=None, mode="NULLABLE"),
        schema.SchemaField("bytes_field", field_type=None, mode="NULLABLE"),
        schema.SchemaField("string_field", field_type=None, mode="NULLABLE"),
        schema.SchemaField("numeric_field", field_type=None, mode="NULLABLE"),
        schema.SchemaField("bignumeric_field", field_type=None, mode="NULLABLE"),
    )

    with warnings.catch_warnings(record=True) as warned:
        augmented_schema = module_under_test.augment_schema(dataframe, current_schema)

    # there should be no relevant warnings
    unwanted_warnings = [
        warning for warning in warned if "Pyarrow could not" in str(warning)
    ]
    assert not unwanted_warnings

    # the augmented schema must match the expected
    expected_schema = (
        schema.SchemaField("bool_field", field_type="BOOL", mode="NULLABLE"),
        schema.SchemaField("int_field", field_type="INT64", mode="NULLABLE"),
        schema.SchemaField("float_field", field_type="FLOAT64", mode="NULLABLE"),
        schema.SchemaField("time_field", field_type="TIME", mode="NULLABLE"),
        schema.SchemaField("timestamp_field", field_type="TIMESTAMP", mode="NULLABLE"),
        schema.SchemaField("date_field", field_type="DATE", mode="NULLABLE"),
        schema.SchemaField("bytes_field", field_type="BYTES", mode="NULLABLE"),
        schema.SchemaField("string_field", field_type="STRING", mode="NULLABLE"),
        schema.SchemaField("numeric_field", field_type="NUMERIC", mode="NULLABLE"),
        schema.SchemaField(
            "bignumeric_field", field_type="BIGNUMERIC", mode="NULLABLE"
        ),
    )

    by_name = operator.attrgetter("name")
    assert sorted(augmented_schema, key=by_name) == sorted(expected_schema, key=by_name)


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
def test_augment_schema_type_detection_fails(module_under_test):
    dataframe = pandas.DataFrame(
        data=[
            {
                "status": "FOO",
                "struct_field": {"one": 1},
                "struct_field_2": {"foo": "123"},
            },
            {
                "status": "BAR",
                "struct_field": {"two": "111"},
                "struct_field_2": {"bar": 27},
            },
        ]
    )
    current_schema = [
        schema.SchemaField("status", field_type="STRING", mode="NULLABLE"),
        schema.SchemaField("struct_field", field_type=None, mode="NULLABLE"),
        schema.SchemaField("struct_field_2", field_type=None, mode="NULLABLE"),
    ]

    with warnings.catch_warnings(record=True) as warned:
        augmented_schema = module_under_test.augment_schema(dataframe, current_schema)

    assert augmented_schema is None

    expected_warnings = [
        warning for warning in warned if "could not determine" in str(warning)
    ]
    assert len(expected_warnings) == 1
    warning_msg = str(expected_warnings[0])
    assert "pyarrow" in warning_msg.lower()
    assert "struct_field" in warning_msg and "struct_field_2" in warning_msg


@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
def test_dataframe_to_parquet_dict_sequence_schema(module_under_test):
    dict_schema = [
        {"name": "field01", "type": "STRING", "mode": "REQUIRED"},
        {"name": "field02", "type": "BOOL", "mode": "NULLABLE"},
    ]

    dataframe = pandas.DataFrame(
        {"field01": ["hello", "world"], "field02": [True, False]}
    )

    write_table_patch = mock.patch.object(
        module_under_test.pyarrow.parquet, "write_table", autospec=True
    )
    to_arrow_patch = mock.patch.object(
        module_under_test, "dataframe_to_arrow", autospec=True
    )

    with write_table_patch, to_arrow_patch as fake_to_arrow:
        module_under_test.dataframe_to_parquet(dataframe, dict_schema, None)

    expected_schema_arg = [
        schema.SchemaField("field01", "STRING", mode="REQUIRED"),
        schema.SchemaField("field02", "BOOL", mode="NULLABLE"),
    ]
    schema_arg = fake_to_arrow.call_args.args[1]
    assert schema_arg == expected_schema_arg


@pytest.mark.skipif(
    bigquery_storage is None, reason="Requires `google-cloud-bigquery-storage`"
)
def test__download_table_bqstorage_stream_includes_read_session(
    monkeypatch, module_under_test
):
    import google.cloud.bigquery_storage_v1.reader
    import google.cloud.bigquery_storage_v1.types

    monkeypatch.setattr(_helpers.BQ_STORAGE_VERSIONS, "_installed_version", None)
    monkeypatch.setattr(bigquery_storage, "__version__", "2.5.0")
    bqstorage_client = mock.create_autospec(
        bigquery_storage.BigQueryReadClient, instance=True
    )
    reader = mock.create_autospec(
        google.cloud.bigquery_storage_v1.reader.ReadRowsStream, instance=True
    )
    bqstorage_client.read_rows.return_value = reader
    session = google.cloud.bigquery_storage_v1.types.ReadSession()

    module_under_test._download_table_bqstorage_stream(
        module_under_test._DownloadState(),
        bqstorage_client,
        session,
        google.cloud.bigquery_storage_v1.types.ReadStream(name="test"),
        queue.Queue(),
        mock.Mock(),
    )

    reader.rows.assert_called_once_with(session)


@pytest.mark.skipif(
    bigquery_storage is None
    or not _helpers.BQ_STORAGE_VERSIONS.is_read_session_optional,
    reason="Requires `google-cloud-bigquery-storage` >= 2.6.0",
)
def test__download_table_bqstorage_stream_omits_read_session(
    monkeypatch, module_under_test
):
    import google.cloud.bigquery_storage_v1.reader
    import google.cloud.bigquery_storage_v1.types

    monkeypatch.setattr(_helpers.BQ_STORAGE_VERSIONS, "_installed_version", None)
    monkeypatch.setattr(bigquery_storage, "__version__", "2.6.0")
    bqstorage_client = mock.create_autospec(
        bigquery_storage.BigQueryReadClient, instance=True
    )
    reader = mock.create_autospec(
        google.cloud.bigquery_storage_v1.reader.ReadRowsStream, instance=True
    )
    bqstorage_client.read_rows.return_value = reader
    session = google.cloud.bigquery_storage_v1.types.ReadSession()

    module_under_test._download_table_bqstorage_stream(
        module_under_test._DownloadState(),
        bqstorage_client,
        session,
        google.cloud.bigquery_storage_v1.types.ReadStream(name="test"),
        queue.Queue(),
        mock.Mock(),
    )

    reader.rows.assert_called_once_with()


@pytest.mark.parametrize(
    "stream_count,maxsize_kwarg,expected_call_count,expected_maxsize",
    [
        (3, {"max_queue_size": 2}, 3, 2),  # custom queue size
        (4, {}, 4, 4),  # default queue size
        (7, {"max_queue_size": None}, 7, 0),  # infinite queue size
    ],
)
@pytest.mark.skipif(
    bigquery_storage is None, reason="Requires `google-cloud-bigquery-storage`"
)
def test__download_table_bqstorage(
    module_under_test,
    stream_count,
    maxsize_kwarg,
    expected_call_count,
    expected_maxsize,
):
    from google.cloud.bigquery import dataset
    from google.cloud.bigquery import table

    queue_used = None  # A reference to the queue used by code under test.

    bqstorage_client = mock.create_autospec(
        bigquery_storage.BigQueryReadClient, instance=True
    )
    fake_session = mock.Mock(streams=["stream/s{i}" for i in range(stream_count)])
    bqstorage_client.create_read_session.return_value = fake_session

    table_ref = table.TableReference(
        dataset.DatasetReference("project-x", "dataset-y"), "table-z",
    )

    def fake_download_stream(
        download_state, bqstorage_client, session, stream, worker_queue, page_to_item
    ):
        nonlocal queue_used
        queue_used = worker_queue
        try:
            worker_queue.put_nowait("result_page")
        except queue.Full:  # pragma: NO COVER
            pass

    download_stream = mock.Mock(side_effect=fake_download_stream)

    with mock.patch.object(
        module_under_test, "_download_table_bqstorage_stream", new=download_stream
    ):
        result_gen = module_under_test._download_table_bqstorage(
            "some-project", table_ref, bqstorage_client, **maxsize_kwarg
        )
        list(result_gen)

    # Timing-safe, as the method under test should block until the pool shutdown is
    # complete, at which point all download stream workers have already been submitted
    # to the thread pool.
    assert download_stream.call_count == stream_count  # once for each stream
    assert queue_used.maxsize == expected_maxsize


@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
def test_download_arrow_row_iterator_unknown_field_type(module_under_test):
    fake_page = api_core.page_iterator.Page(
        parent=mock.Mock(),
        items=[{"page_data": "foo"}],
        item_to_value=api_core.page_iterator._item_to_value_identity,
    )
    fake_page._columns = [[1, 10, 100], [2.2, 22.22, 222.222]]
    pages = [fake_page]

    bq_schema = [
        schema.SchemaField("population_size", "INTEGER"),
        schema.SchemaField("alien_field", "ALIEN_FLOAT_TYPE"),
    ]

    results_gen = module_under_test.download_arrow_row_iterator(pages, bq_schema)

    with warnings.catch_warnings(record=True) as warned:
        result = next(results_gen)

    unwanted_warnings = [
        warning
        for warning in warned
        if "please pass schema= explicitly" in str(warning).lower()
    ]
    assert not unwanted_warnings

    assert len(result.columns) == 2
    col = result.columns[0]
    assert type(col) is pyarrow.lib.Int64Array
    assert col.to_pylist() == [1, 10, 100]
    col = result.columns[1]
    assert type(col) is pyarrow.lib.DoubleArray
    assert col.to_pylist() == [2.2, 22.22, 222.222]


@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
def test_download_arrow_row_iterator_known_field_type(module_under_test):
    fake_page = api_core.page_iterator.Page(
        parent=mock.Mock(),
        items=[{"page_data": "foo"}],
        item_to_value=api_core.page_iterator._item_to_value_identity,
    )
    fake_page._columns = [[1, 10, 100], ["2.2", "22.22", "222.222"]]
    pages = [fake_page]

    bq_schema = [
        schema.SchemaField("population_size", "INTEGER"),
        schema.SchemaField("non_alien_field", "STRING"),
    ]

    results_gen = module_under_test.download_arrow_row_iterator(pages, bq_schema)
    with warnings.catch_warnings(record=True) as warned:
        result = next(results_gen)

    unwanted_warnings = [
        warning
        for warning in warned
        if "please pass schema= explicitly" in str(warning).lower()
    ]
    assert not unwanted_warnings

    assert len(result.columns) == 2
    col = result.columns[0]
    assert type(col) is pyarrow.lib.Int64Array
    assert col.to_pylist() == [1, 10, 100]
    col = result.columns[1]
    assert type(col) is pyarrow.lib.StringArray
    assert col.to_pylist() == ["2.2", "22.22", "222.222"]


@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
def test_download_arrow_row_iterator_dict_sequence_schema(module_under_test):
    fake_page = api_core.page_iterator.Page(
        parent=mock.Mock(),
        items=[{"page_data": "foo"}],
        item_to_value=api_core.page_iterator._item_to_value_identity,
    )
    fake_page._columns = [[1, 10, 100], ["2.2", "22.22", "222.222"]]
    pages = [fake_page]

    dict_schema = [
        {"name": "population_size", "type": "INTEGER", "mode": "NULLABLE"},
        {"name": "non_alien_field", "type": "STRING", "mode": "NULLABLE"},
    ]

    results_gen = module_under_test.download_arrow_row_iterator(pages, dict_schema)
    result = next(results_gen)

    assert len(result.columns) == 2
    col = result.columns[0]
    assert type(col) is pyarrow.lib.Int64Array
    assert col.to_pylist() == [1, 10, 100]
    col = result.columns[1]
    assert type(col) is pyarrow.lib.StringArray
    assert col.to_pylist() == ["2.2", "22.22", "222.222"]


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
def test_download_dataframe_row_iterator_dict_sequence_schema(module_under_test):
    fake_page = api_core.page_iterator.Page(
        parent=mock.Mock(),
        items=[{"page_data": "foo"}],
        item_to_value=api_core.page_iterator._item_to_value_identity,
    )
    fake_page._columns = [[1, 10, 100], ["2.2", "22.22", "222.222"]]
    pages = [fake_page]

    dict_schema = [
        {"name": "population_size", "type": "INTEGER", "mode": "NULLABLE"},
        {"name": "non_alien_field", "type": "STRING", "mode": "NULLABLE"},
    ]

    results_gen = module_under_test.download_dataframe_row_iterator(
        pages, dict_schema, dtypes={}
    )
    result = next(results_gen)

    expected_result = pandas.DataFrame(
        collections.OrderedDict(
            [
                ("population_size", [1, 10, 100]),
                ("non_alien_field", ["2.2", "22.22", "222.222"]),
            ]
        )
    )
    assert result.equals(expected_result)

    with pytest.raises(StopIteration):
        result = next(results_gen)


@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
def test_table_data_listpage_to_dataframe_skips_stop_iteration(module_under_test):
    dataframe = module_under_test._row_iterator_page_to_dataframe([], [], {})
    assert isinstance(dataframe, pandas.DataFrame)


@pytest.mark.skipif(isinstance(pyarrow, mock.Mock), reason="Requires `pyarrow`")
def test_bq_to_arrow_field_type_override(module_under_test):
    # When loading pandas data, we may need to override the type
    # decision based on data contents, because GEOGRAPHY data can be
    # stored as either text or binary.

    assert (
        module_under_test.bq_to_arrow_field(schema.SchemaField("g", "GEOGRAPHY")).type
        == pyarrow.string()
    )

    assert (
        module_under_test.bq_to_arrow_field(
            schema.SchemaField("g", "GEOGRAPHY"), pyarrow.binary(),
        ).type
        == pyarrow.binary()
    )
