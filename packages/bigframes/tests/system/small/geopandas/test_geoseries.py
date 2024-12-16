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

import geopandas  # type: ignore
import google.api_core.exceptions
import pandas as pd
import pytest

import bigframes.geopandas
import bigframes.series
from tests.system.utils import assert_series_equal


@pytest.fixture(scope="session")
def urban_areas_dfs(session, urban_areas_table_id):
    bf_ua = session.read_gbq(urban_areas_table_id, index_col="geo_id")
    pd_ua = bf_ua.to_pandas()
    return (bf_ua, pd_ua)


def test_geo_x(urban_areas_dfs):
    bf_ua, pd_ua = urban_areas_dfs
    bf_series: bigframes.geopandas.GeoSeries = bf_ua["internal_point_geom"].geo
    pd_series: geopandas.GeoSeries = geopandas.GeoSeries(pd_ua["internal_point_geom"])
    bf_result = bf_series.x.to_pandas()
    pd_result = pd_series.x

    assert_series_equal(
        pd_result.astype(pd.Float64Dtype()),
        bf_result,
    )


def test_geo_x_non_point(urban_areas_dfs):
    bf_ua, _ = urban_areas_dfs
    bf_series: bigframes.geopandas.GeoSeries = bf_ua["urban_area_geom"].geo

    with pytest.raises(google.api_core.exceptions.BadRequest, match="ST_X"):
        bf_series.x.to_pandas()


def test_geo_y(urban_areas_dfs):
    bf_ua, pd_ua = urban_areas_dfs
    bf_series: bigframes.geopandas.GeoSeries = bf_ua["internal_point_geom"].geo
    pd_series: geopandas.GeoSeries = geopandas.GeoSeries(pd_ua["internal_point_geom"])
    bf_result = bf_series.y.to_pandas()
    pd_result = pd_series.y

    assert_series_equal(
        pd_result.astype(pd.Float64Dtype()),
        bf_result,
    )
