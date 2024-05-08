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
    visits = df["totals"].struct.field("visits")
    total_visits = visits.groupby(parsed_date).sum()

    # Expected output: total_visits.head()
    # date
    # 2016-08-01 00:00:00+00:00    1711
    # 2016-08-02 00:00:00+00:00    2140
    # 2016-08-03 00:00:00+00:00    2890
    # 2016-08-04 00:00:00+00:00    3161
    # 2016-08-05 00:00:00+00:00    2702
    # Name: visits, dtype: Int64

    total_visits.plot.line()

    # [END bigquery_dataframes_single_timeseries_forecasting_model_tutorial]
