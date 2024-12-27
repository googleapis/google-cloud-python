# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (t
# you may not use this file except in compliance wi
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in
# distributed under the License is distributed on a
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, eit
# See the License for the specific language governi
# limitations under the License.


def test_create_single_timeseries() -> None:
    # [START bigquery_dataframes_single_timeseries_forecasting_model_tutorial]
    import bigframes.pandas as bpd

    # Start by loading the historical data from BigQuerythat you want to analyze and forecast.
    # This clause indicates that you are querying the ga_sessions_* tables in the google_analytics_sample dataset.
    # Read and visualize the time series you want to forecast.
    df = bpd.read_gbq("bigquery-public-data.google_analytics_sample.ga_sessions_*")
    parsed_date = bpd.to_datetime(df.date, format="%Y%m%d", utc=True)
    parsed_date.name = "parsed_date"
    visits = df["totals"].struct.field("visits")
    visits.name = "total_visits"
    total_visits = visits.groupby(parsed_date).sum()

    # Expected output: total_visits.head()
    # parsed_date
    # 2016-08-01 00:00:00+00:00    1711
    # 2016-08-02 00:00:00+00:00    2140
    # 2016-08-03 00:00:00+00:00    2890
    # 2016-08-04 00:00:00+00:00    3161
    # 2016-08-05 00:00:00+00:00    2702
    # Name: total_visits, dtype: Int64

    total_visits.plot.line()

    # [END bigquery_dataframes_single_timeseries_forecasting_model_tutorial]

    # [START bigquery_dataframes_single_timeseries_forecasting_model_tutorial_create]
    from bigframes.ml import forecasting
    import bigframes.pandas as bpd

    # Create a time series model to forecast total site visits:
    # The auto_arima option defaults to True, so the auto.ARIMA algorithm automatically
    # tunes the hyperparameters in the model.
    # The data_frequency option defaults to 'auto_frequency so the training
    # process automatically infers the data frequency of the input time series.
    # The decompose_time_series option defaults to True, so that information about
    # the time series data is returned when you evaluate the model in the next step.
    model = forecasting.ARIMAPlus()
    model.auto_arima = True
    model.data_frequency = "auto_frequency"
    model.decompose_time_series = True

    # Use the data loaded in the previous step to fit the model
    training_data = total_visits.to_frame().reset_index(drop=False)

    X = training_data[["parsed_date"]]
    y = training_data[["total_visits"]]

    model.fit(X, y)
    # [END bigquery_dataframes_single_timeseries_forecasting_model_tutorial_create]
    assert model is not None
    assert parsed_date is not None
    assert total_visits is not None
