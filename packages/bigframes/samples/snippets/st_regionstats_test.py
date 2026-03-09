# Copyright 2025 Google LLC
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

"""Code sample for https://docs.cloud.google.com/bigquery/docs/raster-data#analytics-hub-source"""


def test_st_regionstats() -> None:
    project_id = "bigframes-dev"

    # [START bigquery_dataframes_st_regionstats]
    import datetime
    from typing import cast

    import bigframes.bigquery as bbq
    import bigframes.pandas as bpd

    # TODO: Set the project_id to your Google Cloud project ID.
    # project_id = "your-project-id"
    bpd.options.bigquery.project = project_id

    # TODO: Set the dataset_id to the ID of the dataset that contains the
    # `climate` table. This is likely a linked dataset to Earth Engine.
    # See: https://cloud.google.com/bigquery/docs/link-earth-engine
    linked_dataset = "era5_land_daily_aggregated"

    # For the best efficiency, use partial ordering mode.
    bpd.options.bigquery.ordering_mode = "partial"

    # Load the table of country boundaries.
    countries = bpd.read_gbq("bigquery-public-data.overture_maps.division_area")

    # Filter to just the countries.
    countries = countries[countries["subtype"] == "country"].copy()
    countries["name"] = countries["names"].struct.field("primary")
    countries["simplified_geometry"] = bbq.st_simplify(
        countries["geometry"],
        tolerance_meters=10_000,
    )

    # Get the reference to the temperature data from a linked dataset.
    # Note: This sample assumes you have a linked dataset to Earth Engine.
    image_href = (
        bpd.read_gbq(f"{project_id}.{linked_dataset}.climate")
        .set_index("start_datetime")
        .loc[[datetime.datetime(2025, 1, 1, tzinfo=datetime.timezone.utc)], :]
    )
    raster_id = image_href["assets"].struct.field("image").struct.field("href")
    raster_id = raster_id.item()
    stats = bbq.st_regionstats(
        countries["simplified_geometry"],
        raster_id=cast(str, raster_id),
        band="temperature_2m",
    )

    # Extract the mean and convert from Kelvin to Celsius.
    countries["mean_temperature"] = stats.struct.field("mean") - 273.15

    # Sort by the mean temperature to find the warmest countries.
    result = countries[["name", "mean_temperature"]].sort_values(
        "mean_temperature", ascending=False
    )
    print(result.head(10))
    # [END bigquery_dataframes_st_regionstats]

    assert len(result) > 0


if __name__ == "__main__":
    test_st_regionstats()
