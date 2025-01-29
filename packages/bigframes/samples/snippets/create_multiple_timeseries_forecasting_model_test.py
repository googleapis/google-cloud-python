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

    df = bpd.read_gbq("bigquery-public-data.new_york.citibike_trips")

    features = bpd.DataFrame(
        {
            "num_trips": df.starttime,
            "date": df["starttime"].dt.date,
        }
    )
    num_trips = features.groupby(["date"], as_index=False).count()
    model = forecasting.ARIMAPlus()

    X = num_trips["date"].to_frame()
    y = num_trips["num_trips"].to_frame()

    model.fit(X, y)
    # The model.fit() call above created a temporary model.
    # Use the to_gbq() method to write to a permanent location.

    model.to_gbq(
        your_model_id,  # For example: "bqml_tutorial.nyc_citibike_arima_model",
        replace=True,
    )
    # [END bigquery_dataframes_bqml_arima_multiple_step_3_fit]
