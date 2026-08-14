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

# This example demonstrates how to build an **incremental dbt Python model**
# using BigFrames.
#
# Incremental models are essential for efficiently processing large datasets by
# only transforming new or changed data, rather than reprocessing the entire
# dataset every time. If the target table already exists, dbt will perform a
# merge based on the specified unique keys; otherwise, it will create a new
# table automatically.
#
# This model also showcases the definition and application of a **BigFrames
# User-Defined Function (UDF)** to add a descriptive summary column based on
# temperature data. BigFrames UDFs allow you to execute custom Python logic
# directly within BigQuery, leveraging BigQuery's scalability.


def model(dbt, session):
    # Optional: override settings from dbt_project.yml.
    # When both are set, dbt.config takes precedence over dbt_project.yml.
    dbt.config(
        # Use BigFrames mode to execute this Python model. This enables
        # pandas-like operations directly on BigQuery data.
        submission_method="bigframes",
        # Materialize this model as an 'incremental' table. This tells dbt to
        # only process new or updated data on subsequent runs.
        materialized="incremental",
        # Use MERGE strategy to update rows during incremental runs.
        incremental_strategy="merge",
        # Define the composite key that uniquely identifies a row in the
        # target table. This key is used by the 'merge' strategy to match
        # existing rows for updates during incremental runs.
        unique_key=["state_name", "county_name", "date_local"],
    )

    # Reference an upstream dbt model or an existing BigQuery table as a
    # BigFrames DataFrame. It allows you to seamlessly use the output of another
    # dbt model as input to this one.
    df = dbt.ref("dbt_bigframes_code_sample_1")

    # Define a BigFrames UDF to generate a temperature description.
    # BigFrames UDFs allow you to define custom Python logic that executes
    # directly within BigQuery. This is powerful for complex transformations.
    @session.udf(dataset="dbt_sample_dataset", name="describe_udf")
    def describe(
        max_temperature: float,
        min_temperature: float,
    ) -> str:
        is_hot = max_temperature > 85.0
        is_cold = min_temperature < 50.0

        if is_hot and is_cold:
            return "Expect both hot and cold conditions today."
        if is_hot:
            return "Overall, it's a hot day."
        if is_cold:
            return "Overall, it's a cold day."
        return "Comfortable throughout the day."

    # Apply the UDF using combine and store the result in a column "describe".
    df["describe"] = df["max_temperature"].combine(df["min_temperature"], describe)

    # Return the transformed BigFrames DataFrame.
    # This DataFrame will be the final output of your incremental dbt model.
    # On subsequent runs, only new or changed rows will be processed and merged
    # into the target BigQuery table based on the `unique_key`.
    return df
