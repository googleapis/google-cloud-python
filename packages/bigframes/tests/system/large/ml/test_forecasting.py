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

import pytest

from bigframes.ml import forecasting
from bigframes.testing import utils

ARIMA_EVALUATE_OUTPUT_COL = [
    "non_seasonal_p",
    "non_seasonal_d",
    "non_seasonal_q",
    "has_drift",
    "log_likelihood",
    "AIC",
    "variance",
    "seasonal_periods",
    "has_holiday_effect",
    "has_spikes_and_dips",
    "has_step_changes",
    "error_message",
]


def _fit_arima_model(time_series_df_default_index):
    model = forecasting.ARIMAPlus()
    X_train = time_series_df_default_index["parsed_date"]
    y_train = time_series_df_default_index[["total_visits"]]
    return model, X_train, y_train


@pytest.fixture(scope="module")
def arima_model(time_series_df_default_index):
    model, X_train, y_train = _fit_arima_model(time_series_df_default_index)
    model.fit(X_train, y_train)
    return model


@pytest.fixture(scope="module")
def arima_model_w_id(time_series_df_default_index):
    model, X_train, y_train = _fit_arima_model(time_series_df_default_index)
    id_cols = time_series_df_default_index[["id"]]
    model.fit(X_train, y_train, id_col=id_cols)
    return model


@pytest.mark.parametrize("id_col_name", [None, "id"])
def test_arima_plus_model_fit_score(
    dataset_id,
    new_time_series_df,
    new_time_series_df_w_id,
    arima_model,
    arima_model_w_id,
    id_col_name,
):
    curr_model = arima_model_w_id if id_col_name else arima_model
    if id_col_name:
        result = curr_model.score(
            new_time_series_df_w_id[["parsed_date"]],
            new_time_series_df_w_id[["total_visits"]],
            id_col=new_time_series_df_w_id[[id_col_name]],
        ).to_pandas()
    else:
        result = curr_model.score(
            new_time_series_df[["parsed_date"]], new_time_series_df[["total_visits"]]
        ).to_pandas()
    expected_columns = [
        "mean_absolute_error",
        "mean_squared_error",
        "root_mean_squared_error",
        "mean_absolute_percentage_error",
        "symmetric_mean_absolute_percentage_error",
    ]
    if id_col_name:
        expected_columns.insert(0, id_col_name)
    utils.check_pandas_df_schema_and_index(
        result,
        columns=expected_columns,
        index=2 if id_col_name else 1,
    )

    # save, load to ensure configuration was kept
    reloaded_model = curr_model.to_gbq(
        f"{dataset_id}.temp_arima_plus_model", replace=True
    )
    assert (
        f"{dataset_id}.temp_arima_plus_model" in reloaded_model._bqml_model.model_name
    )


@pytest.mark.parametrize("id_col_name", [None, "id"])
def test_arima_plus_model_fit_summary(
    dataset_id, arima_model, arima_model_w_id, id_col_name
):
    curr_model = arima_model_w_id if id_col_name else arima_model
    result = curr_model.summary().to_pandas()
    expected_columns = (
        [id_col_name] + ARIMA_EVALUATE_OUTPUT_COL
        if id_col_name
        else ARIMA_EVALUATE_OUTPUT_COL
    )
    utils.check_pandas_df_schema_and_index(
        result, columns=expected_columns, index=2 if id_col_name else 1
    )
    # save, load to ensure configuration was kept
    reloaded_model = curr_model.to_gbq(
        f"{dataset_id}.temp_arima_plus_model", replace=True
    )
    assert (
        f"{dataset_id}.temp_arima_plus_model" in reloaded_model._bqml_model.model_name
    )


@pytest.mark.parametrize("id_col_name", [None, "id"])
def test_arima_coefficients(arima_model, arima_model_w_id, id_col_name):
    result = (
        arima_model_w_id.coef_.to_pandas()
        if id_col_name
        else arima_model.coef_.to_pandas()
    )
    expected_columns = [
        "ar_coefficients",
        "ma_coefficients",
        "intercept_or_drift",
    ]
    if id_col_name:
        expected_columns.insert(0, id_col_name)
    utils.check_pandas_df_schema_and_index(
        result, columns=expected_columns, index=2 if id_col_name else 1
    )


@pytest.mark.parametrize("id_col_name", [None, "id"])
def test_arima_plus_model_fit_params(
    time_series_df_default_index, dataset_id, id_col_name
):
    model = forecasting.ARIMAPlus(
        horizon=100,
        auto_arima=True,
        auto_arima_max_order=4,
        auto_arima_min_order=1,
        data_frequency="daily",
        holiday_region="US",
        clean_spikes_and_dips=False,
        adjust_step_changes=False,
        forecast_limit_lower_bound=0.0,
        time_series_length_fraction=0.5,
        min_time_series_length=10,
        trend_smoothing_window_size=5,
        decompose_time_series=False,
    )

    X_train = time_series_df_default_index[["parsed_date"]]
    y_train = time_series_df_default_index["total_visits"]
    if id_col_name is None:
        model.fit(X_train, y_train)
    else:
        id_cols = time_series_df_default_index[[id_col_name]]
        model.fit(X_train, y_train, id_col=id_cols)

    # save, load to ensure configuration was kept
    reloaded_model = model.to_gbq(f"{dataset_id}.temp_arima_plus_model", replace=True)
    assert reloaded_model._bqml_model is not None
    assert (
        f"{dataset_id}.temp_arima_plus_model" in reloaded_model._bqml_model.model_name
    )

    assert reloaded_model.horizon == 100
    assert reloaded_model.auto_arima is True
    assert reloaded_model.auto_arima_max_order == 4
    assert reloaded_model.auto_arima_min_order == 1
    assert reloaded_model.data_frequency == "DAILY"
    assert reloaded_model.holiday_region == "US"
    assert reloaded_model.clean_spikes_and_dips is False
    assert reloaded_model.adjust_step_changes is False
    # TODO(b/391399223): API must return forecastLimitLowerBound for the following assertion
    # assert reloaded_model.forecast_limit_lower_bound == 0.0
    assert reloaded_model.time_series_length_fraction == 0.5
    assert reloaded_model.min_time_series_length == 10
    assert reloaded_model.trend_smoothing_window_size == 5
    assert reloaded_model.decompose_time_series is False
