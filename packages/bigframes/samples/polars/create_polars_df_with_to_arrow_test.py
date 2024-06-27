# Copyright 2024 Google LLC
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


def test_create_polars_df() -> None:
    # [START bigquery_dataframes_to_polars]
    import polars

    import bigframes.enums
    import bigframes.pandas as bpd

    bf_df = bpd.read_gbq_table(
        "bigquery-public-data.usa_names.usa_1910_current",
        # Setting index_col to either a unique column or NULL will give the
        # best performance.
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )
    # TODO(developer): Do some analysis using BigQuery DataFrames.
    # ...

    # Run the query and download the results as an Arrow table to convert into
    # a Polars DataFrame. Use ordered=False if your polars analysis is OK with
    # non-deterministic ordering.
    arrow_table = bf_df.to_arrow(ordered=False)
    polars_df = polars.from_arrow(arrow_table)
    # [END bigquery_dataframes_to_polars]

    assert polars_df.shape == bf_df.shape
    assert polars_df["number"].sum() == bf_df["number"].sum()
