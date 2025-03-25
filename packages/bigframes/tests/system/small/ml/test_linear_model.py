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

import re

import google.api_core.exceptions
import pandas
import pytest

from bigframes.ml import linear_model


def test_linear_reg_model_score(penguins_linear_model, penguins_df_default_index):
    df = penguins_df_default_index.dropna()
    X_test = df[
        [
            "species",
            "island",
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
            "sex",
        ]
    ]
    y_test = df[["body_mass_g"]]
    result = penguins_linear_model.score(X_test, y_test).to_pandas()
    expected = pandas.DataFrame(
        {
            "mean_absolute_error": [225.817334],
            "mean_squared_error": [80540.705944],
            "mean_squared_log_error": [0.004972],
            "median_absolute_error": [173.080816],
            "r2_score": [0.87529],
            "explained_variance": [0.87529],
        },
        dtype="Float64",
    )
    pandas.testing.assert_frame_equal(
        result,
        expected,
        check_exact=False,
        rtol=0.1,
        # int64 Index by default in pandas versus Int64 (nullable) Index in BigQuery DataFrame
        check_index_type=False,
    )


def test_linear_reg_model_score_series(
    penguins_linear_model, penguins_df_default_index
):
    df = penguins_df_default_index.dropna()
    X_test = df[
        [
            "species",
            "island",
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
            "sex",
        ]
    ]
    y_test = df["body_mass_g"]
    result = penguins_linear_model.score(X_test, y_test).to_pandas()
    expected = pandas.DataFrame(
        {
            "mean_absolute_error": [225.817334],
            "mean_squared_error": [80540.705944],
            "mean_squared_log_error": [0.004972],
            "median_absolute_error": [173.080816],
            "r2_score": [0.87529],
            "explained_variance": [0.87529],
        },
        dtype="Float64",
    )
    pandas.testing.assert_frame_equal(
        result,
        expected,
        check_exact=False,
        rtol=0.1,
        # int64 Index by default in pandas versus Int64 (nullable) Index in BigQuery DataFrame
        check_index_type=False,
    )


def test_linear_reg_model_predict(penguins_linear_model, new_penguins_df):
    predictions = penguins_linear_model.predict(new_penguins_df).to_pandas()
    assert predictions.shape == (3, 8)
    result = predictions[["predicted_body_mass_g"]]
    expected = pandas.DataFrame(
        {"predicted_body_mass_g": [4030.1, 3280.8, 3177.9]},
        dtype="Float64",
        index=pandas.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )
    pandas.testing.assert_frame_equal(
        result.sort_index(),
        expected,
        check_exact=False,
        rtol=0.1,
    )


def test_linear_reg_model_predict_explain(penguins_linear_model, new_penguins_df):
    predictions = penguins_linear_model.predict_explain(new_penguins_df).to_pandas()
    assert predictions.shape == (3, 12)
    result = predictions[["predicted_body_mass_g", "approximation_error"]]
    expected = pandas.DataFrame(
        {
            "predicted_body_mass_g": [4030.1, 3280.8, 3177.9],
            "approximation_error": [
                0.0,
                0.0,
                0.0,
            ],
        },
        dtype="Float64",
        index=pandas.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )
    pandas.testing.assert_frame_equal(
        result.sort_index(),
        expected,
        check_exact=False,
        rtol=0.1,
    )


def test_linear_model_predict_explain_top_k_features(
    penguins_logistic_model: linear_model.LinearRegression, new_penguins_df
):
    top_k_features = 0

    with pytest.raises(
        ValueError,
        match=re.escape(f"top_k_features must be at least 1, but is {top_k_features}."),
    ):
        penguins_logistic_model.predict_explain(
            new_penguins_df, top_k_features=top_k_features
        ).to_pandas()


def test_linear_reg_model_predict_params(
    penguins_linear_model: linear_model.LinearRegression, new_penguins_df
):
    predictions = penguins_linear_model.predict(new_penguins_df).to_pandas()
    assert predictions.shape[0] >= 1
    prediction_columns = set(predictions.columns)
    expected_columns = {
        "predicted_body_mass_g",
        "species",
        "island",
        "culmen_length_mm",
        "culmen_depth_mm",
        "flipper_length_mm",
        "body_mass_g",
        "sex",
    }
    assert expected_columns <= prediction_columns


