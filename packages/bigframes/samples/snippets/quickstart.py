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


def run_quickstart(project_id: str):
    import bigframes

    session_options = bigframes.BigQueryOptions()
    session = bigframes.connect(session_options)

    your_gcp_project_id = project_id
    query_or_table = "bigquery-public-data.ml_datasets.penguins"
    df_session = session.read_gbq(query_or_table)
    average_body_mass = df_session["body_mass_g"].mean()
    print(f"average_body_mass (df_session): {average_body_mass}")

    # [START bigquery_bigframes_quickstart]
    import bigframes.pandas as bpd

    # Set BigQuery DataFrames options
    bpd.options.bigquery.project = your_gcp_project_id
    bpd.options.bigquery.location = "us"

    # Create a DataFrame from a BigQuery table
    query_or_table = "bigquery-public-data.ml_datasets.penguins"
    df = bpd.read_gbq(query_or_table)

    # Use the DataFrame just as you would a pandas DataFrame, but calculations
    # happen in the BigQuery query engine instead of the local system.
    average_body_mass = df["body_mass_g"].mean()
    print(f"average_body_mass: {average_body_mass}")

    # Create the Linear Regression model
    from bigframes.ml.linear_model import LinearRegression

    # Filter down to the data we want to analyze
    adelie_data = df[df.species == "Adelie Penguin (Pygoscelis adeliae)"]

    # Drop the columns we don't care about
    adelie_data = adelie_data.drop(columns=["species"])

    # Drop rows with nulls to get our training data
    training_data = adelie_data.dropna()

    # Pick feature columns and label column
    X = training_data[
        [
            "island",
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
            "sex",
        ]
    ]
    y = training_data[["body_mass_g"]]

    model = LinearRegression(fit_intercept=False)
    model.fit(X, y)
    model.score(X, y)
    # [END bigquery_bigframes_quickstart]
