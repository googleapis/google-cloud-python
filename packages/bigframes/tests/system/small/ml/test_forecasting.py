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


def test_model_predict(time_series_arima_plus_model):
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


def test_model_score(time_series_arima_plus_model, new_time_series_df):
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


def test_model_score_series(time_series_arima_plus_model, new_time_series_df):
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