def test_linear_reg_model_predict_explain_params(
    penguins_linear_model: linear_model.LinearRegression, new_penguins_df
):
    predictions = penguins_linear_model.predict_explain(new_penguins_df).to_pandas()
    assert predictions.shape[0] >= 1
    prediction_columns = set(predictions.columns)
    expected_columns = {
        "predicted_body_mass_g",
        "top_feature_attributions",
        "baseline_prediction_value",
        "prediction_value",
        "approximation_error",
        "species",
        "island",
        "culmen_length_mm",
        "culmen_depth_mm",
        "flipper_length_mm",
        "body_mass_g",
        "sex",
    }
    assert expected_columns <= prediction_columns


def test_to_gbq_saved_linear_reg_model_scores(
    penguins_linear_model, table_id_unique, penguins_df_default_index
):
    saved_model = penguins_linear_model.to_gbq(table_id_unique, replace=True)
    df = penguins_df_default_index.dropna()
    X_test = df[
        [
            "species",
            "island",
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
            "sex",
        ]
    ]
    y_test = df[["body_mass_g"]]
    result = saved_model.score(X_test, y_test).to_pandas()
    expected = pandas.DataFrame(
        {
            "mean_absolute_error": [227.01223],
            "mean_squared_error": [81838.159892],
            "mean_squared_log_error": [0.00507],
            "median_absolute_error": [173.080816],
            "r2_score": [0.872377],
            "explained_variance": [0.872377],
        },
        dtype="Float64",
    )
    pandas.testing.assert_frame_equal(
        result,
        expected,
        check_exact=False,
        rtol=0.1,
        # int64 Index by default in pandas versus Int64 (nullable) Index in BigQuery DataFrame
        check_index_type=False,
    )


def test_linear_reg_model_global_explain(
    penguins_linear_model_w_global_explain, new_penguins_df
):
    training_data = new_penguins_df.dropna(subset=["body_mass_g"])
    X = training_data.drop(columns=["body_mass_g"])
    y = training_data[["body_mass_g"]]
    penguins_linear_model_w_global_explain.fit(X, y)
    global_ex = penguins_linear_model_w_global_explain.global_explain()
    assert global_ex.shape == (6, 1)
    expected_columns = pandas.Index(["attribution"])
    pandas.testing.assert_index_equal(global_ex.columns, expected_columns)
    result = global_ex.to_pandas().drop(["attribution"], axis=1).sort_index()
    expected_feature = (
        pandas.DataFrame(
            {
                "feature": [
                    "island",
                    "species",
                    "sex",
                    "flipper_length_mm",
                    "culmen_depth_mm",
                    "culmen_length_mm",
                ]
            },
        )
        .set_index("feature")
        .sort_index()
    )
    pandas.testing.assert_frame_equal(
        result,
        expected_feature,
        check_exact=False,
        check_index_type=False,
    )


def test_to_gbq_replace(penguins_linear_model, table_id_unique):
    penguins_linear_model.to_gbq(table_id_unique, replace=True)
    with pytest.raises(google.api_core.exceptions.Conflict):
        penguins_linear_model.to_gbq(table_id_unique)


def test_logistic_model_score(penguins_logistic_model, penguins_df_default_index):
    df = penguins_df_default_index.dropna()
    X_test = df[
        [
            "species",
            "island",
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
            "body_mass_g",
        ]
    ]
    y_test = df[["sex"]]
    result = penguins_logistic_model.score(X_test, y_test).to_pandas()
    expected = pandas.DataFrame(
        {
            "precision": [0.616753],
            "recall": [0.618615],
            "accuracy": [0.92515],
            "f1_score": [0.617681],
            "log_loss": [1.498832],
            "roc_auc": [0.975807],
        },
        dtype="Float64",
    )
    pandas.testing.assert_frame_equal(
        result,
        expected,
        check_exact=False,
        rtol=0.1,
        # int64 Index by default in pandas versus Int64 (nullable) Index in BigQuery DataFrame
        check_index_type=False,
    )


