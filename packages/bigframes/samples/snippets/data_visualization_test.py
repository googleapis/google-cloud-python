# Copyright 2025 Google LLC
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


def test_data_visualization() -> None:
    # [START bigquery_dataframes_data_visualization_penguin_histogram]
    import bigframes.pandas as bpd

    penguins = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")
    penguins["culmen_depth_mm"].plot.hist(bins=40)
    # [END bigquery_dataframes_data_visualization_penguin_histogram]

    # [START bigquery_dataframes_data_visualization_noaa_line_chart]
    import bigframes.pandas as bpd

    noaa_surface = bpd.read_gbq("bigquery-public-data.noaa_gsod.gsod2021")

    # Calculate median temperature for each day
    noaa_surface_median_temps = noaa_surface[["date", "temp"]].groupby("date").median()

    noaa_surface_median_temps.plot.line()
    # [END bigquery_dataframes_data_visualization_noaa_line_chart]

    # [START bigquery_dataframes_data_visualization_usa_names_area_chart]
    import bigframes.pandas as bpd

    usa_names = bpd.read_gbq("bigquery-public-data.usa_names.usa_1910_2013")

    # Count the occurences of the target names each year. The result is a dataframe with a multi-index.
    name_counts = (
        usa_names[usa_names["name"].isin(("Mary", "Emily", "Lisa"))]
        .groupby(("year", "name"))["number"]
        .sum()
    )

    # Flatten the index of the dataframe so that the counts for each name has their own columns.
    name_counts = name_counts.unstack(level=1).fillna(0)

    name_counts.plot.area(stacked=False, alpha=0.5)
    # [END bigquery_dataframes_data_visualization_usa_names_area_chart]

    # [START bigquery_dataframes_data_visualization_penguin_bar_chart]
    import bigframes.pandas as bpd

    penguins = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")

    penguin_count_by_sex = (
        penguins[penguins["sex"].isin(("MALE", "FEMALE"))]
        .groupby("sex")["species"]
        .count()
    )
    penguin_count_by_sex.plot.bar()
    # [END bigquery_dataframes_data_visualization_penguin_bar_chart]

    # [START bigquery_dataframes_data_visualization_taxi_scatter_plot]
    import bigframes.pandas as bpd

    taxi_trips = bpd.read_gbq(
        "bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2021"
    ).dropna()

    # Data Cleaning
    taxi_trips = taxi_trips[
        taxi_trips["trip_distance"].between(0, 10, inclusive="right")
    ]
    taxi_trips = taxi_trips[taxi_trips["fare_amount"].between(0, 50, inclusive="right")]

    # If you are using partial ordering mode, you will also need to assign an order to your dataset.
    # Otherwise, the next line can be skipped.
    taxi_trips = taxi_trips.sort_values("pickup_datetime")

    taxi_trips.plot.scatter(x="trip_distance", y="fare_amount", alpha=0.5)
    # [END bigquery_dataframes_data_visualization_taxi_scatter_plot]

    # [START bigquery_dataframes_data_visualization_noaa_sampling_n]
    import bigframes.pandas as bpd

    noaa_surface = bpd.read_gbq("bigquery-public-data.noaa_gsod.gsod2021")

    # Calculate median temperature for each day
    noaa_surface_median_temps = noaa_surface[["date", "temp"]].groupby("date").median()

    noaa_surface_median_temps.plot.line(sampling_n=40)
    # [END bigquery_dataframes_data_visualization_noaa_sampling_n]

    # [START bigquery_dataframes_data_visualization_usa_names_subplots]
    import bigframes.pandas as bpd

    usa_names = bpd.read_gbq("bigquery-public-data.usa_names.usa_1910_2013")

    # Count the occurences of the target names each year. The result is a dataframe with a multi-index.
    name_counts = (
        usa_names[usa_names["name"].isin(("Mary", "Emily", "Lisa"))]
        .groupby(("year", "name"))["number"]
        .sum()
    )

    # Flatten the index of the dataframe so that the counts for each name has their own columns.
    name_counts = name_counts.unstack(level=1).fillna(0)

    name_counts.plot.area(subplots=True, alpha=0.5)
    # [END bigquery_dataframes_data_visualization_usa_names_subplots]

    # [START bigquery_dataframes_data_visualization_taxi_scatter_multidimension]
    import bigframes.pandas as bpd

    taxi_trips = bpd.read_gbq(
        "bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2021"
    ).dropna()

    # Data Cleaning
    taxi_trips = taxi_trips[
        taxi_trips["trip_distance"].between(0, 10, inclusive="right")
    ]
    taxi_trips = taxi_trips[taxi_trips["fare_amount"].between(0, 50, inclusive="right")]

    # If you are using partial ordering mode, you also need to assign an order to your dataset.
    # Otherwise, the next line can be skipped.
    taxi_trips = taxi_trips.sort_values("pickup_datetime")

    taxi_trips["passenger_count_scaled"] = taxi_trips["passenger_count"] * 30

    taxi_trips.plot.scatter(
        x="trip_distance",
        xlabel="trip distance (miles)",
        y="fare_amount",
        ylabel="fare amount (usd)",
        alpha=0.5,
        s="passenger_count_scaled",
        label="passenger_count",
        c="tip_amount",
        cmap="jet",
        colorbar=True,
        legend=True,
        figsize=(15, 7),
        sampling_n=1000,
    )
    # [END bigquery_dataframes_data_visualization_taxi_scatter_multidimension]
