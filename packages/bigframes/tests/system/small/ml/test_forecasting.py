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

from datetime import datetime

import pandas as pd
import pyarrow as pa
import pytz

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


def test_arima_plus_predict_default(
    time_series_arima_plus_model: forecasting.ARIMAPlus,
):
    utc = pytz.utc
    predictions = time_series_arima_plus_model.predict().to_pandas()
    assert predictions.shape == (3, 8)
    result = predictions[["forecast_timestamp", "forecast_value"]]
    expected = pd.DataFrame(
        {
            "forecast_timestamp": [
                datetime(2017, 8, 2, tzinfo=utc),
                datetime(2017, 8, 3, tzinfo=utc),
                datetime(2017, 8, 4, tzinfo=utc),
            ],
            "forecast_value": [2724.472284, 2593.368389, 2353.613034],
        }
    )
    expected["forecast_value"] = expected["forecast_value"].astype(pd.Float64Dtype())
    expected["forecast_timestamp"] = expected["forecast_timestamp"].astype(
        pd.ArrowDtype(pa.timestamp("us", tz="UTC"))
    )

    pd.testing.assert_frame_equal(
        result,
        expected,
        rtol=0.1,
        check_index_type=False,
    )


def test_arima_plus_predict_params(time_series_arima_plus_model: forecasting.ARIMAPlus):
    utc = pytz.utc
    predictions = time_series_arima_plus_model.predict(
        horizon=4, confidence_level=0.9
    ).to_pandas()
    assert predictions.shape == (4, 8)
    result = predictions[["forecast_timestamp", "forecast_value"]]
    expected = pd.DataFrame(
        {
            "forecast_timestamp": [
                datetime(2017, 8, 2, tzinfo=utc),
                datetime(2017, 8, 3, tzinfo=utc),
                datetime(2017, 8, 4, tzinfo=utc),
                datetime(2017, 8, 5, tzinfo=utc),
            ],
            "forecast_value": [2724.472284, 2593.368389, 2353.613034, 1781.623071],
        }
    )
    expected["forecast_value"] = expected["forecast_value"].astype(pd.Float64Dtype())
    expected["forecast_timestamp"] = expected["forecast_timestamp"].astype(
        pd.ArrowDtype(pa.timestamp("us", tz="UTC"))
    )

    pd.testing.assert_frame_equal(
        result,
        expected,
        rtol=0.1,
        check_index_type=False,
    )


def test_arima_plus_detect_anomalies(
    time_series_arima_plus_model: forecasting.ARIMAPlus, new_time_series_df
):
    anomalies = time_series_arima_plus_model.detect_anomalies(
        new_time_series_df
    ).to_pandas()

    expected = pd.DataFrame(
        {
            "is_anomaly": [False, False, False],
            "lower_bound": [2349.301736, 2153.614829, 1849.040192],
            "upper_bound": [3099.642833, 3033.12195, 2858.185876],
            "anomaly_probability": [0.757824, 0.322559, 0.43011],
        },
    )
    pd.testing.assert_frame_equal(
        anomalies[["is_anomaly", "lower_bound", "upper_bound", "anomaly_probability"]],
        expected,
        rtol=0.1,
        check_index_type=False,
        check_dtype=False,
    )


def test_arima_plus_detect_anomalies_params(
    time_series_arima_plus_model: forecasting.ARIMAPlus, new_time_series_df
):
    anomalies = time_series_arima_plus_model.detect_anomalies(
        new_time_series_df, anomaly_prob_threshold=0.7
    ).to_pandas()

    expected = pd.DataFrame(
        {
            "is_anomaly": [True, False, False],
            "lower_bound": [2525.5363, 2360.1870, 2086.0609],
            "upper_bound": [2923.408256, 2826.54981, 2621.165188],
            "anomaly_probability": [0.757824, 0.322559, 0.43011],
        },
    )
    pd.testing.assert_frame_equal(
        anomalies[["is_anomaly", "lower_bound", "upper_bound", "anomaly_probability"]],
        expected,
        rtol=0.1,
        check_index_type=False,
        check_dtype=False,
    )


def test_arima_plus_score(
    time_series_arima_plus_model: forecasting.ARIMAPlus, new_time_series_df
):
    result = time_series_arima_plus_model.score(
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
    pd.testing.assert_frame_equal(
        result,
        expected,
        rtol=0.1,
        check_index_type=False,
    )


def test_arima_plus_summary(time_series_arima_plus_model: forecasting.ARIMAPlus):
    result = time_series_arima_plus_model.summary()
    assert result.shape == (1, 12)
    assert all(column in result.columns for column in ARIMA_EVALUATE_OUTPUT_COL)


def test_arima_plus_summary_show_all_candidates(
    time_series_arima_plus_model: forecasting.ARIMAPlus,
):
    result = time_series_arima_plus_model.summary(
        show_all_candidate_models=True,
    )
    assert result.shape[0] > 1
    assert all(column in result.columns for column in ARIMA_EVALUATE_OUTPUT_COL)


def test_arima_plus_score_series(
    time_series_arima_plus_model: forecasting.ARIMAPlus, new_time_series_df
):
    result = time_series_arima_plus_model.score(
        new_time_series_df["parsed_date"], new_time_series_df["total_visits"]
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
    pd.testing.assert_frame_equal(
        result,
        expected,
        rtol=0.1,
        check_index_type=False,
    )


def test_arima_plus_summary_series(time_series_arima_plus_model: forecasting.ARIMAPlus):
    result = time_series_arima_plus_model.summary()
    assert result.shape == (1, 12)
    assert all(column in result.columns for column in ARIMA_EVALUATE_OUTPUT_COL)
