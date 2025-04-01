# Copyright 2024 Google LLC
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


def test_multiple_timeseries_forecasting_model(random_model_id: str) -> None:
    your_model_id = random_model_id

    # [START bigquery_dataframes_bqml_arima_multiple_step_2_visualize]

    import bigframes.pandas as bpd

    df = bpd.read_gbq("bigquery-public-data.new_york.citibike_trips")

    features = bpd.DataFrame(
        {
            "num_trips": df.starttime,
            "date": df["starttime"].dt.date,
        }
    )
    date = df["starttime"].dt.date
    df.groupby([date])
    num_trips = features.groupby(["date"]).count()

    # Results from running "print(num_trips)"

    #                num_trips
    # date
    # 2013-07-01      16650
    # 2013-07-02      22745
    # 2013-07-03      21864
    # 2013-07-04      22326
    # 2013-07-05      21842
    # 2013-07-06      20467
    # 2013-07-07      20477
    # 2013-07-08      21615
    # 2013-07-09      26641
    # 2013-07-10      25732
    # 2013-07-11      24417
    # 2013-07-12      19006
    # 2013-07-13      26119
    # 2013-07-14      29287
    # 2013-07-15      28069
    # 2013-07-16      29842
    # 2013-07-17      30550
    # 2013-07-18      28869
    # 2013-07-19      26591
    # 2013-07-20      25278
    # 2013-07-21      30297
    # 2013-07-22      25979
    # 2013-07-23      32376
    # 2013-07-24      35271
    # 2013-07-25      31084

    num_trips.plot.line(
        # Rotate the x labels so they are more visible.
        rot=45,
    )

    # [END bigquery_dataframes_bqml_arima_multiple_step_2_visualize]

    # [START bigquery_dataframes_bqml_arima_multiple_step_3_fit]
    from bigframes.ml import forecasting
    import bigframes.pandas as bpd

    model = forecasting.ARIMAPlus(
        # To reduce the query runtime with the compromise of a potential slight
        # drop in model quality, you could decrease the value of the
        # auto_arima_max_order. This shrinks the search space of hyperparameter
        # tuning in the auto.ARIMA algorithm.
        auto_arima_max_order=5,
    )

    df = bpd.read_gbq("bigquery-public-data.new_york.citibike_trips")

    # This query creates twelve time series models, one for each of the twelve
    # Citi Bike start stations in the input data. If you remove this row
    # filter, there would be 600+ time series to forecast.
    df = df[df["start_station_name"].str.contains("Central Park")]

    features = bpd.DataFrame(
        {
            "start_station_name": df["start_station_name"],
            "num_trips": df["starttime"],
            "date": df["starttime"].dt.date,
        }
    )
    num_trips = features.groupby(
        ["start_station_name", "date"],
        as_index=False,
    ).count()

    X = num_trips["date"].to_frame()
    y = num_trips["num_trips"].to_frame()

    model.fit(
        X,
        y,
        # The input data that you want to get forecasts for,
        # in this case the Citi Bike station, as represented by the
        # start_station_name column.
        id_col=num_trips["start_station_name"].to_frame(),
    )

    # The model.fit() call above created a temporary model.
    # Use the to_gbq() method to write to a permanent location.
    model.to_gbq(
        your_model_id,  # For example: "bqml_tutorial.nyc_citibike_arima_model",
        replace=True,
    )
    # [END bigquery_dataframes_bqml_arima_multiple_step_3_fit]

    # [START bigquery_dataframes_bqml_arima_multiple_step_4_evaluate]
    # Evaluate the time series models by using the summary() function. The summary()
    # function shows you the evaluation metrics of all the candidate models evaluated
    # during the process of automatic hyperparameter tuning.
    summary = model.summary()
    print(summary.peek())

    # Expected output:
    #    start_station_name                  non_seasonal_p  non_seasonal_d   non_seasonal_q  has_drift  log_likelihood           AIC     variance ...
    # 1         Central Park West & W 72 St               0               1                5      False    -1966.449243   3944.898487  1215.689281 ...
    # 8            Central Park W & W 96 St               0               0                5      False     -274.459923    562.919847   655.776577 ...
    # 9        Central Park West & W 102 St               0               0                0      False     -226.639918    457.279835    258.83582 ...
    # 11        Central Park West & W 76 St               1               1                2      False    -1700.456924   3408.913848   383.254161 ...
    # 4   Grand Army Plaza & Central Park S               0               1                5      False    -5507.553498  11027.106996   624.138741 ...
    # [END bigquery_dataframes_bqml_arima_multiple_step_4_evaluate]

    # [START bigquery_dataframes_bqml_arima_multiple_step_5_coefficients]
    coef = model.coef_
    print(coef.peek())

    # Expected output:
    #    start_station_name                                              ar_coefficients                                   ma_coefficients intercept_or_drift
    # 5    Central Park West & W 68 St                                                [] [-0.41014089  0.21979212 -0.59854213 -0.251438...                0.0
    # 6         Central Park S & 6 Ave                                                [] [-0.71488957 -0.36835772  0.61008532  0.183290...                0.0
    # 0    Central Park West & W 85 St                                                [] [-0.39270166 -0.74494638  0.76432596  0.489146...                0.0
    # 3    W 82 St & Central Park West                         [-0.50219511 -0.64820817]             [-0.20665325  0.67683137 -0.68108631]                0.0
    # 11  W 106 St & Central Park West [-0.70442887 -0.66885553 -0.25030325 -0.34160669]                                                []                0.0
    # [END bigquery_dataframes_bqml_arima_multiple_step_5_coefficients]

    # [START bigquery_dataframes_bqml_arima_multiple_step_6_forecast]
    prediction = model.predict(horizon=3, confidence_level=0.9)

    print(prediction.peek())
    # Expected output:
    #            forecast_timestamp                             start_station_name  forecast_value  standard_error  confidence_level ...
    # 4   2016-10-01 00:00:00+00:00                         Central Park S & 6 Ave      302.377201       32.572948               0.9 ...
    # 14  2016-10-02 00:00:00+00:00  Central Park North & Adam Clayton Powell Blvd      263.917567       45.284082               0.9 ...
    # 1   2016-09-25 00:00:00+00:00                    Central Park West & W 85 St      189.574706       39.874856               0.9 ...
    # 20  2016-10-02 00:00:00+00:00                    Central Park West & W 72 St      175.474862       40.940794               0.9 ...
    # 12  2016-10-01 00:00:00+00:00                   W 106 St & Central Park West        63.88163       18.088868               0.9 ...
    # [END bigquery_dataframes_bqml_arima_multiple_step_6_forecast]
