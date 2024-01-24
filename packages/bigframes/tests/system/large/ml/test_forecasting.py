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

from bigframes.ml import forecasting

ARIMA_EVALUATE_OUTPUT_COL = [
    "non_seasonal_p",
    "non_seasonal_d",
    "non_seasonal_q",
    "log_likelihood",
    "AIC",
    "variance",
    "seasonal_periods",
    "has_holiday_effect",
    "has_spikes_and_dips",
    "has_step_changes",
    "error_message",
]


def test_arima_plus_model_fit_score(
    time_series_df_default_index, dataset_id, new_time_series_df
):
    model = forecasting.ARIMAPlus()
    X_train = time_series_df_default_index[["parsed_date"]]
    y_train = time_series_df_default_index[["total_visits"]]
    model.fit(X_train, y_train)

    result = model.score(
        new_time_series_df[["parsed_date"]], new_time_series_df[["total_visits"]]
    ).to_pandas()
    expected = pd.DataFrame(
        {
            "mean_absolute_error": [154.742547],
            "mean_squared_error": [26844.868855],
            "root_mean_squared_error": [163.844038],
            "mean_absolute_percentage_error": [6.189702],
            "symmetric_mean_absolute_percentage_error": [6.097155],
        },
        dtype="Float64",
    )
    expected = expected.reindex(index=expected.index.astype("Int64"))
    pd.testing.assert_frame_equal(result, expected, check_exact=False, rtol=0.1)

    # save, load to ensure configuration was kept
    reloaded_model = model.to_gbq(f"{dataset_id}.temp_arima_plus_model", replace=True)
    assert (
        f"{dataset_id}.temp_arima_plus_model" in reloaded_model._bqml_model.model_name
    )


def test_arima_plus_model_fit_summary(time_series_df_default_index, dataset_id):
    model = forecasting.ARIMAPlus()
    X_train = time_series_df_default_index[["parsed_date"]]
    y_train = time_series_df_default_index[["total_visits"]]
    model.fit(X_train, y_train)

    result = model.summary()
    assert result.shape == (1, 12)
    assert all(column in result.columns for column in ARIMA_EVALUATE_OUTPUT_COL)

    # save, load to ensure configuration was kept
    reloaded_model = model.to_gbq(f"{dataset_id}.temp_arima_plus_model", replace=True)
    assert (
        f"{dataset_id}.temp_arima_plus_model" in reloaded_model._bqml_model.model_name
    )
