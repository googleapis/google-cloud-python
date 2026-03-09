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


def test_bigquery_dataframes_load_data_from_csv() -> None:
    # [START bigquery_dataframes_load_data_from_csv]
    import bigframes.pandas as bpd

    filepath_or_buffer = "gs://cloud-samples-data/bigquery/us-states/us-states.csv"
    df_from_gcs = bpd.read_csv(filepath_or_buffer)
    # Display the first few rows of the DataFrame:
    df_from_gcs.head()
    # [END bigquery_dataframes_load_data_from_csv]
    assert df_from_gcs is not None
