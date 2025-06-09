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
import pandas.testing
import pytest
from shapely.geometry import (  # type: ignore
    GeometryCollection,
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
)

from bigframes.bigquery import st_length
import bigframes.bigquery as bbq
import bigframes.geopandas


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
        rtol=0.1,
    )


# Expected length for 1 degree of longitude at the equator is approx 111195.079734 meters
DEG_LNG_EQUATOR_METERS = 111195.07973400292


def test_st_length_various_geometries(session):
    input_geometries = [
        Point(0, 0),
        LineString([(0, 0), (1, 0)]),
        Polygon([(0, 0), (1, 0), (0, 1), (0, 0)]),
        MultiPoint([Point(0, 0), Point(1, 1)]),
        MultiLineString([LineString([(0, 0), (1, 0)]), LineString([(0, 0), (0, 1)])]),
        MultiPolygon(
            [
                Polygon([(0, 0), (1, 0), (0, 1), (0, 0)]),
                Polygon([(2, 2), (3, 2), (2, 3), (2, 2)]),
            ]
        ),
        GeometryCollection([Point(0, 0), LineString([(0, 0), (1, 0)])]),
        GeometryCollection([]),
        None,  # Represents NULL geography input
        GeometryCollection([Point(1, 1), Point(2, 2)]),
    ]
    geoseries = bigframes.geopandas.GeoSeries(input_geometries, session=session)

    expected_lengths = pd.Series(
        [
            0.0,  # Point
            DEG_LNG_EQUATOR_METERS,  # LineString
            0.0,  # Polygon
            0.0,  # MultiPoint
            2 * DEG_LNG_EQUATOR_METERS,  # MultiLineString
            0.0,  # MultiPolygon
            DEG_LNG_EQUATOR_METERS,  # GeometryCollection (Point + LineString)
            0.0,  # Empty GeometryCollection
            pd.NA,  # None input for ST_LENGTH(NULL) is NULL
            0.0,  # GeometryCollection (Point + Point)
        ],
        index=pd.Index(range(10), dtype="Int64"),
        dtype="Float64",
    )

    # Test default use_spheroid
    result_default = st_length(geoseries).to_pandas()
    pd.testing.assert_series_equal(
        result_default,
        expected_lengths,
        rtol=1e-3,
        atol=1e-3,  # For comparisons involving 0.0
    )  # type: ignore

    # Test explicit use_spheroid=False
    result_explicit_false = st_length(geoseries, use_spheroid=False).to_pandas()
    pd.testing.assert_series_equal(
        result_explicit_false,
        expected_lengths,
        rtol=1e-3,
        atol=1e-3,  # For comparisons involving 0.0
    )  # type: ignore


def test_geo_st_difference_with_geometry_objects():
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

    geobf_s1 = bigframes.geopandas.GeoSeries(data=data1)
    geobf_s2 = bigframes.geopandas.GeoSeries(data=data2)
    geobf_s_result = bbq.st_difference(geobf_s1, geobf_s2).to_pandas()

    expected = pd.Series(
        [
            GeometryCollection([]),
            GeometryCollection([]),
            Point(0, 1),
        ],
        index=[0, 1, 2],
        dtype=geopandas.array.GeometryDtype(),
    )
    pandas.testing.assert_series_equal(
        geobf_s_result,
        expected,
        check_index_type=False,
        check_exact=False,
        rtol=0.1,
    )


def test_geo_st_difference_with_single_geometry_object():
    pytest.importorskip(
        "shapely",
        minversion="2.0.0",
        reason="shapely objects must be hashable to include in our expression trees",
    )

    data1 = [
        Polygon([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]),
        Polygon([(0, 1), (10, 1), (10, 9), (0, 9), (0, 1)]),
        Point(0, 1),
    ]

    geobf_s1 = bigframes.geopandas.GeoSeries(data=data1)
    geobf_s_result = bbq.st_difference(
        geobf_s1,
        Polygon([(0, 0), (10, 0), (10, 5), (0, 5), (0, 0)]),
    ).to_pandas()

    expected = pd.Series(
        [
            Polygon([(10, 5), (10, 10), (0, 10), (0, 5), (10, 5)]),
            Polygon([(10, 5), (10, 9), (0, 9), (0, 5), (10, 5)]),
            GeometryCollection([]),
        ],
        index=[0, 1, 2],
        dtype=geopandas.array.GeometryDtype(),
    )
    pandas.testing.assert_series_equal(
        geobf_s_result,
        expected,
        check_index_type=False,
        check_exact=False,
        rtol=0.1,
    )


