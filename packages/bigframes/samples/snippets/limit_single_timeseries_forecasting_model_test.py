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


def test_limit_single_timeseries(random_model_id: str) -> None:
    your_model_id = random_model_id

    # [START bigquery_dataframes_bqml_limit_forecast_visualize]
    import bigframes.pandas as bpd

    df = bpd.read_gbq("bigquery-public-data.new_york.citibike_trips")

    features = bpd.DataFrame(
        {
            "num_trips": df.starttime,
            "date": df["starttime"].dt.date,
        }
    )
    num_trips = features.groupby(["date"]).count()

    num_trips.plot.line()
    # [END bigquery_dataframes_bqml_limit_forecast_visualize]

    # [START bigquery_dataframes_bqml_limit_forecast_create]
    from bigframes.ml import forecasting
    import bigframes.pandas as bpd

    df = bpd.read_gbq("bigquery-public-data.new_york.citibike_trips")

    features = bpd.DataFrame(
        {
            "start_station_id": df["start_station_id"],
            "num_trips": df.starttime,
            "date": df["starttime"].dt.date,
        }
    )
    num_trips = features.groupby(["date", "start_station_id"], as_index=False).count()
    model = forecasting.ARIMAPlus()

    X = num_trips[["date"]]
    y = num_trips[["num_trips"]]
    id_col = num_trips[["start_station_id"]]

    model.fit(X, y, id_col=id_col)

    model.to_gbq(
        your_model_id,  # For example: "bqml_tutorial.nyc_citibike_arima_model",
        replace=True,
    )
    # [END bigquery_dataframes_bqml_limit_forecast_create]
    assert df is not None
    assert features is not None
    assert num_trips is not None
