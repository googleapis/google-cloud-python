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

import re

import bigframes_vendored.constants as constants
import geopandas  # type: ignore
from geopandas.array import GeometryDtype  # type:ignore
import geopandas.testing  # type:ignore
import google.api_core.exceptions
import pandas as pd
import pytest
from shapely.geometry import (  # type: ignore
    GeometryCollection,
    LineString,
    Point,
    Polygon,
)

import bigframes.geopandas
import bigframes.pandas
import bigframes.series
from bigframes.testing.utils import assert_series_equal


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


def test_geo_area_not_supported():
    s = bigframes.pandas.Series(
        [
            Polygon([(0, 0), (1, 1), (0, 1)]),
            Polygon([(10, 0), (10, 5), (0, 0)]),
            Polygon([(0, 0), (2, 2), (2, 0)]),
            LineString([(0, 0), (1, 1), (0, 1)]),
            Point(0, 1),
        ],
        dtype=GeometryDtype(),
    )
    bf_series: bigframes.geopandas.GeoSeries = s.geo
    with pytest.raises(
        NotImplementedError,
        match=re.escape(
            f"GeoSeries.area is not supported. Use bigframes.bigquery.st_area(series), instead. {constants.FEEDBACK_LINK}"
        ),
    ):
        bf_series.area


def test_geoseries_length_property_not_implemented(session):
    gs = bigframes.geopandas.GeoSeries([Point(0, 0)], session=session)
    with pytest.raises(
        NotImplementedError,
        match=re.escape(
            "GeoSeries.length is not yet implemented. Please use bigframes.bigquery.st_length(geoseries) instead."
        ),
    ):
        _ = gs.length


def test_geo_distance_not_supported():
    s1 = bigframes.pandas.Series(
        [
            Polygon([(0, 0), (1, 1), (0, 1)]),
            Polygon([(10, 0), (10, 5), (0, 0)]),
            Polygon([(0, 0), (2, 2), (2, 0)]),
            LineString([(0, 0), (1, 1), (0, 1)]),
            Point(0, 1),
        ],
        dtype=GeometryDtype(),
    )
    s2 = bigframes.geopandas.GeoSeries(
        [
            Polygon([(0, 0), (1, 1), (0, 1)]),
            Polygon([(10, 0), (10, 5), (0, 0)]),
            Polygon([(0, 0), (2, 2), (2, 0)]),
            LineString([(0, 0), (1, 1), (0, 1)]),
            Point(0, 1),
        ]
    )
    with pytest.raises(
        NotImplementedError,
        match=re.escape("GeoSeries.distance is not supported."),
    ):
        s1.geo.distance(s2)


def test_geo_from_xy():
    x = [2.5, 5, -3.0]
    y = [0.5, 1, 1.5]
    bf_result = (
        bigframes.geopandas.GeoSeries.from_xy(x, y)
        .astype(geopandas.array.GeometryDtype())
        .to_pandas()
    )
    pd_result = geopandas.GeoSeries.from_xy(x, y, crs="EPSG:4326").astype(
        geopandas.array.GeometryDtype()
    )

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
        check_series_type=False,
        check_index=False,
    )


def test_geo_from_wkt():
    wkts = [
        "Point(0 1)",
        "Point(2 4)",
        "Point(5 3)",
        "Point(6 8)",
    ]

    bf_result = bigframes.geopandas.GeoSeries.from_wkt(wkts).to_pandas()

    pd_result = geopandas.GeoSeries.from_wkt(wkts)

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
        check_series_type=False,
        check_index=False,
    )


def test_geo_to_wkt():
    bf_geo = bigframes.geopandas.GeoSeries(
        [
            Point(0, 1),
            Point(2, 4),
            Point(5, 3),
            Point(6, 8),
        ]
    )

    pd_geo = geopandas.GeoSeries(
        [
            Point(0, 1),
            Point(2, 4),
            Point(5, 3),
            Point(6, 8),
        ]
    )

    # Test was failing before using str.replace because the pd_result had extra
    # whitespace "POINT (0 1)" while bf_result had none "POINT(0 1)".
    # str.replace replaces any encountered whitespaces with none.
    bf_result = (
        bf_geo.to_wkt().astype("string[pyarrow]").to_pandas().str.replace(" ", "")
    )

    pd_result = pd_geo.to_wkt().astype("string[pyarrow]").str.replace(" ", "")

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
        check_index=False,
    )


