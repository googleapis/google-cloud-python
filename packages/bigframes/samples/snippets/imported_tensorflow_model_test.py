# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (t
# you may not use this file except in compliance wi
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in
# distributed under the License is distributed on a
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, eit
# See the License for the specific language governi
# limitations under the License.


def test_imported_tensorflow_model() -> None:
    # Determine project id, in this case prefer the one set in the environment
    # variable GOOGLE_CLOUD_PROJECT (if any)
    import os

    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "bigframes-dev")

    # [START bigquery_dataframes_imported_tensorflow_tutorial_import_tensorflow_models]
    import bigframes
    from bigframes.ml.imported import TensorFlowModel

    bigframes.options.bigquery.project = PROJECT_ID
    # You can change the location to one of the valid locations: https://cloud.google.com/bigquery/docs/locations#supported_locations
    bigframes.options.bigquery.location = "US"

    imported_tensorflow_model = TensorFlowModel(
        model_path="gs://cloud-training-demos/txtclass/export/exporter/1549825580/*"
    )
    # [END bigquery_dataframes_imported_tensorflow_tutorial_import_tensorflow_models]
    assert imported_tensorflow_model is not None

    # [START bigquery_dataframes_imported_tensorflow_tutorial_make_predictions]
    import bigframes.pandas as bpd

    df = bpd.read_gbq("bigquery-public-data.hacker_news.full")
    df_pred = df.rename(columns={"title": "input"})
    predictions = imported_tensorflow_model.predict(df_pred)
    predictions.head(5)
    # [END bigquery_dataframes_imported_tensorflow_tutorial_make_predictions]
