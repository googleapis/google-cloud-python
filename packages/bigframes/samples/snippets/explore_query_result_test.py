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


def test_bigquery_dataframes_explore_query_result() -> None:
    # [START bigquery_dataframes_explore_query_result]
    import bigframes.pandas as bpd

    # Load data from BigQuery
    query_or_table = "bigquery-public-data.ml_datasets.penguins"
    bq_df = bpd.read_gbq(query_or_table)

    # Inspect one of the columns (or series) of the DataFrame:
    bq_df["body_mass_g"]

    # Compute the mean of this series:
    average_body_mass = bq_df["body_mass_g"].mean()
    print(f"average_body_mass: {average_body_mass}")

    # Find the heaviest species using the groupby operation to calculate the
    # mean body_mass_g:
    (
        bq_df["body_mass_g"]
        .groupby(by=bq_df["species"])
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    # Create the Linear Regression model
    from bigframes.ml.linear_model import LinearRegression

    # Filter down to the data we want to analyze
    adelie_data = bq_df[bq_df.species == "Adelie Penguin (Pygoscelis adeliae)"]

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
    # [END bigquery_dataframes_explore_query_result]
    assert average_body_mass is not None
    assert model is not None
