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


def test_kmeans_sample(project_id: str, random_model_id_eu: str) -> None:
    your_gcp_project_id = project_id
    your_model_id = random_model_id_eu
    # [START bigquery_dataframes_bqml_kmeans]
    import datetime

    import pandas as pd

    import bigframes
    import bigframes.pandas as bpd

    bigframes.options.bigquery.project = your_gcp_project_id
    # Compute in the EU multi-region to query the London bicycles dataset.
    bigframes.options.bigquery.location = "EU"

    # Extract the information you'll need to train the k-means model in this
    # tutorial. Use the read_gbq function to represent cycle hires
    # data as a DataFrame.
    h = bpd.read_gbq(
        "bigquery-public-data.london_bicycles.cycle_hire",
        col_order=["start_station_name", "start_station_id", "start_date", "duration"],
    ).rename(
        columns={
            "start_station_name": "station_name",
            "start_station_id": "station_id",
        }
    )

    s = bpd.read_gbq(
        # Use ST_GEOPOINT and ST_DISTANCE to analyze geographical
        # data. These functions determine spatial relationships between
        # geographical features.
        """
        SELECT
        id,
        ST_DISTANCE(
            ST_GEOGPOINT(s.longitude, s.latitude),
            ST_GEOGPOINT(-0.1, 51.5)
        ) / 1000 AS distance_from_city_center
        FROM
        `bigquery-public-data.london_bicycles.cycle_stations` s
        """
    )

    # Define Python datetime objects in the UTC timezone for range comparison,
    # because BigQuery stores timestamp data in the UTC timezone.
    sample_time = datetime.datetime(2015, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
    sample_time2 = datetime.datetime(2016, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)

    h = h.loc[(h["start_date"] >= sample_time) & (h["start_date"] <= sample_time2)]

    # Replace each day-of-the-week number with the corresponding "weekday" or
    # "weekend" label by using the Series.map method.
    h = h.assign(
        isweekday=h.start_date.dt.dayofweek.map(
            {
                0: "weekday",
                1: "weekday",
                2: "weekday",
                3: "weekday",
                4: "weekday",
                5: "weekend",
                6: "weekend",
            }
        )
    )

    # Supplement each trip in "h" with the station distance information from
    # "s" by merging the two DataFrames by station ID.
    merged_df = h.merge(
        right=s,
        how="inner",
        left_on="station_id",
        right_on="id",
    )

    # Engineer features to cluster the stations. For each station, find the
    # average trip duration, number of trips, and distance from city center.
    stationstats = merged_df.groupby(["station_name", "isweekday"]).agg(
        {"duration": ["mean", "count"], "distance_from_city_center": "max"}
    )
    stationstats.columns = pd.Index(
        ["duration", "num_trips", "distance_from_city_center"]
    )
    stationstats = stationstats.sort_values(
        by="distance_from_city_center", ascending=True
    ).reset_index()

    # Expected output results: >>> stationstats.head(3)
    # station_name	isweekday duration  num_trips	distance_from_city_center
    # Borough Road...	weekday	    1110	    5749	    0.12624
    # Borough Road...	weekend	    2125	    1774	    0.12624
    # Webber Street...	weekday	    795	        6517	    0.164021
    #   3 rows × 5 columns

    # [END bigquery_dataframes_bqml_kmeans]

    # [START bigquery_dataframes_bqml_kmeans_fit]

    from bigframes.ml.cluster import KMeans

    # To determine an optimal number of clusters, construct and fit several
    # K-Means objects with different values of num_clusters, find the error
    # measure, and pick the point at which the error measure is at its minimum
    # value.
    cluster_model = KMeans(n_clusters=4)
    cluster_model.fit(stationstats)
    cluster_model.to_gbq(
        your_model_id,  # For example: "bqml_tutorial.london_station_clusters"
        replace=True,
    )
    # [END bigquery_dataframes_bqml_kmeans_fit]

    # [START bigquery_dataframes_bqml_kmeans_predict]

    # Select model you'll use for predictions. `read_gbq_model` loads model
    # data from BigQuery, but you could also use the `cluster_model` object
    # from previous steps.
    cluster_model = bpd.read_gbq_model(
        your_model_id,
        # For example: "bqml_tutorial.london_station_clusters",
    )

    # Use 'contains' function to filter by stations containing the string
    # "Kennington".
    stationstats = stationstats.loc[
        stationstats["station_name"].str.contains("Kennington")
    ]

    result = cluster_model.predict(stationstats)

    # Expected output results:   >>>results.peek(3)
    # CENTROID...	NEAREST...	station_name  isweekday	 duration num_trips dist...
    # 	1	[{'CENTROID_ID'...	Borough...	  weekday	  1110	    5749	0.13
    # 	2	[{'CENTROID_ID'...	Borough...	  weekend	  2125      1774	0.13
    # 	1	[{'CENTROID_ID'...	Webber...	  weekday	  795	    6517	0.16
    #   3 rows × 7 columns

    # [END bigquery_dataframes_bqml_kmeans_predict]

    assert result is not None