def test_geo_st_difference_with_similar_geometry_objects():
    data1 = [
        Polygon([(0, 0), (10, 0), (10, 10), (0, 0)]),
        Polygon([(0, 0), (1, 1), (0, 1)]),
        Point(0, 1),
    ]

    geobf_s1 = bigframes.geopandas.GeoSeries(data=data1)
    geobf_s_result = bbq.st_difference(geobf_s1, geobf_s1).to_pandas()

    expected = pd.Series(
        [GeometryCollection([]), GeometryCollection([]), GeometryCollection([])],
        index=[0, 1, 2],
        dtype=geopandas.array.GeometryDtype(),
    )
    pandas.testing.assert_series_equal(
        geobf_s_result,
        expected,
        check_index_type=False,
        check_exact=False,
        rtol=0.1,
    )


def test_geo_st_distance_with_geometry_objects():
    data1 = [
        # 0.00001 is approximately 1 meter.
        Polygon([(0, 0), (0.00001, 0), (0.00001, 0.00001), (0, 0.00001), (0, 0)]),
        Polygon(
            [
                (0.00002, 0),
                (0.00003, 0),
                (0.00003, 0.00001),
                (0.00002, 0.00001),
                (0.00002, 0),
            ]
        ),
        Point(0, 0.00002),
    ]

    data2 = [
        Polygon(
            [
                (0.00002, 0),
                (0.00003, 0),
                (0.00003, 0.00001),
                (0.00002, 0.00001),
                (0.00002, 0),
            ]
        ),
        Point(0, 0.00002),
        Polygon([(0, 0), (0.00001, 0), (0.00001, 0.00001), (0, 0.00001), (0, 0)]),
        Point(
            1, 1
        ),  # No matching row in data1, so this will be NULL after the call to distance.
    ]

    geobf_s1 = bigframes.geopandas.GeoSeries(data=data1)
    geobf_s2 = bigframes.geopandas.GeoSeries(data=data2)
    geobf_s_result = bbq.st_distance(geobf_s1, geobf_s2).to_pandas()

    expected = pd.Series(
        [
            1.112,
            2.486,
            1.112,
            None,
        ],
        index=[0, 1, 2, 3],
        dtype="Float64",
    )
    pandas.testing.assert_series_equal(
        geobf_s_result,
        expected,
        check_index_type=False,
        check_exact=False,
        rtol=0.1,
    )


def test_geo_st_distance_with_single_geometry_object():
    pytest.importorskip(
        "shapely",
        minversion="2.0.0",
        reason="shapely objects must be hashable to include in our expression trees",
    )

    data1 = [
        # 0.00001 is approximately 1 meter.
        Polygon([(0, 0), (0.00001, 0), (0.00001, 0.00001), (0, 0.00001), (0, 0)]),
        Polygon(
            [
                (0.00001, 0),
                (0.00002, 0),
                (0.00002, 0.00001),
                (0.00001, 0.00001),
                (0.00001, 0),
            ]
        ),
        Point(0, 0.00002),
    ]

    geobf_s1 = bigframes.geopandas.GeoSeries(data=data1)
    geobf_s_result = bbq.st_distance(
        geobf_s1,
        Point(0, 0),
    ).to_pandas()

    expected = pd.Series(
        [
            0,
            1.112,
            2.224,
        ],
        dtype="Float64",
    )
    pandas.testing.assert_series_equal(
        geobf_s_result,
        expected,
        check_index_type=False,
        check_exact=False,
        rtol=0.1,
    )


