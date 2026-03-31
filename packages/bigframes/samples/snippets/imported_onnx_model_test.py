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


def test_imported_sklearn_onnx_model() -> None:
    # Determine project id, in this case prefer the one set in the environment
    # variable GOOGLE_CLOUD_PROJECT (if any)
    import os

    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "bigframes-dev")

    # [START bigquery_dataframes_imported_sklearn_onnx_tutorial_import_onnx_models]
    import bigframes
    from bigframes.ml.imported import ONNXModel

    bigframes.options.bigquery.project = PROJECT_ID
    # You can change the location to one of the valid locations: https://cloud.google.com/bigquery/docs/locations#supported_locations
    bigframes.options.bigquery.location = "US"

    imported_onnx_model = ONNXModel(
        model_path="gs://cloud-samples-data/bigquery/ml/onnx/pipeline_rf.onnx"
    )
    # [END bigquery_dataframes_imported_sklearn_onnx_tutorial_import_onnx_models]
    assert imported_onnx_model is not None

    # [START bigquery_dataframes_imported_sklearn_onnx_tutorial_make_predictions]
    import bigframes.pandas as bpd

    df = bpd.read_gbq("bigquery-public-data.ml_datasets.iris")
    predictions = imported_onnx_model.predict(df)
    predictions.peek(5)
    # [END bigquery_dataframes_imported_sklearn_onnx_tutorial_make_predictions]