def test_logistic_model_score_series(
    penguins_logistic_model, penguins_df_default_index
):
    df = penguins_df_default_index.dropna()
    X_test = df[
        [
            "species",
            "island",
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
            "body_mass_g",
        ]
    ]
    y_test = df["sex"]
    result = penguins_logistic_model.score(X_test, y_test).to_pandas()
    expected = pandas.DataFrame(
        {
            "precision": [0.616753],
            "recall": [0.618615],
            "accuracy": [0.92515],
            "f1_score": [0.617681],
            "log_loss": [1.498832],
            "roc_auc": [0.975807],
        },
        dtype="Float64",
    )
    pandas.testing.assert_frame_equal(
        result,
        expected,
        check_exact=False,
        rtol=0.1,
        # int64 Index by default in pandas versus Int64 (nullable) Index in BigQuery DataFrame
        check_index_type=False,
    )


def test_logistic_model_predict(penguins_logistic_model, new_penguins_df):
    predictions = penguins_logistic_model.predict(new_penguins_df).to_pandas()
    assert predictions.shape == (3, 9)
    result = predictions[["predicted_sex"]]
    expected = pandas.DataFrame(
        {"predicted_sex": ["MALE", "MALE", "FEMALE"]},
        dtype="string[pyarrow]",
        index=pandas.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )
    pandas.testing.assert_frame_equal(
        result.sort_index(),
        expected,
        check_exact=False,
        rtol=0.1,
    )


def test_logistic_model_predict_explain_top_k_features(
    penguins_logistic_model: linear_model.LogisticRegression, new_penguins_df
):
    top_k_features = 0

    with pytest.raises(
        ValueError,
        match=re.escape(f"top_k_features must be at least 1, but is {top_k_features}."),
    ):
        penguins_logistic_model.predict_explain(
            new_penguins_df, top_k_features=top_k_features
        ).to_pandas()


def test_logistic_model_predict_params(
    penguins_logistic_model: linear_model.LogisticRegression, new_penguins_df
):
    predictions = penguins_logistic_model.predict(new_penguins_df).to_pandas()
    assert predictions.shape[0] >= 1
    prediction_columns = set(predictions.columns)
    expected_columns = {
        "predicted_sex",
        "predicted_sex_probs",
        "species",
        "island",
        "culmen_length_mm",
        "culmen_depth_mm",
        "flipper_length_mm",
        "body_mass_g",
        "sex",
    }
    assert expected_columns <= prediction_columns


def test_logistic_model_predict_explain_params(
    penguins_logistic_model: linear_model.LogisticRegression, new_penguins_df
):
    predictions = penguins_logistic_model.predict_explain(new_penguins_df).to_pandas()
    assert predictions.shape[0] >= 1
    prediction_columns = set(predictions.columns)
    expected_columns = {
        "predicted_sex",
        "probability",
        "top_feature_attributions",
        "baseline_prediction_value",
        "prediction_value",
        "approximation_error",
        "species",
        "island",
        "culmen_length_mm",
        "culmen_depth_mm",
        "flipper_length_mm",
        "body_mass_g",
        "sex",
    }
    assert expected_columns <= prediction_columns


def test_logistic_model_to_gbq_saved_score(
    penguins_logistic_model, table_id_unique, penguins_df_default_index
):
    saved_model = penguins_logistic_model.to_gbq(table_id_unique, replace=True)
    df = penguins_df_default_index.dropna()
    X_test = df[
        [
            "species",
            "island",
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
            "body_mass_g",
        ]
    ]
    y_test = df[["sex"]]
    result = saved_model.score(X_test, y_test).to_pandas()
    expected = pandas.DataFrame(
        {
            "precision": [0.616753],
            "recall": [0.618615],
            "accuracy": [0.92515],
            "f1_score": [0.617681],
            "log_loss": [1.498832],
            "roc_auc": [0.975807],
        },
        dtype="Float64",
    )
    pandas.testing.assert_frame_equal(
        result,
        expected,
        check_exact=False,
        rtol=0.1,
        # int64 Index by default in pandas versus Int64 (nullable) Index in BigQuery DataFrame
        check_index_type=False,
    )
