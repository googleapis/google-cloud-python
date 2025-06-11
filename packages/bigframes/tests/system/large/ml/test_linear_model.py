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

from bigframes.ml import model_selection
import bigframes.ml.linear_model
from bigframes.testing import utils


def test_linear_regression_configure_fit_score(penguins_df_default_index, dataset_id):
    model = bigframes.ml.linear_model.LinearRegression()

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
    utils.check_pandas_df_schema_and_index(
        result, columns=utils.ML_REGRESSION_METRICS, index=1
    )

    # save, load, check parameters to ensure configuration was kept
    reloaded_model = model.to_gbq(f"{dataset_id}.temp_configured_model", replace=True)
    assert reloaded_model._bqml_model is not None
    assert (
        f"{dataset_id}.temp_configured_model" in reloaded_model._bqml_model.model_name
    )
    assert reloaded_model.optimize_strategy == "NORMAL_EQUATION"
    assert reloaded_model.fit_intercept is True
    assert reloaded_model.calculate_p_values is False
    assert reloaded_model.enable_global_explain is False
    assert reloaded_model.l1_reg is None
    assert reloaded_model.l2_reg == 0.0
    assert reloaded_model.learning_rate is None
    assert reloaded_model.learning_rate_strategy == "line_search"
    assert reloaded_model.ls_init_learning_rate is None
    assert reloaded_model.max_iterations == 20
    assert reloaded_model.tol == 0.01


def test_linear_regression_configure_fit_with_eval_score(
    penguins_df_default_index, dataset_id
):
    model = bigframes.ml.linear_model.LinearRegression()

    df = penguins_df_default_index.dropna()
    X = df[
        [
            "species",
            "island",
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
            "sex",
        ]
    ]
    y = df[["body_mass_g"]]

    X_train, X_eval, y_train, y_eval = model_selection.train_test_split(X, y)

    model.fit(X_train, y_train, X_eval=X_eval, y_eval=y_eval)

    # Check score to ensure the model was fitted
    result = model.score(X_eval, y_eval).to_pandas()
    utils.check_pandas_df_schema_and_index(
        result, columns=utils.ML_REGRESSION_METRICS, index=1
    )

    # save, load, check parameters to ensure configuration was kept
    bq_model_name = f"{dataset_id}.temp_configured_model"
    reloaded_model = model.to_gbq(bq_model_name, replace=True)
    assert reloaded_model._bqml_model is not None
    assert (
        f"{dataset_id}.temp_configured_model" in reloaded_model._bqml_model.model_name
    )
    assert reloaded_model.optimize_strategy == "NORMAL_EQUATION"
    assert reloaded_model.fit_intercept is True
    assert reloaded_model.calculate_p_values is False
    assert reloaded_model.enable_global_explain is False
    assert reloaded_model.l1_reg is None
    assert reloaded_model.l2_reg == 0.0
    assert reloaded_model.learning_rate is None
    assert reloaded_model.learning_rate_strategy == "line_search"
    assert reloaded_model.ls_init_learning_rate is None
    assert reloaded_model.max_iterations == 20
    assert reloaded_model.tol == 0.01

    # make sure the bqml model was internally created with custom split
    bq_model = penguins_df_default_index._session.bqclient.get_model(bq_model_name)
    last_fitting = bq_model.training_runs[-1]["trainingOptions"]
    assert last_fitting["dataSplitMethod"] == "CUSTOM"
    assert "dataSplitColumn" in last_fitting

    # make sure the bqml model has the same  evaluation metrics attached as
    # returned by model.score()
    bq_model_expected_eval_metrics = result[utils.ML_REGRESSION_METRICS[:5]]
    bq_model_eval_metrics = bq_model.training_runs[-1]["evaluationMetrics"][
        "regressionMetrics"
    ]
    bq_model_eval_metrics = pd.DataFrame(
        [
            [
                bq_model_eval_metrics["meanAbsoluteError"],
                bq_model_eval_metrics["meanSquaredError"],
                bq_model_eval_metrics["meanSquaredLogError"],
                bq_model_eval_metrics["medianAbsoluteError"],
                bq_model_eval_metrics["rSquared"],
            ]
        ],
        columns=utils.ML_REGRESSION_METRICS[:5],
    )
    pd.testing.assert_frame_equal(
        bq_model_expected_eval_metrics,
        bq_model_eval_metrics,
        check_dtype=False,
        check_index_type=False,
    )


