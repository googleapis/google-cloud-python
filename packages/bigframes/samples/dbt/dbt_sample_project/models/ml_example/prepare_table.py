# Copyright 2025 Google LLC
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

# This DBT Python model processes EPA historical air quality data from BigQuery
# using BigFrames. The primary goal is to merge several hourly summary
# tables into a single, unified DataFrame for later prediction. It includes the
# following steps:
#   1. Reading and Cleaning: It reads individual hourly summary tables from
#      BigQuery for various atmospheric parameters (like CO, O3, temperature,
#      and wind speed). Each table is cleaned by sorting, removing duplicates,
#      and renaming columns for clarity.
#   2. Combining Data: It then merges these cleaned tables into a single,
#      comprehensive DataFrame. An inner join is used to ensure the final output
#      only includes records with complete data across all parameters.
#   3. Final Output: The unified DataFrame is returned as the model's output,
#      creating a corresponding BigQuery table for future use.
#
# See more details from the related blog post: https://docs.getdbt.com/blog/train-linear-dbt-bigframes


import bigframes.pandas as bpd

def model(dbt, session):
    # Optional: override settings from dbt_project.yml.
    # When both are set, dbt.config takes precedence over dbt_project.yml.
    dbt.config(submission_method="bigframes", timeout=6000)

    # Define the dataset and the columns of interest representing various parameters 
    # in the atmosphere.
    dataset = "bigquery-public-data.epa_historical_air_quality"
    index_columns = ["state_name", "county_name", "site_num", "date_local", "time_local"]
    param_column = "parameter_name"
    value_column = "sample_measurement"

    # Initialize a list for collecting dataframes from individual parameters.
    params_dfs = []

    # Collect dataframes from tables which contain data for single parameter.
    table_param_dict = {
        "co_hourly_summary" : "co",
        "no2_hourly_summary" : "no2",
        "o3_hourly_summary" : "o3",
        "pressure_hourly_summary" : "pressure",
        "so2_hourly_summary" : "so2",
        "temperature_hourly_summary" : "temperature",
    }

    for table, param in table_param_dict.items():
        param_df = bpd.read_gbq(
            f"{dataset}.{table}",
            columns=index_columns + [value_column]
        )
        param_df = param_df\
            .sort_values(index_columns)\
            .drop_duplicates(index_columns)\
            .set_index(index_columns)\
            .rename(columns={value_column : param})
        params_dfs.append(param_df)

    # Collect dataframes from the table containing wind speed.
    # Optionally: collect dataframes from other tables containing
    # wind direction, NO, NOx, and NOy data as needed.
    wind_table = f"{dataset}.wind_hourly_summary"
    bpd.read_gbq(wind_table, columns=[param_column]).value_counts()

    wind_speed_df = bpd.read_gbq(
        wind_table,
        columns=index_columns + [value_column],
        filters=[(param_column, "==", "Wind Speed - Resultant")]
    )
    wind_speed_df = wind_speed_df\
        .sort_values(index_columns)\
        .drop_duplicates(index_columns)\
        .set_index(index_columns)\
        .rename(columns={value_column: "wind_speed"})
    params_dfs.append(wind_speed_df)

    # Combine data for all the selected parameters.
    df = bpd.concat(params_dfs, axis=1, join="inner")
    df = df.reset_index()

    return df
