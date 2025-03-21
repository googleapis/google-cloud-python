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

from __future__ import annotations

from bigframes import operations as ops
import bigframes.dtypes
import bigframes.geopandas
import bigframes.series

"""
Search functions defined from
https://cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions
"""


def st_area(series: bigframes.series.Series) -> bigframes.series.Series:
    """
    Returns the area in square meters covered by the polygons in the input
    GEOGRAPHY.

    If geography_expression is a point or a line, returns zero. If
    geography_expression is a collection, returns the area of the polygons
    in the collection; if the collection doesn't contain polygons, returns zero.


    ..note::
        BigQuery's Geography functions, like `st_area`, interpret the geometry
        data type as a point set on the Earth's surface. A point set is a set
        of points, lines, and polygons on the WGS84 reference spheroid, with
        geodesic edges. See: https://cloud.google.com/bigquery/docs/geospatial-data


    **Examples:**

        >>> import bigframes.geopandas
        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> from shapely.geometry import Polygon, LineString, Point
        >>> bpd.options.display.progress_bar = None

        >>> series = bigframes.geopandas.GeoSeries(
        ...         [
        ...             Polygon([(0.0, 0.0), (0.1, 0.1), (0.0, 0.1)]),
        ...             Polygon([(0.10, 0.4), (0.9, 0.5), (0.10, 0.5)]),
        ...             Polygon([(0.1, 0.1), (0.2, 0.1), (0.2, 0.2)]),
        ...             LineString([(0, 0), (1, 1), (0, 1)]),
        ...             Point(0, 1),
        ...         ]
        ... )
        >>> series
        0              POLYGON ((0 0, 0.1 0.1, 0 0.1, 0 0))
        1    POLYGON ((0.1 0.4, 0.9 0.5, 0.1 0.5, 0.1 0.4))
        2    POLYGON ((0.1 0.1, 0.2 0.1, 0.2 0.2, 0.1 0.1))
        3                        LINESTRING (0 0, 1 1, 0 1)
        4                                       POINT (0 1)
        dtype: geometry

        >>> bbq.st_area(series)
        0    61821689.855985
        1    494563347.88721
        2    61821689.855841
        3                0.0
        4                0.0
        dtype: Float64

    Use `round()` to round the outputed areas to the neares ten millions

        >>> bbq.st_area(series).round(-7)
        0     60000000.0
        1    490000000.0
        2     60000000.0
        3            0.0
        4            0.0
        dtype: Float64

    Returns:
      bigframes.pandas.Series:
          Series of float representing the areas.
    """
    series = series._apply_unary_op(ops.geo_area_op)
    series.name = None
    return series


def st_difference(
    series: bigframes.series.Series, other: bigframes.series.Series
) -> bigframes.series.Series:
    """
    Returns a GEOGRAPHY that represents the point set difference of
    `geography_1` and `geography_2`. Therefore, the result consists of the part
    of `geography_1` that doesn't intersect with `geography_2`.

    If `geometry_1` is completely contained in `geometry_2`, then ST_DIFFERENCE
    returns an empty GEOGRAPHY.

    ..note::
        BigQuery's Geography functions, like `st_difference`, interpret the geometry
        data type as a point set on the Earth's surface. A point set is a set
        of points, lines, and polygons on the WGS84 reference spheroid, with
        geodesic edges. See: https://cloud.google.com/bigquery/docs/geospatial-data

    **Examples:**

        >>> import bigframes as bpd
        >>> import bigframes.bigquery as bbq
        >>> import bigframes.geopandas
        >>> from shapely.geometry import Polygon, LineString, Point
        >>> bpd.options.display.progress_bar = None

    We can check two GeoSeries against each other, row by row.

        >>> s1 = bigframes.geopandas.GeoSeries(
        ...    [
        ...        Polygon([(0, 0), (2, 2), (0, 2)]),
        ...        Polygon([(0, 0), (2, 2), (0, 2)]),
        ...        LineString([(0, 0), (2, 2)]),
        ...        LineString([(2, 0), (0, 2)]),
        ...        Point(0, 1),
        ...    ],
        ... )
        >>> s2 = bigframes.geopandas.GeoSeries(
        ...    [
        ...        Polygon([(0, 0), (1, 1), (0, 1)]),
        ...        LineString([(1, 0), (1, 3)]),
        ...        LineString([(2, 0), (0, 2)]),
        ...        Point(1, 1),
        ...        Point(0, 1),
        ...    ],
        ...    index=range(1, 6),
        ... )

        >>> s1
        0    POLYGON ((0 0, 2 2, 0 2, 0 0))
        1    POLYGON ((0 0, 2 2, 0 2, 0 0))
        2             LINESTRING (0 0, 2 2)
        3             LINESTRING (2 0, 0 2)
        4                       POINT (0 1)
        dtype: geometry

        >>> s2
        1    POLYGON ((0 0, 1 1, 0 1, 0 0))
        2             LINESTRING (1 0, 1 3)
        3             LINESTRING (2 0, 0 2)
        4                       POINT (1 1)
        5                       POINT (0 1)
        dtype: geometry

        >>> bbq.st_difference(s1, s2)
        0                                               None
        1    POLYGON ((0.99954 1, 2 2, 0 2, 0 1, 0.99954 1))
        2                   LINESTRING (0 0, 1 1.00046, 2 2)
        3                           GEOMETRYCOLLECTION EMPTY
        4                                        POINT (0 1)
        5                                               None
        dtype: geometry

    We can also check difference of single shapely geometries:

        >>> sbq1 = bigframes.geopandas.GeoSeries(
        ...     [
        ...         Polygon([(0, 0), (10, 0), (10, 10), (0, 0)])
        ...     ]
        ... )
        >>> sbq2 = bigframes.geopandas.GeoSeries(
        ...     [
        ...         Polygon([(4, 2), (6, 2), (8, 6), (4, 2)])
        ...     ]
        ... )

        >>> sbq1
        0    POLYGON ((0 0, 10 0, 10 10, 0 0))
        dtype: geometry

        >>> sbq2
        0    POLYGON ((4 2, 6 2, 8 6, 4 2))
        dtype: geometry

        >>> bbq.st_difference(sbq1, sbq2)
        0    POLYGON ((0 0, 10 0, 10 10, 0 0), (8 6, 6 2, 4...
        dtype: geometry

    Additionally, we can check difference of a GeoSeries against a single shapely geometry:

        >>> bbq.st_difference(s1, sbq2)
        0    POLYGON ((0 0, 2 2, 0 2, 0 0))
        1                              None
        2                              None
        3                              None
        4                              None
        dtype: geometry

    Args:
        other (bigframes.series.Series or geometric object):
            The GeoSeries (elementwise) or geometric object to find the difference to.

    Returns:
        bigframes.series.Series:
            A GeoSeries of the points in each aligned geometry that are not
            in other.
    """
    return series._apply_binary_op(other, ops.geo_st_difference_op)