def test_linear_regression_customized_params_fit_score(
    penguins_df_default_index, dataset_id
):
    model = bigframes.ml.linear_model.LinearRegression(
        fit_intercept=False,
        l2_reg=0.2,
        tol=0.02,
        l1_reg=0.2,
        max_iterations=30,
        optimize_strategy="batch_gradient_descent",
        learning_rate_strategy="constant",
        learning_rate=0.2,
    )

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
    utils.check_pandas_df_schema_and_index(
        result, columns=utils.ML_REGRESSION_METRICS, index=1
    )

    # save, load, check parameters to ensure configuration was kept
    reloaded_model = model.to_gbq(f"{dataset_id}.temp_configured_model", replace=True)
    assert reloaded_model._bqml_model is not None
    assert (
        f"{dataset_id}.temp_configured_model" in reloaded_model._bqml_model.model_name
    )
    assert reloaded_model.optimize_strategy == "BATCH_GRADIENT_DESCENT"
    assert reloaded_model.fit_intercept is False
    assert reloaded_model.calculate_p_values is False
    assert reloaded_model.enable_global_explain is False
    assert reloaded_model.l1_reg == 0.2
    assert reloaded_model.l2_reg == 0.2
    assert reloaded_model.ls_init_learning_rate is None
    assert reloaded_model.max_iterations == 30
    assert reloaded_model.tol == 0.02
    assert reloaded_model.learning_rate_strategy == "CONSTANT"
    assert reloaded_model.learning_rate == 0.2


def test_unordered_mode_linear_regression_configure_fit_score_predict(
    unordered_session, penguins_table_id, dataset_id
):
    model = bigframes.ml.linear_model.LinearRegression()

    df = unordered_session.read_gbq(penguins_table_id).dropna()
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

    start_execution_count = df._block._expr.session._metrics.execution_count
    model.fit(X_train, y_train)
    end_execution_count = df._block._expr.session._metrics.execution_count
    # The fit function initiates two queries: the first generates and caches
    # the training data, while the second creates and fits the model.
    assert end_execution_count - start_execution_count == 2

    # Check score to ensure the model was fitted
    start_execution_count = end_execution_count
    result = model.score(X_train, y_train).to_pandas()
    end_execution_count = df._block._expr.session._metrics.execution_count
    # The score function and to_pandas reuse same result.
    assert end_execution_count - start_execution_count == 1

    utils.check_pandas_df_schema_and_index(
        result, columns=utils.ML_REGRESSION_METRICS, index=1
    )

    # save, load, check parameters to ensure configuration was kept
    reloaded_model = model.to_gbq(f"{dataset_id}.temp_configured_model", replace=True)
    assert reloaded_model._bqml_model is not None
    assert (
        f"{dataset_id}.temp_configured_model" in reloaded_model._bqml_model.model_name
    )
    assert reloaded_model.optimize_strategy == "NORMAL_EQUATION"
    assert reloaded_model.fit_intercept is True
    assert reloaded_model.calculate_p_values is False
    assert reloaded_model.enable_global_explain is False
    assert reloaded_model.l1_reg is None
    assert reloaded_model.l2_reg == 0.0
    assert reloaded_model.learning_rate is None
    assert reloaded_model.learning_rate_strategy == "line_search"
    assert reloaded_model.ls_init_learning_rate is None
    assert reloaded_model.max_iterations == 20
    assert reloaded_model.tol == 0.01

    start_execution_count = df._block._expr.session._metrics.execution_count
    pred = reloaded_model.predict(df)
    end_execution_count = df._block._expr.session._metrics.execution_count
    assert end_execution_count - start_execution_count == 1
    utils.check_pandas_df_schema_and_index(
        pred,
        columns=("predicted_body_mass_g",),
        col_exact=False,
        index=334,
    )


# TODO(garrettwu): add tests for param warm_start. Requires a trained model.


def test_logistic_regression_configure_fit_score(penguins_df_default_index, dataset_id):
    model = bigframes.ml.linear_model.LogisticRegression()

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
    utils.check_pandas_df_schema_and_index(
        result, columns=utils.ML_CLASSFICATION_METRICS, index=1
    )

    # save, load, check parameters to ensure configuration was kept
    reloaded_model = model.to_gbq(
        f"{dataset_id}.temp_configured_logistic_reg_model", replace=True
    )
    assert reloaded_model._bqml_model is not None
    assert (
        f"{dataset_id}.temp_configured_logistic_reg_model"
        in reloaded_model._bqml_model.model_name
    )
    assert reloaded_model.fit_intercept is True
    assert reloaded_model.class_weight is None


