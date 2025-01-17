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

import bigframes.bigquery


def test_sql_scalar_on_scalars_null_index(scalars_df_null_index):
    series = bigframes.bigquery.sql_scalar(
        """
        CAST({0} AS INT64)
        + BYTE_LENGTH({1})
        + UNIX_DATE({2})
        + EXTRACT(YEAR FROM {3})
        + ST_NUMPOINTS({4})
        + LEAST(
            {5},
            CAST({6} AS INT64),
            CAST({7} AS INT64)
        ) + CHAR_LENGTH({8})
        + EXTRACT(SECOND FROM {9})
        + UNIX_SECONDS({10})
        """,
        columns=[
            # Try to include all scalar types in a single test.
            scalars_df_null_index["bool_col"],
            scalars_df_null_index["bytes_col"],
            scalars_df_null_index["date_col"],
            scalars_df_null_index["datetime_col"],
            scalars_df_null_index["geography_col"],
            scalars_df_null_index["int64_col"],
            scalars_df_null_index["numeric_col"],
            scalars_df_null_index["float64_col"],
            scalars_df_null_index["string_col"],
            scalars_df_null_index["time_col"],
            scalars_df_null_index["timestamp_col"],
        ],
    )
    result = series.to_pandas()
    assert len(result) == len(scalars_df_null_index)
