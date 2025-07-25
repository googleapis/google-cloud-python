# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This example demonstrates one of the most general usages of transforming raw
# BigQuery data into a processed table using a dbt Python model with BigFrames.
# See more from: https://cloud.google.com/bigquery/docs/dataframes-dbt.
#
# Key defaults when using BigFrames in a dbt Python model for BigQuery:
# - The default materialization is 'table' unless specified otherwise. This
#   means dbt will create a new BigQuery table from the result of this model.
# - The default timeout for the job is 3600 seconds (60 minutes). This can be
#   adjusted if your processing requires more time.
# - If no runtime template is provided, dbt will automatically create and reuse
#   a default one for executing the Python code in BigQuery.
#
# BigFrames provides a pandas-like API for BigQuery data, enabling familiar
# data manipulation directly within your dbt project. This code sample
# illustrates a basic pattern for:
# 1. Reading data from an existing BigQuery dataset.
# 2. Processing it using pandas-like DataFrame operations powered by BigFrames.
# 3. Outputting a cleaned and transformed table, managed by dbt.


def model(dbt, session):
    # Optional: Override settings from your dbt_project.yml file.
    # When both are set, dbt.config takes precedence over dbt_project.yml.
    #
    # Use `dbt.config(submission_method="bigframes")` to tell dbt to execute
    # this Python model using BigQuery DataFrames (BigFrames). This allows you
    # to write pandas-like code that operates directly on BigQuery data
    # without needing to pull all data into memory.
    dbt.config(submission_method="bigframes")

    # Define the BigQuery table path from which to read data.
    table = "bigquery-public-data.epa_historical_air_quality.temperature_hourly_summary"

    # Define the specific columns to select from the BigQuery table.
    columns = [
        "state_name",
        "county_name",
        "date_local",
        "time_local",
        "sample_measurement",
    ]

    # Read data from the specified BigQuery table into a BigFrames DataFrame.
    df = session.read_gbq(table, columns=columns)

    # Sort the DataFrame by the specified columns. This prepares the data for
    # `drop_duplicates` to ensure consistent duplicate removal.
    df = df.sort_values(columns).drop_duplicates(columns)

    # Group the DataFrame by 'state_name', 'county_name', and 'date_local'. For
    # each group, calculate the minimum and maximum of the 'sample_measurement'
    # column. The result will be a BigFrames DataFrame with a MultiIndex.
    result = df.groupby(["state_name", "county_name", "date_local"])[
        "sample_measurement"
    ].agg(["min", "max"])

    # Rename some columns and convert the MultiIndex of the 'result' DataFrame
    # into regular columns. This flattens the DataFrame so 'state_name',
    # 'county_name', and 'date_local' become regular columns again.
    result = result.rename(
        columns={"min": "min_temperature", "max": "max_temperature"}
    ).reset_index()

    # Return the processed BigFrames DataFrame.
    # In a dbt Python model, this DataFrame will be materialized as a table
    return result
