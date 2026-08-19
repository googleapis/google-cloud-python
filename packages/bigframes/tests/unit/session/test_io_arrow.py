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

import pyarrow as pa
import pytest

import bigframes.pandas as bpd
from bigframes.testing import mocks


@pytest.fixture(scope="module")
def session():
    # Use the mock session from bigframes.testing
    return mocks.create_bigquery_session()


def test_read_arrow_empty_table(session):
    empty_table = pa.Table.from_pydict(
        {
            "col_a": pa.array([], type=pa.int64()),
            "col_b": pa.array([], type=pa.string()),
        }
    )
    df = session.read_arrow(empty_table)
    assert isinstance(df, bpd.DataFrame)
    assert df.shape == (0, 2)
    assert list(df.columns) == ["col_a", "col_b"]
    pd_df = df.to_pandas()
    assert pd_df.empty
    assert list(pd_df.columns) == ["col_a", "col_b"]
    assert pd_df["col_a"].dtype == "Int64"
    assert pd_df["col_b"].dtype == "string[pyarrow]"


@pytest.mark.parametrize(
    "data,arrow_type,expected_bq_type_kind",
    [
        ([1, 2], pa.int8(), "INTEGER"),
        ([1, 2], pa.int16(), "INTEGER"),
        ([1, 2], pa.int32(), "INTEGER"),
        ([1, 2], pa.int64(), "INTEGER"),
        ([1.0, 2.0], pa.float32(), "FLOAT"),
        ([1.0, 2.0], pa.float64(), "FLOAT"),
        ([True, False], pa.bool_(), "BOOLEAN"),
        (["a", "b"], pa.string(), "STRING"),
        (["a", "b"], pa.large_string(), "STRING"),
        ([b"a", b"b"], pa.binary(), "BYTES"),
        ([b"a", b"b"], pa.large_binary(), "BYTES"),
        (
            [
                pa.scalar(1000, type=pa.duration("s")),
                pa.scalar(2000, type=pa.duration("s")),
            ],
            pa.duration("s"),
            "INTEGER",
        ),
        ([datetime.date(2023, 1, 1)], pa.date32(), "DATE"),
        (
            [datetime.datetime(2023, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)],
            pa.timestamp("s", tz="UTC"),
            "TIMESTAMP",
        ),
        (
            [datetime.datetime(2023, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)],
            pa.timestamp("ms", tz="UTC"),
            "TIMESTAMP",
        ),
        (
            [datetime.datetime(2023, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)],
            pa.timestamp("us", tz="UTC"),
            "TIMESTAMP",
        ),
        ([datetime.time(12, 34, 56, 789000)], pa.time64("us"), "TIME"),
    ],
)
def test_read_arrow_type_mappings(session, data, arrow_type, expected_bq_type_kind):
    """
    Tests that various arrow types are mapped to the expected BigQuery types.
    This is an indirect check via the resulting DataFrame's schema.
    """
    pa_table = pa.Table.from_arrays([pa.array(data, type=arrow_type)], names=["col"])
    df = session.read_arrow(pa_table)

    bigquery_schema = df._block.expr.schema.to_bigquery()
    assert len(bigquery_schema) == 2  # offsets + value
    field = bigquery_schema[-1]
    assert field.field_type.upper() == expected_bq_type_kind

    # Also check pandas dtype after conversion for good measure
    pd_df = df.to_pandas()
    assert pd_df["col"].shape == (len(data),)


def test_read_arrow_list_type(session):
    pa_table = pa.Table.from_arrays(
        [pa.array([[1, 2], [3, 4, 5]], type=pa.list_(pa.int64()))], names=["list_col"]
    )
    df = session.read_arrow(pa_table)

    bigquery_schema = df._block.expr.schema.to_bigquery()
    assert len(bigquery_schema) == 2  # offsets + value
    field = bigquery_schema[-1]
    assert field.mode.upper() == "REPEATED"
    assert field.field_type.upper() == "INTEGER"


def test_read_arrow_struct_type(session):
    struct_type = pa.struct([("a", pa.int64()), ("b", pa.string())])
    pa_table = pa.Table.from_arrays(
        [pa.array([{"a": 1, "b": "x"}, {"a": 2, "b": "y"}], type=struct_type)],
        names=["struct_col"],
    )
    df = session.read_arrow(pa_table)

    bigquery_schema = df._block.expr.schema.to_bigquery()
    assert len(bigquery_schema) == 2  # offsets + value
    field = bigquery_schema[-1]
    assert field.field_type.upper() == "RECORD"
    assert field.fields[0].name == "a"
    assert field.fields[1].name == "b"
