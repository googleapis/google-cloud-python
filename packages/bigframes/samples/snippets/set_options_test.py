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


def test_bigquery_dataframes_set_options() -> None:
    # Close the session before resetting the options
    import bigframes.pandas as bpd

    bpd.close_session()

    try:
        # [START bigquery_dataframes_set_options]
        import bigframes.pandas as bpd

        PROJECT_ID = "bigframes-dev"  # @param {type:"string"}
        REGION = "US"  # @param {type:"string"}

        # Set BigQuery DataFrames options
        # Note: The project option is not required in all environments.
        # On BigQuery Studio, the project ID is automatically detected.
        bpd.options.bigquery.project = PROJECT_ID

        # Note: The location option is not required.
        # It defaults to the location of the first table or query
        # passed to read_gbq(). For APIs where a location can't be
        # auto-detected, the location defaults to the "US" location.
        bpd.options.bigquery.location = REGION

        # [END bigquery_dataframes_set_options]
        assert bpd.options.bigquery.project == PROJECT_ID
        assert bpd.options.bigquery.location == REGION
    finally:
        bpd.close_session()
        bpd.options.reset()
