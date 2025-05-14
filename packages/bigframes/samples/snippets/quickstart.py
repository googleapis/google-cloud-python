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


def run_quickstart(project_id: str) -> None:
    your_gcp_project_id = project_id

    # [START bigquery_bigframes_quickstart]
    import bigframes.pandas as bpd

    # Set BigQuery DataFrames options
    # Note: The project option is not required in all environments.
    # On BigQuery Studio, the project ID is automatically detected.
    bpd.options.bigquery.project = your_gcp_project_id

    # Use "partial" ordering mode to generate more efficient queries, but the
    # order of the rows in DataFrames may not be deterministic if you have not
    # explictly sorted it. Some operations that depend on the order, such as
    # head() will not function until you explictly order the DataFrame. Set the
    # ordering mode to "strict" (default) for more pandas compatibility.
    bpd.options.bigquery.ordering_mode = "partial"

    # Create a DataFrame from a BigQuery table
    query_or_table = "bigquery-public-data.ml_datasets.penguins"
    df = bpd.read_gbq(query_or_table)

    # Efficiently preview the results using the .peek() method.
    df.peek()

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
