# Copyright 2021 Google LLC
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

"""System tests for Arrow connector."""

import pytest

pyarrow = pytest.importorskip(
    "pyarrow", minversion="3.0.0"
)  # Needs decimal256 for BIGNUMERIC columns.


@pytest.mark.parametrize(
    ("max_results", "scalars_table_name"),
    (
        (None, "scalars_table"),  # Use BQ Storage API.
        (10, "scalars_table"),  # Use REST API.
        (None, "scalars_extreme_table"),  # Use BQ Storage API.
        (10, "scalars_extreme_table"),  # Use REST API.
    ),
)
def test_list_rows_nullable_scalars_dtypes(
    bigquery_client,
    scalars_table,
    scalars_extreme_table,
    max_results,
    scalars_table_name,
):
    table_id = scalars_table
    if scalars_table_name == "scalars_extreme_table":
        table_id = scalars_extreme_table
    arrow_table = bigquery_client.list_rows(
        table_id, max_results=max_results,
    ).to_arrow()

    schema = arrow_table.schema
    bignumeric_type = schema.field("bignumeric_col").type
    # 77th digit is partial.
    # https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#decimal_types
    assert bignumeric_type.precision in {76, 77}
    assert bignumeric_type.scale == 38

    bool_type = schema.field("bool_col").type
    assert bool_type.equals(pyarrow.bool_())

    bytes_type = schema.field("bytes_col").type
    assert bytes_type.equals(pyarrow.binary())

    date_type = schema.field("date_col").type
    assert date_type.equals(pyarrow.date32())

    datetime_type = schema.field("datetime_col").type
    assert datetime_type.unit == "us"
    assert datetime_type.tz is None

    float64_type = schema.field("float64_col").type
    assert float64_type.equals(pyarrow.float64())

    geography_type = schema.field("geography_col").type
    assert geography_type.equals(pyarrow.string())

    int64_type = schema.field("int64_col").type
    assert int64_type.equals(pyarrow.int64())

    numeric_type = schema.field("numeric_col").type
    assert numeric_type.precision == 38
    assert numeric_type.scale == 9

    string_type = schema.field("string_col").type
    assert string_type.equals(pyarrow.string())

    time_type = schema.field("time_col").type
    assert time_type.equals(pyarrow.time64("us"))

    timestamp_type = schema.field("timestamp_col").type
    assert timestamp_type.unit == "us"
    assert timestamp_type.tz is not None
