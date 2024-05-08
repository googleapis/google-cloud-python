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


def test_regression_model() -> None:
    # [START bigquery_dataframes_regression_model]
    from bigframes.ml.linear_model import LinearRegression
    import bigframes.pandas as bpd

    # Load data from BigQuery
    query_or_table = "bigquery-public-data.ml_datasets.penguins"
    bq_df = bpd.read_gbq(query_or_table)

    # Filter down to the data to the Adelie Penguin species
    adelie_data = bq_df[bq_df.species == "Adelie Penguin (Pygoscelis adeliae)"]

    # Drop the species column
    adelie_data = adelie_data.drop(columns=["species"])

    # Drop rows with nulls to get training data
    training_data = adelie_data.dropna()

    # Specify your feature (or input) columns and the label (or output) column:
    feature_columns = training_data[
        ["island", "culmen_length_mm", "culmen_depth_mm", "flipper_length_mm", "sex"]
    ]
    label_columns = training_data[["body_mass_g"]]

    test_data = adelie_data[adelie_data.body_mass_g.isnull()]

    # Create the linear model
    model = LinearRegression()
    model.fit(feature_columns, label_columns)

    # Score the model
    score = model.score(feature_columns, label_columns)

    # Predict using the model
    result = model.predict(test_data)
    # [END bigquery_dataframes_regression_model]
    assert test_data is not None
    assert feature_columns is not None
    assert label_columns is not None
    assert model is not None
    assert score is not None
    assert result is not None