def test_geo_st_intersection_with_geometry_objects():
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

    geobf_s1 = bigframes.geopandas.GeoSeries(data=data1)
    geobf_s2 = bigframes.geopandas.GeoSeries(data=data2)
    geobf_s_result = bbq.st_intersection(geobf_s1, geobf_s2).to_pandas()

    expected = pd.Series(
        [
            Polygon([(0, 0), (10, 0), (10, 10), (0, 0)]),
            Polygon([(0, 0), (1, 1), (0, 1), (0, 0)]),
            GeometryCollection([]),
        ],
        index=[0, 1, 2],
        dtype=geopandas.array.GeometryDtype(),
    )
    pandas.testing.assert_series_equal(
        geobf_s_result,
        expected,
        check_index_type=False,
        check_exact=False,
        rtol=0.1,
    )


def test_geo_st_intersection_with_single_geometry_object():
    pytest.importorskip(
        "shapely",
        minversion="2.0.0",
        reason="shapely objects must be hashable to include in our expression trees",
    )

    data1 = [
        Polygon([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]),
        Polygon([(0, 1), (10, 1), (10, 9), (0, 9), (0, 1)]),
        Point(0, 1),
    ]

    geobf_s1 = bigframes.geopandas.GeoSeries(data=data1)
    geobf_s_result = bbq.st_intersection(
        geobf_s1,
        Polygon([(0, 0), (10, 0), (10, 5), (0, 5), (0, 0)]),
    ).to_pandas()

    expected = pd.Series(
        [
            Polygon([(0, 0), (10, 0), (10, 5), (0, 5), (0, 0)]),
            Polygon([(0, 1), (10, 1), (10, 5), (0, 5), (0, 1)]),
            Point(0, 1),
        ],
        index=[0, 1, 2],
        dtype=geopandas.array.GeometryDtype(),
    )
    pandas.testing.assert_series_equal(
        geobf_s_result,
        expected,
        check_index_type=False,
        check_exact=False,
        rtol=0.1,
    )


def test_geo_st_intersection_with_similar_geometry_objects():
    data1 = [
        Polygon([(0, 0), (10, 0), (10, 10), (0, 0)]),
        Polygon([(0, 0), (1, 1), (0, 1)]),
        Point(0, 1),
    ]

    geobf_s1 = bigframes.geopandas.GeoSeries(data=data1)
    geobf_s_result = bbq.st_intersection(geobf_s1, geobf_s1).to_pandas()

    expected = pd.Series(
        [
            Polygon([(0, 0), (10, 0), (10, 10), (0, 0)]),
            Polygon([(0, 0), (1, 1), (0, 1)]),
            Point(0, 1),
        ],
        index=[0, 1, 2],
        dtype=geopandas.array.GeometryDtype(),
    )
    pandas.testing.assert_series_equal(
        geobf_s_result,
        expected,
        check_index_type=False,
        check_exact=False,
        rtol=0.1,
    )


def test_geo_st_isclosed():
    bf_gs = bigframes.geopandas.GeoSeries(
        [
            Point(0, 0),  # Point
            LineString([(0, 0), (1, 1)]),  # Open LineString
            LineString([(0, 0), (1, 1), (0, 1), (0, 0)]),  # Closed LineString
            Polygon([(0, 0), (1, 1), (0, 1)]),  # Open polygon
            GeometryCollection(),  # Empty GeometryCollection
            bigframes.geopandas.GeoSeries.from_wkt(["GEOMETRYCOLLECTION EMPTY"]).iloc[
                0
            ],  # Also empty
            None,  # Should be filtered out by dropna
        ],
        index=[0, 1, 2, 3, 4, 5, 6],
    )
    bf_result = bbq.st_isclosed(bf_gs).to_pandas()

    # Expected results based on ST_ISCLOSED documentation:
    expected_data = [
        True,  # Point: True
        False,  # Open LineString: False
        True,  # Closed LineString: True
        False,  # Polygon: False (only True if it's a full polygon)
        False,  # Empty GeometryCollection: False (An empty GEOGRAPHY isn't closed)
        False,  # GEOMETRYCOLLECTION EMPTY: False
        None,
    ]
    expected_series = pd.Series(data=expected_data, dtype="boolean")

    pd.testing.assert_series_equal(
        bf_result,
        expected_series,
        # We default to Int64 (nullable) dtype, but pandas defaults to int64 index.
        check_index_type=False,
    )
