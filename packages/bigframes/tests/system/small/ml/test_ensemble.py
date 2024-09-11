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

from unittest import TestCase

import google.api_core.exceptions
import pandas
import pytest

import bigframes.ml.ensemble


def test_xgbregressor_model_score(
    penguins_xgbregressor_model, penguins_df_default_index
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
    y_test = df[["sex"]]
    result = penguins_xgbregressor_model.score(X_test, y_test).to_pandas()
    expected = pandas.DataFrame(
        {
            "mean_absolute_error": [108.77582],
            "mean_squared_error": [20943.272738],
            "mean_squared_log_error": [0.00135],
            "median_absolute_error": [86.313477],
            "r2_score": [0.967571],
            "explained_variance": [0.967609],
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


def test_xgbregressor_model_score_series(
    penguins_xgbregressor_model, penguins_df_default_index
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
    result = penguins_xgbregressor_model.score(X_test, y_test).to_pandas()
    expected = pandas.DataFrame(
        {
            "mean_absolute_error": [108.77582],
            "mean_squared_error": [20943.272738],
            "mean_squared_log_error": [0.00135],
            "median_absolute_error": [86.313477],
            "r2_score": [0.967571],
            "explained_variance": [0.967609],
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


def test_xgbregressor_model_predict(
    penguins_xgbregressor_model: bigframes.ml.ensemble.XGBRegressor, new_penguins_df
):
    predictions = penguins_xgbregressor_model.predict(new_penguins_df).to_pandas()
    assert predictions.shape == (3, 8)
    result = predictions[["predicted_body_mass_g"]]
    expected = pandas.DataFrame(
        {"predicted_body_mass_g": ["4293.1538089", "3410.0271", "3357.944"]},
        dtype="Float64",
        index=pandas.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )
    pandas.testing.assert_frame_equal(
        result.sort_index(),
        expected,
        check_exact=False,
        rtol=0.1,
        check_index_type=False,
    )


def test_to_gbq_saved_xgbregressor_model_scores(
    penguins_xgbregressor_model, dataset_id, penguins_df_default_index
):
    saved_model = penguins_xgbregressor_model.to_gbq(
        f"{dataset_id}.test_penguins_model", replace=True
    )
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
            "mean_absolute_error": [109.016973],
            "mean_squared_error": [20867.299758],
            "mean_squared_log_error": [0.00135],
            "median_absolute_error": [86.490234],
            "r2_score": [0.967458],
            "explained_variance": [0.967504],
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


def test_to_xgbregressor_model_gbq_replace(penguins_xgbregressor_model, dataset_id):
    penguins_xgbregressor_model.to_gbq(
        f"{dataset_id}.test_penguins_model", replace=True
    )
    with pytest.raises(google.api_core.exceptions.Conflict):
        penguins_xgbregressor_model.to_gbq(f"{dataset_id}.test_penguins_model")


def test_xgbclassifier_model_score(
    penguins_xgbclassifier_model, penguins_df_default_index
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
    y_test = df[["sex"]]
    result = penguins_xgbclassifier_model.score(X_test, y_test).to_pandas()
    TestCase().assertSequenceEqual(result.shape, (1, 6))
    for col_name in [
        "precision",
        "recall",
        "accuracy",
        "f1_score",
        "log_loss",
        "roc_auc",
    ]:
        assert col_name in result.columns


def test_xgbclassifier_model_score_series(
    penguins_xgbclassifier_model, penguins_df_default_index
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
    result = penguins_xgbclassifier_model.score(X_test, y_test).to_pandas()
    TestCase().assertSequenceEqual(result.shape, (1, 6))
    for col_name in [
        "precision",
        "recall",
        "accuracy",
        "f1_score",
        "log_loss",
        "roc_auc",
    ]:
        assert col_name in result.columns


def test_xgbclassifier_model_predict(
    penguins_xgbclassifier_model: bigframes.ml.ensemble.XGBClassifier, new_penguins_df
):
    predictions = penguins_xgbclassifier_model.predict(new_penguins_df).to_pandas()
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
        check_index_type=False,
    )


def test_to_gbq_saved_xgbclassifier_model_scores(
    penguins_xgbclassifier_model, dataset_id, penguins_df_default_index
):
    saved_model = penguins_xgbclassifier_model.to_gbq(
        f"{dataset_id}.test_penguins_model", replace=True
    )
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
            "precision": [1.0],
            "recall": [1.0],
            "accuracy": [1.0],
            "f1_score": [1.0],
            "log_loss": [0.331442],
            "roc_auc": [1.0],
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
    assert saved_model.max_depth == 6
    assert saved_model.max_iterations == 20


def test_to_xgbclassifier_model_gbq_replace(penguins_xgbclassifier_model, dataset_id):
    penguins_xgbclassifier_model.to_gbq(
        f"{dataset_id}.test_penguins_model", replace=True
    )
    with pytest.raises(google.api_core.exceptions.Conflict):
        penguins_xgbclassifier_model.to_gbq(f"{dataset_id}.test_penguins_model")


def test_randomforestregressor_model_score(
    penguins_randomforest_regressor_model, penguins_df_default_index
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
    y_test = df[["sex"]]
    result = penguins_randomforest_regressor_model.score(X_test, y_test).to_pandas()
    expected = pandas.DataFrame(
        {
            "mean_absolute_error": [317.031042],
            "mean_squared_error": [159713.053504],
            "mean_squared_log_error": [0.008449],
            "median_absolute_error": [258.385742],
            "r2_score": [0.752698],
            "explained_variance": [0.756173],
        },
        dtype="Float64",
    )
    pandas.testing.assert_frame_equal(
        result,
        expected,
        check_exact=False,
        rtol=0.1,
        # int64 Index by default in pandas versus Int64 (nullable) Index in BigFramese
        check_index_type=False,
    )


def test_randomforestregressor_model_score_series(
    penguins_randomforest_regressor_model, penguins_df_default_index
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
    result = penguins_randomforest_regressor_model.score(X_test, y_test).to_pandas()
    expected = pandas.DataFrame(
        {
            "mean_absolute_error": [317.031042],
            "mean_squared_error": [159713.053504],
            "mean_squared_log_error": [0.008449],
            "median_absolute_error": [258.385742],
            "r2_score": [0.752698],
            "explained_variance": [0.756173],
        },
        dtype="Float64",
    )
    pandas.testing.assert_frame_equal(
        result,
        expected,
        check_exact=False,
        rtol=0.1,
        # int64 Index by default in pandas versus Int64 (nullable) Index in BigFramese
        check_index_type=False,
    )


def test_randomforestregressor_model_predict(
    penguins_randomforest_regressor_model: bigframes.ml.ensemble.RandomForestRegressor,
    new_penguins_df,
):
    predictions = penguins_randomforest_regressor_model.predict(
        new_penguins_df
    ).to_pandas()
    assert predictions.shape == (3, 8)
    result = predictions[["predicted_body_mass_g"]]
    expected = pandas.DataFrame(
        {"predicted_body_mass_g": ["3897.341797", "3458.385742", "3458.385742"]},
        dtype="Float64",
        index=pandas.Index([1633, 1672, 1690], name="tag_number", dtype="Int64"),
    )
    pandas.testing.assert_frame_equal(
        result.sort_index(),
        expected,
        check_exact=False,
        rtol=0.1,
        check_index_type=False,
    )


def test_to_gbq_saved_randomforestregressor_model_scores(
    penguins_randomforest_regressor_model, dataset_id, penguins_df_default_index
):
    saved_model = penguins_randomforest_regressor_model.to_gbq(
        f"{dataset_id}.test_penguins_model", replace=True
    )
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
            "mean_absolute_error": [319.239235],
            "mean_squared_error": [161913.126651],
            "mean_squared_log_error": [0.008611],
            "median_absolute_error": [266.614258],
            "r2_score": [0.747504],
            "explained_variance": [0.750358],
        },
        dtype="Float64",
    )
    pandas.testing.assert_frame_equal(
        result,
        expected,
        check_exact=False,
        rtol=0.1,
        # int64 Index by default in pandas versus Int64 (nullable) Index in BigFramese
        check_index_type=False,
    )


def test_to_randomforestregressor_model_gbq_replace(
    penguins_randomforest_regressor_model, dataset_id
):
    penguins_randomforest_regressor_model.to_gbq(
        f"{dataset_id}.test_penguins_model", replace=True
    )
    with pytest.raises(google.api_core.exceptions.Conflict):
        penguins_randomforest_regressor_model.to_gbq(
            f"{dataset_id}.test_penguins_model"
        )


def test_randomforestclassifier_model_score(
    penguins_randomforest_classifier_model, penguins_df_default_index
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
    y_test = df[["sex"]]
    result = penguins_randomforest_classifier_model.score(X_test, y_test).to_pandas()
    TestCase().assertSequenceEqual(result.shape, (1, 6))
    for col_name in [
        "precision",
        "recall",
        "accuracy",
        "f1_score",
        "log_loss",
        "roc_auc",
    ]:
        assert col_name in result.columns


def test_randomforestclassifier_model_score_series(
    penguins_randomforest_classifier_model, penguins_df_default_index
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
    result = penguins_randomforest_classifier_model.score(X_test, y_test).to_pandas()
    TestCase().assertSequenceEqual(result.shape, (1, 6))
    for col_name in [
        "precision",
        "recall",
        "accuracy",
        "f1_score",
        "log_loss",
        "roc_auc",
    ]:
        assert col_name in result.columns


def test_randomforestclassifier_model_predict(
    penguins_randomforest_classifier_model: bigframes.ml.ensemble.RandomForestClassifier,
    new_penguins_df,
):
    predictions = penguins_randomforest_classifier_model.predict(
        new_penguins_df
    ).to_pandas()
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
        check_index_type=False,
    )


def test_to_gbq_saved_randomforestclassifier_model_scores(
    penguins_randomforest_classifier_model, dataset_id, penguins_df_default_index
):
    saved_model = penguins_randomforest_classifier_model.to_gbq(
        f"{dataset_id}.test_penguins_model", replace=True
    )
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
            "precision": [0.636746],
            "recall": [0.638636],
            "accuracy": [0.95509],
            "f1_score": [0.637688],
            "log_loss": [0.886307],
            "roc_auc": [0.966543],
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


def test_to_randomforestclassifier_model_gbq_replace(
    penguins_randomforest_classifier_model, dataset_id
):
    penguins_randomforest_classifier_model.to_gbq(
        f"{dataset_id}.test_penguins_model", replace=True
    )
    with pytest.raises(google.api_core.exceptions.Conflict):
        penguins_randomforest_classifier_model.to_gbq(
            f"{dataset_id}.test_penguins_model"
        )
