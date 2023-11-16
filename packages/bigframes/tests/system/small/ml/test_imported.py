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
    model = imported.TensorFlowModel(model_path=imported_onnx_model_path)
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
        atol=0.1,
    )


def test_onnx_model_to_gbq(imported_onnx_model: imported.ONNXModel, dataset_id: str):
    imported_onnx_model.to_gbq(f"{dataset_id}.test_onnx_model", replace=True)
    with pytest.raises(google.api_core.exceptions.Conflict):
        imported_onnx_model.to_gbq(f"{dataset_id}.test_onnx_model")
