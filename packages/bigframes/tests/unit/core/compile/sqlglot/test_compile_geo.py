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

import pytest

import bigframes.bigquery as bbq
import bigframes.geopandas as gpd

pytest.importorskip("pytest_snapshot")


def test_st_regionstats(compiler_session, snapshot):
    geos = gpd.GeoSeries(["POINT(1 1)"], session=compiler_session)
    result = bbq.st_regionstats(
        geos,
        "ee://some/raster/uri",
        band="band1",
        include="some equation",
        options={"scale": 100},
    )
    assert "area" in result.struct.dtypes.index
    snapshot.assert_match(result.struct.explode().sql, "out.sql")


def test_st_regionstats_without_optional_args(compiler_session, snapshot):
    geos = gpd.GeoSeries(["POINT(1 1)"], session=compiler_session)
    result = bbq.st_regionstats(
        geos,
        "ee://some/raster/uri",
    )
    assert "area" in result.struct.dtypes.index
    snapshot.assert_match(result.struct.explode().sql, "out.sql")


def test_st_simplify(compiler_session, snapshot):
    geos = gpd.GeoSeries(["POINT(1 1)"], session=compiler_session)
    result = bbq.st_simplify(
        geos,
        tolerance_meters=123.125,
    )
    snapshot.assert_match(result.to_frame().sql, "out.sql")
