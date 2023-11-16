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

import pandas
import pytest

import bigframes.ml.ensemble


@pytest.mark.flaky(retries=2, delay=120)
def test_xgbregressor_default_params(penguins_df_default_index, dataset_id):
    model = bigframes.ml.ensemble.XGBRegressor()

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
    expected = pandas.DataFrame(
        {
            "mean_absolute_error": [97.368139],
            "mean_squared_error": [16284.877027],
            "mean_squared_log_error": [0.0010189],
            "median_absolute_error": [72.158691],
            "r2_score": [0.974784],
            "explained_variance": [0.974845],
        },
        dtype="Float64",
    )
    expected = expected.reindex(index=expected.index.astype("Int64"))
    pandas.testing.assert_frame_equal(result, expected, check_exact=False, rtol=0.1)

    # save, load, check parameters to ensure configuration was kept
    reloaded_model = model.to_gbq(
        f"{dataset_id}.temp_configured_xgbregressor_model", replace=True
    )
    assert (
        f"{dataset_id}.temp_configured_xgbregressor_model"
        in reloaded_model._bqml_model.model_name
    )


@pytest.mark.flaky(retries=2, delay=120)
def test_xgbregressor_dart_booster_multiple_params(
    penguins_df_default_index, dataset_id
):
    model = bigframes.ml.ensemble.XGBRegressor(
        booster="dart",
        tree_method="auto",
        min_tree_child_weight=2,
        colsample_bytree=0.95,
        colsample_bylevel=0.95,
        colsample_bynode=0.95,
        num_parallel_tree=2,
        max_depth=4,
        subsample=0.95,
        reg_alpha=0.0001,
        reg_lambda=0.0001,
        learning_rate=0.015,
        max_iterations=4,
        min_rel_progress=0.02,
    )

    df = penguins_df_default_index.dropna().sample(n=70)
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
    TestCase().assertSequenceEqual(result.shape, (1, 6))
    for col_name in [
        "mean_absolute_error",
        "mean_squared_error",
        "mean_squared_log_error",
        "median_absolute_error",
        "r2_score",
        "explained_variance",
    ]:
        assert col_name in result.columns

    # save, load, check parameters to ensure configuration was kept
    reloaded_model = model.to_gbq(
        f"{dataset_id}.temp_configured_xgbregressor_model", replace=True
    )
    assert (
        f"{dataset_id}.temp_configured_xgbregressor_model"
        in reloaded_model._bqml_model.model_name
    )
    assert reloaded_model.booster == "DART"
    assert reloaded_model.dart_normalized_type == "tree"
    assert reloaded_model.tree_method == "AUTO"
    assert reloaded_model.colsample_bytree == 0.95
    assert reloaded_model.colsample_bylevel == 0.95
    assert reloaded_model.colsample_bynode == 0.95
    assert reloaded_model.early_stop is True
    assert reloaded_model.subsample == 0.95
    assert reloaded_model.reg_alpha == 0.0001
    assert reloaded_model.reg_lambda == 0.0001
    assert reloaded_model.learning_rate == 0.015
    assert reloaded_model.max_iterations == 4
    assert reloaded_model.min_rel_progress == 0.02
    assert reloaded_model.gamma == 0.0
    assert reloaded_model.max_depth == 4
    assert reloaded_model.min_tree_child_weight == 2
    assert reloaded_model.num_parallel_tree == 2


@pytest.mark.flaky(retries=2, delay=120)
def test_xgbclassifier_default_params(penguins_df_default_index, dataset_id):
    model = bigframes.ml.ensemble.XGBClassifier()

    df = penguins_df_default_index.dropna().sample(n=70)
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

    # save, load, check parameters to ensure configuration was kept
    reloaded_model = model.to_gbq(
        f"{dataset_id}.temp_configured_xgbclassifier_model", replace=True
    )
    assert (
        f"{dataset_id}.temp_configured_xgbclassifier_model"
        in reloaded_model._bqml_model.model_name
    )


# @pytest.mark.flaky(retries=2, delay=120)
def test_xgbclassifier_dart_booster_multiple_params(
    penguins_df_default_index, dataset_id
):
    model = bigframes.ml.ensemble.XGBClassifier(
        booster="dart",
        tree_method="auto",
        min_tree_child_weight=2,
        colsample_bytree=0.95,
        colsample_bylevel=0.95,
        colsample_bynode=0.95,
        num_parallel_tree=2,
        max_depth=4,
        subsample=0.95,
        reg_alpha=0.0001,
        reg_lambda=0.0001,
        learning_rate=0.015,
        max_iterations=4,
        min_rel_progress=0.02,
    )

    df = penguins_df_default_index.dropna().sample(n=70)
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

    # save, load, check parameters to ensure configuration was kept
    reloaded_model = model.to_gbq(
        f"{dataset_id}.temp_configured_xgbclassifier_model", replace=True
    )
    assert (
        f"{dataset_id}.temp_configured_xgbclassifier_model"
        in reloaded_model._bqml_model.model_name
    )
    assert reloaded_model.booster == "DART"
    assert reloaded_model.dart_normalized_type == "tree"
    assert reloaded_model.tree_method == "AUTO"
    assert reloaded_model.colsample_bytree == 0.95
    assert reloaded_model.colsample_bylevel == 0.95
    assert reloaded_model.colsample_bynode == 0.95
    assert reloaded_model.early_stop is True
    assert reloaded_model.subsample == 0.95
    assert reloaded_model.reg_alpha == 0.0001
    assert reloaded_model.reg_lambda == 0.0001
    assert reloaded_model.learning_rate == 0.015
    assert reloaded_model.max_iterations == 4
    assert reloaded_model.min_rel_progress == 0.02
    assert reloaded_model.gamma == 0.0
    assert reloaded_model.max_depth == 4
    assert reloaded_model.min_tree_child_weight == 2
    assert reloaded_model.num_parallel_tree == 2


