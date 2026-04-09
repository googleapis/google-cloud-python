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

import google.api_core.exceptions
import numpy as np
import pandas as pd
import pytest

from bigframes.ml import imported


def test_tensorflow_create_model(imported_tensorflow_model):
    # Model creation doesn't return error
    assert imported_tensorflow_model is not None


def test_tensorflow_create_model_default_session(imported_tensorflow_model_path):
    model = imported.TensorFlowModel(model_path=imported_tensorflow_model_path)
    assert model is not None


def test_tensorflow_model_predict(imported_tensorflow_model, llm_text_df):
    df = llm_text_df.rename(columns={"prompt": "input"})
    predictions = imported_tensorflow_model.predict(df).to_pandas()
    assert predictions.shape == (3, 2)
    result = predictions[["dense_1"]]
    # The values are non-human-readable. As they are a dense layer of Neural Network.
    # And since it is pretrained and imported, the model is a opaque-box.
    # We may want to switch to better test model and cases.
    value = np.array(
        [9.375373792863684e-07, 0.00015779426030348986, 0.9998412132263184]
    )
    expected = pd.DataFrame(
        {
            "dense_1": [value, value, value],
        },
    )
    expected.set_index(expected.index.astype("Int64"), inplace=True)
    pd.testing.assert_frame_equal(
        result,
        expected,
        check_exact=False,
        check_dtype=False,
        atol=0.1,
    )


def test_tensorflow_model_to_gbq(
    imported_tensorflow_model: imported.TensorFlowModel, dataset_id: str
):
    imported_tensorflow_model.to_gbq(f"{dataset_id}.test_tf_model", replace=True)
    with pytest.raises(google.api_core.exceptions.Conflict):
        imported_tensorflow_model.to_gbq(f"{dataset_id}.test_tf_model")


def test_onnx_create_model(imported_onnx_model):
    # Model creation doesn't return error
    assert imported_onnx_model is not None


def test_onnx_create_model_default_session(imported_onnx_model_path):
    model = imported.ONNXModel(model_path=imported_onnx_model_path)
    assert model is not None


def test_onnx_model_predict(imported_onnx_model, onnx_iris_df):
    predictions = imported_onnx_model.predict(onnx_iris_df).to_pandas()
    assert predictions.shape == (3, 7)
    result = predictions[["label", "probabilities"]]
    value1 = np.array([0.9999993443489075, 0.0, 0.0])
    value2 = np.array([0.0, 0.0, 0.9999993443489075])
    expected = pd.DataFrame(
        {
            "label": pd.array([0, 0, 2]).astype("Int64"),
            "probabilities": [value1, value1, value2],
        },
        index=pd.Index([0, 1, 2], dtype="Int64"),
    )
    pd.testing.assert_frame_equal(
        result,
        expected,
        check_exact=False,
        check_dtype=False,
        atol=0.1,
    )


def test_onnx_model_to_gbq(imported_onnx_model: imported.ONNXModel, dataset_id: str):
    imported_onnx_model.to_gbq(f"{dataset_id}.test_onnx_model", replace=True)
    with pytest.raises(google.api_core.exceptions.Conflict):
        imported_onnx_model.to_gbq(f"{dataset_id}.test_onnx_model")


def test_xgboost_create_model(imported_xgboost_model):
    # Model creation doesn't return error
    assert imported_xgboost_model is not None


def test_xgboost_create_model_default_session(imported_xgboost_array_model_path):
    model = imported.XGBoostModel(model_path=imported_xgboost_array_model_path)
    assert model is not None


def test_xgboost_model_predict(imported_xgboost_model, xgboost_iris_df):
    predictions = imported_xgboost_model.predict(xgboost_iris_df).to_pandas()
    assert predictions.shape == (3, 5)
    result = predictions[["predicted_label"]]
    value1 = np.array([0.00362173, 0.01580198, 0.98057634])
    value2 = np.array([0.00349651, 0.00999565, 0.98650789])
    value3 = np.array([0.00561748, 0.0108124, 0.98357016])
    expected = pd.DataFrame(
        {
            "predicted_label": [value1, value2, value3],
        },
        index=pd.Index([0, 1, 2], dtype="Int64"),
    )
    pd.testing.assert_frame_equal(
        result,
        expected,
        check_exact=False,
        check_dtype=False,
        atol=0.1,
    )


def test_xgboost_model_to_gbq(
    imported_xgboost_model: imported.XGBoostModel, dataset_id: str
):
    imported_xgboost_model.to_gbq(f"{dataset_id}.test_xgboost_model", replace=True)
    with pytest.raises(google.api_core.exceptions.Conflict):
        imported_xgboost_model.to_gbq(f"{dataset_id}.test_xgboost_model")