def test_geo_boundary():
    bf_s = bigframes.pandas.Series(
        [
            Polygon([(0, 0), (1, 1), (0, 1)]),
            Polygon([(10, 0), (10, 5), (0, 0)]),
            Polygon([(0, 0), (2, 2), (2, 0)]),
            LineString([(0, 0), (1, 1), (0, 1)]),
            Point(0, 1),
        ],
    )

    pd_s = geopandas.GeoSeries(
        [
            Polygon([(0, 0), (1, 1), (0, 1)]),
            Polygon([(10, 0), (10, 5), (0, 0)]),
            Polygon([(0, 0), (2, 2), (2, 0)]),
            LineString([(0, 0), (1, 1), (0, 1)]),
            Point(0, 1),
        ],
        index=pd.Index([0, 1, 2, 3, 4], dtype="Int64"),
    )

    bf_result = bf_s.geo.boundary.to_pandas()
    pd_result = pd_s.boundary

    geopandas.testing.assert_geoseries_equal(
        bf_result,
        pd_result,
        check_series_type=False,
        check_index_type=False,
    )


# the GeoSeries and GeoPandas results are not always the same.
# For example, when the difference between two polygons is empty,
# GeoPandas returns 'POLYGON EMPTY' while GeoSeries returns 'GeometryCollection([])'.
# This is why we are hard-coding the expected results.
def test_geo_difference_with_geometry_objects():
    data1 = [
        Polygon([(0, 0), (10, 0), (10, 10), (0, 0)]),
        Polygon([(0, 0), (1, 1), (0, 1), (0, 0)]),
        Point(0, 1),
    ]

    data2 = [
        Polygon([(0, 0), (10, 0), (10, 10), (0, 0)]),
        Polygon([(0, 0), (1, 1), (0, 1), (0, 0)]),
        LineString([(2, 0), (0, 2)]),
    ]

    bf_s1 = bigframes.geopandas.GeoSeries(data=data1)
    bf_s2 = bigframes.geopandas.GeoSeries(data=data2)

    bf_result = bf_s1.difference(bf_s2).to_pandas()

    expected = bigframes.geopandas.GeoSeries(
        [
            Polygon([]),
            Polygon([]),
            Point(0, 1),
        ],
        index=[0, 1, 2],
    ).to_pandas()

    assert bf_result.dtype == "geometry"
    assert expected.iloc[0].equals(bf_result.iloc[0])
    assert expected.iloc[1].equals(bf_result.iloc[1])
    assert expected.iloc[2].equals(bf_result.iloc[2])


def test_geo_difference_with_single_geometry_object():
    data1 = [
        Polygon([(0, 0), (10, 0), (10, 10), (0, 0)]),
        Polygon([(4, 2), (6, 2), (8, 6), (4, 2)]),
        Point(0, 1),
    ]

    bf_s1 = bigframes.geopandas.GeoSeries(data=data1)
    bf_result = bf_s1.difference(
        bigframes.geopandas.GeoSeries(
            [
                Polygon([(0, 0), (10, 0), (10, 10), (0, 0)]),
                Polygon([(1, 0), (0, 5), (0, 0), (1, 0)]),
            ]
        ),
    ).to_pandas()

    expected = bigframes.geopandas.GeoSeries(
        [
            GeometryCollection([]),
            Polygon([(4, 2), (6, 2), (8, 6), (4, 2)]),
            None,
        ],
        index=[0, 1, 2],
    ).to_pandas()

    assert bf_result.dtype == "geometry"
    assert (expected.iloc[0]).equals(bf_result.iloc[0])
    assert expected.iloc[1] == bf_result.iloc[1]
    assert expected.iloc[2] == bf_result.iloc[2]


def test_geo_difference_with_similar_geometry_objects():
    data1 = [
        Polygon([(0, 0), (10, 0), (10, 10), (0, 0)]),
        Polygon([(0, 0), (1, 1), (0, 1)]),
        Point(0, 1),
    ]

    bf_s1 = bigframes.geopandas.GeoSeries(data=data1)
    bf_result = bf_s1.difference(bf_s1).to_pandas()

    expected = bigframes.geopandas.GeoSeries(
        [GeometryCollection([]), GeometryCollection([]), GeometryCollection([])],
        index=[0, 1, 2],
    ).to_pandas()

    assert bf_result.dtype == "geometry"
    assert expected.iloc[0].equals(bf_result.iloc[0])
    assert expected.iloc[1].equals(bf_result.iloc[1])
    assert expected.iloc[2].equals(bf_result.iloc[2])


