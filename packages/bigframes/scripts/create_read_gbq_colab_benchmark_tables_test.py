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

from __future__ import annotations

import base64
import datetime
import json
import math
import re

# Assuming the script to be tested is in the same directory or accessible via PYTHONPATH
from create_read_gbq_colab_benchmark_tables import (
    BIGQUERY_DATA_TYPE_SIZES,
    generate_batch,
    generate_work_items,
    get_bq_schema,
)
import numpy as np
import pytest


# Helper function to calculate estimated row size from schema
def _calculate_row_size(schema: list[tuple[str, str, int | None]]) -> int:
    """Calculates the estimated byte size of a row based on the schema.
    Note: This is a simplified calculation for testing and might not perfectly
    match BigQuery's internal storage, especially for complex types or NULLs.
    """
    size = 0
    for _, bq_type, length in schema:
        if bq_type in ["STRING", "BYTES", "JSON"]:
            # Base cost (e.g., 2 bytes) + content length
            size += BIGQUERY_DATA_TYPE_SIZES[bq_type] + (
                length if length is not None else 0
            )
        elif bq_type in BIGQUERY_DATA_TYPE_SIZES:
            size += BIGQUERY_DATA_TYPE_SIZES[bq_type]
        else:
            raise AssertionError(f"Got unexpected type {bq_type}")
    return size


# --- Tests for get_bq_schema ---


def test_get_bq_schema_zero_bytes():
    assert get_bq_schema(0) == []


def test_get_bq_schema_one_byte():
    schema = get_bq_schema(1)

    assert len(schema) == 1
    assert schema[0][1] == "BOOL"  # ('col_bool_fallback_0', 'BOOL', None) or similar
    assert _calculate_row_size(schema) == 1


def test_get_bq_schema_exact_fixed_fit():
    # BOOL (1) + INT64 (8) = 9 bytes
    target_size = 9
    schema = get_bq_schema(target_size)

    assert len(schema) == 2
    assert schema[0][1] == "BOOL"
    assert schema[1][1] == "INT64"
    assert _calculate_row_size(schema) == target_size


def test_get_bq_schema_needs_flexible_string():
    # Sum of all fixed types:
    # BOOL 1, INT64 8, FLOAT64 8, NUMERIC 16, DATE 8, DATETIME 8, TIMESTAMP 8, TIME 8
    # Total = 1+8+8+16+8+8+8+8 = 65
    target_size = 65 + 1
    schema = get_bq_schema(target_size)

    assert _calculate_row_size(schema) == 65 + 2 + 2 + 1

    string_cols = [s for s in schema if s[1] == "STRING"]
    assert len(string_cols) == 1
    assert string_cols[0][2] == 0

    bytes_cols = [s for s in schema if s[1] == "BYTES"]
    assert len(bytes_cols) == 1
    assert bytes_cols[0][2] == 0

    json_cols = [s for s in schema if s[1] == "JSON"]
    assert len(json_cols) == 1
    assert json_cols[0][2] == 1


def test_get_bq_schema_flexible_expansion():
    # Sum of all fixed types:
    # BOOL 1, INT64 8, FLOAT64 8, NUMERIC 16, DATE 8, DATETIME 8, TIMESTAMP 8, TIME 8
    # Total = 1+8+8+16+8+8+8+8 = 65
    target_size = 65 + 3 * 5
    schema = get_bq_schema(target_size)

    assert _calculate_row_size(schema) == target_size

    string_cols = [s for s in schema if s[1] == "STRING"]
    assert len(string_cols) == 1
    assert string_cols[0][2] == 3

    bytes_cols = [s for s in schema if s[1] == "BYTES"]
    assert len(bytes_cols) == 1
    assert bytes_cols[0][2] == 3

    json_cols = [s for s in schema if s[1] == "JSON"]
    assert len(json_cols) == 1
    assert json_cols[0][2] == 5


def test_get_bq_schema_all_fixed_types_possible():
    # Sum of all fixed types:
    # BOOL 1, INT64 8, FLOAT64 8, NUMERIC 16, DATE 8, DATETIME 8, TIMESTAMP 8, TIME 8
    # Total = 1+8+8+16+8+8+8+8 = 65
    target_size = 65
    schema = get_bq_schema(target_size)

    expected_fixed_types = {
        "BOOL",
        "INT64",
        "FLOAT64",
        "NUMERIC",
        "DATE",
        "DATETIME",
        "TIMESTAMP",
        "TIME",
    }
    present_types = {s[1] for s in schema}

    assert expected_fixed_types.issubset(present_types)

    # Check if the size is close to target.
    # All fixed (65)
    calculated_size = _calculate_row_size(schema)
    assert calculated_size == target_size


def test_get_bq_schema_uniqueness_of_column_names():
    target_size = 100  # A size that generates multiple columns
    schema = get_bq_schema(target_size)

    column_names = [s[0] for s in schema]
    assert len(column_names) == len(set(column_names))


# --- Tests for generate_work_items ---


def test_generate_work_items_zero_rows():
    schema = [("col_int", "INT64", None)]
    data_generator = generate_work_items(
        "some_table", schema, num_rows=0, batch_size=10
    )

    # Expect the generator to be exhausted
    with pytest.raises(StopIteration):
        next(data_generator)


def test_generate_work_items_basic_schema_and_batching():
    schema = [("id", "INT64", None), ("is_active", "BOOL", None)]
    num_rows = 25
    batch_size = 10

    generated_rows_count = 0
    batch_count = 0
    for work_item in generate_work_items("some_table", schema, num_rows, batch_size):
        table_id, schema_def, num_rows_in_batch = work_item
        assert table_id == "some_table"
        assert schema_def == schema
        assert num_rows_in_batch <= num_rows
        assert num_rows_in_batch <= batch_size
        batch_count += 1
        generated_rows_count += num_rows_in_batch

    assert generated_rows_count == num_rows
    assert batch_count == math.ceil(num_rows / batch_size)  # 25/10 = 2.5 -> 3 batches