def test_logistic_regression_configure_fit_with_eval_score(
    penguins_df_default_index, dataset_id
):
    model = bigframes.ml.linear_model.LogisticRegression()

    df = penguins_df_default_index.dropna()
    df = df[df["sex"].isin(["MALE", "FEMALE"])]

    X = df[
        [
            "species",
            "island",
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
            "body_mass_g",
        ]
    ]
    y = df[["sex"]]

    X_train, X_eval, y_train, y_eval = model_selection.train_test_split(X, y)

    model.fit(X_train, y_train, X_eval=X_eval, y_eval=y_eval)

    # Check score to ensure the model was fitted
    result = model.score(X_eval, y_eval).to_pandas()
    utils.check_pandas_df_schema_and_index(
        result, columns=utils.ML_CLASSFICATION_METRICS, index=1
    )

    # save, load, check parameters to ensure configuration was kept
    bq_model_name = f"{dataset_id}.temp_configured_logistic_reg_model"
    reloaded_model = model.to_gbq(bq_model_name, replace=True)
    assert reloaded_model._bqml_model is not None
    assert (
        f"{dataset_id}.temp_configured_logistic_reg_model"
        in reloaded_model._bqml_model.model_name
    )
    assert reloaded_model.fit_intercept is True
    assert reloaded_model.class_weight is None

    # make sure the bqml model was internally created with custom split
    bq_model = penguins_df_default_index._session.bqclient.get_model(bq_model_name)
    last_fitting = bq_model.training_runs[-1]["trainingOptions"]
    assert last_fitting["dataSplitMethod"] == "CUSTOM"
    assert "dataSplitColumn" in last_fitting

    # make sure the bqml model has the same  evaluation metrics attached as
    # returned by model.score()
    bq_model_expected_eval_metrics = result
    bq_model_eval_metrics = bq_model.training_runs[-1]["evaluationMetrics"][
        "binaryClassificationMetrics"
    ]["aggregateClassificationMetrics"]
    bq_model_eval_metrics = pd.DataFrame(
        [
            [
                bq_model_eval_metrics["precision"],
                bq_model_eval_metrics["recall"],
                bq_model_eval_metrics["accuracy"],
                bq_model_eval_metrics["f1Score"],
                bq_model_eval_metrics["logLoss"],
                bq_model_eval_metrics["rocAuc"],
            ]
        ],
        columns=utils.ML_CLASSFICATION_METRICS,
    )
    pd.testing.assert_frame_equal(
        bq_model_expected_eval_metrics,
        bq_model_eval_metrics,
        check_dtype=False,
        check_index_type=False,
    )


def test_logistic_regression_customized_params_fit_score(
    penguins_df_default_index, dataset_id
):
    model = bigframes.ml.linear_model.LogisticRegression(
        fit_intercept=False,
        class_weight="balanced",
        l2_reg=0.2,
        tol=0.02,
        l1_reg=0.2,
        max_iterations=30,
        optimize_strategy="batch_gradient_descent",
        learning_rate_strategy="constant",
        learning_rate=0.2,
    )
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
    utils.check_pandas_df_schema_and_index(
        result, columns=utils.ML_CLASSFICATION_METRICS, index=1
    )

    # save, load, check parameters to ensure configuration was kept
    reloaded_model = model.to_gbq(
        f"{dataset_id}.temp_configured_logistic_reg_model", replace=True
    )
    assert reloaded_model._bqml_model is not None
    assert (
        f"{dataset_id}.temp_configured_logistic_reg_model"
        in reloaded_model._bqml_model.model_name
    )
    assert reloaded_model.fit_intercept is False
    assert reloaded_model.class_weight == "balanced"
    assert reloaded_model.calculate_p_values is False
    assert reloaded_model.enable_global_explain is False
    assert reloaded_model.l1_reg == 0.2
    assert reloaded_model.l2_reg == 0.2
    assert reloaded_model.ls_init_learning_rate is None
    assert reloaded_model.max_iterations == 30
    assert reloaded_model.tol == 0.02
    assert reloaded_model.learning_rate_strategy == "CONSTANT"
    assert reloaded_model.learning_rate == 0.2


def test_model_centroids_with_custom_index(penguins_df_default_index):
    model = bigframes.ml.linear_model.LogisticRegression(
        fit_intercept=False,
        class_weight="balanced",
        l2_reg=0.2,
        tol=0.02,
        l1_reg=0.2,
        max_iterations=30,
        optimize_strategy="batch_gradient_descent",
        learning_rate_strategy="constant",
        learning_rate=0.2,
    )
    df = penguins_df_default_index.dropna().set_index(["species", "island"])
    X_train = df[
        [
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
        ]
    ]
    y_train = df[["sex"]]
    model.fit(X_train, y_train)

    # If this line executes without errors, the model has correctly ignored the custom index columns
    model.predict(X_train.reset_index(drop=True))
