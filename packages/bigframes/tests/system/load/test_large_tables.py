# Copyright 2024 Google LLC
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

"""Load test for query (SQL) inputs with large results sizes."""

import pytest

import bigframes.pandas as bpd

KB_BYTES = 1000
MB_BYTES = 1000 * KB_BYTES
GB_BYTES = 1000 * MB_BYTES
TB_BYTES = 1000 * GB_BYTES


@pytest.mark.parametrize(
    ("sql", "expected_bytes"),
    (
        pytest.param(
            "SELECT * FROM load_testing.scalars_1gb",
            GB_BYTES,
            id="1gb",
        ),
        pytest.param(
            "SELECT * FROM load_testing.scalars_10gb",
            10 * GB_BYTES,
            id="10gb",
        ),
        pytest.param(
            "SELECT * FROM load_testing.scalars_100gb",
            100 * GB_BYTES,
            id="100gb",
        ),
        pytest.param(
            "SELECT * FROM load_testing.scalars_1tb",
            TB_BYTES,
            id="1tb",
        ),
    ),
)
def test_read_gbq_sql_large_results(sql, expected_bytes):
    df = bpd.read_gbq(sql)
    assert df.memory_usage().sum() >= expected_bytes


def test_df_repr_large_table():
    df = bpd.read_gbq("load_testing.scalars_100gb")
    row_count, column_count = df.shape
    expected = f"[{row_count} rows x {column_count} columns]"
    actual = repr(df)
    assert expected in actual


def test_series_repr_large_table():
    df = bpd.read_gbq("load_testing.scalars_1tb")
    actual = repr(df["string_col"])
    assert actual is not None


def test_index_repr_large_table():
    df = bpd.read_gbq("load_testing.scalars_1tb")
    actual = repr(df.index)
    assert actual is not None


def test_to_pandas_batches_large_table():
    df = bpd.read_gbq("load_testing.scalars_100gb")
    _, expected_column_count = df.shape

    # download only a few batches, since 1tb would be too much
    iterable = df.to_pandas_batches(
        page_size=500, max_results=1500, allow_large_results=True
    )
    # use page size since client library doesn't support
    # streaming only part of the dataframe via bqstorage
    for pdf in iterable:
        batch_row_count, batch_column_count = pdf.shape
        assert batch_column_count == expected_column_count
        assert 0 < batch_row_count <= 500


@pytest.mark.skip(reason="See if it caused kokoro build aborted.")
def test_to_pandas_large_table():
    df = bpd.read_gbq("load_testing.scalars_10gb")
    # df will be downloaded locally
    expected_row_count, expected_column_count = df.shape

    df_converted = df.to_pandas()
    row_count, column_count = df_converted.shape
    assert column_count == expected_column_count
    assert row_count == expected_row_count