def test_generate_work_items_batch_size_larger_than_num_rows():
    schema = [("value", "FLOAT64", None)]
    num_rows = 5
    batch_size = 100

    generated_rows_count = 0
    batch_count = 0
    for work_item in generate_work_items("some_table", schema, num_rows, batch_size):
        table_id, schema_def, num_rows_in_batch = work_item
        assert table_id == "some_table"
        assert schema_def == schema
        assert num_rows_in_batch == num_rows  # Should be one batch with all rows
        batch_count += 1
        generated_rows_count += num_rows_in_batch

    assert generated_rows_count == num_rows
    assert batch_count == 1


def test_generate_work_items_all_datatypes(rng):
    schema = [
        ("c_bool", "BOOL", None),
        ("c_int64", "INT64", None),
        ("c_float64", "FLOAT64", None),
        ("c_numeric", "NUMERIC", None),
        ("c_date", "DATE", None),
        ("c_datetime", "DATETIME", None),
        ("c_timestamp", "TIMESTAMP", None),
        ("c_time", "TIME", None),
        ("c_string", "STRING", 10),
        ("c_bytes", "BYTES", 5),
        ("c_json", "JSON", 20),  # Length for JSON is content hint
    ]
    num_rows = 3
    batch_size = 2  # To test multiple batches

    total_rows_processed = 0
    for work_item in generate_work_items("some_table", schema, num_rows, batch_size):
        table_id, schema_def, num_rows_in_batch = work_item
        assert table_id == "some_table"
        assert schema_def == schema
        assert num_rows_in_batch <= batch_size
        assert num_rows_in_batch <= num_rows

        total_rows_processed += num_rows_in_batch

    assert total_rows_processed == num_rows


# --- Pytest Fixture for RNG ---
@pytest.fixture
def rng():
    return np.random.default_rng(seed=42)


def test_generate_batch_basic_schema(rng):
    schema = [("id", "INT64", None), ("is_active", "BOOL", None)]
    batch = generate_batch(schema, 5, rng)

    assert len(batch) == 5

    for row in batch:
        assert isinstance(row, dict)
        assert "id" in row
        assert "is_active" in row
        assert isinstance(row["id"], int)
        assert isinstance(row["is_active"], bool)


def test_generate_batch_all_datatypes(rng):
    schema = [
        ("c_bool", "BOOL", None),
        ("c_int64", "INT64", None),
        ("c_float64", "FLOAT64", None),
        ("c_numeric", "NUMERIC", None),
        ("c_date", "DATE", None),
        ("c_datetime", "DATETIME", None),
        ("c_timestamp", "TIMESTAMP", None),
        ("c_time", "TIME", None),
        ("c_string", "STRING", 10),
        ("c_bytes", "BYTES", 5),
        ("c_json", "JSON", 20),  # Length for JSON is content hint
    ]
    num_rows = 3

    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    time_pattern = re.compile(r"^\d{2}:\d{2}:\d{2}(\.\d{1,6})?$")
    # BQ DATETIME: YYYY-MM-DD HH:MM:SS.ffffff
    datetime_pattern = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(\.\d{1,6})?$")
    # BQ TIMESTAMP (UTC 'Z'): YYYY-MM-DDTHH:MM:SS.ffffffZ
    timestamp_pattern = re.compile(
        r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,6})?Z$"
    )
    numeric_pattern = re.compile(r"^-?\d+\.\d{9}$")

    batch = generate_batch(schema, num_rows, rng)
    assert len(batch) == num_rows

    for row in batch:
        assert isinstance(row["c_bool"], bool)
        assert isinstance(row["c_int64"], int)
        assert isinstance(row["c_float64"], float)

        assert isinstance(row["c_numeric"], str)
        assert numeric_pattern.match(row["c_numeric"])

        assert isinstance(row["c_date"], str)
        assert date_pattern.match(row["c_date"])
        datetime.date.fromisoformat(row["c_date"])  # Check parsable

        assert isinstance(row["c_datetime"], str)
        assert datetime_pattern.match(row["c_datetime"])
        datetime.datetime.fromisoformat(row["c_datetime"])  # Check parsable

        assert isinstance(row["c_timestamp"], str)
        assert timestamp_pattern.match(row["c_timestamp"])
        # datetime.fromisoformat can parse 'Z' if Python >= 3.11, or needs replace('Z', '+00:00')
        dt_obj = datetime.datetime.fromisoformat(
            row["c_timestamp"].replace("Z", "+00:00")
        )
        assert dt_obj.tzinfo == datetime.timezone.utc

        assert isinstance(row["c_time"], str)
        assert time_pattern.match(row["c_time"])
        datetime.time.fromisoformat(row["c_time"])  # Check parsable

        assert isinstance(row["c_string"], str)
        assert len(row["c_string"]) == 10

        c_bytes = base64.b64decode(row["c_bytes"])
        assert isinstance(c_bytes, bytes)
        assert len(c_bytes) == 5

        assert isinstance(row["c_json"], str)
        try:
            json.loads(row["c_json"])  # Check if it's valid JSON
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON string generated: {row['c_json']}")
        # Note: Exact length check for JSON is hard due to content variability and escaping.
        # The 'length' parameter for JSON in schema is a hint for content size.
        # We are primarily testing that it's valid JSON.
