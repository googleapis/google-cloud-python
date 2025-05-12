# Copyright 2023 Google LLC
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


def test_bigquery_dataframes_examples() -> None:
    # [START bigquery_dataframes_bigquery_methods_array_agg]
    import bigframes.bigquery as bbq
    import bigframes.pandas as bpd

    s = bpd.Series([0, 1, 2, 3, 4, 5])

    # Group values by whether they are divisble by 2 and aggregate them into arrays
    bbq.array_agg(s.groupby(s % 2 == 0))
    # False    [1 3 5]
    # True     [0 2 4]
    # dtype: list<item: int64>[pyarrow]
    # [END bigquery_dataframes_bigquery_methods_array_agg]

    # [START bigquery_dataframes_bigquery_methods_struct]
    import bigframes.bigquery as bbq
    import bigframes.pandas as bpd

    # Load data from BigQuery
    query_or_table = "bigquery-public-data.ml_datasets.penguins"
    bq_df = bpd.read_gbq(query_or_table)

    # Create a new STRUCT Series with subfields for each column in a DataFrames.
    lengths = bbq.struct(
        bq_df[["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm"]]
    )

    lengths.peek()
    # 146	{'culmen_length_mm': 51.1, 'culmen_depth_mm': ...
    # 278	{'culmen_length_mm': 48.2, 'culmen_depth_mm': ...
    # 337	{'culmen_length_mm': 36.4, 'culmen_depth_mm': ...
    # 154	{'culmen_length_mm': 46.5, 'culmen_depth_mm': ...
    # 185	{'culmen_length_mm': 50.1, 'culmen_depth_mm': ...
    # dtype: struct[pyarrow]
    # [END bigquery_dataframes_bigquery_methods_struct]

    # [START bigquery_dataframes_bigquery_methods_unix_micros]
    import pandas as pd

    import bigframes.bigquery as bbq
    import bigframes.pandas as bpd

    # Create a series that consists of three timestamps: [1970-01-01, 1970-01-02, 1970-01-03]
    s = bpd.Series(pd.date_range("1970-01-01", periods=3, freq="d", tz="UTC"))

    bbq.unix_micros(s)
    # 0               0
    # 1     86400000000
    # 2    172800000000
    # dtype: Int64
    # [END bigquery_dataframes_bigquery_methods_unix_micros]

    # [START bigquery_dataframes_bigquery_methods_scalar]
    import bigframes.bigquery as bbq
    import bigframes.pandas as bpd

    # Load data from BigQuery
    query_or_table = "bigquery-public-data.ml_datasets.penguins"

    # The sql_scalar function can be used to inject SQL syntax that is not supported
    # or difficult to express with the bigframes.pandas APIs.
    bq_df = bpd.read_gbq(query_or_table)
    shortest = bbq.sql_scalar(
        "LEAST({0}, {1}, {2})",
        columns=[
            bq_df["culmen_depth_mm"],
            bq_df["culmen_length_mm"],
            bq_df["flipper_length_mm"],
        ],
    )

    shortest.peek()
    #         0
    # 149	18.9
    # 33	16.3
    # 296	17.2
    # 287	17.0
    # 307	15.0
    # dtype: Float64
    # [END bigquery_dataframes_bigquery_methods_scalar]
    assert bq_df is not None
    assert lengths is not None
    assert shortest is not None
