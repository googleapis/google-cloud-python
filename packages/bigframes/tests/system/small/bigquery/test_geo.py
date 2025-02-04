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

import geopandas  # type: ignore
import pandas as pd
from shapely.geometry import LineString, Point, Polygon  # type: ignore

import bigframes.bigquery as bbq
import bigframes.geopandas
import bigframes.series


def test_geo_st_area():
    data = [
        Polygon([(0.000, 0.0), (0.001, 0.001), (0.000, 0.001)]),
        Polygon([(0.0010, 0.004), (0.009, 0.005), (0.0010, 0.005)]),
        Polygon([(0.001, 0.001), (0.002, 0.001), (0.002, 0.002)]),
        LineString([(0, 0), (1, 1), (0, 1)]),
        Point(0, 1),
    ]

    geopd_s = geopandas.GeoSeries(data=data, crs="EPSG:4326")
    geobf_s = bigframes.geopandas.GeoSeries(data=data)

    # For `geopd_s`, the data was further projected with `geopandas.GeoSeries.to_crs`
    # to `to_crs(26393)` to get the area in square meter. See: https://geopandas.org/en/stable/docs/user_guide/projections.html
    # and https://spatialreference.org/ref/epsg/26393/. We then rounded both results
    # to get them as close to each other as possible. Initially, the area results
    # were +ten-millions. We added more zeros after the decimal point to round the
    # area results to the nearest thousands.
    geopd_s_result = geopd_s.to_crs(26393).area.round(-3)
    geobf_s_result = bbq.st_area(geobf_s).to_pandas().round(-3)
    assert geobf_s_result.iloc[0] >= 1000

    pd.testing.assert_series_equal(
        geobf_s_result,
        geopd_s_result,
        check_dtype=False,
        check_index_type=False,
        check_exact=False,
        rtol=1,
    )
