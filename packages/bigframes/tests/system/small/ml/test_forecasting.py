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
import pytest
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


@pytest.mark.parametrize("id_col_name", [None, "id"])
def test_arima_plus_predict_default(
    time_series_arima_plus_model: forecasting.ARIMAPlus,
    time_series_arima_plus_model_w_id: forecasting.ARIMAPlus,
    id_col_name,
):
    utc = pytz.utc
    predictions = (
        (
            time_series_arima_plus_model_w_id
            if id_col_name
            else time_series_arima_plus_model
        )
        .predict()
        .to_pandas()
    )
    assert predictions.shape == ((6, 9) if id_col_name else (3, 8))
    result = predictions[["forecast_timestamp", "forecast_value"]]
    if id_col_name:
        result["id"] = predictions[["id"]]
        result = result[["id", "forecast_timestamp", "forecast_value"]]

    if id_col_name:
        expected = pd.DataFrame(
            {
                "id": ["1", "2", "1", "2", "1", "2"],
                "forecast_timestamp": [
                    datetime(2017, 8, 2, tzinfo=utc),
                    datetime(2017, 8, 2, tzinfo=utc),
                    datetime(2017, 8, 3, tzinfo=utc),
                    datetime(2017, 8, 3, tzinfo=utc),
                    datetime(2017, 8, 4, tzinfo=utc),
                    datetime(2017, 8, 4, tzinfo=utc),
                ],
                "forecast_value": [
                    2634.796023,
                    2634.796023,
                    2621.332461,
                    2621.332461,
                    2396.095462,
                    2396.095462,
                ],
            }
        )
        expected["id"] = expected["id"].astype("string[pyarrow]")
    else:
        expected = pd.DataFrame(
            {
                "forecast_timestamp": [
                    datetime(2017, 8, 2, tzinfo=utc),
                    datetime(2017, 8, 3, tzinfo=utc),
                    datetime(2017, 8, 4, tzinfo=utc),
                ],
                "forecast_value": [
                    2634.796023,
                    2621.332461,
                    2396.095462,
                ],
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


@pytest.mark.parametrize("id_col_name", [None, "id"])
def test_arima_plus_predict_explain_default(
    time_series_arima_plus_model: forecasting.ARIMAPlus,
    time_series_arima_plus_model_w_id: forecasting.ARIMAPlus,
    id_col_name,
):
    utc = pytz.utc
    predictions = (
        (
            time_series_arima_plus_model_w_id
            if id_col_name
            else time_series_arima_plus_model
        )
        .predict_explain()
        .to_pandas()
    )
    assert predictions.shape[0] == (738 if id_col_name else 369)
    predictions = predictions[
        predictions["time_series_type"] == "forecast"
    ].reset_index(drop=True)
    assert predictions.shape[0] == (6 if id_col_name else 3)
    result = predictions[["time_series_timestamp", "time_series_data"]]
    if id_col_name:
        result["id"] = predictions[["id"]]
        result = result[["id", "time_series_timestamp", "time_series_data"]]
    if id_col_name:
        expected = pd.DataFrame(
            {
                "id": ["1", "2", "1", "2", "1", "2"],
                "time_series_timestamp": [
                    datetime(2017, 8, 2, tzinfo=utc),
                    datetime(2017, 8, 2, tzinfo=utc),
                    datetime(2017, 8, 3, tzinfo=utc),
                    datetime(2017, 8, 3, tzinfo=utc),
                    datetime(2017, 8, 4, tzinfo=utc),
                    datetime(2017, 8, 4, tzinfo=utc),
                ],
                "time_series_data": [
                    2634.796023,
                    2634.796023,
                    2621.332461,
                    2621.332461,
                    2396.095462,
                    2396.095462,
                ],
            }
        )
        expected["id"] = expected["id"].astype("string[pyarrow]")
    else:
        expected = pd.DataFrame(
            {
                "time_series_timestamp": [
                    datetime(2017, 8, 2, tzinfo=utc),
                    datetime(2017, 8, 3, tzinfo=utc),
                    datetime(2017, 8, 4, tzinfo=utc),
                ],
                "time_series_data": [
                    2634.796023,
                    2621.332461,
                    2396.095462,
                ],
            }
        )
    expected["time_series_data"] = expected["time_series_data"].astype(
        pd.Float64Dtype()
    )
    expected["time_series_timestamp"] = expected["time_series_timestamp"].astype(
        pd.ArrowDtype(pa.timestamp("us", tz="UTC"))
    )

    pd.testing.assert_frame_equal(
        result,
        expected,
        rtol=0.1,
        check_index_type=False,
    )


@pytest.mark.parametrize("id_col_name", [None, "id"])
def test_arima_plus_predict_params(
    time_series_arima_plus_model: forecasting.ARIMAPlus,
    time_series_arima_plus_model_w_id: forecasting.ARIMAPlus,
    id_col_name,
):
    utc = pytz.utc
    predictions = (
        (
            time_series_arima_plus_model_w_id
            if id_col_name
            else time_series_arima_plus_model
        )
        .predict(horizon=4, confidence_level=0.9)
        .to_pandas()
    )
    assert predictions.shape == ((8, 9) if id_col_name else (4, 8))
    result = predictions[["forecast_timestamp", "forecast_value"]]
    if id_col_name:
        result["id"] = predictions[["id"]]
        result = result[["id", "forecast_timestamp", "forecast_value"]]

    if id_col_name:
        expected = pd.DataFrame(
            {
                "id": ["1", "2", "1", "2", "1", "2", "1", "2"],
                "forecast_timestamp": [
                    datetime(2017, 8, 2, tzinfo=utc),
                    datetime(2017, 8, 2, tzinfo=utc),
                    datetime(2017, 8, 3, tzinfo=utc),
                    datetime(2017, 8, 3, tzinfo=utc),
                    datetime(2017, 8, 4, tzinfo=utc),
                    datetime(2017, 8, 4, tzinfo=utc),
                    datetime(2017, 8, 5, tzinfo=utc),
                    datetime(2017, 8, 5, tzinfo=utc),
                ],
                "forecast_value": [
                    2634.796023,
                    2634.796023,
                    2621.332461,
                    2621.332461,
                    2396.095462,
                    2396.095462,
                    1781.623071,
                    1781.623071,
                ],
            }
        )
        expected["id"] = expected["id"].astype("string[pyarrow]")
    else:
        expected = pd.DataFrame(
            {
                "forecast_timestamp": [
                    datetime(2017, 8, 2, tzinfo=utc),
                    datetime(2017, 8, 3, tzinfo=utc),
                    datetime(2017, 8, 4, tzinfo=utc),
                    datetime(2017, 8, 5, tzinfo=utc),
                ],
                "forecast_value": [
                    2634.796023,
                    2621.332461,
                    2396.095462,
                    1781.623071,
                ],
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


@pytest.mark.parametrize("id_col_name", [None, "id"])
def test_arima_plus_predict_explain_params(
    time_series_arima_plus_model: forecasting.ARIMAPlus,
    time_series_arima_plus_model_w_id: forecasting.ARIMAPlus,
    id_col_name,
):
    predictions = (
        (
            time_series_arima_plus_model_w_id
            if id_col_name
            else time_series_arima_plus_model
        )
        .predict_explain(horizon=4, confidence_level=0.9)
        .to_pandas()
    )
    assert predictions.shape[0] >= 1
    prediction_columns = set(predictions.columns)
    expected_columns = {
        "time_series_timestamp",
        "time_series_type",
        "time_series_data",
        "time_series_adjusted_data",
        "standard_error",
        "confidence_level",
        "prediction_interval_lower_bound",
        "trend",
        "seasonal_period_yearly",
        "seasonal_period_quarterly",
        "seasonal_period_monthly",
        "seasonal_period_weekly",
        "seasonal_period_daily",
        "holiday_effect",
    }
    if id_col_name:
        expected_columns.add("id")
    assert expected_columns <= prediction_columns


@pytest.mark.parametrize("id_col_name", [None, "id"])
def test_arima_plus_detect_anomalies(
    time_series_arima_plus_model: forecasting.ARIMAPlus,
    time_series_arima_plus_model_w_id: forecasting.ARIMAPlus,
    new_time_series_df,
    new_time_series_df_w_id,
    id_col_name,
):
    anomalies = (
        (
            time_series_arima_plus_model_w_id
            if id_col_name
            else time_series_arima_plus_model
        )
        .detect_anomalies(
            new_time_series_df_w_id if id_col_name else new_time_series_df
        )
        .to_pandas()
    )

    if id_col_name:
        expected = pd.DataFrame(
            {
                "is_anomaly": [False, False, False, False, False, False],
                "lower_bound": [
                    2229.930578,
                    2229.930578,
                    2149.645455,
                    2149.645455,
                    1892.873256,
                    1892.873256,
                ],
                "upper_bound": [
                    3039.6614686,
                    3039.6614686,
                    3093.019467,
                    3093.019467,
                    2899.317669,
                    2899.317669,
                ],
                "anomaly_probability": [
                    0.48545926,
                    0.48545926,
                    0.3856835,
                    0.3856835,
                    0.314156,
                    0.314156,
                ],
            },
        )
    else:
        expected = pd.DataFrame(
            {
                "is_anomaly": [False, False, False],
                "lower_bound": [2229.930578, 2149.645455, 1892.873256],
                "upper_bound": [3039.6614686, 3093.019467, 2899.317669],
                "anomaly_probability": [0.48545926, 0.3856835, 0.314156],
            },
        )
    pd.testing.assert_frame_equal(
        anomalies[["is_anomaly", "lower_bound", "upper_bound", "anomaly_probability"]],
        expected,
        rtol=0.1,
        check_index_type=False,
        check_dtype=False,
    )


@pytest.mark.parametrize("id_col_name", [None, "id"])
def test_arima_plus_detect_anomalies_params(
    time_series_arima_plus_model: forecasting.ARIMAPlus,
    time_series_arima_plus_model_w_id: forecasting.ARIMAPlus,
    new_time_series_df,
    new_time_series_df_w_id,
    id_col_name,
):
    anomalies = (
        (
            time_series_arima_plus_model_w_id
            if id_col_name
            else time_series_arima_plus_model
        )
        .detect_anomalies(
            new_time_series_df_w_id if id_col_name else new_time_series_df,
            anomaly_prob_threshold=0.7,
        )
        .to_pandas()
    )
    if id_col_name:
        expected = pd.DataFrame(
            {
                "is_anomaly": [False, False, False, False, False, False],
                "lower_bound": [
                    2420.11419,
                    2420.11419,
                    2360.1870,
                    2360.1870,
                    2086.0609,
                    2086.0609,
                ],
                "upper_bound": [
                    2849.47785,
                    2849.47785,
                    2826.54981,
                    2826.54981,
                    2621.165188,
                    2621.165188,
                ],
                "anomaly_probability": [
                    0.485459,
                    0.485459,
                    0.385683,
                    0.385683,
                    0.314156,
                    0.314156,
                ],
            },
        )
    else:
        expected = pd.DataFrame(
            {
                "is_anomaly": [False, False, False],
                "lower_bound": [2420.11419, 2360.1870, 2086.0609],
                "upper_bound": [2849.47785, 2826.54981, 2621.165188],
                "anomaly_probability": [0.485459, 0.385683, 0.314156],
            },
        )
    pd.testing.assert_frame_equal(
        anomalies[["is_anomaly", "lower_bound", "upper_bound", "anomaly_probability"]],
        expected,
        rtol=0.1,
        check_index_type=False,
        check_dtype=False,
    )


@pytest.mark.parametrize("id_col_name", [None, "id"])
def test_arima_plus_score(
    time_series_arima_plus_model: forecasting.ARIMAPlus,
    time_series_arima_plus_model_w_id: forecasting.ARIMAPlus,
    new_time_series_df,
    new_time_series_df_w_id,
    id_col_name,
):
    if id_col_name:
        result = time_series_arima_plus_model_w_id.score(
            new_time_series_df_w_id[["parsed_date"]],
            new_time_series_df_w_id[["total_visits"]],
            new_time_series_df_w_id[["id"]],
        ).to_pandas()
    else:
        result = time_series_arima_plus_model.score(
            new_time_series_df[["parsed_date"]], new_time_series_df[["total_visits"]]
        ).to_pandas()
    if id_col_name:
        expected = pd.DataFrame(
            {
                "id": ["2", "1"],
                "mean_absolute_error": [120.011007, 120.011007],
                "mean_squared_error": [14562.562359, 14562.562359],
                "root_mean_squared_error": [120.675442, 120.675442],
                "mean_absolute_percentage_error": [4.80044, 4.80044],
                "symmetric_mean_absolute_percentage_error": [4.744332, 4.744332],
            },
            dtype="Float64",
        )
        expected["id"] = expected["id"].astype(str).str.replace(r"\.0$", "", regex=True)
        expected["id"] = expected["id"].astype("string[pyarrow]")
    else:
        expected = pd.DataFrame(
            {
                "mean_absolute_error": [120.0110074],
                "mean_squared_error": [14562.5623594],
                "root_mean_squared_error": [120.675442],
                "mean_absolute_percentage_error": [4.80044],
                "symmetric_mean_absolute_percentage_error": [4.744332],
            },
            dtype="Float64",
        )
    pd.testing.assert_frame_equal(
        result,
        expected,
        rtol=0.1,
        check_index_type=False,
    )


@pytest.mark.parametrize("id_col_name", [None, "id"])
def test_arima_plus_summary(
    time_series_arima_plus_model: forecasting.ARIMAPlus,
    time_series_arima_plus_model_w_id: forecasting.ARIMAPlus,
    id_col_name,
):
    result = (
        time_series_arima_plus_model_w_id
        if id_col_name
        else time_series_arima_plus_model
    ).summary()
    assert result.shape == ((2, 13) if id_col_name else (1, 12))
    expected_columns = (
        [id_col_name] + ARIMA_EVALUATE_OUTPUT_COL
        if id_col_name
        else ARIMA_EVALUATE_OUTPUT_COL
    )
    assert all(column in result.columns for column in expected_columns)


@pytest.mark.parametrize("id_col_name", [None, "id"])
def test_arima_plus_summary_show_all_candidates(
    time_series_arima_plus_model: forecasting.ARIMAPlus,
    time_series_arima_plus_model_w_id: forecasting.ARIMAPlus,
    id_col_name,
):
    result = (
        time_series_arima_plus_model_w_id
        if id_col_name
        else time_series_arima_plus_model
    ).summary(
        show_all_candidate_models=True,
    )
    assert result.shape[0] > 1
    expected_columns = (
        [id_col_name] + ARIMA_EVALUATE_OUTPUT_COL
        if id_col_name
        else ARIMA_EVALUATE_OUTPUT_COL
    )
    assert all(column in result.columns for column in expected_columns)


@pytest.mark.parametrize("id_col_name", [None, "id"])
def test_arima_plus_score_series(
    time_series_arima_plus_model: forecasting.ARIMAPlus,
    time_series_arima_plus_model_w_id: forecasting.ARIMAPlus,
    new_time_series_df,
    new_time_series_df_w_id,
    id_col_name,
):
    if id_col_name:
        result = time_series_arima_plus_model_w_id.score(
            new_time_series_df_w_id["parsed_date"],
            new_time_series_df_w_id["total_visits"],
            new_time_series_df_w_id["id"],
        ).to_pandas()
    else:
        result = time_series_arima_plus_model.score(
            new_time_series_df["parsed_date"], new_time_series_df["total_visits"]
        ).to_pandas()
    if id_col_name:
        expected = pd.DataFrame(
            {
                "id": ["2", "1"],
                "mean_absolute_error": [120.011007, 120.011007],
                "mean_squared_error": [14562.562359, 14562.562359],
                "root_mean_squared_error": [120.675442, 120.675442],
                "mean_absolute_percentage_error": [4.80044, 4.80044],
                "symmetric_mean_absolute_percentage_error": [4.744332, 4.744332],
            },
            dtype="Float64",
        )
        expected["id"] = expected["id"].astype(str).str.replace(r"\.0$", "", regex=True)
        expected["id"] = expected["id"].astype("string[pyarrow]")
    else:
        expected = pd.DataFrame(
            {
                "mean_absolute_error": [120.0110074],
                "mean_squared_error": [14562.5623594],
                "root_mean_squared_error": [120.675442],
                "mean_absolute_percentage_error": [4.80044],
                "symmetric_mean_absolute_percentage_error": [4.744332],
            },
            dtype="Float64",
        )
    pd.testing.assert_frame_equal(
        result,
        expected,
        rtol=0.1,
        check_index_type=False,
    )


@pytest.mark.parametrize("id_col_name", [None, "id"])
def test_arima_plus_summary_series(
    time_series_arima_plus_model: forecasting.ARIMAPlus,
    time_series_arima_plus_model_w_id: forecasting.ARIMAPlus,
    id_col_name,
):
    result = (
        time_series_arima_plus_model_w_id
        if id_col_name
        else time_series_arima_plus_model
    ).summary()
    assert result.shape == ((2, 13) if id_col_name else (1, 12))
    expected_columns = (
        [id_col_name] + ARIMA_EVALUATE_OUTPUT_COL
        if id_col_name
        else ARIMA_EVALUATE_OUTPUT_COL
    )
    assert all(column in result.columns for column in expected_columns)