def test_geo_drop_duplicates():
    bf_series = bigframes.geopandas.GeoSeries(
        [Point(1, 1), Point(2, 2), Point(3, 3), Point(2, 2)]
    )

    pd_series = geopandas.GeoSeries(
        [Point(1, 1), Point(2, 2), Point(3, 3), Point(2, 2)]
    )

    bf_result = bf_series.drop_duplicates().to_pandas()
    pd_result = pd_series.drop_duplicates()

    pd.testing.assert_series_equal(
        geopandas.GeoSeries(bf_result), pd_result, check_index=False
    )


# the GeoSeries and GeoPandas results are not always the same.
# For example, when the intersection between two polygons is empty,
# GeoPandas returns 'POLYGON EMPTY' while GeoSeries returns 'GeometryCollection([])'.
# This is why we are hard-coding the expected results.
def test_geo_intersection_with_geometry_objects():
    data1 = [
        Polygon([(0, 0), (10, 0), (10, 10), (0, 0)]),
        Polygon([(0, 0), (1, 1), (0, 1), (0, 0)]),
        Point(0, 1),
    ]

    data2 = [
        Polygon([(0, 0), (10, 0), (10, 10), (0, 0)]),
        Polygon([(0, 0), (1, 1), (0, 1), (0, 0)]),
        LineString([(2, 0), (0, 2)]),
    ]

    bf_s1 = bigframes.geopandas.GeoSeries(data=data1)
    bf_s2 = bigframes.geopandas.GeoSeries(data=data2)

    bf_result = bf_s1.intersection(bf_s2).to_pandas()

    expected = bigframes.geopandas.GeoSeries(
        [
            Polygon([(0, 0), (10, 0), (10, 10), (0, 0)]),
            Polygon([(0, 0), (1, 1), (0, 1), (0, 0)]),
            GeometryCollection([]),
        ],
    ).to_pandas()

    assert bf_result.dtype == "geometry"
    assert expected.iloc[0].equals(bf_result.iloc[0])
    assert expected.iloc[1].equals(bf_result.iloc[1])
    assert expected.iloc[2].equals(bf_result.iloc[2])


def test_geo_intersection_with_single_geometry_object():
    data1 = [
        Polygon([(0, 0), (10, 0), (10, 10), (0, 0)]),
        Polygon([(4, 2), (6, 2), (8, 6), (4, 2)]),
        Point(0, 1),
    ]

    bf_s1 = bigframes.geopandas.GeoSeries(data=data1)
    bf_result = bf_s1.intersection(
        bigframes.geopandas.GeoSeries(
            [
                Polygon([(0, 0), (10, 0), (10, 10), (0, 0)]),
                Polygon([(1, 0), (0, 5), (0, 0), (1, 0)]),
            ]
        ),
    ).to_pandas()

    expected = bigframes.geopandas.GeoSeries(
        [
            Polygon([(0, 0), (10, 0), (10, 10), (0, 0)]),
            GeometryCollection([]),
            None,
        ],
        index=[0, 1, 2],
    ).to_pandas()

    assert bf_result.dtype == "geometry"
    assert (expected.iloc[0]).equals(bf_result.iloc[0])
    assert expected.iloc[1] == bf_result.iloc[1]
    assert expected.iloc[2] == bf_result.iloc[2]


def test_geo_intersection_with_similar_geometry_objects():
    data1 = [
        Polygon([(0, 0), (10, 0), (10, 10), (0, 0)]),
        Polygon([(0, 0), (1, 1), (0, 1)]),
        Point(0, 1),
    ]

    bf_s1 = bigframes.geopandas.GeoSeries(data=data1)
    bf_result = bf_s1.intersection(bf_s1).to_pandas()

    expected = bigframes.geopandas.GeoSeries(
        [
            Polygon([(0, 0), (10, 0), (10, 10), (0, 0)]),
            Polygon([(0, 0), (1, 1), (0, 1)]),
            Point(0, 1),
        ],
        index=[0, 1, 2],
    ).to_pandas()

    assert bf_result.dtype == "geometry"
    assert expected.iloc[0].equals(bf_result.iloc[0])
    assert expected.iloc[1].equals(bf_result.iloc[1])
    assert expected.iloc[2].equals(bf_result.iloc[2])