@pytest.mark.flaky(retries=2, delay=120)
def test_randomforestregressor_default_params(penguins_df_default_index, dataset_id):
    model = bigframes.ml.ensemble.RandomForestRegressor()

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
    TestCase().assertSequenceEqual(result.shape, (1, 6))
    for col_name in [
        "mean_absolute_error",
        "mean_squared_error",
        "mean_squared_log_error",
        "median_absolute_error",
        "r2_score",
        "explained_variance",
    ]:
        assert col_name in result.columns

    # save, load, check parameters to ensure configuration was kept
    reloaded_model = model.to_gbq(
        f"{dataset_id}.temp_configured_randomforestregressor_model", replace=True
    )
    assert (
        f"{dataset_id}.temp_configured_randomforestregressor_model"
        in reloaded_model._bqml_model.model_name
    )


@pytest.mark.flaky(retries=2, delay=120)
def test_randomforestregressor_multiple_params(penguins_df_default_index, dataset_id):
    model = bigframes.ml.ensemble.RandomForestRegressor(
        tree_method="auto",
        min_tree_child_weight=2,
        colsample_bytree=0.95,
        colsample_bylevel=0.95,
        colsample_bynode=0.95,
        num_parallel_tree=90,
        max_depth=14,
        subsample=0.95,
        reg_alpha=0.0001,
        reg_lambda=0.0001,
        min_rel_progress=0.02,
    )

    df = penguins_df_default_index.dropna().sample(n=70)
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
    TestCase().assertSequenceEqual(result.shape, (1, 6))
    for col_name in [
        "mean_absolute_error",
        "mean_squared_error",
        "mean_squared_log_error",
        "median_absolute_error",
        "r2_score",
        "explained_variance",
    ]:
        assert col_name in result.columns

    # save, load, check parameters to ensure configuration was kept
    reloaded_model = model.to_gbq(
        f"{dataset_id}.temp_configured_randomforestregressor_model", replace=True
    )
    assert (
        f"{dataset_id}.temp_configured_randomforestregressor_model"
        in reloaded_model._bqml_model.model_name
    )
    assert reloaded_model.tree_method == "AUTO"
    assert reloaded_model.colsample_bytree == 0.95
    assert reloaded_model.colsample_bylevel == 0.95
    assert reloaded_model.colsample_bynode == 0.95
    assert reloaded_model.early_stop is True
    assert reloaded_model.subsample == 0.95
    assert reloaded_model.reg_alpha == 0.0001
    assert reloaded_model.reg_lambda == 0.0001
    assert reloaded_model.min_rel_progress == 0.02
    assert reloaded_model.gamma == 0.0
    assert reloaded_model.max_depth == 14
    assert reloaded_model.min_tree_child_weight == 2
    assert reloaded_model.num_parallel_tree == 90
    assert reloaded_model.enable_global_explain is False


@pytest.mark.flaky(retries=2, delay=120)
def test_randomforestclassifier_default_params(penguins_df_default_index, dataset_id):
    model = bigframes.ml.ensemble.RandomForestClassifier()

    df = penguins_df_default_index.dropna().sample(n=70)
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

    # save, load, check parameters to ensure configuration was kept
    reloaded_model = model.to_gbq(
        f"{dataset_id}.temp_configured_randomforestclassifier_model", replace=True
    )
    assert (
        f"{dataset_id}.temp_configured_randomforestclassifier_model"
        in reloaded_model._bqml_model.model_name
    )


@pytest.mark.flaky(retries=2, delay=120)
def test_randomforestclassifier_multiple_params(penguins_df_default_index, dataset_id):
    model = bigframes.ml.ensemble.RandomForestClassifier(
        tree_method="AUTO",
        min_tree_child_weight=2,
        colsample_bytree=0.95,
        colsample_bylevel=0.95,
        colsample_bynode=0.95,
        num_parallel_tree=90,
        max_depth=14,
        subsample=0.95,
        reg_alpha=0.0001,
        reg_lambda=0.0001,
        min_rel_progress=0.02,
    )

    df = penguins_df_default_index.dropna().sample(n=70)
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

    # save, load, check parameters to ensure configuration was kept
    reloaded_model = model.to_gbq(
        f"{dataset_id}.temp_configured_randomforestclassifier_model", replace=True
    )
    assert (
        f"{dataset_id}.temp_configured_randomforestclassifier_model"
        in reloaded_model._bqml_model.model_name
    )
    assert reloaded_model.tree_method == "AUTO"
    assert reloaded_model.colsample_bytree == 0.95
    assert reloaded_model.colsample_bylevel == 0.95
    assert reloaded_model.colsample_bynode == 0.95
    assert reloaded_model.early_stop is True
    assert reloaded_model.subsample == 0.95
    assert reloaded_model.reg_alpha == 0.0001
    assert reloaded_model.reg_lambda == 0.0001
    assert reloaded_model.min_rel_progress == 0.02
    assert reloaded_model.gamma == 0.0
    assert reloaded_model.max_depth == 14
    assert reloaded_model.min_tree_child_weight == 2
    assert reloaded_model.num_parallel_tree == 90
    assert reloaded_model.enable_global_explain is False
