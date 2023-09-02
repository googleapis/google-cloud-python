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

import pandas as pd

import bigframes.ml.linear_model


def test_linear_regression_configure_fit_score(penguins_df_default_index, dataset_id):
    model = bigframes.ml.linear_model.LinearRegression(fit_intercept=False)

    df = penguins_df_default_index.dropna()
    X_train = df[
        [
            "species",
            "island",
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
            "sex",
        ]
    ]
    y_train = df[["body_mass_g"]]
    model.fit(X_train, y_train)

    # Check score to ensure the model was fitted
    result = model.score(X_train, y_train).to_pandas()
    expected = pd.DataFrame(
        {
            "mean_absolute_error": [225.735767],
            "mean_squared_error": [80417.461828],
            "mean_squared_log_error": [0.004967],
            "median_absolute_error": [172.543702],
            "r2_score": [0.87548],
            "explained_variance": [0.87548],
        },
        dtype="Float64",
    )
    expected = expected.reindex(index=expected.index.astype("Int64"))
    pd.testing.assert_frame_equal(result, expected, check_exact=False, rtol=0.1)

    # save, load, check parameters to ensure configuration was kept
    reloaded_model = model.to_gbq(f"{dataset_id}.temp_configured_model", replace=True)
    assert (
        f"{dataset_id}.temp_configured_model" in reloaded_model._bqml_model.model_name
    )

    # TODO(yunmengxie): enable this once b/277242951 (fit_intercept missing from API) is fixed
    # assert reloaded_model.fit_intercept == False


def test_linear_regression_manual_split_configure_fit_score(
    penguins_df_default_index, dataset_id
):
    model = bigframes.ml.linear_model.LinearRegression(fit_intercept=True)

    df = penguins_df_default_index.dropna()
    X_train = df[
        [
            "species",
            "island",
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
            "sex",
        ]
    ]
    y_train = df[["body_mass_g"]]
    model.fit(X_train, y_train)

    # Check score to ensure the model was fitted
    result = model.score(X_train, y_train).to_pandas()
    expected = pd.DataFrame(
        {
            "mean_absolute_error": [225.735767],
            "mean_squared_error": [80417.461828],
            "mean_squared_log_error": [0.004967],
            "median_absolute_error": [172.543702],
            "r2_score": [0.87548],
            "explained_variance": [0.87548],
        },
        dtype="Float64",
    )
    expected = expected.reindex(index=expected.index.astype("Int64"))
    pd.testing.assert_frame_equal(result, expected, check_exact=False, rtol=0.1)

    # save, load, check parameters to ensure configuration was kept
    reloaded_model = model.to_gbq(f"{dataset_id}.temp_configured_model", replace=True)
    assert (
        f"{dataset_id}.temp_configured_model" in reloaded_model._bqml_model.model_name
    )
    assert reloaded_model.fit_intercept is True


def test_logistic_regression_auto_class_weights_configure_fit_score(
    penguins_df_default_index, dataset_id
):
    model = bigframes.ml.linear_model.LogisticRegression()
    df = penguins_df_default_index.dropna()
    X_train = df[
        [
            "species",
            "island",
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
        ]
    ]
    y_train = df[["sex"]]
    model.fit(X_train, y_train)

    # Check score to ensure the model was fitted
    result = model.score(X_train, y_train).to_pandas()
    expected = pd.DataFrame(
        {
            "precision": [0.58085],
            "recall": [0.582576],
            "accuracy": [0.871257],
            "f1_score": [0.58171],
            "log_loss": [1.59285],
            "roc_auc": [0.9602],
        },
        dtype="Float64",
    )
    expected = expected.reindex(index=expected.index.astype("Int64"))
    pd.testing.assert_frame_equal(result, expected, check_exact=False, rtol=0.1)

    # save, load, check parameters to ensure configuration was kept
    reloaded_model = model.to_gbq(
        f"{dataset_id}.temp_configured_logistic_reg_model", replace=True
    )
    assert (
        f"{dataset_id}.temp_configured_logistic_reg_model"
        in reloaded_model._bqml_model.model_name
    )
    assert reloaded_model.fit_intercept is True
    # TODO(gaotianxiang): enable this once (auto_class_weights missing from API) is fixed
    # assert reloaded_model.auto_class_weights is True


def test_logistic_regression_manual_split_configure_fit_score(
    penguins_df_default_index, dataset_id
):
    model = bigframes.ml.linear_model.LogisticRegression(fit_intercept=True)

    df = penguins_df_default_index.dropna()
    X_train = df[
        [
            "species",
            "island",
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
            "body_mass_g",
        ]
    ]
    y_train = df[["sex"]]
    model.fit(X_train, y_train)

    # Check score to ensure the model was fitted
    result = model.score(X_train, y_train).to_pandas()
    expected = pd.DataFrame(
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
    expected = expected.reindex(index=expected.index.astype("Int64"))
    pd.testing.assert_frame_equal(result, expected, check_exact=False, rtol=0.1)

    # save, load, check parameters to ensure configuration was kept
    reloaded_model = model.to_gbq(
        f"{dataset_id}.temp_configured_logistic_reg_model", replace=True
    )
    assert (
        f"{dataset_id}.temp_configured_logistic_reg_model"
        in reloaded_model._bqml_model.model_name
    )
    assert reloaded_model.fit_intercept is True
    assert reloaded_model.auto_class_weights is False
